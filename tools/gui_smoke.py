"""Headless-ish UI smoke test.

Builds the whole window, visits every tab, exercises the lesson / drill /
problem navigation, flips the language to German and back, and asserts nothing
raised. Needs a display — on CI run it under xvfb:

    xvfb-run -a python tools/gui_smoke.py
"""
from __future__ import annotations

import os
import sys
import traceback

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app as pyforge  # noqa: E402
import i18n  # noqa: E402

errors: list[str] = []


def exercise(a) -> None:
    for key in pyforge.App.NAV:
        a.show(key)
        a.update()

    a.show("learn")
    a.views["learn"].show_tab("task")
    a.views["learn"].next_lesson()
    a.views["learn"].prev_lesson()
    a.update()

    a.show("practice")
    for _ in range(6):
        a.views["practice"].new_task()
    a.update()

    a.show("interview")
    for _ in range(6):
        a.views["interview"].random_problem()
    a.views["interview"]._clear_placeholder()
    a.views["interview"].search_var.set("sum")
    a.update()
    a.views["interview"].search_var.set("")
    a.views["interview"].topic.current(2)
    a.views["interview"].refresh_list()
    a.views["interview"].topic.current(0)
    a.views["interview"].refresh_list()

    a.show("playground")
    a.show("progress")
    a.update()


def run() -> None:
    a = pyforge.App()

    def step():
        try:
            start = i18n.LANG
            exercise(a)

            a.toggle_language()
            a.update()
            assert i18n.LANG != start, "language did not change"
            exercise(a)

            a.toggle_language()
            a.update()
            assert i18n.LANG == start, "language did not switch back"
            exercise(a)
        except Exception:
            errors.append(traceback.format_exc())
        a.after(150, a.destroy)

    a.after(400, step)
    a.mainloop()


if __name__ == "__main__":
    try:
        run()
    except Exception:
        errors.append(traceback.format_exc())

    if errors:
        print("GUI SMOKE FAILED")
        for err in errors:
            print(err)
        sys.exit(1)
    print("GUI smoke test OK (en -> de -> en)")
