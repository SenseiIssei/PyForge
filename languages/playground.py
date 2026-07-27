"""Starter programs for the Playground, one per language.

Each one does the same three things, so switching language shows you the same
program written idiomatically elsewhere: read whatever is on stdin, print
something formatted, and loop.

The comments are translated, because the Playground is a place you read as much
as you type.
"""
from __future__ import annotations

# ---------------------------------------------------------------------------
_COMMENTS = {
    "python": {
        "en": ("Scratch space. Ctrl+Enter runs it, your output shows below.\n"
               "The Input (stdin) box on the right feeds input() — like a judge does."),
        "de": ("Freier Platz. Strg+Enter fuehrt aus, deine Ausgabe erscheint unten.\n"
               "Das Eingabefeld rechts fuettert input() — genau wie ein Pruefsystem."),
        "fr": ("Espace libre. Ctrl+Entree execute, la sortie s'affiche en dessous.\n"
               "Le champ Entree a droite alimente input(), comme un juge en ligne."),
        "es": ("Espacio libre. Ctrl+Intro lo ejecuta y la salida aparece abajo.\n"
               "El campo de entrada de la derecha alimenta input(), como un juez."),
    },
}

_HEADERS = {
    "en": ("Scratch space — {run} runs it, your output shows below.",
           "The Input (stdin) box on the right feeds the program, like a judge does."),
    "de": ("Freier Platz — {run} fuehrt aus, deine Ausgabe erscheint unten.",
           "Das Eingabefeld rechts fuettert das Programm, genau wie ein Pruefsystem."),
    "fr": ("Espace libre — {run} execute, la sortie s'affiche en dessous.",
           "Le champ Entree a droite alimente le programme, comme un juge en ligne."),
    "es": ("Espacio libre — {run} lo ejecuta y la salida aparece abajo.",
           "El campo de entrada de la derecha alimenta el programa, como un juez."),
}

_LABELS = {
    "en": ("read", "sum", "max", "nothing on stdin — try 3 1 4 1 5", "squared is"),
    "de": ("gelesen", "Summe", "Maximum", "nichts auf stdin — versuch 3 1 4 1 5",
           "zum Quadrat ist"),
    "fr": ("lu", "somme", "max", "rien sur stdin — essayez 3 1 4 1 5", "au carre fait"),
    "es": ("leido", "suma", "max", "nada en stdin — prueba 3 1 4 1 5", "al cuadrado es"),
}


def _head(language: str, comment: str, run_key: str) -> str:
    first, second = _HEADERS.get(language, _HEADERS["en"])
    return f"{comment} {first.format(run=run_key)}\n{comment} {second}\n"


