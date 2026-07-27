"""CodeForge - learn Python, then grind interview problems. Run this file.

    python app.py

Zero dependencies: standard library + tkinter only.
Available in English and German — the flag button at the top of the sidebar
switches the entire app, lessons and problem statements included.
"""
from __future__ import annotations

import random
import sys
import threading
import tkinter as tk
from tkinter import ttk

import curriculum
import drills
import drills_multi
import i18n
import languages as LG
import lessons as lessons_mod
import lessons_multi
import problems as problems_mod
import problems_multi
import runner
import theme as T
from editor import CodeEditor, Console
from i18n import t
from progress import Progress
from taskview import TaskView

APP_NAME = "CodeForge"


# ===========================================================================
#  A full-panel message — used when a tab does not apply to the chosen
#  programming language, or when its toolchain is missing.
# ===========================================================================
class NoticeView(tk.Frame):
    def __init__(self, master, title: str, body: str,
                 button: str = "", command=None):
        super().__init__(master, bg=T.BG)
        wrap = tk.Frame(self, bg=T.BG)
        wrap.place(relx=0.5, rely=0.42, anchor="center")

        card = T.card(wrap, bg=T.PANEL)
        card.pack()
        box = card.inner  # type: ignore[attr-defined]
        tk.Label(box, text=title, bg=T.PANEL, fg=T.TEXT, font=T.fonts()["h2"],
                 anchor="w", justify="left").pack(anchor="w", padx=30, pady=(26, 8))
        tk.Label(box, text=body, bg=T.PANEL, fg=T.MUTED, font=T.fonts()["ui"],
                 wraplength=520, justify="left").pack(anchor="w", padx=30,
                                                      pady=(0, 20))
        if button and command:
            T.Button(box, button, command, variant="primary").pack(
                anchor="w", padx=30, pady=(0, 26))
        else:
            tk.Frame(box, bg=T.PANEL, height=6).pack()


