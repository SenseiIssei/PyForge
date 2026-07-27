"""C++ backend.

Prefers g++ or clang++. On Windows without either it falls back to the MSVC
compiler that ships with Visual Studio, invoked through vcvars64.bat so cl.exe
finds its headers and libraries.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import time

from .base import (BOOL, END, FLOAT, INT, SENTINEL, STR, Backend, RunOutcome, Sig,
                   is_list, parse_values, quote, read_protocol)

HARNESS_HEAD = f'''

// --- CodeForge test harness (generated) ------------------------------------
#include <cmath>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

static std::string cf_str(long long v) {{ return std::to_string(v); }}
static std::string cf_str(bool v) {{ return v ? "true" : "false"; }}
static std::string cf_str(double v) {{
    std::ostringstream os; os << v; return os.str();
}}
static std::string cf_str(const std::string& v) {{ return v; }}

template <typename T>
static std::string cf_str(const std::vector<T>& v) {{
    std::string out = "[";
    for (size_t i = 0; i < v.size(); ++i) {{
        if (i) out += ", ";
        out += cf_str(v[i]);
    }}
    return out + "]";
}}

static std::string cf_clean(std::string s) {{
    std::string out;
    for (char c : s) {{
        if (c == '|') out += "\\u00a6";
        else if (c == '\\n' || c == '\\r') out += ' ';
        else out += c;
    }}
    return out;
}}

static bool cf_eq(double a, double b) {{
    return std::fabs(a - b) <= 1e-6 * std::fmax(1.0, std::fabs(b));
}}
static bool cf_eq(long long a, long long b) {{ return a == b; }}
static bool cf_eq(bool a, bool b) {{ return a == b; }}
static bool cf_eq(const std::string& a, const std::string& b) {{ return a == b; }}

template <typename T>
static bool cf_eq(const std::vector<T>& a, const std::vector<T>& b) {{
    if (a.size() != b.size()) return false;
    for (size_t i = 0; i < a.size(); ++i) if (!cf_eq(a[i], b[i])) return false;
    return true;
}}

int main() {{
'''


class CppBackend(Backend):
    id = "cpp"
    label = "C++"
    ext = ".cpp"
    comment = "//"
    install_hint = ("Install g++ (build-essential / Xcode command line tools) or "
                    "Visual Studio with the C++ workload.")

    _vcvars_cache: str | None = None

    # ------------------------------------------------------------ toolchain
    @classmethod
    def _vcvars(cls) -> str | None:
        if cls._vcvars_cache is not None:
            return cls._vcvars_cache or None
        found = ""
        if os.name == "nt":
            program_files = os.environ.get("ProgramFiles(x86)",
                                           r"C:\Program Files (x86)")
            vswhere = os.path.join(program_files, "Microsoft Visual Studio",
                                   "Installer", "vswhere.exe")
            if os.path.isfile(vswhere):
                try:
                    result = subprocess.run(
                        [vswhere, "-latest", "-products", "*", "-requires",
                         "Microsoft.VisualStudio.Component.VC.Tools.x86.x64",
                         "-property", "installationPath"],
                        capture_output=True, text=True, timeout=25,
                        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
                    root = result.stdout.strip().splitlines()
                    if root:
                        candidate = os.path.join(root[0], "VC", "Auxiliary", "Build",
                                                 "vcvars64.bat")
                        if os.path.isfile(candidate):
                            found = candidate
                except Exception:
                    found = ""
        cls._vcvars_cache = found
        return found or None

    def _compiler(self) -> tuple[str, str]:
        """('gcc'|'clang'|'msvc'|'', description)."""
        for name, kind in (("g++", "gcc"), ("clang++", "clang")):
            if self._which(name):
                ok, version = self._version([name, "--version"])
                if ok:
                    return kind, version
        if self._vcvars():
            return "msvc", "MSVC (Visual Studio)"
        return "", ""

    def probe(self):
        kind, version = self._compiler()
        if not kind:
            return False, "no C++ compiler found"
        return True, version

    # ------------------------------------------------------------- codegen
    def type_name(self, type_str: str) -> str:
        if is_list(type_str):
            return f"std::vector<{self.type_name(type_str[5:-1])}>"
        return {INT: "long long", FLOAT: "double", BOOL: "bool",
                STR: "std::string"}[type_str]

    def param_type(self, type_str: str) -> str:
        if is_list(type_str) or type_str == STR:
            return f"const {self.type_name(type_str)}&"
        return self.type_name(type_str)

    def literal(self, value, type_str: str) -> str:
        if value is None:
            return f"{self.type_name(type_str)}{{}}"
        if is_list(type_str):
            inner = type_str[5:-1]
            body = ", ".join(self.literal(v, inner) for v in value)
            return f"{self.type_name(type_str)}{{{body}}}"
        if type_str == STR:
            return f"std::string({quote(str(value))})"
        if type_str == BOOL:
            return "true" if value else "false"
        if type_str == FLOAT:
            return repr(float(value))
        return f"{int(value)}LL"

    def starter(self, func: str, sig: Sig, doc: str = "") -> str:
        params = ", ".join(f"{self.param_type(t)} {n}" for n, t in sig.params)
        head = f"// {doc}\n" if doc else ""
        return ("#include <string>\n#include <vector>\n\n"
                f"{head}{self.type_name(sig.ret)} {func}({params}) {{\n"
                f"    // your code here\n    return {self._zero(sig.ret)};\n}}\n")

    def _zero(self, type_str: str) -> str:
        if is_list(type_str) or type_str == STR:
            return "{}"
        return {INT: "0", FLOAT: "0", BOOL: "false"}[type_str]

    def harness(self, func: str, sig: Sig, values) -> str:
        parts = [HARNESS_HEAD]
        for index, (args, expected) in enumerate(values):
            arg_src = ", ".join(self.literal(a, t) for a, t in zip(args, sig.types))
            ret = self.type_name(sig.ret)
            parts.append(f"""    try {{
        {ret} got = {func}({arg_src});
        {ret} exp = {self.literal(expected, sig.ret)};
        if (cf_eq(got, exp)) std::cout << "{SENTINEL}|{index}|PASS" << std::endl;
        else std::cout << "{SENTINEL}|{index}|FAIL|" << cf_clean(cf_str(got))
                       << "|" << cf_clean(cf_str(exp)) << std::endl;
    }} catch (const std::exception& e) {{
        std::cout << "{SENTINEL}|{index}|ERROR|" << cf_clean(e.what()) << std::endl;
    }} catch (...) {{
        std::cout << "{SENTINEL}|{index}|ERROR|unknown exception" << std::endl;
    }}
