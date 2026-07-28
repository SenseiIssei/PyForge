# Roadmap

Where CodeForge stands and what comes next. Written so the project can be picked up
cold — from a fresh clone, on a different machine, months later.

---

## Where it stands

Every tab works in every one of the seven languages.

| | Python | JS | Java | C# | Go | Rust | C++ |
|---|---|---|---|---|---|---|---|
| **Learn** | 17 lessons | 4 | 4 | 4 | 4 | 4 | 4 |
| **Practice** | 31 generators | 6 | 6 | 6 | 6 | 6 | 6 |
| **Interview** | 28 + 64 | 28 | 28 | 28 | 28 | 28 | 28 |
| **Playground** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

Interface: English, German, French, Spanish (152 strings each).
Content: the 28 multi-language problems exist in all four; the Python-only curriculum,
drills and 64-problem bank are English and German, and fall back to English.

`selftest_multi.py` performs 286 verified runs against the real toolchains.

---

## Next, in the order I would do it

### 1. Fill the per-language courses out
Four lessons per language gets someone productive; it is not a course. The obvious
additions, in rough order of value:

- **Control flow and loops** — every language has one, none of them are quite alike
  (Go has no `while`; Rust has `loop`/`match`; C++ has three kinds of `for`).
- **Big-O in that language** — the Python lesson on complexity is the most useful one in
  the whole app and has no counterpart elsewhere. Each language needs its own version:
  `std::vector` reallocation, Java's boxing costs, Go's slice aliasing, JavaScript's
  `sort` allocating.
- **Errors** — Java/C# exceptions, Go's `error`, Rust's `Result`, C++ exceptions vs
  error codes. Currently only Go and Rust touch this, inside another lesson.
- **The standard library tour** — what to reach for so you do not hand-roll it.

Target: 8 lessons per language. Add them to `lessons_multi.py`; `curriculum.py` needs no
change.

### 2. More portable drills
Six generators is thin against Python's 31. The Python ones that port cleanly:
`digit_sum`, `gcd_lcm`, `caesar`, `palindrome`, `anagram`, `rle`, `chunk`, `interleave`,
`running`, `matrix_op`, `binary_ops`, `word_freq`.

Each costs seven reference solutions with the random parameter interpolated. That is the
real work, and there is no shortcut — see `drills_multi.py` for the pattern.

### 3. The rest of the Codility set, everywhere
Sixteen of the Python-only 64 are Codility lesson tasks that are not yet portable:
MaxCounters, GenomicRangeQuery, Fish, StoneWall, EquiLeader, MinAvgTwoSlice,
NumberOfDiscIntersections, CountFactors, MinPerimeterRectangle, ChocolatesByNumbers,
Triangle, MaxProductOfThree, Distinct, PermCheck, FrogRiverOne, MissingInteger.

Moving one means adding a `Sig`, cases, and seven solutions to `problems_multi.py`.
MaxCounters is the highest-value one — it is the task most people fail.

### 4. French and Spanish for the Python content
The 17 lessons, 31 drills and 64 problems are English and German. The machinery is
already there (`i18n.pick` falls back to English), so this is pure translation:
`lessons_de.py` and `problems_de.py` show the shape; drills carry their text inline
because they interpolate random values.

### 5. More languages
The backend interface is small — `probe`, `type_name`, `literal`, `starter`, `harness`,
`run` — and `languages/base.py` documents it. Reasonable candidates, easiest first:
**TypeScript** (reuse the JavaScript backend with `tsc`), **Kotlin** (reuse much of
Java), **Swift**, **PHP**, **Ruby**.

Each also needs: a Playground template and build recipe in `languages/playground.py`,
28 problem solutions, 6 drill solutions, and 4 lessons.

### 6. Things the app does not do yet
- **A timed mock test.** Codility gives you three tasks and 90 minutes. The Interview tab
  has a per-task timer but no session mode.
- **Complexity feedback.** The app states a target complexity and asks whether you met
  it; it never measures. Timing a solution against two input sizes and reporting the
  growth would be honest and genuinely novel.
- **Spaced repetition.** Solved problems are marked and never resurface. `progress.json`
  already records attempts and dates, so scheduling is a small step.
- **Editor niceties.** No find/replace, no multi-cursor, no bracket-match highlight.

---

## Things worth knowing before you touch it

**Everything is verified, and the verification is the point.** Each round of content has
caught real bugs — a Java harness exceeding the 64 KB per-method bytecode limit, Rust
unable to infer the type of an empty `vec![]`, a list argument nested one level too deep
that silently passed the whole list as a single string in all seven languages. Run the
tests before pushing:

```bash
python selftest.py 3 en      # Python lessons, drills, problems
python selftest.py 3 de      # ... and German, plus translation coverage
python selftest_multi.py     # every language: lessons, examples, drills, problems
python tools/gui_smoke.py    # the UI, 4 interface languages x 7 programming languages
```

`selftest_multi.py` skips languages whose toolchain is missing rather than failing, so it
is useful on any machine. Give it a language name to test just that one.

**No JSON anywhere in the harnesses.** Java, Rust and C++ do not ship a parser, so test
cases are rendered as native literals and the generated harness compares them itself,
reporting through a one-line-per-case text protocol. `languages/base.py` explains it.

**Type signatures drive everything.** A task declares `Sig([("nums", L(INT))], INT)`, and
that produces both the starter code and the harness for all seven languages. If a problem
cannot be typed — a heterogeneous list, a null return in a language without nullable
integers — it stays Python-only. That is a real constraint, not an oversight.

**Test-case arity is checked, because it has bitten.** `case(["a", "b"], ...)` means one
list argument; `case((x, y), ...)` means two. `selftest_multi.py` verifies this against
the signature without needing a toolchain.

**Platform gotchas that cost time once already:**
- `macos-13` (Intel) runners queue indefinitely and block releases — the workflow only
  builds `macos-latest` (Apple Silicon). Intel Mac users build from source.
- MSVC has to be invoked through a generated `.bat`; passing `vcvars` plus redirections
  as one `cmd /c` argument gets mangled by Windows quoting.
- Windows renders flag emoji as boxed letters, so the language flags are drawn on a
  `tk.Canvas`.
- A frozen PyInstaller build has no `python.exe` beside it, so the app relaunches its own
  executable as the interpreter. `tools/verify_frozen.py` checks that path in CI, because
  it is invisible from the GUI.

**Commits are authored as `SenseiIssei <54678128+SenseiIssei@users.noreply.github.com>`.**
The repo is configured for it; a fresh clone needs `git config user.name/user.email` set
again.
