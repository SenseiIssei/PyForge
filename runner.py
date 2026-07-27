"""Executes user code in a separate Python process.

Two modes:
  * run_script()  - plain execution, stdin supported (Playground / examples)
  * run_tests()   - imports the user's module, calls one function per test case
                    and reports pass/fail per case as structured JSON.

Running out-of-process keeps the GUI alive even when the user writes
`while True: pass` - the subprocess just hits the timeout and gets killed.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import time
import traceback
from dataclasses import dataclass, field

TIMEOUT = 10.0
MAX_OUTPUT = 20000

HARNESS = r'''
import io, json, sys, time, traceback, contextlib, math

cfg_path, out_path = sys.argv[1], sys.argv[2]
with open(cfg_path, "r", encoding="utf-8") as fh:
    cfg = json.load(fh)

result = {"import_error": None, "stdout": "", "cases": [], "elapsed": 0.0}
buf = io.StringIO()

def approx(a, b, tol=1e-6):
    if isinstance(a, float) or isinstance(b, float):
        try:
            return math.isclose(float(a), float(b), rel_tol=tol, abs_tol=tol)
        except (TypeError, ValueError):
            return False
    return None

def equal(got, exp):
    r = approx(got, exp)
    if r is not None:
        return r
    if isinstance(exp, (list, tuple)) and isinstance(got, (list, tuple)):
        if len(got) != len(exp):
            return False
        return all(equal(g, e) for g, e in zip(got, exp))
    if isinstance(exp, dict) and isinstance(got, dict):
        return exp.keys() == got.keys() and all(equal(got[k], exp[k]) for k in exp)
    return got == exp

def short(value, limit=220):
    try:
        text = repr(value)
    except Exception:
        text = "<unrepr-able object>"
    return text if len(text) <= limit else text[:limit] + " ..."

start = time.perf_counter()
ns = {"__name__": "__usercode__"}
try:
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        exec(compile(cfg["source"], "your_code.py", "exec"), ns)
except BaseException:
    result["import_error"] = traceback.format_exc(limit=6)
    result["stdout"] = buf.getvalue()
    result["elapsed"] = time.perf_counter() - start
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(result, fh)
    sys.exit(0)

checker = None
if cfg.get("checker_src"):
    cns = {}
    exec(cfg["checker_src"], cns)
    checker = cns.get("check")

func = ns.get(cfg["func"])
if not callable(func):
    result["import_error"] = (
        "NameError: your code does not define a function called '%s'.\n"
        "Keep the given function name - the tests call it by that name." % cfg["func"]
    )
else:
    for case in cfg["cases"]:
        args = eval(case["args"], {"__builtins__": __builtins__}, {})
        if not isinstance(args, tuple):
            args = (args,)
        expected = eval(case["expected"], {"__builtins__": __builtins__}, {}) \
            if case.get("expected") is not None else None
        entry = {"args": short(args), "expected": short(expected),
                 "got": None, "passed": False, "error": None,
                 "hidden": case.get("hidden", False), "label": case.get("label", "")}
        t0 = time.perf_counter()
        try:
            with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
                got = func(*[a for a in args])
            entry["got"] = short(got)
            entry["passed"] = bool(checker(args, got)) if checker else equal(got, expected)
        except BaseException:
            tb = traceback.format_exc(limit=4)
            entry["error"] = tb.strip().splitlines()[-1]
            entry["traceback"] = tb
        entry["ms"] = (time.perf_counter() - t0) * 1000.0
        result["cases"].append(entry)

result["stdout"] = buf.getvalue()[:20000]
result["elapsed"] = time.perf_counter() - start
with open(out_path, "w", encoding="utf-8") as fh:
    json.dump(result, fh)
'''


@dataclass
class CaseResult:
    args: str
    expected: str
    got: str | None
    passed: bool
    error: str | None
    hidden: bool = False
    label: str = ""
    ms: float = 0.0
    traceback: str = ""


@dataclass
class TestReport:
    ok: bool = False
    timed_out: bool = False
    import_error: str | None = None
    stdout: str = ""
    elapsed: float = 0.0
    cases: list[CaseResult] = field(default_factory=list)

    @property
    def passed(self) -> int:
        return sum(1 for c in self.cases if c.passed)

    @property
    def total(self) -> int:
        return len(self.cases)


CHILD_FLAG = "--codeforge-child"


def is_frozen() -> bool:
    return bool(getattr(sys, "frozen", False))


def _python() -> str:
    exe = sys.executable
    if os.name == "nt" and exe.lower().endswith("python.exe"):
        pyw = exe[:-len("python.exe")] + "pythonw.exe"
        if os.path.exists(pyw):
            return pyw  # avoids a console window flashing on every run
    return exe


def _interpreter() -> list[str]:
    """The command prefix that runs a .py file.

    In a PyInstaller build there is no separate python.exe — sys.executable IS
    the app. So the app re-invokes itself with CHILD_FLAG, which makes it act as
    a plain interpreter instead of opening a window (see run_child below).
    """
    if is_frozen():
        return [sys.executable, CHILD_FLAG]
    return [_python(), "-X", "utf8", "-I"]


def run_child() -> int:
    """Entry point for the child process of a frozen build.

    argv is [app.exe, CHILD_FLAG, script.py, *script_args]; we execute
    script.py as __main__ with the remaining arguments and exit.
    """
    import io

    # A --windowed PyInstaller build starts with sys.stdout/stderr set to None.
    # The parent handed us real pipes on fds 1 and 2, so rebind to those.
    for fd, name in ((1, "stdout"), (2, "stderr")):
        if getattr(sys, name, None) is None:
            try:
                stream = io.TextIOWrapper(open(fd, "wb", closefd=False),
                                          encoding="utf-8", errors="replace",
                                          line_buffering=True)
            except OSError:
                stream = io.StringIO()
            setattr(sys, name, stream)
    if sys.stdin is None:
        try:
            sys.stdin = io.TextIOWrapper(open(0, "rb", closefd=False),
                                         encoding="utf-8", errors="replace")
        except OSError:
            sys.stdin = io.StringIO()

    script = sys.argv[2]
    sys.argv = [script] + sys.argv[3:]
    try:
        with open(script, "r", encoding="utf-8") as fh:
            source = fh.read()
        namespace = {"__name__": "__main__", "__file__": script,
                     "__builtins__": __builtins__}
        exec(compile(source, os.path.basename(script), "exec"), namespace)
    except SystemExit as exc:
        return int(exc.code or 0)
    except BaseException:
        traceback.print_exc()
        return 1
    finally:
        for name in ("stdout", "stderr"):
            try:
                getattr(sys, name).flush()
            except Exception:
                pass
    return 0


def _popen_kwargs() -> dict:
    kw: dict = {}
    if os.name == "nt":
        kw["creationflags"] = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    return kw


def run_script(source: str, stdin: str = "", timeout: float = TIMEOUT) -> tuple[str, str, bool, float]:
    """Run source as a plain script. Returns (stdout, stderr, timed_out, seconds)."""
    with tempfile.TemporaryDirectory(prefix="codeforge_") as tmp:
        path = os.path.join(tmp, "your_code.py")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(source)
        start = time.perf_counter()
        try:
            proc = subprocess.run(
                _interpreter() + [path],
                input=stdin, capture_output=True, text=True, timeout=timeout,
                cwd=tmp, encoding="utf-8", errors="replace", **_popen_kwargs())
        except subprocess.TimeoutExpired:
            return "", "", True, timeout
        except Exception:
            return "", traceback.format_exc(), False, time.perf_counter() - start
        elapsed = time.perf_counter() - start
        return proc.stdout[:MAX_OUTPUT], proc.stderr[:MAX_OUTPUT], False, elapsed


def run_tests(source: str, func: str, cases: list[dict],
              checker_src: str = "", timeout: float = TIMEOUT) -> TestReport:
    """Run the user's function against `cases`.

    Each case is {"args": "<python literal tuple repr>",
                  "expected": "<python literal repr>",
                  "hidden": bool, "label": str}
    """
    report = TestReport()
    with tempfile.TemporaryDirectory(prefix="codeforge_") as tmp:
        harness = os.path.join(tmp, "_harness.py")
        cfg_path = os.path.join(tmp, "_cfg.json")
        out_path = os.path.join(tmp, "_out.json")
        with open(harness, "w", encoding="utf-8") as fh:
            fh.write(HARNESS)
        with open(cfg_path, "w", encoding="utf-8") as fh:
            json.dump({"source": source, "func": func, "cases": cases,
                       "checker_src": checker_src}, fh)
        try:
            subprocess.run(_interpreter() + [harness, cfg_path, out_path],
                           capture_output=True, text=True, timeout=timeout, cwd=tmp,
                           encoding="utf-8", errors="replace", **_popen_kwargs())
        except subprocess.TimeoutExpired:
            report.timed_out = True
            return report
        except Exception:
            report.import_error = traceback.format_exc()
            return report

        if not os.path.exists(out_path):
            report.import_error = "The test process crashed before producing a result."
            return report
        with open(out_path, "r", encoding="utf-8") as fh:
            data = json.load(fh)

    report.import_error = data.get("import_error")
    report.stdout = data.get("stdout", "")
    report.elapsed = data.get("elapsed", 0.0)
    for c in data.get("cases", []):
        report.cases.append(CaseResult(
            args=c["args"], expected=c["expected"], got=c.get("got"),
            passed=c.get("passed", False), error=c.get("error"),
            hidden=c.get("hidden", False), label=c.get("label", ""),
            ms=c.get("ms", 0.0), traceback=c.get("traceback", "")))
    report.ok = (report.import_error is None and report.total > 0
                 and report.passed == report.total)
    return report


def error_line(text: str) -> int | None:
    """Pull the failing line number out of a traceback that points at your_code.py."""
    line = None
    for part in text.splitlines():
        part = part.strip()
        if part.startswith('File "your_code.py"') and ", line " in part:
            try:
                line = int(part.split(", line ")[1].split(",")[0].strip())
            except (IndexError, ValueError):
                pass
    return line
