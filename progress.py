"""Progress, XP and streak tracking, persisted to progress.json next to the app."""
from __future__ import annotations

import datetime as dt
import json
import os

STORE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "progress.json")

DEFAULT = {
    "language": "en",
    "xp": 0,
    "streak": 0,
    "best_streak": 0,
    "last_day": "",
    "lessons_done": [],
    "problems_solved": [],
    "attempts": {},          # id -> attempts
    "drill_solved": 0,
    "drill_attempts": 0,
    "topic_solved": {},      # topic -> count
    "history": [],           # [{"day": "2026-07-27", "solved": 3}]
    "recent": [],            # last solved ids
}

XP_FOR = {"Easy": 10, "Medium": 20, "Hard": 35}


class Progress:
    def __init__(self, path: str = STORE):
        self.path = path
        self.data = dict(DEFAULT)
        self.load()

    # ------------------------------------------------------------------ io
    def load(self) -> None:
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as fh:
                    saved = json.load(fh)
                for key, value in DEFAULT.items():
                    self.data[key] = saved.get(key, value if not isinstance(value, (list, dict))
                                               else type(value)())
            except (OSError, ValueError):
                self.data = dict(DEFAULT)
        self.touch_day()

    def save(self) -> None:
        try:
            with open(self.path, "w", encoding="utf-8") as fh:
                json.dump(self.data, fh, indent=2)
        except OSError:
            pass

    # --------------------------------------------------------------- streak
    def touch_day(self) -> None:
        today = dt.date.today().isoformat()
        last = self.data.get("last_day", "")
        if last == today:
            return
        if last:
            gap = (dt.date.today() - dt.date.fromisoformat(last)).days
            self.data["streak"] = self.data["streak"] + 1 if gap == 1 else 1
        else:
            self.data["streak"] = 1
        self.data["best_streak"] = max(self.data["best_streak"], self.data["streak"])
        self.data["last_day"] = today
        self.save()

    # --------------------------------------------------------------- events
    def attempt(self, task_id: str) -> None:
        self.data["attempts"][task_id] = self.data["attempts"].get(task_id, 0) + 1
        self.save()

    def solved(self, task_id: str, difficulty: str = "Easy", topic: str = "General",
               kind: str = "interview") -> int:
        """Record a solve. Returns XP gained (0 if it was already solved)."""
        self.touch_day()
        gained = 0
        bucket = "lessons_done" if kind == "lesson" else "problems_solved"
        if kind == "drill":
            self.data["drill_solved"] += 1
            gained = XP_FOR.get(difficulty, 10)
        elif task_id not in self.data[bucket]:
            self.data[bucket].append(task_id)
            gained = XP_FOR.get(difficulty, 10) if kind != "lesson" else 8
        else:
            gained = 2  # small reward for re-solving
        self.data["xp"] += gained
        self.data["topic_solved"][topic] = self.data["topic_solved"].get(topic, 0) + 1

        today = dt.date.today().isoformat()
        hist = self.data["history"]
        if hist and hist[-1].get("day") == today:
            hist[-1]["solved"] += 1
        else:
            hist.append({"day": today, "solved": 1})
            del hist[:-60]

        recent = self.data["recent"]
        entry = f"{kind}:{task_id}"
        if entry in recent:
            recent.remove(entry)
        recent.insert(0, entry)
        del recent[12:]
        self.save()
        return gained

    # ---------------------------------------------------------------- query
    def is_solved(self, task_id: str, kind: str = "interview") -> bool:
        bucket = "lessons_done" if kind == "lesson" else "problems_solved"
        return task_id in self.data[bucket]

    @property
    def level(self) -> int:
        return 1 + int((self.data["xp"] / 100) ** 0.75)

    @property
    def xp(self) -> int:
        return self.data["xp"]

    def level_progress(self) -> tuple[int, int]:
        """(xp into current level, xp needed for the level)."""
        lvl = self.level
        lo = int(((lvl - 1) ** (1 / 0.75)) * 100) if lvl > 1 else 0
        hi = int((lvl ** (1 / 0.75)) * 100)
        return max(0, self.xp - lo), max(1, hi - lo)

    def reset(self) -> None:
        language = self.data.get("language", "en")
        self.data = json.loads(json.dumps(DEFAULT))
        self.data["language"] = language   # a reset is about XP, not preferences
        self.touch_day()
        self.save()
