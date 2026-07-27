"""Python backend. The only one that always works — the app ships an interpreter."""
from __future__ import annotations

import os
import sys
import tempfile
import time

import runner as legacy_runner

from .base import (BOOL, END, FLOAT, INT, SENTINEL, STR, Backend, RunOutcome, Sig,
                   base_of, depth, is_list, parse_values, quote, read_protocol)

class PythonBackend(Backend):
    id = "python"
    label = "Python"
    ext = ".py"
    comment = "#"
    bundled = True
    install_hint = "Python is built into CodeForge — nothing to install."

    def probe(self):
        if legacy_runner.is_frozen():
            return True, f"bundled {sys.version.split()[0]}"
        return True, sys.version.split()[0]

    # ------------------------------------------------------------- codegen
    def type_name(self, type_str: str) -> str:
        if is_list(type_str):
            return f"list[{self.type_name(type_str[5:-1])}]"
        return {INT: "int", FLOAT: "float", BOOL: "bool", STR: "str"}[type_str]

    def literal(self, value, type_str: str) -> str:
        if value is None:
            return "None"
        if is_list(type_str):
            inner = type_str[5:-1]
            return "[" + ", ".join(self.literal(v, inner) for v in value) + "]"
        if type_str == STR:
            return quote(str(value), ascii_only=False)
        if type_str == BOOL:
            return "True" if value else "False"
        if type_str == FLOAT:
            return repr(float(value))
        return repr(int(value))

    def starter(self, func: str, sig: Sig, doc: str = "") -> str:
        params = ", ".join(sig.names)
        body = f'    """{doc}"""\n' if doc else ""
        return f"def {func}({params}):\n{body}    # your code here\n    pass\n"

    def harness(self, func: str, sig: Sig, values) -> str:
        lines = [
            "",
            "",
            "# --- CodeForge test harness (generated) " + "-" * 34,
            "def _cf_fmt(v):",
            "    return repr(v).replace('|', '\\u00a6').replace('\\n', ' ')",
            "",
            "",
            "def _cf_eq(a, b):",
            "    if isinstance(a, float) or isinstance(b, float):",
            "        try:",
            "            return abs(float(a) - float(b)) <= 1e-6 * max(1.0, abs(float(b)))",
            "        except (TypeError, ValueError):",
            "            return False",
            "    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):",
            "        return len(a) == len(b) and all(_cf_eq(x, y) for x, y in zip(a, b))",
            "    return a == b",
            "",
            "",
            "def _cf_main():",
        ]
        for index, (args, expected) in enumerate(values):
            arg_src = ", ".join(self.literal(a, t) for a, t in zip(args, sig.types))
            lines += [
                "    try:",
                f"        _got = {func}({arg_src})",
                f"        _exp = {self.literal(expected, sig.ret)}",
                f"        if _cf_eq(_got, _exp):",
                f"            print('{SENTINEL}|{index}|PASS')",
                "        else:",
                f"            print('{SENTINEL}|{index}|FAIL|' + _cf_fmt(_got) + '|' "
                f"+ _cf_fmt(_exp))",
                "    except BaseException as exc:",
                f"        print('{SENTINEL}|{index}|ERROR|' + type(exc).__name__ + ': ' "
                f"+ str(exc).replace('|', ' ').replace(chr(10), ' '))",
            ]
        lines += [
            f"    print('{END}')",
            "",
            "",
            "_cf_main()",
            "",
        ]
        return "\n".join(lines)

    # ------------------------------------------------------------- running
    def run(self, user_code: str, func: str, sig: Sig, cases: list[dict],
            timeout: float = 25.0) -> RunOutcome:
        outcome = RunOutcome()
        values = parse_values(cases)
        source = user_code.rstrip() + "\n" + self.harness(func, sig, values)
        start = time.perf_counter()
        with tempfile.TemporaryDirectory(prefix="cf_py_") as tmp:
            path = os.path.join(tmp, "your_code.py")
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(source)
            code, out, err, timed_out = self._exec(
                legacy_runner._interpreter() + [path], tmp, timeout)
        outcome.seconds = time.perf_counter() - start
        if timed_out:
            outcome.timed_out = True
            return outcome
        outcome.cases, outcome.stdout, completed = read_protocol(out, cases)
        if not completed and err.strip():
            outcome.runtime_error = err.strip()
        outcome.ok = bool(outcome.cases) and all(c.passed for c in outcome.cases)
        return outcome
