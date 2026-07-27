"""Headless-ish UI smoke test.

Builds the whole window, visits every tab, exercises navigation, flips the
interface language to German and back, and walks through every programming
language. Needs a display — on CI run it under xvfb:

    xvfb-run -a python tools/gui_smoke.py
"""
from __future__ import annotations

import os
import sys
import traceback

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app as pyforge  # noqa: E402
import i18n  # noqa: E402
import languages as LG  # noqa: E402

errors: list[str] = []


def visit_tabs(a) -> None:
    for key in pyforge.App.NAV:
        a.show(key)
        a.update()


def exercise_python(a) -> None:
    visit_tabs(a)

    a.show("learn")
    a.views["learn"].show_tab("task")
    a.views["learn"].next_lesson()
    a.views["learn"].prev_lesson()
    a.update()

    a.show("practice")
    for _ in range(5):
        a.views["practice"].new_task()
    a.update()

    a.show("interview")
    for _ in range(5):
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


def exercise_language(a, language_id: str) -> None:
    """Switch to a language and open a few of its problems."""
    a.set_prog_language(language_id)
    a.update()
    assert LG.CURRENT == language_id, f"did not switch to {language_id}"
    visit_tabs(a)

    view = a.views["interview"]
    if hasattr(view, "random_problem"):          # toolchain present
        for _ in range(3):
            view.random_problem()
            a.update()
        task = view.task_view.task
        assert task is not None, f"no task loaded for {language_id}"
        assert task.starter.strip(), f"empty starter for {language_id}"
        assert task.language == language_id


def run() -> None:
    a = pyforge.App()

    def step():
        try:
            start_ui = i18n.LANG
            start_prog = LG.CURRENT

            # Do not inherit whatever language progress.json was left on.
            a.set_prog_language("python")
            a.update()
            exercise_python(a)

            a.toggle_language()
            a.update()
            assert i18n.LANG != start_ui, "interface language did not change"
            exercise_python(a)

            for language_id in LG.ORDER:
                exercise_language(a, language_id)

            a.set_prog_language(start_prog)
            a.toggle_language()
            a.update()
            assert i18n.LANG == start_ui and LG.CURRENT == start_prog
            visit_tabs(a)
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
    print("GUI smoke test OK — both interface languages, all "
          f"{len(LG.ORDER)} programming languages")
