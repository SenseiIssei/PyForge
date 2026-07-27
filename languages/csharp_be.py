"""C# backend, built on the .NET SDK.

The project directory is reused between runs so NuGet restore and the build
cache survive — otherwise every single test run would pay the cold-start cost.
The target framework is derived from whichever SDK is installed, so this
follows the machine forward instead of pinning an old version.
"""
from __future__ import annotations

import os
import re
import time

from .base import (BOOL, END, FLOAT, INT, SENTINEL, STR, Backend, RunOutcome, Sig,
                   is_list, parse_values, quote, read_protocol)

CSPROJ = """<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>{tfm}</TargetFramework>
    <AssemblyName>cf</AssemblyName>
    <RootNamespace>cf</RootNamespace>
    <Nullable>disable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
    <InvariantGlobalization>true</InvariantGlobalization>
    <GenerateDocumentationFile>false</GenerateDocumentationFile>
    <NoWarn>CS8981;CS0162;CS0168;CS0219</NoWarn>
    <EnableDefaultCompileItems>true</EnableDefaultCompileItems>
  </PropertyGroup>
</Project>
"""

HARNESS_HEAD = f'''// --- CodeForge test harness (generated) ------------------------------------
using System;
using System.Collections;
using System.Globalization;

public static class Harness
{{
    static string Fmt(object v)
    {{
        string s;
        if (v == null) s = "null";
        else if (v is string str) s = str;
        else if (v is double d) s = d.ToString("R", CultureInfo.InvariantCulture);
        else if (v is bool b) s = b ? "true" : "false";
        else if (v is IEnumerable seq)
        {{
            var parts = new System.Collections.Generic.List<string>();
            foreach (var item in seq) parts.Add(Fmt(item));
            s = "[" + string.Join(", ", parts) + "]";
        }}
        else s = Convert.ToString(v, CultureInfo.InvariantCulture);
        return s.Replace("|", "\\u00a6").Replace("\\n", " ");
    }}

    static bool Eq(object a, object b)
    {{
        if (a is double x && b is double y)
            return Math.Abs(x - y) <= 1e-6 * Math.Max(1.0, Math.Abs(y));
        if (a is IEnumerable sa && b is IEnumerable sb && !(a is string))
        {{
            var ea = sa.GetEnumerator();
            var eb = sb.GetEnumerator();
            while (true)
            {{
                bool na = ea.MoveNext(), nb = eb.MoveNext();
                if (na != nb) return false;
                if (!na) return true;
                if (!Eq(ea.Current, eb.Current)) return false;
            }}
        }}
        return Equals(a, b);
    }}

    static void Pass(int i) => Console.WriteLine($"{SENTINEL}|{{i}}|PASS");

    static void Fail(int i, object got, object exp) =>
        Console.WriteLine($"{SENTINEL}|{{i}}|FAIL|{{Fmt(got)}}|{{Fmt(exp)}}");

    static void Err(int i, Exception e) =>
        Console.WriteLine($"{SENTINEL}|{{i}}|ERROR|" +
            (e.GetType().Name + ": " + e.Message).Replace("|", " ").Replace("\\n", " "));

    public static void Main()
    {{
'''


class CSharpBackend(Backend):
    id = "csharp"
    label = "C#"
    ext = ".cs"
    comment = "//"
    install_hint = "Install the .NET SDK from https://dotnet.microsoft.com/download"

    def probe(self):
        ok, version = self._version(["dotnet", "--version"])
        if not ok:
            return False, ".NET SDK not found"
        return True, f".NET {version}"

    def _tfm(self) -> str:
        """net<major>.0 for the newest installed SDK."""
        ok, version = self.available()
        match = re.search(r"(\d+)\.", version or "")
        major = match.group(1) if match else "8"
        return f"net{major}.0"

    # ------------------------------------------------------------- codegen
    def type_name(self, type_str: str) -> str:
        if is_list(type_str):
            return self.type_name(type_str[5:-1]) + "[]"
        return {INT: "long", FLOAT: "double", BOOL: "bool", STR: "string"}[type_str]

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
            return f"{float(value)!r}d"
        return f"{int(value)}L"

    def starter(self, func: str, sig: Sig, doc: str = "") -> str:
        params = ", ".join(f"{self.type_name(t)} {n}" for n, t in sig.params)
        head = f"    // {doc}\n" if doc else ""
        return (f"public static class Solution\n{{\n{head}    public static "
                f"{self.type_name(sig.ret)} {func}({params})\n    {{\n"
                f"        // your code here\n        return {self._zero(sig.ret)};\n"
                f"    }}\n}}\n")

    def _zero(self, type_str: str) -> str:
        if is_list(type_str):
            return f"new {self.type_name(type_str)}{{}}"
        return {INT: "0", FLOAT: "0", BOOL: "false", STR: '""'}[type_str]

    def harness(self, func: str, sig: Sig, values) -> str:
        parts = [HARNESS_HEAD]
        for index, (args, expected) in enumerate(values):
            arg_src = ", ".join(self.literal(a, t) for a, t in zip(args, sig.types))
            ret = self.type_name(sig.ret)
            parts.append(f"""        try
        {{
            {ret} got = Solution.{func}({arg_src});
            {ret} exp = {self.literal(expected, sig.ret)};
            if (Eq(got, exp)) Pass({index}); else Fail({index}, got, exp);
        }}
        catch (Exception e) {{ Err({index}, e); }}
""")
        parts.append(f'        Console.WriteLine("{END}");\n    }}\n}}\n')
        return "".join(parts)

    # ------------------------------------------------------------- running
    def run(self, user_code: str, func: str, sig: Sig, cases: list[dict],
            timeout: float = 90.0) -> RunOutcome:
        outcome = RunOutcome()
        values = parse_values(cases)
        start = time.perf_counter()

        work = os.path.join(self.workspace(), "project")
        os.makedirs(work, exist_ok=True)
        # keep obj/ and bin/ so restore + incremental build stay warm
        with open(os.path.join(work, "cf.csproj"), "w", encoding="utf-8") as handle:
            handle.write(CSPROJ.format(tfm=self._tfm()))
        with open(os.path.join(work, "Solution.cs"), "w", encoding="utf-8") as handle:
            handle.write(user_code.rstrip() + "\n")
        with open(os.path.join(work, "Harness.cs"), "w", encoding="utf-8") as handle:
            handle.write(self.harness(func, sig, values))

        env = dict(os.environ)
        env["DOTNET_CLI_TELEMETRY_OPTOUT"] = "1"
        env["DOTNET_NOLOGO"] = "1"
        env["DOTNET_SKIP_FIRST_TIME_EXPERIENCE"] = "1"

        rc, out, err, timed_out = self._exec(
            ["dotnet", "build", "-c", "Debug", "--nologo", "-v", "q",
             "-o", "out", "cf.csproj"], work, timeout, env=env)
        if timed_out:
            outcome.timed_out = True
            return outcome
        if rc != 0:
            outcome.build_error = self._clean(out or err)
            outcome.seconds = time.perf_counter() - start
            return outcome

        dll = os.path.join(work, "out", "cf.dll")
        rc, out, err, timed_out = self._exec(["dotnet", dll], work, timeout, env=env)
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
                if line.strip() and "Determining projects to restore" not in line
                and not line.strip().startswith("Restored ")]
        return "\n".join(keep).strip() or text.strip()