# ===========================================================================
#  LEARN
# ===========================================================================
class LearnView(tk.Frame):
    def __init__(self, master, app: "App"):
        super().__init__(master, bg=T.BG)
        self.app = app
        self.lesson = None
        self._rows: dict[str, tk.Frame] = {}
        # the course for whichever programming language is active
        self.entries = curriculum.lessons_for()

        paned = tk.PanedWindow(self, orient="horizontal", bg=T.BG, bd=0,
                               sashwidth=6, sashrelief="flat", showhandle=False)
        paned.pack(fill="both", expand=True)

        # ------------------------------------------------------- lesson list
        left = tk.Frame(paned, bg=T.PANEL)
        paned.add(left, minsize=210, width=282, stretch="never")

        header = tk.Frame(left, bg=T.PANEL)
        header.pack(fill="x", padx=16, pady=(16, 8))
        tk.Label(header, text=t("learn.curriculum"), bg=T.PANEL, fg=T.ACCENT,
                 font=T.fonts()["tiny"]).pack(anchor="w")
        self.count_label = tk.Label(header, text="", bg=T.PANEL, fg=T.MUTED,
                                    font=T.fonts()["small"])
        self.count_label.pack(anchor="w", pady=(2, 0))

        container, self.list_frame = T.scrolled_frame(left, bg=T.PANEL)
        container.pack(fill="both", expand=True, padx=(6, 0), pady=(0, 10))
        self._build_list()

        # ------------------------------------------------------ lesson panel
        right = tk.Frame(paned, bg=T.BG)
        paned.add(right, minsize=520, stretch="always")

        head = tk.Frame(right, bg=T.BG)
        head.pack(fill="x", padx=18, pady=(14, 0))
        self.title_label = tk.Label(head, text="", bg=T.BG, fg=T.TEXT,
                                    font=T.fonts()["h1"], anchor="w")
        self.title_label.pack(anchor="w")
        self.section_label = tk.Label(head, text="", bg=T.BG, fg=T.MUTED,
                                      font=T.fonts()["small"], anchor="w")
        self.section_label.pack(anchor="w", pady=(2, 8))

        seg = tk.Frame(right, bg=T.BG)
        seg.pack(fill="x", padx=18)
        self.tab_theory = T.Button(seg, t("learn.tab.theory"),
                                   lambda: self.show_tab("theory"), variant="primary")
        self.tab_theory.pack(side="left")
        self.tab_task = T.Button(seg, t("learn.tab.task"),
                                 lambda: self.show_tab("task"), variant="ghost")
        self.tab_task.pack(side="left", padx=(8, 0))
        self.nav_next = T.Button(seg, t("learn.next"), self.next_lesson, variant="soft")
        self.nav_next.pack(side="right")
        self.nav_prev = T.Button(seg, t("learn.prev"), self.prev_lesson, variant="ghost")
        self.nav_prev.pack(side="right", padx=(0, 8))

        self.body = tk.Frame(right, bg=T.BG)
        self.body.pack(fill="both", expand=True)

        # theory frame -------------------------------------------------------
        self.theory_frame = tk.Frame(self.body, bg=T.BG)
        tpaned = tk.PanedWindow(self.theory_frame, orient="horizontal", bg=T.BG,
                                bd=0, sashwidth=6, sashrelief="flat", showhandle=False)
        tpaned.pack(fill="both", expand=True, padx=14, pady=10)

        tleft = T.card(tpaned, bg=T.PANEL)
        tpaned.add(tleft, minsize=300, width=560, stretch="always")
        tin = tleft.inner  # type: ignore[attr-defined]
        tk.Label(tin, text=t("learn.theory"), bg=T.PANEL, fg=T.ACCENT,
                 font=T.fonts()["tiny"]).pack(anchor="w", padx=14, pady=(10, 2))
        twrap = tk.Frame(tin, bg=T.PANEL)
        twrap.pack(fill="both", expand=True, padx=4, pady=(0, 8))
        thbar = ttk.Scrollbar(twrap, orient="horizontal")
        thbar.pack(side="bottom", fill="x")
        tbar = ttk.Scrollbar(twrap, orient="vertical")
        tbar.pack(side="right", fill="y")
        # wrap="none" — the theory is pre-formatted; word-wrap would mangle
        # the code blocks and the aligned tables inside it.
        self.theory = tk.Text(twrap, bg=T.PANEL, fg=T.TEXT, bd=0, highlightthickness=0,
                              wrap="none", font=T.fonts()["code_small"], padx=12,
                              pady=4, insertwidth=0, yscrollcommand=tbar.set,
                              xscrollcommand=thbar.set,
                              state="disabled", spacing1=1, spacing3=3,
                              selectbackground="#33405c")
        self.theory.pack(side="left", fill="both", expand=True)
        tbar.configure(command=self.theory.yview)
        thbar.configure(command=self.theory.xview)
        self.theory.tag_configure("takeaway", foreground=T.GREEN,
                                  font=T.fonts()["code_bold"])
        self.theory.bind("<MouseWheel>", lambda e: (
            self.theory.yview_scroll(int(-e.delta / 120), "units"), "break")[1])

        tright = tk.Frame(tpaned, bg=T.BG)
        tpaned.add(tright, minsize=340, stretch="always")
        tk.Label(tright, text=t("learn.example"),
                 bg=T.BG, fg=T.MUTED, font=T.fonts()["tiny"]).pack(anchor="w", pady=(0, 4))
        self.example = CodeEditor(tright, height=15, on_run=self.run_example)
        self.example.pack(fill="both", expand=True)
        row = tk.Frame(tright, bg=T.BG)
        row.pack(fill="x", pady=8)
        T.Button(row, t("learn.run_example"), self.run_example,
                 variant="primary").pack(side="left")
        T.Button(row, t("learn.reset_example"), self.reset_example,
                 variant="ghost").pack(side="left", padx=8)
        T.Button(row, t("learn.to_exercise"), lambda: self.show_tab("task"),
                 variant="success").pack(side="right")
        self.example_console = Console(tright, height=8)
        self.example_console.pack(fill="both", expand=False)

        # task frame ---------------------------------------------------------
        self.task_view = TaskView(self.body, on_solved=self._solved,
                                  on_next=self.next_lesson, next_key="learn.next")

        self.show_tab("theory")
        if self.entries:
            self.open_lesson(self.entries[0])

    # ------------------------------------------------------------- list side
    def _build_list(self):
        for child in self.list_frame.winfo_children():
            child.destroy()
        self._rows.clear()
        current_section = None
        for entry in self.entries:
            section = entry.section()
            if section != current_section:
                current_section = section
                tk.Label(self.list_frame, text=section.upper(), bg=T.PANEL,
                         fg=T.FAINT, font=T.fonts()["tiny"], anchor="w").pack(
                    fill="x", padx=14, pady=(12, 4))
            row = tk.Frame(self.list_frame, bg=T.PANEL, cursor="hand2")
            row.pack(fill="x", padx=6, pady=1)
            dot = tk.Label(row, text="○", bg=T.PANEL, fg=T.FAINT,
                           font=T.fonts()["small"])
            dot.pack(side="left", padx=(8, 6))
            label = tk.Label(row, text=entry.title(),
                             bg=T.PANEL, fg=T.TEXT,
                             font=T.fonts()["small"], anchor="w")
            label.pack(side="left", fill="x", expand=True, pady=5)
            row.dot, row.label = dot, label  # type: ignore[attr-defined]
            for widget in (row, dot, label):
                widget.bind("<Button-1>", lambda e, l=entry: self.open_lesson(l))
                widget.bind("<Enter>", lambda e, r=row: self._hover(r, True))
                widget.bind("<Leave>", lambda e, r=row: self._hover(r, False))
            self._rows[entry.id] = row
        self.refresh_marks()

    def _hover(self, row, entering):
        if getattr(row, "_selected", False):
            return
        color = T.ELEV if entering else T.PANEL
        row.configure(bg=color)
        row.dot.configure(bg=color)
        row.label.configure(bg=color)

    def refresh_marks(self):
        done = 0
        for entry in self.entries:
            row = self._rows.get(entry.id)
            if not row:
                continue
            solved = self.app.progress.is_solved(entry.task_id, "lesson")
            done += bool(solved)
            row.dot.configure(text="●" if solved else "○",
                              fg=T.GREEN if solved else T.FAINT)
        self.count_label.configure(
            text=t("learn.done", done=done, total=len(self.entries)))

    def _select_row(self, lesson_id: str):
        for lid, row in self._rows.items():
            selected = lid == lesson_id
            row._selected = selected  # type: ignore[attr-defined]
            color = T.ELEV2 if selected else T.PANEL
            row.configure(bg=color)
            row.dot.configure(bg=color)
            row.label.configure(bg=color, fg=T.TEXT if selected else T.MUTED)

    # ------------------------------------------------------------ open/tabs
    def open_lesson(self, entry):
        self.lesson = entry
        self._select_row(entry.id)
        self.title_label.configure(text=entry.title())
        index = self.entries.index(entry) + 1
        self.section_label.configure(
            text=t("learn.position", section=entry.section(),
                   index=index, total=len(self.entries)))

        self.theory.configure(state="normal")
        self.theory.delete("1.0", "end")
        self.theory.insert("end", entry.theory().strip() + "\n")
        takeaway = entry.takeaway()
        if takeaway:
            self.theory.insert("end", f"\n➜  {takeaway}\n", "takeaway")
        self.theory.configure(state="disabled")
        self.theory.yview_moveto(0)

        self.example.set_code(entry.example())
        self.example_console.clear()
        self.example_console.writeln(t("learn.press_run"), "muted")
        self.task_view.load(entry.task(),
                            solved=self.app.progress.is_solved(entry.task_id, "lesson"))
        self.show_tab("theory")

    def show_tab(self, which: str):
        self.theory_frame.pack_forget()
        self.task_view.pack_forget()
        if which == "theory":
            self.theory_frame.pack(fill="both", expand=True)
            active, inactive = self.tab_theory, self.tab_task
        else:
            self.task_view.pack(fill="both", expand=True)
            active, inactive = self.tab_task, self.tab_theory
        active.configure(bg=T.ACCENT, fg="#ffffff")
        active._bg, active._hover = T.ACCENT, T.ACCENT_HOVER
        inactive.configure(bg=T.PANEL, fg=T.MUTED)
        inactive._bg, inactive._hover = T.PANEL, T.ELEV2

    def next_lesson(self):
        idx = self.entries.index(self.lesson)
        self.open_lesson(self.entries[(idx + 1) % len(self.entries)])

    def prev_lesson(self):
        idx = self.entries.index(self.lesson)
        self.open_lesson(self.entries[idx - 1])

    # --------------------------------------------------------------- example
    def run_example(self):
        source = self.example.get_code()
        self.example_console.clear()
        self.example_console.writeln(t("common.running") + "\n", "muted")

        backend = LG.current()

        def work():
            # The example is a whole program, so it goes through the same path
            # as the Playground rather than the function-grading harness.
            out, err, timed_out, secs = backend.run_program(source)
            self.after(0, lambda: self._example_done(out, err, timed_out, secs))
        threading.Thread(target=work, daemon=True).start()

    def _example_done(self, out, err, timed_out, secs):
        self.example_console.clear()
        if timed_out:
            self.example_console.writeln(t("common.timed_out"), "err")
            return
        if out:
            self.example_console.write(out)
        if err:
            self.example_console.writeln(err, "err")
        self.example_console.writeln(
            t("common.finished", ms=f"{secs * 1000:.0f}"), "muted")

    def reset_example(self):
        if self.lesson:
            self.example.set_code(self.lesson.example())

    def _solved(self, task):
        gained = self.app.progress.solved(task.id, task.difficulty, task.topic, "lesson")
        self.app.on_xp(gained)
        self.refresh_marks()


