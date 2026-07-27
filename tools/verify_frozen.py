"""Prove that a PyInstaller build can still run the user's code.

In a frozen build there is no python.exe next to the app, so CodeForge relaunches
its own executable with `--pyforge-child` and acts as the interpreter itself
(see runner.run_child). That path is easy to break and impossible to notice
from the GUI alone, so CI checks it on every platform before publishing.

    python tools/verify_frozen.py
"""
from __future__ import annotations

import os
import random
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

CANDIDATES = [
    os.path.join(ROOT, "dist", "CodeForge", "CodeForge.exe"),
    os.path.join(ROOT, "dist", "CodeForge", "CodeForge"),
    os.path.join(ROOT, "dist", "CodeForge.app", "Contents", "MacOS", "CodeForge"),
]


def find_executable() -> str:
    for path in CANDIDATES:
        if os.path.isfile(path) and os.access(path, os.X_OK):
            return path
    raise SystemExit("No built executable found — run pyinstaller CodeForge.spec first.\n"
                     "Looked in:\n  " + "\n  ".join(CANDIDATES))


def main() -> int:
    exe = find_executable()
    print("Testing", exe)

    import drills
    import i18n
    import lessons
    import problems
    import runner

    # Pretend we are the frozen app: route every child process through the exe.
    runner._interpreter = lambda: [exe, runner.CHILD_FLAG]

    failures = 0

    # 1. plain script execution, stdin and both output streams
    out, err, timed_out, _ = runner.run_script(
        "import sys\n"
        "print('stdout ok')\n"
        "print('stderr ok', file=sys.stderr)\n"
        "print('stdin ->', sys.stdin.read().strip())\n",
        stdin="42", timeout=90)
    if timed_out or "stdout ok" not in out or "stdin -> 42" not in out:
        print("FAIL  run_script:", repr(out), repr(err), "timeout" if timed_out else "")
        failures += 1
    else:
        print("OK    run_script (stdout, stderr, stdin)")

    # 2. the timeout guard must still kill a runaway child
    _, _, timed_out, _ = runner.run_script("while True:\n    pass\n", timeout=8)
    if not timed_out:
        print("FAIL  runaway child was not stopped by the timeout")
        failures += 1
    else:
        print("OK    timeout kills an endless loop")

    # 3. the real grading harness, in both languages
    rng = random.Random(4242)
    for language in ("en", "de"):
        i18n.set_language(language)
        tasks = ([lessons.task_of(lesson) for lesson in lessons.LESSONS[:3]]
                 + [d.build(rng) for d in drills.REGISTRY[:3]]
                 + [p.build(rng) for p in problems.BANK[:4]])
        for task in tasks:
            report = runner.run_tests(task.solution, task.func, task.cases,
                                      task.checker_src, timeout=90)
            if not report.ok:
                print(f"FAIL  [{language}] {task.title}: "
                      f"{report.import_error or f'{report.passed}/{report.total}'}"
                      f"{' TIMEOUT' if report.timed_out else ''}")
                failures += 1
        print(f"OK    grading harness, {len(tasks)} tasks [{language}]")

    if failures:
        print(f"\n{failures} check(s) failed — the frozen build cannot run user code.")
        return 1
    print("\nFrozen build verified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
