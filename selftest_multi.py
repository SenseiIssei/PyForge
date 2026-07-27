"""Run every multi-language reference solution against its own test cases.

    python selftest_multi.py            # every language that is installed
    python selftest_multi.py rust go    # only these

A language whose toolchain is missing is reported and skipped, not failed —
CodeForge is meant to work on a machine that has only some of them.
"""
from __future__ import annotations

import sys
import time

import i18n
import languages as LG
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

        problems = problems_multi.for_language(backend.id)
        print(f"\n=== {backend.label}  [{info}]  {len(problems)} problems")
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

    # the statements must exist in both languages
    for problem in problems_multi.BANK:
        for language in ("en", "de"):
            if not problem.statement.get(language) or not problem.title.get(language):
                failures.append(f"{problem.id}: missing '{language}' text")

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