# ===========================================================================
#  PRACTICE (randomised drills)
# ===========================================================================
class PracticeView(tk.Frame):
    def __init__(self, master, app: "App"):
        super().__init__(master, bg=T.BG)
        self.app = app
        self.rng = random.Random()

        bar = tk.Frame(self, bg=T.PANEL)
        bar.pack(fill="x")
        inner = tk.Frame(bar, bg=T.PANEL)
        inner.pack(fill="x", padx=18, pady=12)

        tk.Label(inner, text=t("practice.topic"), bg=T.PANEL, fg=T.MUTED,
                 font=T.fonts()["small"]).pack(side="left")
        self.topic_values, topic_labels = i18n.topic_choices(
            self._generator().TOPICS)
        self.topic = ttk.Combobox(inner, state="readonly", width=18,
                                  values=topic_labels)
        self.topic.current(0)
        self.topic.pack(side="left", padx=(8, 18))

        tk.Label(inner, text=t("practice.level"), bg=T.PANEL, fg=T.MUTED,
                 font=T.fonts()["small"]).pack(side="left")
        self.diff_values, diff_labels = i18n.difficulty_choices(["Easy", "Medium"])
        self.difficulty = ttk.Combobox(inner, state="readonly", width=11,
                                       values=diff_labels)
        self.difficulty.current(0)
        self.difficulty.pack(side="left", padx=(8, 18))

        T.Button(inner, t("practice.new"), self.new_task,
                 variant="primary").pack(side="left")

        self.streak_label = tk.Label(inner, text="", bg=T.PANEL, fg=T.MUTED,
                                     font=T.fonts()["small"])
        self.streak_label.pack(side="right")

        tk.Label(self, text=t("practice.blurb"),
                 bg=T.BG, fg=T.FAINT, font=T.fonts()["tiny"], justify="left",
                 anchor="w").pack(anchor="w", padx=20, pady=(8, 0))

        self.task_view = TaskView(self, on_solved=self._solved, on_next=self.new_task,
                                  next_key="practice.another")
        self.task_view.pack(fill="both", expand=True)
        self.new_task()

    @staticmethod
    def _generator():
        """Python keeps its 31 generators; the others use the portable set."""
        return drills if LG.CURRENT == "python" else drills_multi

    def new_task(self):
        topic = self.topic_values[self.topic.current()]
        difficulty = self.diff_values[self.difficulty.current()]
        task = self._generator().generate(topic, difficulty, self.rng)
        self.task_view.load(task)
        self._update_stats()

    def _update_stats(self):
        data = self.app.progress.data
        self.streak_label.configure(
            text=t("practice.stats", solved=data["drill_solved"], streak=data["streak"]))

    def _solved(self, task):
        gained = self.app.progress.solved(task.id, task.difficulty, task.topic, "drill")
        self.app.on_xp(gained)
        self._update_stats()


