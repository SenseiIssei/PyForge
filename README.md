# CodeForge

[![build](https://github.com/SenseiIssei/CodeForge/actions/workflows/build.yml/badge.svg)](https://github.com/SenseiIssei/CodeForge/actions/workflows/build.yml)
[![license: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A desktop app for learning to program and then grinding coding-interview problems —
built for a Codility screen, useful for any of them.

**Switch the programming language inside the app.** Python, JavaScript, Java, C#, Go,
Rust and C++ all work: you get the same problem, starter code generated for that
language's type system, and your solution is compiled and graded by the real toolchain.

**English, German, French and Spanish.** The flag button switches the whole interface,
plus every multi-language problem statement, hint and note. The Python-only curriculum
and drills are English and German; anything without a translation falls back to English
rather than breaking.

Written in Python with **zero third-party dependencies** — standard library and tkinter
only. Nothing to `pip install`.

*Die ganze App gibt es auf Deutsch, und die Programmiersprache lässt sich direkt in der
App umschalten. · Toute l'application existe aussi en français. · La aplicación completa
también está en español.*

## Download

Get the latest build from the
[Releases page](https://github.com/SenseiIssei/CodeForge/releases) — Windows x64,
Linux x64 and macOS (Apple Silicon). Unpack and run `CodeForge`. No Python needed; the
app carries its own interpreter.

On an **Intel Mac**, build it yourself (one command, see below) — GitHub is retiring its
Intel macOS runners, so there is no prebuilt x86_64 archive.

### To use a language other than Python

Python is built in. The others run your code with the real toolchain, so it has to be on
your machine — the language dropdown shows a ✓ next to the ones it found:

| Language   | Needs                            |
|------------|----------------------------------|
| Python     | nothing, it is bundled           |
| JavaScript | Node.js                          |
| Java       | a JDK (`javac` + `java`)         |
| C#         | the .NET SDK                     |
| Go         | the Go toolchain                 |
| Rust       | `rustc` (via rustup)             |
| C++        | g++, clang++, or Visual Studio   |

Nothing is downloaded at runtime and no network is used.

## What's inside

### Learn — 17 lessons *(Python)*
Theory written for someone who has not programmed before, but with the
interview-relevant detail included (why `x in set` beats `x in list`, why `list.pop(0)`
is O(n), why mutable default arguments bite). Each lesson has an editable, runnable
example and a graded exercise with staged hints.

### Practice — 31 randomised drill generators *(Python)*
Every drill is a *generator*: pick a topic, press the button, and you get a fresh
statement with different numbers, different words and freshly computed tests. Grind one
concept twenty times without ever replaying a memorised answer.

### Interview — problems in every language
* **28 multi-language problems** — one statement, generated starter code, and a
  reference solution in all seven languages. Two Sum, Kadane, binary search, sliding
  window, two pointers, hash maps, prefix sums, bit tricks, the sieve of Eratosthenes,
  matrices — plus Codility's BinaryGap, PassingCars, CyclicRotation, Dominator,
  OddOccurrencesInArray and TapeEquilibrium.
* **64 more when Python is selected** — the complete Codility lesson set (BinaryGap,
  MaxCounters, TapeEquilibrium, GenomicRangeQuery, Fish, StoneWall, Dominator …) plus
  the LeetCode patterns that keep coming up.

Hidden tests run on submit, including deliberately large inputs so an O(n²) answer
fails instead of quietly passing.

### Playground *(Python)*
Free editor with an **stdin box**, so you can practise the
`list(map(int, input().split()))` style of judge exactly as Codility runs it.

### Progress
XP, levels, day streak, per-topic breakdown, 14-day chart — in `progress.json`, local.

## How other languages are graded

There is no JSON parser in the harness, because Java, Rust and C++ do not ship one.
Instead each task declares a **type signature**, and the backend renders the test cases
as *native literals* of the target language, generates a harness that compares the
results itself, and prints one line per case in a tiny text protocol:

```
@@CF|0|PASS
@@CF|1|FAIL|[1, 3]|[0, 1]
@@CFEND
```

The same signature generates the starter code, so `sum_range` is
`nums: &[i64] -> i64` in Rust, `long[] -> long` in Java and `[]int -> int` in Go without
anything being written twice.

## The editor

Syntax highlighting, line numbers, auto-indent, bracket completion, `Tab`/`Shift+Tab`
block indent, `Ctrl+/` comment toggle, `Ctrl+D` duplicate line, undo/redo.
Your code runs in a separate process with a timeout, so an infinite loop kills the
sandbox and not the app.

| Key | Does |
|---|---|
| `Ctrl+Enter` | run tests |
| `Ctrl+1..5` | switch tab |
| `Tab` / `Shift+Tab` | indent / dedent |
| `Ctrl+/` | toggle comment |
| `Ctrl+D` | duplicate line |

## Run from source

```bash
python app.py
```

Python 3.9+ with tkinter (Debian/Ubuntu: `sudo apt install python3-tk`).

## Build it yourself

```bash
pip install pyinstaller && pyinstaller --noconfirm CodeForge.spec
```

Then check the packaged build can still execute user code — a frozen app has no
`python.exe` beside it, so CodeForge relaunches its own executable as the interpreter:

```bash
python tools/verify_frozen.py
```

## Tests

Content is verified, not assumed.

```bash
python selftest.py 3 en     # Python lessons, drills and problems
python selftest.py 3 de     # ... and German, plus translation coverage
python selftest_multi.py    # every reference solution in every installed language
python tools/gui_smoke.py   # builds the UI, walks every tab and every language
```

`selftest_multi.py` skips languages whose toolchain is missing instead of failing, so it
is useful on any machine.

## Layout

| File | Purpose |
|---|---|
| `app.py` | window, sidebar, the five tabs |
| `theme.py` | palette, fonts, flat widgets, the hand-drawn flags |
| `editor.py` | code editor and output console |
| `taskview.py` | the shared "solve a task" panel |
| `languages/` | one execution backend per programming language |
| `problems_multi.py` | problems that work in every language |
| `problems.py` · `problems_de.py` | the Python-only interview bank |
| `lessons.py` · `lessons_de.py` | the Python curriculum |
| `drills.py` | randomised generators (German inline — they interpolate values) |
| `runner.py` | the Python-only subprocess runner |
| `i18n.py` | interface language (EN/DE/FR/ES), topic and difficulty names |
| `problems_multi_i18n.py` | French and Spanish text for the multi-language bank |
| `progress.py` | XP, streaks and preferences |

## Adding a language

Implement `languages/base.Backend`: `probe()` to detect the toolchain, `type_name()`
and `literal()` to render values, `starter()` and `harness()` to generate code, and
`run()` to build and execute. Register it in `languages/__init__.py`, add solutions to
the problems in `problems_multi.py`, and run `python selftest_multi.py <your-language>`.
