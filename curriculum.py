"""One interface over both kinds of curriculum.

Python has the original 17-lesson course (lessons.py, translated in
lessons_de.py). The other languages have their own shorter courses in
lessons_multi.py, whose exercises are graded by a languages/ backend rather
than the Python-only runner.

The Learn tab talks to this module and does not care which it is looking at.
"""
from __future__ import annotations

import i18n
import languages as LG
import lessons as py_lessons
import lessons_multi


class Entry:
    """A lesson, whichever course it came from."""

    def __init__(self, native, kind: str):
        self.native = native
        self.kind = kind                      # "python" | "multi"

    # ------------------------------------------------------------- identity
    @property
    def id(self) -> str:
        return self.native.id

    # ---------------------------------------------------------------- text
    def section(self) -> str:
        if self.kind == "python":
            return py_lessons.section_of(self.native)
        return i18n.pick(self.native.section, "")

    def title(self) -> str:
        if self.kind == "python":
            return py_lessons.field_of(self.native, "title")
        return i18n.pick(self.native.title, self.native.id)

    def theory(self) -> str:
        if self.kind == "python":
            return py_lessons.field_of(self.native, "theory")
        return i18n.pick(self.native.theory, "")

    def takeaway(self) -> str:
        if self.kind == "python":
            return py_lessons.field_of(self.native, "takeaway")
        return i18n.pick(self.native.takeaway, "")

    def example(self) -> str:
        if self.kind == "python":
            return py_lessons.field_of(self.native, "example")
        return self.native.example

    # ---------------------------------------------------------------- task
    @property
    def task_id(self) -> str:
        if self.kind == "python":
            return self.native.task.id
        return self.native.id

    def task(self):
        if self.kind == "python":
            return py_lessons.task_of(self.native)
        return self.native.build()


def lessons_for(language_id: str | None = None) -> list[Entry]:
    language_id = language_id or LG.CURRENT
    if language_id == "python":
        return [Entry(lesson, "python") for lesson in py_lessons.LESSONS]
    return [Entry(lesson, "multi")
            for lesson in lessons_multi.for_language(language_id)]


def has_curriculum(language_id: str | None = None) -> bool:
    return bool(lessons_for(language_id))