# ===========================================================================
#  INTERVIEW
# ===========================================================================
class InterviewView(tk.Frame):
    def __init__(self, master, app: "App"):
        super().__init__(master, bg=T.BG)
        self.app = app
        self.rng = random.Random()
        self.current = None
        self._rows: dict[str, tk.Frame] = {}

        paned = tk.PanedWindow(self, orient="horizontal", bg=T.BG, bd=0,
                               sashwidth=6, sashrelief="flat", showhandle=False)
        paned.pack(fill="both", expand=True)

        left = tk.Frame(paned, bg=T.PANEL)
        paned.add(left, minsize=250, width=300, stretch="never")

        head = tk.Frame(left, bg=T.PANEL)
        head.pack(fill="x", padx=14, pady=(14, 6))
        tk.Label(head, text=t("interview.bank"), bg=T.PANEL, fg=T.ACCENT,
                 font=T.fonts()["tiny"]).pack(anchor="w")
        self.count_label = tk.Label(head, text="", bg=T.PANEL, fg=T.MUTED,
                                    font=T.fonts()["small"])
        self.count_label.pack(anchor="w", pady=(2, 0))

        search_wrap = tk.Frame(left, bg=T.ELEV)
        search_wrap.pack(fill="x", padx=12, pady=(6, 6))
        tk.Label(search_wrap, text="⌕", bg=T.ELEV, fg=T.FAINT,
                 font=T.fonts()["ui"]).pack(side="left", padx=(9, 0))
        self.search_var = tk.StringVar()
        self._placeholder_on = False
        self.search_entry = tk.Entry(search_wrap, textvariable=self.search_var,
                                     bg=T.ELEV, fg=T.TEXT, insertbackground=T.CYAN,
                                     bd=0, highlightthickness=0,
                                     font=T.fonts()["small"])
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(6, 10), pady=7)
        self._placeholder = t("interview.search")
        self._show_placeholder()
        self.search_entry.bind("<FocusIn>", self._clear_placeholder)
        self.search_entry.bind("<FocusOut>", lambda e: self._show_placeholder())

        filters = tk.Frame(left, bg=T.PANEL)
        filters.pack(fill="x", padx=12, pady=(0, 8))
        self.topic_values, topic_labels = i18n.topic_choices(self._all_topics())
        self.topic = ttk.Combobox(filters, state="readonly", width=15,
                                  values=topic_labels)
        self.topic.current(0)
        self.topic.pack(side="left")
        self.topic.bind("<<ComboboxSelected>>", lambda e: self.refresh_list())
        self.diff_values, diff_labels = i18n.difficulty_choices(
            problems_mod.DIFFICULTIES)
        self.difficulty = ttk.Combobox(filters, state="readonly", width=9,
                                       values=diff_labels)
        self.difficulty.current(0)
        self.difficulty.pack(side="left", padx=(6, 0))
        self.difficulty.bind("<<ComboboxSelected>>", lambda e: self.refresh_list())

        T.Button(left, t("interview.random"), self.random_problem,
                 variant="soft").pack(fill="x", padx=12, pady=(0, 8))

        container, self.list_frame = T.scrolled_frame(left, bg=T.PANEL)
        container.pack(fill="both", expand=True, padx=(6, 0), pady=(0, 10))

        right = tk.Frame(paned, bg=T.BG)
        paned.add(right, minsize=520, stretch="always")
        self.task_view = TaskView(right, on_solved=self._solved,
                                  on_next=self.random_problem,
                                  next_key="interview.next", show_timer=True)
        self.task_view.pack(fill="both", expand=True)

        # traced only now — the list widgets must exist before the first callback
        self.search_var.trace_add("write", lambda *_: self.refresh_list())
        self.refresh_list()
        first = self._matching()
        if first:
            self.open_problem(first[0])

    # ------------------------------------------------------ search box helpers
    def _show_placeholder(self):
        if not self.search_var.get():
            self._placeholder_on = True
            self.search_entry.configure(fg=T.FAINT)
            self.search_var.set(self._placeholder)

    def _clear_placeholder(self, _=None):
        if self._placeholder_on:
            self._placeholder_on = False
            self.search_var.set("")
            self.search_entry.configure(fg=T.TEXT)

    def query(self) -> str:
        if self._placeholder_on:
            return ""
        return self.search_var.get().strip()

    @staticmethod
    def _all_topics() -> list[str]:
        topics = set(problems_multi.TOPICS)
        if LG.CURRENT == "python":
            topics |= set(problems_mod.TOPICS)
        return sorted(topics)

    def _filters(self) -> tuple[str, str]:
        return (self.topic_values[self.topic.current()],
                self.diff_values[self.difficulty.current()])

    def _matching(self) -> list:
        """Problems for the active programming language.

        Every language gets the multi-language bank; Python additionally gets
        the large Python-only bank it started out with.
        """
        topic, difficulty = self._filters()
        query = self.query()
        items = list(problems_multi.filtered(LG.CURRENT, topic, difficulty, query))
        if LG.CURRENT == "python":
            items += list(problems_mod.filtered(topic, difficulty, query))
        return items

    def refresh_list(self):
        for child in self.list_frame.winfo_children():
            child.destroy()
        self._rows.clear()
        matches = self._matching()
        solved = sum(1 for p in matches
                     if self.app.progress.is_solved(p.id, "interview"))
        total = len(problems_multi.for_language(LG.CURRENT))
        if LG.CURRENT == "python":
            total += len(problems_mod.BANK)
        self.count_label.configure(
            text=t("interview.solved", solved=solved, shown=len(matches),
                   total=total))

        current_topic = None
        for problem in sorted(matches,
                              key=lambda p: (i18n.topic(p.topic), p.difficulty,
                                             p.display_title)):
            shown_topic = i18n.topic(problem.topic)
            if shown_topic != current_topic:
                current_topic = shown_topic
                tk.Label(self.list_frame, text=shown_topic.upper(), bg=T.PANEL,
                         fg=T.FAINT, font=T.fonts()["tiny"], anchor="w").pack(
                    fill="x", padx=14, pady=(10, 3))
            is_solved = self.app.progress.is_solved(problem.id, "interview")
            row = tk.Frame(self.list_frame, bg=T.PANEL, cursor="hand2")
            row.pack(fill="x", padx=6, pady=1)
            tick = tk.Label(row, text="✓" if is_solved else "·", bg=T.PANEL,
                            fg=T.GREEN if is_solved else T.FAINT,
                            font=T.fonts()["small"], width=2)
            tick.pack(side="left", padx=(6, 2))
            label = tk.Label(row, text=problem.display_title, bg=T.PANEL,
                             fg=T.TEXT if not is_solved else T.MUTED,
                             font=T.fonts()["small"], anchor="w")
            label.pack(side="left", fill="x", expand=True, pady=4)
            pill = tk.Label(row, text=i18n.difficulty(problem.difficulty)[0],
                            bg=T.PANEL, fg=T.DIFF_COLORS[problem.difficulty],
                            font=T.fonts()["tiny"], width=2)
            pill.pack(side="right", padx=(0, 8))
            row.parts = (tick, label, pill)  # type: ignore[attr-defined]
            for widget in (row, tick, label, pill):
                widget.bind("<Button-1>", lambda e, p=problem: self.open_problem(p))
                widget.bind("<Enter>", lambda e, r=row: self._hover(r, True))
                widget.bind("<Leave>", lambda e, r=row: self._hover(r, False))
            self._rows[problem.id] = row

    def _hover(self, row, entering):
        if getattr(row, "_selected", False):
            return
        color = T.ELEV if entering else T.PANEL
        row.configure(bg=color)
        for part in row.parts:  # type: ignore[attr-defined]
            part.configure(bg=color)

    def _select(self, pid):
        for rid, row in self._rows.items():
            selected = rid == pid
            row._selected = selected  # type: ignore[attr-defined]
            color = T.ELEV2 if selected else T.PANEL
            row.configure(bg=color)
            for part in row.parts:  # type: ignore[attr-defined]
                part.configure(bg=color)

    def open_problem(self, problem):
        self.current = problem
        self._select(problem.id)
        if isinstance(problem, problems_multi.MultiProblem):
            task = problem.build(LG.CURRENT, self.rng)
        else:
            task = problem.build(self.rng)
        self.task_view.load(task,
                            solved=self.app.progress.is_solved(problem.id, "interview"))

    def random_problem(self):
        pool = self._matching() or problems_multi.for_language(LG.CURRENT)
        if not pool:
            return
        unsolved = [p for p in pool
                    if not self.app.progress.is_solved(p.id, "interview")]
        self.open_problem(self.rng.choice(unsolved or pool))

    def _solved(self, task):
        gained = self.app.progress.solved(task.id, task.difficulty, task.topic,
                                          "interview")
        self.app.on_xp(gained)
        self.refresh_list()
        self._select(task.id)


