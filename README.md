# PyForge

[![build](https://github.com/SenseiIssei/PyForge/actions/workflows/build.yml/badge.svg)](https://github.com/SenseiIssei/PyForge/actions/workflows/build.yml)
[![license: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A desktop app for learning Python from scratch and then grinding coding-interview
problems — built for a Codility screen.

Written in Python, **zero third-party dependencies** (standard library + tkinter only).
Nothing to install, nothing to `pip`.

**English and German.** The flag button at the top of the sidebar switches the entire
app — not just the buttons, but every lesson, every theory text, every problem
statement and every hint. Your choice is remembered in `progress.json`.

*Die ganze App gibt es auch auf Deutsch — der Flaggen-Knopf oben links schaltet um,
inklusive aller Lektionen, Aufgabentexte und Tipps.*

## Download

Grab the latest build for your system from the
[Releases page](https://github.com/SenseiIssei/PyForge/releases) — Windows x64, Linux x64
and macOS (Apple Silicon). Unpack it and run `PyForge`. No Python installation needed;
the app carries its own interpreter and uses it to run the code you write.

On an **Intel Mac** run it from source, or build it yourself in one command (see below) —
GitHub is retiring its Intel macOS runners, so there is no prebuilt x86_64 archive.

## Run from source

Double-click `PyForge.bat` on Windows, or:

```bash
python app.py
```

Needs Python 3.9+ with tkinter (on Debian/Ubuntu: `sudo apt install python3-tk`).

## Build it yourself

```bash
pip install pyinstaller && pyinstaller --noconfirm PyForge.spec
```

The result lands in `dist/`. Then confirm the build can still execute user code — a
frozen app has no `python.exe` beside it, so PyForge relaunches its own executable as
the interpreter, and that path is worth checking:

```bash
python tools/verify_frozen.py
```

## What's inside

### 1 · Learn — 17 lessons
Ordered curriculum, each lesson is three things on one screen:

* **Theory** — written for someone who has not written Python before, but with the
  interview-relevant detail included (why `x in set` beats `x in list`, why
  `list.pop(0)` is O(n), why mutable default arguments bite).
* **Live example** — a real, runnable program you can edit and re-run. It executes in
  a genuine Python subprocess, so `print`, tracebacks, timings all behave normally.
* **Exercise** — a graded task with visible and hidden tests, staged hints, and a
  reference solution.

Sections: Foundations → Data structures → Functions & structure → Interview technique
(Big-O, two pointers/sliding window, prefix sums, recursion + memoisation, stdin/stdout,
reading a traceback).

### 2 · Practice — 31 randomised drill generators
This is the "learn it many times" part. Every drill is a **generator**, not a fixed
task: pick a topic, hit *New random task*, and you get a fresh statement with different
numbers, different words, and freshly computed test cases every single time. You can
grind the same concept twenty times and never replay a memorised answer.

Topics: Basics, Strings, Lists, Sorting, Hash map, Sets, Prefix sums, Two pointers,
Matrix, Bit tricks, Errors.

### 3 · Interview — 64 problems
The bank you actually prepare with:

* **Codility's lesson tasks** — BinaryGap, CyclicRotation, OddOccurrencesInArray,
  FrogJmp, PermMissingElem, TapeEquilibrium, FrogRiverOne, PermCheck, MissingInteger,
  MaxCounters, CountDiv, PassingCars, MinAvgTwoSlice, GenomicRangeQuery, Distinct,
  Triangle, MaxProductOfThree, NumberOfDiscIntersections, Brackets, Fish, Nesting,
  StoneWall, Dominator, EquiLeader, MaxProfit, MaxSliceSum, CountFactors,
  MinPerimeterRectangle, ChocolatesByNumbers.
* **LeetCode patterns** — Two Sum, Valid Parentheses, Maximum Subarray, Product of
  Array Except Self, Longest Substring Without Repeating Characters, Group Anagrams,
  Merge Intervals, Binary Search, Search in Rotated Sorted Array, Climbing Stairs,
  Coin Change, House Robber, Longest Consecutive Sequence, 3Sum, Container With Most
  Water, Move Zeroes, Rotate Array, Majority Element, Single Number, Top K Frequent,
  Valid Palindrome, Longest Common Prefix, Roman to Integer, Spiral Matrix, Number of
  Islands, Merge Two Sorted Lists, Valid Anagram, Contains Duplicate, String
  Compression, Set Matrix Zeroes, Minimum Size Subarray Sum, Isomorphic Strings,
  Kth Largest Element, Summary Ranges, Sort Colors.

Each problem carries the target complexity, staged hints, a note on *why* it is asked,
and — like Codility — hidden tests, including deliberate 100k–200k element cases so an
O(n²) answer times out instead of silently passing.

Every problem also gets **fresh random test cases on each open**, on top of its fixed
examples.

### 4 · Playground
Free-form editor with an **stdin box**, so you can practise the
`list(map(int, input().split()))` style of judge exactly as Codility runs it.

### 5 · Progress
XP, levels, day streak, per-topic breakdown, 14-day activity chart. Stored locally in
`progress.json` next to the app.

## The editor

* Python syntax highlighting, line numbers
* auto-indent (including dedent after `return`/`pass`/`break`)
* bracket and quote auto-closing, selection wrapping
* `Tab` / `Shift+Tab` block indent, `Ctrl+/` comment toggle, `Ctrl+D` duplicate line
* `Ctrl+Enter` runs, undo/redo

Your code runs in a **separate process** with a 10-second timeout, so an infinite loop
kills the sandbox, not the app. Failing tests report the input, the expected value and
what you actually returned; crashes get the exact line highlighted in the editor plus a
plain-English diagnosis (`'NoneType' …` → "you probably forgot a `return`").

## Keyboard

| Key | Does |
|---|---|
| `Ctrl+Enter` | run tests / run code |
| `Ctrl+1..5` | switch tab |
| `Tab` / `Shift+Tab` | indent / dedent selection |
| `Ctrl+/` | toggle comment |
| `Ctrl+D` | duplicate line |

## Files

| File | Purpose |
|---|---|
| `app.py` | window, sidebar, the five views |
| `theme.py` | palette, fonts, flat widget helpers |
| `editor.py` | the code editor + output console |
| `runner.py` | subprocess execution and the test harness |
| `taskview.py` | the shared "solve a task" panel |
| `lessons.py` | the 17-lesson curriculum |
| `drills.py` | the 31 randomised drill generators |
| `problems.py` | the 64-problem interview bank |
| `tasks.py` | the shared Task model |
| `progress.py` | XP / streak / language persistence |
| `i18n.py` | language state, UI strings, topic & difficulty names |
| `lessons_de.py` | German curriculum (theory, examples, exercises) |
| `problems_de.py` | German problem statements, hints and notes |
| `selftest.py` | validates every reference solution against its own tests |
| `PyForge.spec` | PyInstaller recipe (one-dir, windowed) |
| `tools/verify_frozen.py` | proves a packaged build can still run user code |
| `tools/gui_smoke.py` | builds the whole UI, visits every tab, flips the language |

The drills carry their German text inline in `drills.py` rather than in a separate
file, because each statement interpolates its own random values and both languages
need the same numbers.

## Self-test

Content is verified, not assumed. Every reference solution is executed against its own
generated test cases:

```bash
python selftest.py 6 en
```

The first argument is how many random instances of each drill/problem to check (`6`
builds 587 tasks, about a minute). The second is the language — run it for `de` too,
which additionally verifies that every lesson and problem has a German entry and that
no translation points at content that no longer exists:

```bash
python selftest.py 3 de
```

## Adding your own content

A drill is one function:

```python
@drill("my_drill", "Title", "Topic", "Easy")
def _my_drill(rng):
    k = rng.randint(2, 9)
    ref = lambda nums: [n for n in nums if n % k == 0]
    return _task(rng, "my_drill", "Title", "Topic", "Easy", "keep",
                 f"Write keep(nums) keeping multiples of {k}.",
                 "nums", ref,
                 [([1, 2, 3],), ([],), (rand_list(rng),)],
                 ["hint one"], f"def keep(nums):\n    return [n for n in nums if n % {k} == 0]\n")
```

The expected outputs are computed by `ref`, so you never hand-write answers. An interview
problem is a `P(...)` call in `problems.py` — its reference solution is `exec`'d at import
to generate the expected values, which means the "Show solution" button can only ever
display code that provably passes.

Run `python selftest.py` after adding anything.
