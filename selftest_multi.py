"""Run every multi-language reference solution against its own test cases.

    python selftest_multi.py            # every language that is installed
    python selftest_multi.py rust go    # only these

A language whose toolchain is missing is reported and skipped, not failed —
CodeForge is meant to work on a machine that has only some of them.
"""
from __future__ import annotations

import random
import sys
import time

import drills_multi
import i18n
import languages as LG
import lessons_multi
import problems_multi


def main() -> int:
    wanted = [a.lower() for a in sys.argv[1:]] or None
    failures: list[str] = []
    skipped: list[str] = []
    checked = 0
    start = time.perf_counter()

    for backend in LG.all_backends():
        if wanted and backend.id not in wanted:
            continue
        ok, info = backend.available()
        if not ok:
            skipped.append(f"{backend.label}: {info}")
            print(f"\n=== {backend.label}: skipped ({info})")
            continue

        lessons = lessons_multi.for_language(backend.id)
        problems = problems_multi.for_language(backend.id)
        print(f"\n=== {backend.label}  [{info}]  "
              f"{len(lessons)} lessons, {len(problems)} problems")

        # The live example is a whole program the learner will press Run on,
        # so it has to compile and finish on its own.
        for lesson in lessons:
            began = time.perf_counter()
            out, err, timed_out, _ = backend.run_program(lesson.example, "")
            took = time.perf_counter() - began
            checked += 1
            if timed_out or err.strip() or not out.strip():
                failures.append(f"{backend.label}/{lesson.id}: example "
                                f"{'timed out' if timed_out else (err.strip()[:300] or 'printed nothing')}")
                print(f"  FAIL  example {lesson.id:<27} {took:5.1f}s")
                if err.strip():
                    print("        " + err.strip().replace("\n", "\n        ")[:700])
            else:
                print(f"  ok    example {lesson.id:<27} {took:5.1f}s")

        for lesson in lessons:
            began = time.perf_counter()
            outcome = backend.run(lesson.solution, lesson.func, lesson.sig,
                                  lesson.cases)
            took = time.perf_counter() - began
            checked += 1
            if outcome.ok:
                print(f"  ok    lesson {lesson.id:<28} {outcome.passed}/"
                      f"{outcome.total} {took:5.1f}s")
                continue
            reason = (outcome.build_error or outcome.runtime_error
                      or ("timed out" if outcome.timed_out else ""))
            failures.append(f"{backend.label}/{lesson.id}: "
                            f"{outcome.passed}/{outcome.total} {reason[:400]}")
            print(f"  FAIL  lesson {lesson.id:<28} {outcome.passed}/{outcome.total}")
            if reason:
                print("        " + reason.strip().replace("\n", "\n        ")[:700])
            for c in outcome.cases:
                if not c.passed:
                    print(f"        case {c.index}: got={c.got!r} "
                          f"expected={c.expected!r} error={c.error!r}")

        # Randomised drills: build a fresh instance of each and grade it.
        LG.set_current(backend.id)
        rng = random.Random(20260727)
        for spec in drills_multi.REGISTRY:
            task = spec.build(rng)
            began = time.perf_counter()
            outcome = backend.run(task.solution, task.func, task.sig, task.cases)
            took = time.perf_counter() - began
            checked += 1
            if outcome.ok:
                print(f"  ok    drill  {spec.id:<28} {outcome.passed}/"
                      f"{outcome.total} {took:5.1f}s")
                continue
            reason = (outcome.build_error or outcome.runtime_error
                      or ("timed out" if outcome.timed_out else ""))
            failures.append(f"{backend.label}/drill {spec.id}: "
                            f"{outcome.passed}/{outcome.total} {reason[:400]}")
            print(f"  FAIL  drill  {spec.id:<28} {outcome.passed}/{outcome.total}")
            if reason:
                print("        " + reason.strip().replace("\n", "\n        ")[:700])

        for problem in problems:
            source = problem.solutions[backend.id]
            began = time.perf_counter()
            outcome = backend.run(source, problem.func, problem.sig, problem.cases)
            took = time.perf_counter() - began
            checked += 1
            if outcome.ok:
                print(f"  ok    {problem.id:<24} {outcome.passed}/{outcome.total} "
                      f"{took:5.1f}s")
                continue
            reason = (outcome.build_error or outcome.runtime_error
                      or ("timed out" if outcome.timed_out else ""))
            failures.append(f"{backend.label}/{problem.id}: "
                            f"{outcome.passed}/{outcome.total} {reason[:400]}")
            print(f"  FAIL  {problem.id:<24} {outcome.passed}/{outcome.total} "
                  f"{took:5.1f}s")
            if reason:
                print("        " + reason.strip().replace("\n", "\n        ")[:800])
            for c in outcome.cases:
                if not c.passed:
                    print(f"        case {c.index}: got={c.got!r} "
                          f"expected={c.expected!r} error={c.error!r}")

    # ---- structural checks, no toolchain required -------------------------
    import ast

    import problems_multi_i18n

    for problem in problems_multi.BANK:
        for language in ("en", "de"):
            if not problem.statement.get(language) or not problem.title.get(language):
                failures.append(f"{problem.id}: missing '{language}' text")

        # French and Spanish live in the separate translation module. A missing
        # one is not fatal — it falls back to English — but it should be visible.
        extra = problems_multi_i18n.EXTRA.get(problem.id, {})
        for language in ("fr", "es"):
            entry = extra.get(language)
            if not entry or not entry.get("title") or not entry.get("statement"):
                failures.append(f"{problem.id}: no '{language}' translation")

        # Arity: case(["a", "b"], ...) means ONE list argument, while
        # case((x, y), ...) means two. Getting this wrong silently hands the
        # whole list over as a single value — far easier to catch here than to
        # debug in seven languages at once.
        arity = len(problem.sig.params)
        for index, entry in enumerate(problem.cases):
            args = ast.literal_eval(entry["args"])
            if not isinstance(args, tuple):
                args = (args,)
            if len(args) != arity:
                failures.append(
                    f"{problem.id}: case {index} passes {len(args)} argument(s), "
                    f"but the signature declares {arity}")

        for language_id in LG.ORDER:
            if language_id not in problem.solutions:
                failures.append(f"{problem.id}: no {LG.label(language_id)} solution")

    elapsed = time.perf_counter() - start
    print(f"\n{checked} solution runs in {elapsed:.0f}s")
    for line in skipped:
        print(f"  skipped — {line}")
    if failures:
        print(f"\n{len(failures)} FAILURE(S):")
        for line in failures:
            print("  " + line)
        return 1
    print("Every reference solution passes in every installed language.")
    return 0


if __name__ == "__main__":
    i18n.set_language("en")
    sys.exit(main())