# ===========================================================================
#  PLAYGROUND
# ===========================================================================
class PlaygroundView(tk.Frame):
    def __init__(self, master, app: "App"):
        super().__init__(master, bg=T.BG)
        self.app = app

        head = tk.Frame(self, bg=T.BG)
        head.pack(fill="x", padx=18, pady=(14, 6))
        tk.Label(head, text=t("play.title"), bg=T.BG, fg=T.TEXT,
                 font=T.fonts()["h1"]).pack(anchor="w")
        tk.Label(head, text=t("play.sub", label=LG.current().label),
                 bg=T.BG, fg=T.MUTED, font=T.fonts()["small"],
                 justify="left").pack(anchor="w")

        paned = tk.PanedWindow(self, orient="horizontal", bg=T.BG, bd=0,
                               sashwidth=6, sashrelief="flat", showhandle=False)
        paned.pack(fill="both", expand=True, padx=14, pady=10)

        left = tk.Frame(paned, bg=T.BG)
        paned.add(left, minsize=420, width=720, stretch="always")
        self.editor = CodeEditor(left, height=20, on_run=self.run)
        self.editor.pack(fill="both", expand=True)
        self.editor.set_code(LG.current().playground_source(i18n.LANG))

        row = tk.Frame(left, bg=T.BG)
        row.pack(fill="x", pady=8)
        T.Button(row, t("play.run"), self.run, variant="primary").pack(side="left")
        T.Button(row, t("play.clear_out"), lambda: self.console.clear(),
                 variant="ghost").pack(side="left", padx=8)
        T.Button(row, t("play.clear_editor"), lambda: self.editor.set_code(""),
                 variant="ghost").pack(side="left")
        self.timing = tk.Label(row, text="", bg=T.BG, fg=T.FAINT,
                               font=T.fonts()["code_small"])
        self.timing.pack(side="right")

        self.console = Console(left, height=12)
        self.console.pack(fill="both", expand=True)

        right = tk.Frame(paned, bg=T.BG)
        paned.add(right, minsize=180, width=250, stretch="never")
        tk.Label(right, text=t("play.stdin"), bg=T.BG, fg=T.ACCENT,
                 font=T.fonts()["tiny"]).pack(anchor="w", pady=(0, 4))
        self.stdin = CodeEditor(right, height=10, show_numbers=False,
                                font_key="code_small")
        self.stdin.pack(fill="both", expand=True)
        self.stdin.set_code("")
        tk.Label(right, text=t("play.stdin_hint"),
                 bg=T.BG, fg=T.FAINT, font=T.fonts()["tiny"], wraplength=210,
                 justify="left").pack(anchor="w", pady=8)

    def run(self):
        source = self.editor.get_code()
        stdin = self.stdin.get_code()
        self.console.clear()
        self.console.writeln(t("common.running") + "\n", "muted")
        self.timing.configure(text="")

        backend = LG.current()

        def work():
            out, err, timed_out, secs = backend.run_program(source, stdin)
            self.after(0, lambda: self._done(out, err, timed_out, secs))
        threading.Thread(target=work, daemon=True).start()

    def _done(self, out, err, timed_out, secs):
        self.console.clear()
        if timed_out:
            self.console.writeln(t("common.timed_out"), "err")
            return
        if out:
            self.console.write(out)
        if err:
            self.console.writeln(err, "err")
            # only Python reports a line number we can map back to the editor
            line = runner.error_line(err) if LG.CURRENT == "python" else None
            if line:
                self.editor.mark_error_line(line)
        if not out and not err:
            self.console.writeln(t("play.no_output"), "muted")
        self.timing.configure(text=f"{secs * 1000:.0f} ms")