def source_for(backend_id: str, language: str = "en") -> str:
    """The starter program for `backend_id`, commented in `language`."""
    read, total, biggest, empty, squared = _LABELS.get(language, _LABELS["en"])
    run_key = "Strg+Enter" if language == "de" else (
        "Ctrl+Entree" if language == "fr" else
        "Ctrl+Intro" if language == "es" else "Ctrl+Enter")

    if backend_id == "python":
        head = _head(language, "#", run_key)
        return f'''{head}
import sys

data = sys.stdin.read().split()
if data:
    nums = [int(x) for x in data]
    print("{read}:", nums)
    print("{total}:", sum(nums), "{biggest}:", max(nums))
else:
    print("{empty}")

print()
for i in range(1, 6):
    print(f"{{i:>3}} {squared} {{i * i:>4}}")
'''

    if backend_id == "javascript":
        head = _head(language, "//", run_key)
        return f'''{head}
const text = require("fs").readFileSync(0, "utf8").trim();
const data = text ? text.split(/\\s+/) : [];

if (data.length) {{
  const nums = data.map(Number);
  console.log("{read}:", nums);
  console.log("{total}:", nums.reduce((a, b) => a + b, 0),
              "{biggest}:", Math.max(...nums));
}} else {{
  console.log("{empty}");
}}

console.log();
for (let i = 1; i <= 5; i++) {{
  console.log(String(i).padStart(3) + " {squared} " + String(i * i).padStart(4));
}}
'''

    if backend_id == "java":
        head = _head(language, "//", run_key)
        return f'''{head}
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class Main {{
    public static void main(String[] args) {{
        Scanner scanner = new Scanner(System.in);
        List<Long> nums = new ArrayList<>();
        while (scanner.hasNextLong()) nums.add(scanner.nextLong());

        if (!nums.isEmpty()) {{
            long total = 0, biggest = Long.MIN_VALUE;
            for (long n : nums) {{
                total += n;
                if (n > biggest) biggest = n;
            }}
            System.out.println("{read}: " + nums);
            System.out.println("{total}: " + total + "  {biggest}: " + biggest);
        }} else {{
            System.out.println("{empty}");
        }}

        System.out.println();
        for (int i = 1; i <= 5; i++) {{
            System.out.printf("%3d {squared} %4d%n", i, i * i);
        }}
    }}
}}
'''

    if backend_id == "csharp":
        head = _head(language, "//", run_key)
        return f'''{head}
using System;
using System.Collections.Generic;
using System.Linq;

class Program
{{
    static void Main()
    {{
        var text = Console.In.ReadToEnd().Trim();
        var nums = new List<long>();
        if (text.Length > 0)
            foreach (var part in text.Split((char[])null,
                                            StringSplitOptions.RemoveEmptyEntries))
                nums.Add(long.Parse(part));

        if (nums.Count > 0)
        {{
            Console.WriteLine("{read}: [" + string.Join(", ", nums) + "]");
            Console.WriteLine("{total}: " + nums.Sum() + "  {biggest}: " + nums.Max());
        }}
        else
        {{
            Console.WriteLine("{empty}");
        }}

        Console.WriteLine();
        for (int i = 1; i <= 5; i++)
            Console.WriteLine($"{{i,3}} {squared} {{i * i,4}}");
    }}
}}
'''

    if backend_id == "go":
        head = _head(language, "//", run_key)
        return f'''{head}
package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {{
	reader := bufio.NewReader(os.Stdin)
	raw, _ := reader.ReadString(0)
	fields := strings.Fields(raw)

	if len(fields) > 0 {{
		nums := []int{{}}
		total, biggest := 0, 0
		for i, f := range fields {{
			n, _ := strconv.Atoi(f)
			nums = append(nums, n)
			total += n
			if i == 0 || n > biggest {{
				biggest = n
			}}
		}}
		fmt.Println("{read}:", nums)
		fmt.Println("{total}:", total, " {biggest}:", biggest)
	}} else {{
		fmt.Println("{empty}")
	}}

	fmt.Println()
	for i := 1; i <= 5; i++ {{
		fmt.Printf("%3d {squared} %4d\\n", i, i*i)
	}}
}}
'''

    if backend_id == "rust":
        head = _head(language, "//", run_key)
        return f'''{head}
use std::io::Read;

fn main() {{
    let mut raw = String::new();
    std::io::stdin().read_to_string(&mut raw).ok();

    let nums: Vec<i64> = raw
        .split_whitespace()
        .filter_map(|part| part.parse().ok())
        .collect();

    if !nums.is_empty() {{
        let total: i64 = nums.iter().sum();
        let biggest = nums.iter().max().unwrap();
        println!("{read}: {{:?}}", nums);
        println!("{total}: {{}}  {biggest}: {{}}", total, biggest);
    }} else {{
        println!("{empty}");
    }}

    println!();
    for i in 1..=5 {{
        println!("{{:>3}} {squared} {{:>4}}", i, i * i);
    }}
}}
'''

    if backend_id == "cpp":
        head = _head(language, "//", run_key)
        return f'''{head}
#include <iomanip>
#include <iostream>
#include <vector>

int main() {{
    std::vector<long long> nums;
    long long value;
    while (std::cin >> value) nums.push_back(value);

    if (!nums.empty()) {{
        long long total = 0, biggest = nums[0];
        for (long long n : nums) {{
            total += n;
            if (n > biggest) biggest = n;
        }}
        std::cout << "{read}: [";
        for (size_t i = 0; i < nums.size(); ++i) {{
            if (i) std::cout << ", ";
            std::cout << nums[i];
        }}
        std::cout << "]" << std::endl;
        std::cout << "{total}: " << total << "  {biggest}: " << biggest << std::endl;
    }} else {{
        std::cout << "{empty}" << std::endl;
    }}

    std::cout << std::endl;
    for (int i = 1; i <= 5; ++i) {{
        std::cout << std::setw(3) << i << " {squared} "
                  << std::setw(4) << i * i << std::endl;
    }}
    return 0;
}}
'''

    return "// no playground template for this language yet\n"


