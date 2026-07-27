"""The languages CodeForge can teach, execute and grade.

Python always works — the app ships an interpreter. Everything else needs the
real toolchain on the machine; the UI shows which ones are ready and what to
install for the rest.
"""
from __future__ import annotations

from .base import (BOOL, END, FLOAT, INT, SENTINEL, STR, Backend, CaseOutcome, L,
                   RunOutcome, Sig, base_of, depth, elem, is_list)
from .cpp_be import CppBackend
from .csharp_be import CSharpBackend
from .go_be import GoBackend
from .java_be import JavaBackend
from .javascript_be import JavaScriptBackend
from .python_be import PythonBackend
from .rust_be import RustBackend

BACKENDS: dict[str, Backend] = {}
ORDER: list[str] = []

for _cls in (PythonBackend, JavaScriptBackend, JavaBackend, CSharpBackend,
             GoBackend, RustBackend, CppBackend):
    _backend = _cls()
    BACKENDS[_backend.id] = _backend
    ORDER.append(_backend.id)

DEFAULT = "python"
CURRENT = DEFAULT


def set_current(language_id: str) -> str:
    global CURRENT
    CURRENT = language_id if language_id in BACKENDS else DEFAULT
    return CURRENT


def current() -> Backend:
    return BACKENDS[CURRENT]


def get(language_id: str) -> Backend:
    return BACKENDS.get(language_id, BACKENDS[DEFAULT])


def label(language_id: str) -> str:
    backend = BACKENDS.get(language_id)
    return backend.label if backend else language_id


def all_backends() -> list[Backend]:
    return [BACKENDS[i] for i in ORDER]


def detect(refresh: bool = False) -> dict[str, tuple[bool, str]]:
    """{language id: (usable, version or reason)} for every backend."""
    return {i: BACKENDS[i].available(refresh) for i in ORDER}


def usable_ids(refresh: bool = False) -> list[str]:
    return [i for i, (ok, _) in detect(refresh).items() if ok]


__all__ = [
    "BACKENDS", "ORDER", "DEFAULT", "Backend", "Sig", "RunOutcome", "CaseOutcome",
    "INT", "FLOAT", "BOOL", "STR", "L", "SENTINEL", "END",
    "is_list", "elem", "base_of", "depth",
    "get", "label", "all_backends", "detect", "usable_ids",
]
