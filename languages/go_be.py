"""Go backend.

User code and harness live in two files of the same `package main`, so each can
carry its own imports and the user is never fighting the harness over an unused
import — which in Go is a compile error, not a warning.
"""
from __future__ import annotations

import os
import shutil
import tempfile
import time

from .base import (BOOL, END, FLOAT, INT, SENTINEL, STR, Backend, RunOutcome, Sig,
                   is_list, parse_values, quote, read_protocol)

HARNESS_HEAD = f'''package main

// --- CodeForge test harness (generated) ------------------------------------

import (
	"fmt"
	"reflect"
	"strings"
)

func cfFmt(v interface{{}}) string {{
	s := fmt.Sprintf("%v", v)
	s = strings.ReplaceAll(s, "|", "\\u00a6")
	s = strings.ReplaceAll(s, "\\n", " ")
	return s
}}

func cfEq(a, b interface{{}}) bool {{
	if af, ok := a.(float64); ok {{
		if bf, ok2 := b.(float64); ok2 {{
			d := af - bf
			if d < 0 {{
				d = -d
			}}
			m := bf
			if m < 0 {{
				m = -m
			}}
			if m < 1 {{
				m = 1
			}}
			return d <= 1e-6*m
		}}
	}}
	return reflect.DeepEqual(a, b)
}}

func cfCase(index int, run func() (interface{{}}, interface{{}})) {{
	defer func() {{
		if r := recover(); r != nil {{
			msg := strings.ReplaceAll(fmt.Sprintf("%v", r), "|", " ")
			msg = strings.ReplaceAll(msg, "\\n", " ")
			fmt.Printf("{SENTINEL}|%d|ERROR|%s\\n", index, msg)
		}}
	}}()
	got, exp := run()
	if cfEq(got, exp) {{
		fmt.Printf("{SENTINEL}|%d|PASS\\n", index)
	}} else {{
		fmt.Printf("{SENTINEL}|%d|FAIL|%s|%s\\n", index, cfFmt(got), cfFmt(exp))
	}}
}}

func main() {{
'''


class GoBackend(Backend):
    id = "go"
    label = "Go"
    ext = ".go"
    comment = "//"
    install_hint = "Install Go from https://go.dev/dl/"

    def probe(self):
        ok, version = self._version(["go", "version"])
        if not ok:
            return False, "Go not found"
        parts = version.split()
        return True, parts[2].lstrip("go") if len(parts) > 2 else version

    # ------------------------------------------------------------- codegen
    def type_name(self, type_str: str) -> str:
        if is_list(type_str):
            return "[]" + self.type_name(type_str[5:-1])
        return {INT: "int", FLOAT: "float64", BOOL: "bool", STR: "string"}[type_str]

    def literal(self, value, type_str: str) -> str:
        if value is None:
            return self.type_name(type_str) + "{}" if is_list(type_str) else "0"
        if is_list(type_str):
            inner = type_str[5:-1]
            body = ", ".join(self.literal(v, inner) for v in value)
            return f"{self.type_name(type_str)}{{{body}}}"
        if type_str == STR:
            return quote(str(value))
        if type_str == BOOL:
            return "true" if value else "false"
        if type_str == FLOAT:
            return repr(float(value))
        return str(int(value))

    def starter(self, func: str, sig: Sig, doc: str = "") -> str:
        params = ", ".join(f"{n} {self.type_name(t)}" for n, t in sig.params)
        head = f"// {doc}\n" if doc else ""
        zero = self._zero(sig.ret)
        return (f"package main\n\n{head}func {func}({params}) {self.type_name(sig.ret)} "
                f"{{\n\t// your code here\n\treturn {zero}\n}}\n")

    def _zero(self, type_str: str) -> str:
        if is_list(type_str):
            return f"{self.type_name(type_str)}{{}}"
        return {INT: "0", FLOAT: "0", BOOL: "false", STR: '""'}[type_str]

    def harness(self, func: str, sig: Sig, values) -> str:
        lines = [HARNESS_HEAD]
        for index, (args, expected) in enumerate(values):
            arg_src = ", ".join(self.literal(a, t) for a, t in zip(args, sig.types))
            exp_src = self.literal(expected, sig.ret)
            lines.append(
                f"\tcfCase({index}, func() (interface{{}}, interface{{}}) {{\n"
                f"\t\treturn {func}({arg_src}), {exp_src}\n"
                f"\t}})\n")
        lines.append(f'\tfmt.Println("{END}")\n}}\n')
        return "".join(lines)

    # ------------------------------------------------------------- running
    def run(self, user_code: str, func: str, sig: Sig, cases: list[dict],
            timeout: float = 25.0) -> RunOutcome:
        outcome = RunOutcome()
        values = parse_values(cases)
        start = time.perf_counter()

        work = os.path.join(self.workspace(), "run")
        shutil.rmtree(work, ignore_errors=True)
        os.makedirs(work, exist_ok=True)

        code = user_code.strip()
        if not code.startswith("package "):
            code = "package main\n\n" + code
        with open(os.path.join(work, "solution.go"), "w", encoding="utf-8") as handle:
            handle.write(code + "\n")
        with open(os.path.join(work, "harness.go"), "w", encoding="utf-8") as handle:
            handle.write(self.harness(func, sig, values))
        with open(os.path.join(work, "go.mod"), "w", encoding="utf-8") as handle:
            handle.write("module codeforge\n\ngo 1.21\n")

        env = dict(os.environ)
        env.setdefault("GOCACHE", os.path.join(self.workspace(), "gocache"))
        env["GOFLAGS"] = "-mod=mod"
        env["GOTOOLCHAIN"] = "local"

        rc, out, err, timed_out = self._exec(["go", "run", "."], work, timeout, env=env)
        outcome.seconds = time.perf_counter() - start
        if timed_out:
            outcome.timed_out = True
            return outcome

        outcome.cases, outcome.stdout, completed = read_protocol(out, cases)
        if not completed and err.strip() and not any(c.passed for c in outcome.cases):
            outcome.build_error = self._clean(err)
        outcome.ok = bool(outcome.cases) and all(c.passed for c in outcome.cases)
        return outcome

    @staticmethod
    def _clean(text: str) -> str:
        keep = [line for line in text.splitlines()
                if not line.startswith("# ") and "go: downloading" not in line]
        return "\n".join(keep).strip() or text.strip()
