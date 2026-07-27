"""Shared machinery for the per-language execution backends.

How a task runs, in any language:

  1. A task declares a Signature: parameter types and a return type, drawn from
     a tiny type language (int, float, bool, str and lists of those).
  2. The backend renders the test cases as NATIVE LITERALS of the target
     language and generates a harness that calls the user's function once per
     case and compares the result itself.
  3. The harness prints one line per case in a fixed protocol. The parent only
     has to parse those lines — no JSON library is needed in any language,
     which matters because Java, Rust and C++ do not ship one.

Protocol, one line per case on stdout:

     @@CF|<index>|PASS
     @@CF|<index>|FAIL|<got>|<expected>
     @@CF|<index>|ERROR|<message>
     @@CFEND

Anything the user prints lands on stdout too, so the parent picks out the lines
starting with the sentinel and treats the rest as the program's own output.
"""
from __future__ import annotations

import ast
import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field

SENTINEL = "@@CF"
END = "@@CFEND"
TIMEOUT = 25.0          # compiled languages need room for the compiler

# ------------------------------------------------------------------ types
INT = "int"
FLOAT = "float"
BOOL = "bool"
STR = "str"


def L(inner: str) -> str:
    """list of `inner`, e.g. L(INT) -> 'list[int]'."""
    return f"list[{inner}]"


def is_list(type_name: str) -> bool:
    return type_name.startswith("list[")


def elem(type_name: str) -> str:
    """The element type of a list type."""
    assert is_list(type_name), type_name
    return type_name[5:-1]


def base_of(type_name: str) -> str:
    """Strip every list layer: list[list[int]] -> int."""
    while is_list(type_name):
        type_name = elem(type_name)
    return type_name


def depth(type_name: str) -> int:
    count = 0
    while is_list(type_name):
        count += 1
        type_name = elem(type_name)
    return count


@dataclass
class Sig:
    """The shape of the function the user has to write."""
    params: list[tuple[str, str]]      # [(name, type), ...]
    ret: str

    @property
    def types(self) -> list[str]:
        return [t for _, t in self.params]

    @property
    def names(self) -> list[str]:
        return [n for n, _ in self.params]


# ------------------------------------------------------------------ results
@dataclass
class CaseOutcome:
    index: int
    passed: bool
    got: str = ""
    expected: str = ""
    error: str = ""
    hidden: bool = False
    label: str = ""
    args: str = ""


@dataclass
class RunOutcome:
    ok: bool = False
    timed_out: bool = False
    build_error: str = ""
    runtime_error: str = ""
    stdout: str = ""
    seconds: float = 0.0
    cases: list[CaseOutcome] = field(default_factory=list)

    @property
    def passed(self) -> int:
        return sum(1 for c in self.cases if c.passed)

    @property
    def total(self) -> int:
        return len(self.cases)


def parse_values(cases: list[dict]) -> list[tuple[tuple, object]]:
    """Turn the stored reprs back into real Python values."""
    out = []
    for case in cases:
        args = ast.literal_eval(case["args"])
        if not isinstance(args, tuple):
            args = (args,)
        expected = ast.literal_eval(case["expected"]) if case.get("expected") is not None \
            else None
        out.append((args, expected))
    return out


def read_protocol(stdout: str, cases: list[dict]) -> tuple[list[CaseOutcome], str, bool]:
    """Split harness lines from the user's own prints.

    Returns (outcomes, user_output, completed).
    """
    outcomes: dict[int, CaseOutcome] = {}
    user_lines: list[str] = []
    completed = False

    for line in stdout.splitlines():
        if line.startswith(END):
            completed = True
            continue
        if not line.startswith(SENTINEL + "|"):
            user_lines.append(line)
            continue
        parts = line.split("|")
        try:
            index = int(parts[1])
        except (IndexError, ValueError):
            continue
        verdict = parts[2] if len(parts) > 2 else "FAIL"
        if verdict == "PASS":
            outcomes[index] = CaseOutcome(index, True)
        elif verdict == "ERROR":
            outcomes[index] = CaseOutcome(index, False,
                                          error="|".join(parts[3:]) or "runtime error")
        else:
            outcomes[index] = CaseOutcome(index, False,
                                          got=parts[3] if len(parts) > 3 else "",
                                          expected=parts[4] if len(parts) > 4 else "")

    ordered: list[CaseOutcome] = []
    for i, case in enumerate(cases):
        outcome = outcomes.get(i)
        if outcome is None:
            # The process died before reaching this case (a panic or a crash in
            # a language without catchable errors).
            outcome = CaseOutcome(i, False, error="did not run — the program stopped early")
        outcome.hidden = bool(case.get("hidden"))
        outcome.label = case.get("label", "")
        outcome.args = case.get("args", "")
        ordered.append(outcome)
    return ordered, "\n".join(user_lines).strip(), completed


