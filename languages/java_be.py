"""Java backend. User code goes into Solution.java, the harness into Harness.java."""
from __future__ import annotations

import os
import shutil
import time

from .base import (BOOL, END, FLOAT, INT, SENTINEL, STR, Backend, RunOutcome, Sig,
                   is_list, parse_values, quote, read_protocol)

HARNESS_HEAD = f'''// --- CodeForge test harness (generated) ------------------------------------
import java.util.Arrays;
import java.util.Objects;

public class Harness {{

    static String fmt(Object v) {{
        String s;
        if (v == null) s = "null";
        else if (v instanceof long[]) s = Arrays.toString((long[]) v);
        else if (v instanceof int[]) s = Arrays.toString((int[]) v);
        else if (v instanceof double[]) s = Arrays.toString((double[]) v);
        else if (v instanceof boolean[]) s = Arrays.toString((boolean[]) v);
        else if (v instanceof Object[]) s = Arrays.deepToString((Object[]) v);
        else s = String.valueOf(v);
        return s.replace("|", "\\u00a6").replace("\\n", " ");
    }}

    static boolean eq(Object a, Object b) {{
        if (a instanceof Double && b instanceof Double) {{
            double x = (Double) a, y = (Double) b;
            return Math.abs(x - y) <= 1e-6 * Math.max(1.0, Math.abs(y));
        }}
        if (a instanceof double[] && b instanceof double[]) {{
            double[] x = (double[]) a, y = (double[]) b;
            if (x.length != y.length) return false;
            for (int i = 0; i < x.length; i++)
                if (Math.abs(x[i] - y[i]) > 1e-6 * Math.max(1.0, Math.abs(y[i])))
                    return false;
            return true;
        }}
        return Objects.deepEquals(a, b);
    }}

    static void pass(int i) {{ System.out.println("{SENTINEL}|" + i + "|PASS"); }}

    static void fail(int i, Object got, Object exp) {{
        System.out.println("{SENTINEL}|" + i + "|FAIL|" + fmt(got) + "|" + fmt(exp));
    }}

    static void error(int i, Throwable t) {{
        String m = t.getClass().getSimpleName();
        if (t.getMessage() != null) m += ": " + t.getMessage();
        System.out.println("{SENTINEL}|" + i + "|ERROR|"
            + m.replace("|", " ").replace("\\n", " "));
    }}

    public static void main(String[] args) {{
'''


class JavaBackend(Backend):
    id = "java"
    label = "Java"
    ext = ".java"
    comment = "//"
    install_hint = "Install a JDK (Temurin, Oracle or your package manager)."

    def probe(self):
        if not self._which("javac") or not self._which("java"):
            return False, "JDK not found (javac and java must be on PATH)"
        ok, version = self._version(["javac", "-version"])
        return ok, version.replace("javac ", "JDK ") if ok else "JDK not usable"

    # ------------------------------------------------------------- codegen
    def type_name(self, type_str: str) -> str:
        if is_list(type_str):
            return self.type_name(type_str[5:-1]) + "[]"
        return {INT: "long", FLOAT: "double", BOOL: "boolean", STR: "String"}[type_str]

    def literal(self, value, type_str: str) -> str:
        if value is None:
            return "null"
        if is_list(type_str):
            inner = type_str[5:-1]
            body = ", ".join(self.literal(v, inner) for v in value)
            return f"new {self.type_name(type_str)}{{{body}}}"
        if type_str == STR:
            return quote(str(value))
        if type_str == BOOL:
            return "true" if value else "false"
        if type_str == FLOAT:
            return repr(float(value))
        return f"{int(value)}L"

    def _boxed(self, type_str: str) -> str:
        if is_list(type_str):
            return self.type_name(type_str)
        return {INT: "Long", FLOAT: "Double", BOOL: "Boolean", STR: "String"}[type_str]

    def starter(self, func: str, sig: Sig, doc: str = "") -> str:
        params = ", ".join(f"{self.type_name(t)} {n}" for n, t in sig.params)
        head = f"    // {doc}\n" if doc else ""
        return (f"class Solution {{\n{head}    static {self.type_name(sig.ret)} "
                f"{func}({params}) {{\n        // your code here\n"
                f"        return {self._zero(sig.ret)};\n    }}\n}}\n")

    def _zero(self, type_str: str) -> str:
        if is_list(type_str):
            return f"new {self.type_name(type_str)}{{}}"
        return {INT: "0", FLOAT: "0", BOOL: "false", STR: '""'}[type_str]

    def harness(self, func: str, sig: Sig, values) -> str:
        # One method per case. A single main() holding every literal blows past
        # the JVM's 64 KB per-method bytecode limit as soon as a test uses a
        # large array.
        ret = self.type_name(sig.ret)
        methods = []
        calls = []
        for index, (args, expected) in enumerate(values):
            arg_src = ", ".join(self.literal(a, t) for a, t in zip(args, sig.types))
            methods.append(f"""    static void case{index}() {{
        try {{
            {ret} got = Solution.{func}({arg_src});
            {ret} exp = {self.literal(expected, sig.ret)};
            if (eq(got, exp)) pass({index}); else fail({index}, got, exp);
        }} catch (Throwable t) {{ error({index}, t); }}
    }}
""")
            calls.append(f"        case{index}();")
        body = ("".join(methods) + "\n    public static void main(String[] args) {\n"
                + "\n".join(calls) + f'\n        System.out.println("{END}");\n'
                + "    }\n}\n")
        return HARNESS_HEAD.replace("    public static void main(String[] args) {\n",
                                    "") + body

    # ------------------------------------------------------------- running
    def run(self, user_code: str, func: str, sig: Sig, cases: list[dict],
            timeout: float = 30.0) -> RunOutcome:
        outcome = RunOutcome()
        values = parse_values(cases)
        start = time.perf_counter()

        work = os.path.join(self.workspace(), "run")
        shutil.rmtree(work, ignore_errors=True)
        os.makedirs(work, exist_ok=True)

        with open(os.path.join(work, "Solution.java"), "w", encoding="utf-8") as handle:
            handle.write(user_code.rstrip() + "\n")
        with open(os.path.join(work, "Harness.java"), "w", encoding="utf-8") as handle:
            handle.write(self.harness(func, sig, values))

        rc, out, err, timed_out = self._exec(
            ["javac", "-encoding", "UTF-8", "-nowarn", "-d", ".",
             "Solution.java", "Harness.java"], work, timeout)
        if timed_out:
            outcome.timed_out = True
            return outcome
        if rc != 0:
            outcome.build_error = (err or out).strip()
            outcome.seconds = time.perf_counter() - start
            return outcome

        rc, out, err, timed_out = self._exec(
            ["java", "-XX:+UseSerialGC", "-Xshare:auto", "-cp", ".", "Harness"],
            work, timeout)
        outcome.seconds = time.perf_counter() - start
        if timed_out:
            outcome.timed_out = True
            return outcome

        outcome.cases, outcome.stdout, completed = read_protocol(out, cases)
        if not completed and err.strip() and not any(c.passed for c in outcome.cases):
            outcome.runtime_error = err.strip()
        outcome.ok = bool(outcome.cases) and all(c.passed for c in outcome.cases)
        return outcome
