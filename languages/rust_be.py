"""Rust backend. rustc directly — no cargo project, so no network and no wait."""
from __future__ import annotations

import os
import shutil
import time

from .base import (BOOL, END, FLOAT, INT, SENTINEL, STR, Backend, RunOutcome, Sig,
                   is_list, parse_values, quote, read_protocol)

HARNESS_HEAD = f'''

// --- CodeForge test harness (generated) ------------------------------------
#[allow(dead_code)]
fn cf_clean(s: String) -> String {{
    s.replace('|', "\\u{{a6}}").replace('\\n', " ")
}}

#[allow(dead_code)]
fn cf_close(a: f64, b: f64) -> bool {{
    (a - b).abs() <= 1e-6 * f64::max(1.0, b.abs())
}}

fn main() {{
    std::panic::set_hook(Box::new(|_| {{}}));
'''


class RustBackend(Backend):
    id = "rust"
    label = "Rust"
    ext = ".rs"
    comment = "//"
    install_hint = "Install Rust from https://rustup.rs"

    def probe(self):
        ok, version = self._version(["rustc", "--version"])
        if not ok:
            return False, "rustc not found"
        parts = version.split()
        return True, f"Rust {parts[1]}" if len(parts) > 1 else version

    # ------------------------------------------------------------- codegen
    def type_name(self, type_str: str, owned: bool = True) -> str:
        if is_list(type_str):
            return f"Vec<{self.type_name(type_str[5:-1])}>"
        return {INT: "i64", FLOAT: "f64", BOOL: "bool", STR: "String"}[type_str]

    def param_type(self, type_str: str) -> str:
        """Borrowed where that is the idiomatic choice."""
        if is_list(type_str):
            return f"&[{self.type_name(type_str[5:-1])}]"
        if type_str == STR:
            return "&str"
        return self.type_name(type_str)

    def literal(self, value, type_str: str) -> str:
        if value is None:
            return "Default::default()"
        if is_list(type_str):
            inner = type_str[5:-1]
            if not value:
                # vec![] alone gives "type annotations needed"
                return f"Vec::<{self.type_name(inner)}>::new()"
            body = ", ".join(self.literal(v, inner) for v in value)
            return f"vec![{body}]"
        if type_str == STR:
            return f"{quote(str(value))}.to_string()"
        if type_str == BOOL:
            return "true" if value else "false"
        if type_str == FLOAT:
            return f"{float(value)!r}f64"
        return f"{int(value)}i64"

    def arg_literal(self, value, type_str: str) -> str:
        """Same value, shaped for a borrowed parameter."""
        if is_list(type_str):
            return "&" + self.literal(value, type_str)
        if type_str == STR:
            return quote(str(value))
        return self.literal(value, type_str)

    def starter(self, func: str, sig: Sig, doc: str = "") -> str:
        params = ", ".join(f"{n}: {self.param_type(t)}" for n, t in sig.params)
        head = f"// {doc}\n" if doc else ""
        return (f"{head}fn {func}({params}) -> {self.type_name(sig.ret)} {{\n"
                f"    // your code here\n    {self._zero(sig.ret)}\n}}\n")

    def _zero(self, type_str: str) -> str:
        if is_list(type_str):
            return "Vec::new()"
        return {INT: "0", FLOAT: "0.0", BOOL: "false", STR: "String::new()"}[type_str]

    def _cmp(self, ret: str) -> str:
        if ret == FLOAT:
            return "cf_close(got, exp)"
        if ret == "list[float]":
            return ("got.len() == exp.len() && got.iter().zip(exp.iter())"
                    ".all(|(a, b)| cf_close(*a, *b))")
        return "got == exp"

    def harness(self, func: str, sig: Sig, values) -> str:
        parts = [HARNESS_HEAD]
        for index, (args, expected) in enumerate(values):
            arg_src = ", ".join(self.arg_literal(a, t) for a, t in zip(args, sig.types))
            parts.append(f"""    {{
        let outcome = std::panic::catch_unwind(|| {func}({arg_src}));
        match outcome {{
            Ok(got) => {{
                let exp = {self.literal(expected, sig.ret)};
                if {self._cmp(sig.ret)} {{
                    println!("{SENTINEL}|{index}|PASS");
                }} else {{
                    println!("{SENTINEL}|{index}|FAIL|{{}}|{{}}",
                        cf_clean(format!("{{:?}}", got)), cf_clean(format!("{{:?}}", exp)));
                }}
            }}
            Err(e) => {{
                let msg = e.downcast_ref::<String>().cloned()
                    .or_else(|| e.downcast_ref::<&str>().map(|s| s.to_string()))
                    .unwrap_or_else(|| "panicked".to_string());
                println!("{SENTINEL}|{index}|ERROR|{{}}", cf_clean(msg));
            }}
        }}
    }}
""")
        parts.append(f'    println!("{END}");\n}}\n')
        return "".join(parts)

    # ------------------------------------------------------------- running
    def run(self, user_code: str, func: str, sig: Sig, cases: list[dict],
            timeout: float = 45.0) -> RunOutcome:
        outcome = RunOutcome()
        values = parse_values(cases)
        start = time.perf_counter()

        work = os.path.join(self.workspace(), "run")
        shutil.rmtree(work, ignore_errors=True)
        os.makedirs(work, exist_ok=True)

        source = ("#![allow(unused_variables, unused_mut, dead_code, unused_imports)]\n"
                  + user_code.rstrip() + "\n" + self.harness(func, sig, values))
        with open(os.path.join(work, "main.rs"), "w", encoding="utf-8") as handle:
            handle.write(source)

        binary = "prog.exe" if os.name == "nt" else "prog"
        rc, out, err, timed_out = self._exec(
            ["rustc", "--edition", "2024", "-O", "-C", "debuginfo=0",
             "-o", binary, "main.rs"], work, timeout)
        if timed_out:
            outcome.timed_out = True
            return outcome
        if rc != 0:
            outcome.build_error = self._clean(err or out)
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
        keep, seen_error = [], False
        for line in text.splitlines():
            if line.startswith("warning"):
                continue
            if line.startswith("error"):
                seen_error = True
            if seen_error or line.strip():
                keep.append(line)
            if len(keep) > 40:
                break
        return "\n".join(keep).strip() or text.strip()