def quote(text: str, ascii_only: bool = True) -> str:
    """A double-quoted string literal that every C-family language accepts."""
    out = ['"']
    for ch in text:
        if ch == "\\":
            out.append("\\\\")
        elif ch == '"':
            out.append('\\"')
        elif ch == "\n":
            out.append("\\n")
        elif ch == "\r":
            out.append("\\r")
        elif ch == "\t":
            out.append("\\t")
        elif ord(ch) < 32:
            out.append(f"\\u{ord(ch):04x}")
        elif ascii_only and ord(ch) > 126:
            code = ord(ch)
            if code > 0xFFFF:                       # surrogate pair
                code -= 0x10000
                out.append(f"\\u{0xD800 + (code >> 10):04x}")
                out.append(f"\\u{0xDC00 + (code & 0x3FF):04x}")
            else:
                out.append(f"\\u{code:04x}")
        else:
            out.append(ch)
    out.append('"')
    return "".join(out)


def escape_field(text: str, limit: int = 200) -> str:
    """Make a rendered value safe to put in one protocol field."""
    text = text.replace("|", "¦").replace("\r", " ").replace("\n", " ")
    return text if len(text) <= limit else text[:limit] + " …"


# ------------------------------------------------------------------ backend
class Backend:
    """One programming language the app can teach and execute."""

    id = ""
    label = ""
    ext = ".txt"
    comment = "//"
    # shown when the toolchain is missing
    install_hint = ""
    # the app ships a Python interpreter; everything else must be installed
    bundled = False

    # -------------------------------------------------------- availability
    def probe(self) -> tuple[bool, str]:
        """(is usable, version string or reason)."""
        raise NotImplementedError

    _cached: tuple[bool, str] | None = None

    def available(self, refresh: bool = False) -> tuple[bool, str]:
        if self._cached is None or refresh:
            try:
                type(self)._cached = self.probe()
            except Exception as exc:                       # never break the UI
                type(self)._cached = (False, str(exc))
        return type(self)._cached

    # ------------------------------------------------------------- codegen
    def type_name(self, type_str: str) -> str:
        raise NotImplementedError

    def literal(self, value, type_str: str) -> str:
        raise NotImplementedError

    def starter(self, func: str, sig: Sig, doc: str = "") -> str:
        raise NotImplementedError

    def harness(self, func: str, sig: Sig, values: list[tuple[tuple, object]]) -> str:
        raise NotImplementedError

    # --------------------------------------------------------------- running
    def run(self, user_code: str, func: str, sig: Sig, cases: list[dict],
            timeout: float = TIMEOUT) -> RunOutcome:
        raise NotImplementedError

    # ---------------------------------------------------------------- utils
    @staticmethod
    def _exec(cmd: list[str], cwd: str, timeout: float, stdin: str = "",
              env: dict | None = None) -> tuple[int, str, str, bool]:
        kwargs: dict = {}
        if os.name == "nt":
            kwargs["creationflags"] = getattr(subprocess, "CREATE_NO_WINDOW", 0)
        try:
            proc = subprocess.run(cmd, cwd=cwd, input=stdin, capture_output=True,
                                  text=True, timeout=timeout, encoding="utf-8",
                                  errors="replace", env=env, **kwargs)
        except subprocess.TimeoutExpired:
            return -1, "", "", True
        except FileNotFoundError as exc:
            return -1, "", f"{cmd[0]} not found: {exc}", False
        return proc.returncode, proc.stdout or "", proc.stderr or "", False

    @staticmethod
    def _which(name: str) -> str | None:
        return shutil.which(name)

    @staticmethod
    def _version(cmd: list[str]) -> tuple[bool, str]:
        if not shutil.which(cmd[0]):
            return False, ""
        code, out, err, timed_out = Backend._exec(cmd, os.getcwd(), 20)
        if timed_out:
            return False, "toolchain did not respond"
        text = (out or err).strip().splitlines()
        return code == 0, text[0] if text else ""

    def workspace(self) -> str:
        """A reusable scratch directory, so compilers can keep their caches."""
        root = os.path.join(tempfile.gettempdir(), "codeforge", self.id)
        os.makedirs(root, exist_ok=True)
        return root
