"""The shared Task model used by lessons, random drills and interview problems."""
from __future__ import annotations

import random
from dataclasses import dataclass, field


@dataclass
class Task:
    id: str
    title: str
    func: str                       # function name the tests will call
    statement: str                  # what to do (plain text, blank-line separated)
    starter: str = ""               # starter code shown in the editor
    cases: list[dict] = field(default_factory=list)  # {"args","expected","hidden","label"}
    hints: list[str] = field(default_factory=list)
    solution: str = ""
    difficulty: str = "Easy"
    topic: str = "General"
    complexity: str = ""            # target complexity note (interview mode)
    checker_src: str = ""           # optional: defines check(args, got) -> bool
    source: str = "drill"           # drill | lesson | interview
    notes: str = ""                 # extra explanation shown after solving
    # Multi-language tasks carry a type signature; when it is set the task is
    # graded by a languages/ backend instead of the Python-only runner.
    sig: object = None
    language: str = "python"

    def visible_cases(self) -> list[dict]:
        return [c for c in self.cases if not c.get("hidden")]


def pretty_args(args_repr: str) -> str:
    """repr of a 1-tuple ends in ',)' — drop that so calls read naturally."""
    if args_repr.endswith(",)"):
        return args_repr[:-2] + ")"
    return args_repr


def case(args, expected=None, hidden: bool = False, label: str = "") -> dict:
    """Build a serialisable test case from real Python values."""
    if not isinstance(args, tuple):
        args = (args,)
    return {"args": repr(args), "expected": repr(expected),
            "hidden": hidden, "label": label}


def starter_for(func: str, params: str, doc: str = "") -> str:
    body = f'    """{doc}"""\n' if doc else ""
    return f"def {func}({params}):\n{body}    # your code here\n    pass\n"


def make_cases(ref, samples, hidden_from: int = 3, labels=None) -> list[dict]:
    """Compute expected values with a reference solution.

    `samples` is a list of argument tuples. The first `hidden_from` cases are
    shown to the user, the rest run as hidden tests (like a real judge).
    """
    out = []
    for i, args in enumerate(samples):
        if not isinstance(args, tuple):
            args = (args,)
        expected = ref(*[_copy(a) for a in args])
        label = labels[i] if labels and i < len(labels) else ""
        out.append(case(args, expected, hidden=i >= hidden_from, label=label))
    return out


def _copy(value):
    if isinstance(value, list):
        return [_copy(v) for v in value]
    if isinstance(value, dict):
        return {k: _copy(v) for k, v in value.items()}
    if isinstance(value, set):
        return set(value)
    return value


# ---------------------------------------------------------------- random data
def rng_for(seed: int | None = None) -> random.Random:
    return random.Random(seed)


WORDS = [
    "python", "banana", "forge", "kernel", "vector", "matrix", "island", "socket",
    "buffer", "raccoon", "tulip", "hammer", "silver", "orbit", "cactus", "pixel",
    "dragon", "muffin", "quartz", "nebula", "cipher", "walrus", "syntax", "lambda",
    "tensor", "packet", "gopher", "violet", "cobalt", "pepper", "helium", "zebra",
]

NAMES = ["Ada", "Linus", "Grace", "Guido", "Alan", "Barbara", "Ken", "Margaret",
         "Dennis", "Edsger", "Donald", "Radia", "Bjarne", "Anita", "Tim", "Hedy"]

CITIES = ["Berlin", "Lisbon", "Oslo", "Kyoto", "Toronto", "Nairobi", "Quito",
          "Prague", "Dublin", "Seoul", "Bogota", "Vienna"]
