"""JavaScript backend, running on Node.js."""
from __future__ import annotations

import os
import tempfile
import time

from .base import (BOOL, END, FLOAT, INT, SENTINEL, STR, Backend, RunOutcome, Sig,
                   is_list, parse_values, quote, read_protocol)

HELPERS = f"""
// --- CodeForge test harness (generated) ------------------------------------
function _cfFmt(v) {{
  let s;
  if (Array.isArray(v)) s = JSON.stringify(v);
  else if (typeof v === "string") s = JSON.stringify(v);
  else s = String(v);
  return s.replace(/\\|/g, "\\u00a6").replace(/\\r?\\n/g, " ");
}}

function _cfEq(a, b) {{
  if (Array.isArray(a) && Array.isArray(b)) {{
    if (a.length !== b.length) return false;
    for (let i = 0; i < a.length; i++) if (!_cfEq(a[i], b[i])) return false;
    return true;
  }}
  if (typeof a === "number" && typeof b === "number") {{
    if (Number.isInteger(a) && Number.isInteger(b)) return a === b;
    return Math.abs(a - b) <= 1e-6 * Math.max(1, Math.abs(b));
  }}
  return a === b;
}}
"""


class JavaScriptBackend(Backend):
    id = "javascript"
    label = "JavaScript"
    ext = ".js"
    comment = "//"
    install_hint = "Install Node.js from https://nodejs.org (LTS is fine)."

    def probe(self):
        ok, version = self._version(["node", "--version"])
        if not ok:
            return False, "Node.js not found"
        return True, f"Node {version.lstrip('v')}"

    # ------------------------------------------------------------- codegen
    def type_name(self, type_str: str) -> str:
        if is_list(type_str):
            return self.type_name(type_str[5:-1]) + "[]"
        return {INT: "number", FLOAT: "number", BOOL: "boolean", STR: "string"}[type_str]

    def literal(self, value, type_str: str) -> str:
        if value is None:
            return "null"
        if is_list(type_str):
            inner = type_str[5:-1]
            return "[" + ", ".join(self.literal(v, inner) for v in value) + "]"
        if type_str == STR:
            return quote(str(value))
        if type_str == BOOL:
            return "true" if value else "false"
        if type_str == FLOAT:
            return repr(float(value))
        return str(int(value))

    def starter(self, func: str, sig: Sig, doc: str = "") -> str:
        params = ", ".join(sig.names)
        types = ", ".join(f"{n}: {self.type_name(t)}" for n, t in sig.params)
        head = f"/**\n * {doc}\n */\n" if doc else ""
        return (f"{head}// {types}  ->  {self.type_name(sig.ret)}\n"
                f"function {func}({params}) {{\n  // your code here\n}}\n")

    def harness(self, func: str, sig: Sig, values) -> str:
        lines = [HELPERS]
        for index, (args, expected) in enumerate(values):
            arg_src = ", ".join(self.literal(a, t) for a, t in zip(args, sig.types))
            lines.append(f"""
try {{
  const got = {func}({arg_src});
  const exp = {self.literal(expected, sig.ret)};
  if (_cfEq(got, exp)) console.log("{SENTINEL}|{index}|PASS");
  else console.log("{SENTINEL}|{index}|FAIL|" + _cfFmt(got) + "|" + _cfFmt(exp));
}} catch (e) {{
  console.log("{SENTINEL}|{index}|ERROR|" +
    String((e && e.message) || e).replace(/\\|/g, " ").replace(/\\r?\\n/g, " "));
}}""")
        lines.append(f'\nconsole.log("{END}");\n')
        return "\n".join(lines)

    # ------------------------------------------------------------- running
    def run(self, user_code: str, func: str, sig: Sig, cases: list[dict],
            timeout: float = 25.0) -> RunOutcome:
        outcome = RunOutcome()
        values = parse_values(cases)
        source = user_code.rstrip() + "\n" + self.harness(func, sig, values)
        start = time.perf_counter()
        with tempfile.TemporaryDirectory(prefix="cf_js_") as tmp:
            path = os.path.join(tmp, "your_code.js")
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(source)
            code, out, err, timed_out = self._exec(["node", path], tmp, timeout)
        outcome.seconds = time.perf_counter() - start
        if timed_out:
            outcome.timed_out = True
            return outcome
        outcome.cases, outcome.stdout, completed = read_protocol(out, cases)
        if not completed and err.strip():
            # a syntax error means node never produced a single case line
            outcome.build_error = err.strip()
        outcome.ok = bool(outcome.cases) and all(c.passed for c in outcome.cases)
        return outcome