# ===========================================================================
#  PROGRESS
# ===========================================================================
class ProgressView(tk.Frame):
    def __init__(self, master, app: "App"):
        super().__init__(master, bg=T.BG)
        self.app = app
        container, self.inner = T.scrolled_frame(self, bg=T.BG)
        container.pack(fill="both", expand=True)
        self.refresh()

    def refresh(self):
        for child in self.inner.winfo_children():
            child.destroy()
        p = self.app.progress
        data = p.data

        head = tk.Frame(self.inner, bg=T.BG)
        head.pack(fill="x", padx=22, pady=(18, 4))
        tk.Label(head, text=t("prog.title"), bg=T.BG, fg=T.TEXT,
                 font=T.fonts()["h1"]).pack(anchor="w")
        tk.Label(head, text=t("prog.sub"), bg=T.BG, fg=T.MUTED,
                 font=T.fonts()["small"]).pack(anchor="w")

        stats = tk.Frame(self.inner, bg=T.BG)
        stats.pack(fill="x", padx=18, pady=14)
        into, need = p.level_progress()
        tiles = [
            (t("prog.level"), str(p.level),
             t("prog.level.sub", into=into, need=need), T.ACCENT),
            (t("prog.xp"), str(p.xp), t("prog.xp.sub"), T.CYAN),
            (t("prog.streak"), str(data["streak"]),
             t("prog.streak.sub", best=data["best_streak"]), T.ORANGE),
            (t("prog.lessons"),
             f"{len(data['lessons_done'])}/{len(lessons_mod.LESSONS)}",
             t("prog.lessons.sub"), T.GREEN),
            (t("prog.problems"),
             f"{len(data['problems_solved'])}/{len(problems_mod.BANK)}",
             t("prog.problems.sub"), T.PINK),
            (t("prog.drills"), str(data["drill_solved"]), t("prog.drills.sub"), T.YELLOW),
        ]
        for i, (label, value, sub, color) in enumerate(tiles):
            tile = T.card(stats, bg=T.PANEL)
            tile.grid(row=0, column=i, sticky="nsew", padx=4)
            stats.grid_columnconfigure(i, weight=1)
            box = tile.inner  # type: ignore[attr-defined]
            tk.Label(box, text=label, bg=T.PANEL, fg=T.FAINT,
                     font=T.fonts()["tiny"]).pack(anchor="w", padx=14, pady=(12, 0))
            tk.Label(box, text=value, bg=T.PANEL, fg=color,
                     font=T.fonts()["h1"]).pack(anchor="w", padx=14)
            tk.Label(box, text=sub, bg=T.PANEL, fg=T.MUTED,
                     font=T.fonts()["tiny"]).pack(anchor="w", padx=14, pady=(0, 12))

        # ---------------------------------------------------------- by topic
        body = tk.Frame(self.inner, bg=T.BG)
        body.pack(fill="both", expand=True, padx=18, pady=(4, 20))
        body.grid_columnconfigure(0, weight=3)
        body.grid_columnconfigure(1, weight=2)

        topic_card = T.card(body, bg=T.PANEL)
        topic_card.grid(row=0, column=0, sticky="nsew", padx=(0, 6))
        box = topic_card.inner  # type: ignore[attr-defined]
        tk.Label(box, text=t("prog.by_topic"), bg=T.PANEL, fg=T.ACCENT,
                 font=T.fonts()["tiny"]).pack(anchor="w", padx=16, pady=(14, 8))

        topic_counts = data["topic_solved"]
        if not topic_counts:
            tk.Label(box, text=t("prog.nothing"),
                     bg=T.PANEL, fg=T.MUTED, font=T.fonts()["small"]).pack(
                anchor="w", padx=16, pady=(0, 16))
        else:
            biggest = max(topic_counts.values())
            for topic, count in sorted(topic_counts.items(), key=lambda kv: -kv[1]):
                row = tk.Frame(box, bg=T.PANEL)
                row.pack(fill="x", padx=16, pady=2)
                tk.Label(row, text=i18n.topic(topic), bg=T.PANEL, fg=T.TEXT, width=22,
                         anchor="w", font=T.fonts()["small"]).pack(side="left")
                track = tk.Frame(row, bg=T.ELEV, height=10)
                track.pack(side="left", fill="x", expand=True, padx=8)
                track.pack_propagate(False)
                fill = tk.Frame(track, bg=T.ACCENT, height=10)
                fill.place(relwidth=count / biggest, relheight=1)
                tk.Label(row, text=str(count), bg=T.PANEL, fg=T.MUTED, width=4,
                         anchor="e", font=T.fonts()["small"]).pack(side="right")
            tk.Frame(box, bg=T.PANEL, height=14).pack()

        # ---------------------------------------------------------- activity
        act_card = T.card(body, bg=T.PANEL)
        act_card.grid(row=0, column=1, sticky="nsew", padx=(6, 0))
        abox = act_card.inner  # type: ignore[attr-defined]
        tk.Label(abox, text=t("prog.last14"), bg=T.PANEL, fg=T.ACCENT,
                 font=T.fonts()["tiny"]).pack(anchor="w", padx=16, pady=(14, 8))
        history = data["history"][-14:]
        if not history:
            tk.Label(abox, text=t("prog.no_activity"), bg=T.PANEL, fg=T.MUTED,
                     font=T.fonts()["small"]).pack(anchor="w", padx=16)
        else:
            peak = max(h["solved"] for h in history)
            chart = tk.Frame(abox, bg=T.PANEL, height=110)
            chart.pack(fill="x", padx=16)
            chart.pack_propagate(False)
            for h in history:
                col = tk.Frame(chart, bg=T.PANEL)
                col.pack(side="left", fill="both", expand=True, padx=1)
                tk.Frame(col, bg=T.PANEL).pack(side="top", fill="both", expand=True)
                bar = tk.Frame(col, bg=T.ACCENT,
                               height=max(4, int(90 * h["solved"] / peak)))
                bar.pack(side="bottom", fill="x")
                tk.Label(col, text=h["day"][-2:], bg=T.PANEL, fg=T.FAINT,
                         font=T.fonts()["tiny"]).pack(side="bottom")
            tk.Frame(abox, bg=T.PANEL, height=10).pack()

        tk.Label(abox, text=t("prog.recent"), bg=T.PANEL, fg=T.ACCENT,
                 font=T.fonts()["tiny"]).pack(anchor="w", padx=16, pady=(12, 6))
        recent = data["recent"][:8]
        if not recent:
            tk.Label(abox, text="—", bg=T.PANEL, fg=T.MUTED,
                     font=T.fonts()["small"]).pack(anchor="w", padx=16, pady=(0, 14))
        for entry in recent:
            kind, _, tid = entry.partition(":")
            tk.Label(abox, text=f"  {t('prog.kind.' + kind):<12} {self._pretty(kind, tid)}",
                     bg=T.PANEL, fg=T.MUTED, font=T.fonts()["code_small"],
                     anchor="w").pack(fill="x", padx=16)
        tk.Frame(abox, bg=T.PANEL, height=16).pack()

        footer = tk.Frame(self.inner, bg=T.BG)
        footer.pack(fill="x", padx=22, pady=(0, 24))
        T.Button(footer, t("prog.reset"), self._reset, variant="danger").pack(side="left")
        tk.Label(footer, text=t("prog.reset_note"), bg=T.BG, fg=T.FAINT,
                 font=T.fonts()["tiny"]).pack(side="left")

    @staticmethod
    def _pretty(kind: str, tid: str) -> str:
        if kind == "lesson":
            lesson = lessons_mod.by_id(tid.replace("lesson_", ""))
            if lesson:
                return lessons_mod.field_of(lesson, "title")
            for other in lessons_multi.REGISTRY:      # a per-language lesson
                if other.id == tid:
                    return f"{LG.label(other.language)} · {i18n.pick(other.title, tid)}"
            return tid
        if kind == "interview":
            problem = problems_mod.by_id(tid)
            if problem:
                return problem.display_title
            multi = problems_multi.by_id(tid)
            return multi.display_title if multi else tid
        return tid.replace("drill_", "").rsplit("_", 1)[0].replace("_", " ")

    def _reset(self):
        win = tk.Toplevel(self)
        win.title(t("prog.reset_title"))
        win.configure(bg=T.PANEL)
        win.transient(self.winfo_toplevel())
        win.resizable(False, False)
        tk.Label(win, text=t("prog.reset_ask"), bg=T.PANEL,
                 fg=T.TEXT, font=T.fonts()["ui"], padx=24, pady=18).pack()
        row = tk.Frame(win, bg=T.PANEL)
        row.pack(pady=(0, 18))

        def confirm():
            self.app.progress.reset()
            win.destroy()
            self.app.refresh_all()

        T.Button(row, t("prog.reset_yes"), confirm, variant="danger").pack(
            side="left", padx=6)
        T.Button(row, t("prog.reset_no"), win.destroy, variant="soft").pack(
            side="left", padx=6)
        win.grab_set()