""")
        parts.append(f'    std::cout << "{END}" << std::endl;\n    return 0;\n}}\n')
        return "".join(parts)

    # ------------------------------------------------------------- running
    def run(self, user_code: str, func: str, sig: Sig, cases: list[dict],
            timeout: float = 60.0) -> RunOutcome:
        outcome = RunOutcome()
        values = parse_values(cases)
        start = time.perf_counter()

        kind, _ = self._compiler()
        if not kind:
            outcome.build_error = "No C++ compiler found."
            return outcome

        work = os.path.join(self.workspace(), "run")
        shutil.rmtree(work, ignore_errors=True)
        os.makedirs(work, exist_ok=True)
        source = user_code.rstrip() + "\n" + self.harness(func, sig, values)
        with open(os.path.join(work, "main.cpp"), "w", encoding="utf-8") as handle:
            handle.write(source)

        binary = "prog.exe" if os.name == "nt" else "prog"
        if kind == "msvc":
            # Go through a .bat file: passing the vcvars path plus redirections
            # as one cmd /c argument gets mangled by Windows quoting rules.
            os.makedirs(os.path.join(work, "obj"), exist_ok=True)
            script = os.path.join(work, "cf_build.bat")
            with open(script, "w", encoding="mbcs", newline="\r\n") as handle:
                handle.write("@echo off\n")
                handle.write(f'call "{self._vcvars()}" >nul 2>&1\n')
                handle.write(f"cl /nologo /std:c++20 /EHsc /O2 /utf-8 /W1 "
                             f"/Fe:{binary} /Fo:obj\\ main.cpp\n")
                handle.write("exit /b %ERRORLEVEL%\n")
            rc, out, err, timed_out = self._exec(["cmd", "/c", script], work, timeout)
            build_log = out or err
        else:
            compiler = "g++" if kind == "gcc" else "clang++"
            rc, out, err, timed_out = self._exec(
                [compiler, "-std=c++20", "-O2", "-w", "-o", binary, "main.cpp"],
                work, timeout)
            build_log = err or out

        if timed_out:
            outcome.timed_out = True
            return outcome
        if rc != 0:
            outcome.build_error = self._clean(build_log)
            outcome.seconds = time.perf_counter() - start
            return outcome

        rc, out, err, timed_out = self._exec(
            [os.path.join(work, binary)], work, timeout)
        outcome.seconds = time.perf_counter() - start
        if timed_out:
            outcome.timed_out = True
            return outcome

        outcome.cases, outcome.stdout, completed = read_protocol(out, cases)
        if not completed and err.strip() and not any(c.passed for c in outcome.cases):
            outcome.runtime_error = err.strip()
        outcome.ok = bool(outcome.cases) and all(c.passed for c in outcome.cases)
        return outcome

    @staticmethod
    def _clean(text: str) -> str:
        keep = [line for line in text.splitlines()
                if line.strip() and line.strip() != "main.cpp"]
        return "\n".join(keep[:40]).strip() or text.strip()