# ===========================================================================
#  How each toolchain builds and runs a free-form program.
#
#  Kept here rather than in the seven backend modules: this is the same
#  information in seven dialects, and reading it side by side is how you spot
#  that one of them is wrong.
# ===========================================================================
import os  # noqa: E402  (kept next to the code that uses it)


def _go_mod() -> dict:
    return {"go.mod": "module codeforge\n\ngo 1.21\n"}


def _csproj(tfm: str) -> dict:
    return {"cf.csproj": f"""<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>{tfm}</TargetFramework>
    <AssemblyName>cf</AssemblyName>
    <Nullable>disable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
    <InvariantGlobalization>true</InvariantGlobalization>
    <NoWarn>CS8981;CS0162;CS0168;CS0219</NoWarn>
  </PropertyGroup>
</Project>
"""}


SPEC: dict[str, dict] = {
    "python": {
        "file": "main.py",
        "build": lambda backend, work, binary: None,
        "run": lambda backend, work, binary: _python_command(work),
    },
    "javascript": {
        "file": "main.js",
        "build": lambda backend, work, binary: None,
        "run": lambda backend, work, binary: ["node", "main.js"],
    },
    "java": {
        "file": "Main.java",
        "build": lambda backend, work, binary: [
            "javac", "-encoding", "UTF-8", "-nowarn", "-d", ".", "Main.java"],
        "run": lambda backend, work, binary: ["java", "-cp", ".", "Main"],
    },
    "csharp": {
        "file": "Program.cs",
        "extra": lambda backend, work: _csproj(backend._tfm()),
        "build": lambda backend, work, binary: [
            "dotnet", "build", "-c", "Debug", "--nologo", "-v", "q",
            "-o", "out", "cf.csproj"],
        "run": lambda backend, work, binary: [
            "dotnet", os.path.join(work, "out", "cf.dll")],
        "env": lambda backend, work: {"DOTNET_CLI_TELEMETRY_OPTOUT": "1",
                                      "DOTNET_NOLOGO": "1"},
    },
    "go": {
        "file": "main.go",
        "extra": lambda backend, work: _go_mod(),
        "build": lambda backend, work, binary: None,
        "run": lambda backend, work, binary: ["go", "run", "."],
        "env": lambda backend, work: {
            "GOCACHE": os.path.join(backend.workspace(), "gocache"),
            "GOFLAGS": "-mod=mod", "GOTOOLCHAIN": "local"},
    },
    "rust": {
        "file": "main.rs",
        "build": lambda backend, work, binary: [
            "rustc", "--edition", "2024", "-O", "-C", "debuginfo=0",
            "-o", binary, "main.rs"],
        "run": lambda backend, work, binary: [os.path.join(work, binary)],
    },
    "cpp": {
        "file": "main.cpp",
        "build": lambda backend, work, binary: _cpp_build(backend, work, binary),
        "run": lambda backend, work, binary: [os.path.join(work, binary)],
    },
}


def _python_command(work: str) -> list[str]:
    import runner as legacy_runner
    return legacy_runner._interpreter() + ["main.py"]


def _cpp_build(backend, work: str, binary: str) -> list[str]:
    kind, _ = backend._compiler()
    if kind == "msvc":
        # Same reason as in the grading path: passing vcvars plus redirections
        # as one cmd /c argument gets mangled by Windows quoting.
        os.makedirs(os.path.join(work, "obj"), exist_ok=True)
        script = os.path.join(work, "cf_build.bat")
        with open(script, "w", encoding="mbcs", newline="\r\n") as handle:
            handle.write("@echo off\n")
            handle.write(f'call "{backend._vcvars()}" >nul 2>&1\n')
            handle.write(f"cl /nologo /std:c++20 /EHsc /O2 /utf-8 /W1 "
                         f"/Fe:{binary} /Fo:obj\\ main.cpp\n")
            handle.write("exit /b %ERRORLEVEL%\n")
        return ["cmd", "/c", script]
    compiler = "g++" if kind == "gcc" else "clang++"
    return [compiler, "-std=c++20", "-O2", "-w", "-o", binary, "main.cpp"]


def spec(backend_id: str) -> dict | None:
    return SPEC.get(backend_id)