# ===========================================================================
#  APP SHELL
# ===========================================================================
class App(tk.Tk):
    NAV = ["learn", "practice", "interview", "playground", "progress"]

    def __init__(self):
        super().__init__()
        self.configure(bg=T.BG)
        self.geometry("1440x900")
        self.minsize(1100, 700)

        T.init_fonts(self)
        T.apply_ttk_theme(self)
        self.progress = Progress()
        i18n.set_language(self.progress.data.get("language", "en"))
        LG.set_current(self.progress.data.get("prog_language", LG.DEFAULT))

        self._xp_job = None
        self.views: dict[str, tk.Frame] = {}
        self.nav_buttons: dict[str, tk.Frame] = {}
        self.current = None
        self.sidebar = None

        self.content = tk.Frame(self, bg=T.BG)
        self.content.pack(side="left", fill="both", expand=True)
        self._build_sidebar()
        self._build_views()

        self.show("learn")
        self._bind_shortcuts()
        self.update_xp_bar()

    # -------------------------------------------------------------- sidebar
    def _build_sidebar(self):
        self.title(f"{APP_NAME} — {t('app.tagline')}")
        bar = tk.Frame(self, bg=T.PANEL, width=210)
        bar.pack(side="left", fill="y", before=self.content)
        bar.pack_propagate(False)
        self.sidebar = bar

        top = tk.Frame(bar, bg=T.PANEL)
        top.pack(fill="x", padx=16, pady=(20, 4))
        logo = tk.Frame(top, bg=T.PANEL)
        logo.pack(side="left")
        tk.Label(logo, text="Code", bg=T.PANEL, fg=T.ACCENT, padx=0,
                 font=T.fonts()["logo"]).pack(side="left")
        tk.Label(logo, text="Forge", bg=T.PANEL, fg=T.TEXT, padx=0,
                 font=T.fonts()["logo"]).pack(side="left")

        self.flag = T.FlagButton(top, lambda: i18n.LANG, self.set_ui_language,
                                 i18n.LANGUAGES, i18n.LANGUAGE_NAMES,
                                 title=t("shell.choose_language"))
        self.flag.pack(side="right", pady=3)

        tk.Label(bar, text=t("app.tagline"), bg=T.PANEL, fg=T.FAINT,
                 font=T.fonts()["tiny"], wraplength=170, justify="left").pack(
            anchor="w", padx=20, pady=(0, 4))
        tk.Label(bar, text=t("shell.lang_hint"), bg=T.PANEL, fg=T.FAINT,
                 font=T.fonts()["tiny"], wraplength=170, justify="left").pack(
            anchor="w", padx=20, pady=(0, 12))

        # ---------------------------------------------- programming language
        tk.Label(bar, text=t("lang.section"), bg=T.PANEL, fg=T.ACCENT,
                 font=T.fonts()["tiny"]).pack(anchor="w", padx=20, pady=(0, 4))

        detected = LG.detect()
        self.prog_values = list(LG.ORDER)
        labels = []
        for language_id in self.prog_values:
            backend = LG.get(language_id)
            usable = detected[language_id][0]
            mark = "✓" if usable else "·"
            labels.append(f"{mark}  {backend.label}")
        self.prog_combo = ttk.Combobox(bar, state="readonly", values=labels, width=17)
        self.prog_combo.current(self.prog_values.index(LG.CURRENT))
        self.prog_combo.pack(anchor="w", padx=18, pady=(0, 3))
        self.prog_combo.bind(
            "<<ComboboxSelected>>",
            lambda e: self.set_prog_language(self.prog_values[self.prog_combo.current()]))

        usable, info = LG.current().available()
        self.prog_status = tk.Label(
            bar, text=info if usable else t("lang.missing"), bg=T.PANEL,
            fg=T.GREEN if usable else T.YELLOW, font=T.fonts()["tiny"],
            wraplength=170, justify="left")
        self.prog_status.pack(anchor="w", padx=20, pady=(0, 14))

        for key in self.NAV:
            row = tk.Frame(bar, bg=T.PANEL, cursor="hand2")
            row.pack(fill="x", padx=10, pady=2)
            accent = tk.Frame(row, bg=T.PANEL, width=3)
            accent.pack(side="left", fill="y")
            text_box = tk.Frame(row, bg=T.PANEL)
            text_box.pack(side="left", fill="x", expand=True, padx=(9, 0), pady=7)
            name = tk.Label(text_box, text=t(f"nav.{key}"), bg=T.PANEL, fg=T.MUTED,
                            font=T.fonts()["ui_bold"], anchor="w")
            name.pack(fill="x")
            sub = tk.Label(text_box, text=t(f"nav.{key}.sub"), bg=T.PANEL, fg=T.FAINT,
                           font=T.fonts()["tiny"], anchor="w", wraplength=165,
                           justify="left")
            sub.pack(fill="x")
            row.parts = (accent, text_box, name, sub)  # type: ignore[attr-defined]
            for widget in (row, text_box, name, sub):
                widget.bind("<Button-1>", lambda e, k=key: self.show(k))
            self.nav_buttons[key] = row

        tk.Frame(bar, bg=T.PANEL).pack(fill="both", expand=True)

        xp_box = tk.Frame(bar, bg=T.PANEL)
        xp_box.pack(fill="x", padx=18, pady=(0, 10))
        self.level_label = tk.Label(xp_box, text="", bg=T.PANEL, fg=T.TEXT,
                                    font=T.fonts()["small_bold"], anchor="w")
        self.level_label.pack(fill="x")
        self.xp_track = tk.Frame(xp_box, bg=T.ELEV, height=6)
        self.xp_track.pack(fill="x", pady=(5, 4))
        self.xp_track.pack_propagate(False)
        self.xp_fill = tk.Frame(self.xp_track, bg=T.ACCENT, height=6)
        self.xp_fill.place(relwidth=0.0, relheight=1)
        self.xp_sub = tk.Label(xp_box, text="", bg=T.PANEL, fg=T.FAINT,
                               font=T.fonts()["tiny"], anchor="w")
        self.xp_sub.pack(fill="x")

        self.toast = tk.Label(bar, text="", bg=T.PANEL, fg=T.GREEN,
                              font=T.fonts()["small_bold"])
        self.toast.pack(fill="x", padx=18, pady=(0, 6))

        tk.Label(bar, text=t("shell.shortcuts"),
                 bg=T.PANEL, fg=T.FAINT, font=T.fonts()["tiny"],
                 wraplength=170, justify="left").pack(anchor="w", padx=18, pady=(0, 16))

    def _python_only(self, area_key: str) -> NoticeView:
        return NoticeView(
            self.content,
            t("lang.python_only_title"),
            t("lang.python_only_body", area=t(area_key), label=LG.current().label),
            button=f"→ Python",
            command=lambda: self.set_prog_language("python"))

    def _build_views(self):
        usable, _ = LG.current().available()
        backend = LG.current()
        missing = NoticeView(
            self.content,
            t("lang.missing_title", label=backend.label),
            t("lang.missing_body", label=backend.label,
              hint=backend.install_hint, button=t("lang.detect")),
            button=t("lang.detect"), command=self.recheck_toolchains)

        if usable:
            self.views["practice"] = PracticeView(self.content, self)
        else:
            self.views["practice"] = NoticeView(
                self.content,
                t("lang.missing_title", label=backend.label),
                t("lang.missing_body", label=backend.label,
                  hint=backend.install_hint, button=t("lang.detect")),
                button=t("lang.detect"), command=self.recheck_toolchains)

        if usable and curriculum.has_curriculum():
            self.views["learn"] = LearnView(self.content, self)
        elif not usable:
            self.views["learn"] = NoticeView(
                self.content,
                t("lang.missing_title", label=backend.label),
                t("lang.missing_body", label=backend.label,
                  hint=backend.install_hint, button=t("lang.detect")),
                button=t("lang.detect"), command=self.recheck_toolchains)
        else:
            self.views["learn"] = self._python_only("lang.area_curriculum")

        if usable:
            self.views["interview"] = InterviewView(self.content, self)
            self.views["playground"] = PlaygroundView(self.content, self)
        else:
            self.views["interview"] = missing
            self.views["playground"] = NoticeView(
                self.content,
                t("lang.missing_title", label=backend.label),
                t("lang.missing_body", label=backend.label,
                  hint=backend.install_hint, button=t("lang.detect")),
                button=t("lang.detect"), command=self.recheck_toolchains)

        self.views["progress"] = ProgressView(self.content, self)

    def _bind_shortcuts(self):
        for i, key in enumerate(self.NAV, start=1):
            self.bind_all(f"<Control-Key-{i}>", lambda e, k=key: self.show(k))

    # -------------------------------------------- programming language
    def set_prog_language(self, language_id: str):
        if language_id == LG.CURRENT:
            return
        LG.set_current(language_id)
        self.progress.data["prog_language"] = LG.CURRENT
        self.progress.save()
        self.rebuild()

    def recheck_toolchains(self):
        LG.detect(refresh=True)
        self.rebuild()

    # ------------------------------------------------------------- language
    def set_ui_language(self, code: str):
        if code == i18n.LANG:
            return
        i18n.set_language(code)
        self.progress.data["language"] = i18n.LANG
        self.progress.save()
        self.rebuild()

    def toggle_language(self):
        """Step to the next interface language — kept for the keyboard/tests."""
        order = list(i18n.LANGUAGES)
        self.set_ui_language(order[(order.index(i18n.LANG) + 1) % len(order)])

    def rebuild(self):
        """Tear the UI down and build it again in the new language."""
        keep = self.current
        for view in self.views.values():
            view.destroy()
        self.views.clear()
        self.nav_buttons.clear()
        if self.sidebar is not None:
            self.sidebar.destroy()
        self._build_sidebar()
        self._build_views()
        self.current = None
        self.show(keep or "learn")
        self.update_xp_bar()

    # ----------------------------------------------------------- navigation
    def show(self, key: str):
        if self.current == key:
            return
        for view in self.views.values():
            view.pack_forget()
        self.views[key].pack(fill="both", expand=True)
        self.current = key
        for k, row in self.nav_buttons.items():
            accent, text_box, name, sub = row.parts  # type: ignore[attr-defined]
            active = k == key
            bg = T.ELEV if active else T.PANEL
            row.configure(bg=bg)
            text_box.configure(bg=bg)
            name.configure(bg=bg, fg=T.TEXT if active else T.MUTED)
            sub.configure(bg=bg, fg=T.MUTED if active else T.FAINT)
            accent.configure(bg=T.ACCENT if active else bg)
        if key == "progress":
            self.views["progress"].refresh()

    # ------------------------------------------------------------------- xp
    def on_xp(self, gained: int):
        self.update_xp_bar()
        if gained:
            self.toast.configure(text=t("shell.gained", n=gained))
            if self._xp_job:
                self.after_cancel(self._xp_job)
            self._xp_job = self.after(2600, lambda: self.toast.configure(text=""))

    def update_xp_bar(self):
        into, need = self.progress.level_progress()
        self.level_label.configure(text=t("shell.level", n=self.progress.level))
        self.xp_fill.place(relwidth=min(1.0, into / need), relheight=1)
        self.xp_sub.configure(text=t("shell.xp", xp=self.progress.xp,
                                     left=need - into))

    def refresh_all(self):
        self.update_xp_bar()
        for key, method in (("learn", "refresh_marks"), ("interview", "refresh_list"),
                            ("progress", "refresh")):
            view = self.views.get(key)
            if hasattr(view, method):
                getattr(view, method)()


def main():
    # In a PyInstaller build the app doubles as the interpreter for the code the
    # user writes; this branch must run before any window is created.
    if len(sys.argv) > 2 and sys.argv[1] == runner.CHILD_FLAG:
        raise SystemExit(runner.run_child())
    if sys.version_info < (3, 9):
        raise SystemExit("CodeForge needs Python 3.9 or newer.")
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
