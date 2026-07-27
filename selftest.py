"""Self-check: every reference solution must pass its own generated tests.

Run it after editing content:

    python selftest.py
"""
from __future__ import annotations

import random
import sys
import time

import drills
import i18n
import lessons as lessons_mod
import problems as problems_mod
import runner

failures: list[str] = []
checked = 0


def check_translations() -> None:
    """Every lesson/problem must have a German entry, and every German entry
    must point at something that still exists."""
    import lessons_de
    import problems_de

    for lesson in lessons_mod.LESSONS:
        if lesson.id not in lessons_de.LESSONS_DE:
            failures.append(f"  lessons_de: missing entry for '{lesson.id}'")
    for key in lessons_de.LESSONS_DE:
        if not lessons_mod.by_id(key):
            failures.append(f"  lessons_de: '{key}' has no English lesson")
    for problem in problems_mod.BANK:
        if problem.id not in problems_de.PROBLEMS_DE:
            failures.append(f"  problems_de: missing entry for '{problem.id}'")
    for key in problems_de.PROBLEMS_DE:
        if not problems_mod.by_id(key):
            failures.append(f"  problems_de: '{key}' has no English problem")
    for drill in drills.REGISTRY:
        task = drill.build(random.Random(7))
        if not task.title or not task.statement:
            failures.append(f"  drill '{drill.id}': empty title/statement in "
                            f"{i18n.LANG}")


def check(label: str, task) -> None:
    global checked
    checked += 1
    if not task.solution.strip():
        failures.append(f"{label}: no solution recorded")
        return
    report = runner.run_tests(task.solution, task.func, task.cases,
                              task.checker_src, timeout=25)
    if report.timed_out:
        failures.append(f"{label}: reference solution TIMED OUT")
        return
    if report.import_error:
        failures.append(f"{label}: {report.import_error.strip().splitlines()[-1]}")
        return
    if not report.ok:
        bad = [c for c in report.cases if not c.passed][:2]
        detail = "; ".join(
            f"args={c.args} expected={c.expected} got={c.got} err={c.error}"
            for c in bad)
        failures.append(f"{label}: {report.passed}/{report.total} — {detail}")


def main() -> int:
    start = time.perf_counter()
    repeats = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    language = sys.argv[2] if len(sys.argv) > 2 else "en"
    i18n.set_language(language)
    rng = random.Random(1234)

    print(f"Language: {i18n.LANG}")
    check_translations()

    print(f"Lessons ({len(lessons_mod.LESSONS)})")
    for lesson in lessons_mod.LESSONS:
        check(f"  lesson/{lesson.id}", lessons_mod.task_of(lesson))
        print(".", end="", flush=True)
    print()

    print(f"Drills ({len(drills.REGISTRY)}) x{repeats} random instances each")
    for d in drills.REGISTRY:
        for _ in range(repeats):
            check(f"  drill/{d.id}", d.build(rng))
        print(".", end="", flush=True)
    print()

    print(f"Problems ({len(problems_mod.BANK)}) x{repeats} random instances each")
    for problem in problems_mod.BANK:
        for _ in range(repeats):
            check(f"  problem/{problem.id}", problem.build(rng))
        print(".", end="", flush=True)
    print()

    elapsed = time.perf_counter() - start
    print(f"\n{checked} tasks checked in {elapsed:.1f}s")
    if failures:
        print(f"\n{len(failures)} FAILURE(S):")
        for line in failures:
            print(" ", line)
        return 1
    print("All reference solutions pass their own tests.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
