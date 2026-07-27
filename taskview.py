"""The reusable "solve a task" panel: statement | editor + console.

Used by the Learn, Practice and Interview tabs so all three behave identically.
Every visible string goes through i18n.t().
"""
from __future__ import annotations

import threading
import time
import tkinter as tk
from tkinter import ttk

import i18n
import runner
import theme as T
from editor import CodeEditor, Console
from i18n import t
from tasks import Task, pretty_args


class TaskView(tk.Frame):
    def __init__(self, master, on_solved=None, on_next=None, next_key="",
                 show_timer: bool = False):
        super().__init__(master, bg=T.BG)
        self.task: Task | None = None
        self.on_solved = on_solved
        self.on_next = on_next
        self.next_key = next_key
        self._busy = False
        self._hint_index = 0
        self._solution_shown = False
        self._start_time = 0.0
        self._timer_job = None
        self.show_timer = show_timer

        # ------------------------------------------------------------ header
        head = tk.Frame(self, bg=T.BG)
        head.pack(fill="x", padx=18, pady=(14, 8))

        title_row = tk.Frame(head, bg=T.BG)
        title_row.pack(fill="x")
        self.title_label = tk.Label(title_row, text="", bg=T.BG, fg=T.TEXT,
                                    font=T.fonts()["h2"], anchor="w")
        self.title_label.pack(side="left")

        self.diff_pill = tk.Label(title_row, text="", bg=T.PANEL, fg=T.GREEN,
                                  font=T.fonts()["tiny"], padx=8, pady=2)
        self.diff_pill.pack(side="left", padx=(10, 4))
        self.topic_pill = tk.Label(title_row, text="", bg=T.PANEL, fg=T.MUTED,
                                   font=T.fonts()["tiny"], padx=8, pady=2)
        self.topic_pill.pack(side="left", padx=4)
        self.solved_pill = tk.Label(title_row, text="", bg=T.PANEL, fg=T.GREEN,
                                    font=T.fonts()["tiny"], padx=8, pady=2)

        self.timer_label = tk.Label(title_row, text="", bg=T.BG, fg=T.FAINT,
                                    font=T.fonts()["code_small"])
        if show_timer:
            self.timer_label.pack(side="right")

        self.complexity_label = tk.Label(head, text="", bg=T.BG, fg=T.CYAN,
                                         font=T.fonts()["small"], anchor="w")
        self.complexity_label.pack(fill="x", pady=(4, 0))

        # ------------------------------------------------------------- split
        paned = tk.PanedWindow(self, orient="horizontal", bg=T.BG, bd=0,
                               sashwidth=6, sashrelief="flat", showhandle=False,
                               sashpad=0)
        paned.pack(fill="both", expand=True, padx=14, pady=(6, 10))

        left = tk.Frame(paned, bg=T.BG)
        paned.add(left, minsize=280, width=545, stretch="always")

        stmt_card = T.card(left, bg=T.PANEL)
        stmt_card.pack(fill="both", expand=True)
        inner = stmt_card.inner  # type: ignore[attr-defined]

        bar = tk.Frame(inner, bg=T.PANEL)
        bar.pack(fill="x", padx=12, pady=(10, 4))
        tk.Label(bar, text=t("task.header"), bg=T.PANEL, fg=T.ACCENT,
                 font=T.fonts()["tiny"]).pack(side="left")

        stmt_wrap = tk.Frame(inner, bg=T.PANEL)
        stmt_wrap.pack(fill="both", expand=True, padx=4, pady=(0, 8))
        hbar = ttk.Scrollbar(stmt_wrap, orient="horizontal")
        hbar.pack(side="bottom", fill="x")
        sbar = ttk.Scrollbar(stmt_wrap, orient="vertical")
        sbar.pack(side="right", fill="y")
        # wrap="none": statements are pre-formatted, word-wrap would destroy
        # the alignment of the code examples inside them.
        self.statement = tk.Text(stmt_wrap, bg=T.PANEL, fg=T.TEXT, bd=0,
                                 highlightthickness=0, wrap="none",
                                 font=T.fonts()["code_small"], padx=10, pady=4,
                                 insertwidth=0, yscrollcommand=sbar.set,
                                 xscrollcommand=hbar.set,
                                 state="disabled", spacing1=1, spacing3=3,
                                 selectbackground="#33405c")
        self.statement.pack(side="left", fill="both", expand=True)
        sbar.configure(command=self.statement.yview)
        hbar.configure(command=self.statement.xview)
        self.statement.tag_configure("code", foreground=T.SYN["string"],
                                     font=T.fonts()["code_small"])
        self.statement.tag_configure("hint", foreground=T.YELLOW)
        self.statement.tag_configure("note", foreground=T.CYAN)
        self.statement.tag_configure("head", foreground=T.ACCENT,
                                     font=T.fonts()["code_bold"])
        self.statement.bind("<MouseWheel>", lambda e: (
            self.statement.yview_scroll(int(-e.delta / 120), "units"), "break")[1])

        right = tk.Frame(paned, bg=T.BG)
        paned.add(right, minsize=340, stretch="always")

        self.editor = CodeEditor(right, height=16, on_run=self.run_tests)
        self.editor.pack(fill="both", expand=True)

        # -------------------------------------------------------- action bar
        actions = tk.Frame(right, bg=T.BG)
        actions.pack(fill="x", pady=(8, 6))

        # packed first so it always keeps its space when the row gets tight
        self.btn_next = T.Button(actions, t(next_key) + "  →" if next_key else "",
                                 self._next, variant="success")
        if on_next:
            self.btn_next.pack(side="right")

        self.btn_test = T.Button(actions, t("task.run_tests"), self.run_tests,
                                 variant="primary")
        self.btn_test.pack(side="left")
        self.btn_run = T.Button(actions, t("task.run_code"), self.run_plain,
                                variant="soft")
        self.btn_run.pack(side="left", padx=(8, 0))
        self.btn_hint = T.Button(actions, t("task.hint"), self.show_hint, variant="ghost")
        self.btn_hint.pack(side="left", padx=(8, 0))
        self.btn_solution = T.Button(actions, t("task.solution"), self.show_solution,
                                     variant="ghost")
        self.btn_solution.pack(side="left", padx=(8, 0))
        self.btn_reset = T.Button(actions, t("task.reset"), self.reset_code,
                                  variant="ghost")
        self.btn_reset.pack(side="left", padx=(8, 0))

        self.status = tk.Label(right, text="", bg=T.BG, fg=T.MUTED,
                               font=T.fonts()["small"], anchor="w")
        self.status.pack(fill="x", pady=(0, 4))

        self.console = Console(right, height=9)
        self.console.pack(fill="both", expand=False)

    # ------------------------------------------------------------------ task
    def load(self, task: Task, solved: bool = False) -> None:
        self.task = task
        self._hint_index = 0
        self._solution_shown = False
        self.title_label.configure(text=task.title)
        self.diff_pill.configure(text=i18n.difficulty(task.difficulty).upper(),
                                 fg=T.DIFF_COLORS.get(task.difficulty, T.MUTED))
        self.topic_pill.configure(text=i18n.topic(task.topic).upper())
        if solved:
            self.solved_pill.configure(text=t("task.solved_pill"))
            self.solved_pill.pack(side="left", padx=4)
        else:
            self.solved_pill.pack_forget()
        self.complexity_label.configure(
            text=t("task.complexity", value=task.complexity) if task.complexity else "")

        self._render_statement()
        self.editor.set_code(task.starter)
        self.editor.mark_error_line(None)
        self.console.clear()
        visible = len(task.visible_cases())
        hidden = len(task.cases) - visible
        self.console.writeln(t("task.loaded", n=len(task.cases), shown=visible,
                               hidden=hidden), "muted")
        self.console.writeln(t("task.write"), "muted")
        self.status.configure(text="", fg=T.MUTED)
        self.btn_hint.configure(text=t("task.hint_n", i=0, total=len(task.hints)))
        self.btn_solution.configure(text=t("task.solution"))
        if self.show_timer:
            self._start_time = time.time()
            self._tick()

    def _render_statement(self) -> None:
        task = self.task
        if task is None:
            return
        st = self.statement
        st.configure(state="normal")
        st.delete("1.0", "end")
        st.insert("end", task.statement + "\n\n")
        cases = task.visible_cases()
        if cases:
            st.insert("end", t("task.examples") + "\n", "head")
            for c in cases:
                label = f"  # {c['label']}\n" if c.get("label") else ""
                st.insert("end", label, "note")
                call = f"  {task.func}{pretty_args(c['args'])}"
                if task.checker_src:
                    st.insert("end", call + "\n", "code")
                else:
                    st.insert("end", f"{call}  ->  {c['expected']}\n", "code")
        hidden = len(task.cases) - len(cases)
        if hidden:
            st.insert("end", t("task.hidden_note", n=hidden), "note")
        st.configure(state="disabled")

    def _append_statement(self, text: str, tag: str = "hint") -> None:
        self.statement.configure(state="normal")
        self.statement.insert("end", text, tag)
        self.statement.see("end")
        self.statement.configure(state="disabled")

    # --------------------------------------------------------------- actions
    def show_hint(self) -> None:
        if not self.task or not self.task.hints:
            self.console.writeln(t("task.no_hints"), "muted")
            return
        if self._hint_index >= len(self.task.hints):
            self.console.writeln(t("task.last_hint"), "muted")
            return
        hint = self.task.hints[self._hint_index]
        self._hint_index += 1
        self._append_statement(t("task.hint_line", i=self._hint_index, text=hint), "hint")
        self.btn_hint.configure(text=t("task.hint_n", i=self._hint_index,
                                       total=len(self.task.hints)))

    def show_solution(self) -> None:
        if not self.task:
            return
        if not self._solution_shown:
            self._solution_shown = True
            self.console.clear()
            self.console.writeln(t("task.solution_intro"), "warn")
            self.console.writeln(self.task.solution or t("task.no_solution"), "info")
            self.btn_solution.configure(text=t("task.load_solution"))
        else:
            self.editor.set_code(self.task.solution)
            self.console.writeln(t("task.solution_loaded"), "muted")

    def reset_code(self) -> None:
        if self.task:
            self.editor.set_code(self.task.starter)
            self.editor.mark_error_line(None)
            self.console.clear()
            self.status.configure(text="")

    def _next(self) -> None:
        if self.on_next:
            self.on_next()

    # ----------------------------------------------------------- run helpers
    def _set_busy(self, value: bool) -> None:
        self._busy = value
        self.btn_test.configure(text=t("task.running") if value else t("task.run_tests"))

    def run_plain(self) -> None:
        """Execute the editor content as a plain script (prints show up below)."""
        if self._busy:
            return
        source = self.editor.get_code()
        self.console.clear()
        self.console.writeln(t("task.script_run") + "\n", "muted")
        self._set_busy(True)

        def work():
            out, err, timed_out, secs = runner.run_script(source)
            self.after(0, lambda: self._show_plain(out, err, timed_out, secs))

        threading.Thread(target=work, daemon=True).start()

    def _show_plain(self, out, err, timed_out, secs) -> None:
        self._set_busy(False)
        if timed_out:
            self.console.writeln(t("task.timeout_10"), "err")
            return
        if out:
            self.console.write(out)
        if err:
            self.console.writeln(err, "err")
            self.editor.mark_error_line(runner.error_line(err))
        if not out and not err:
            self.console.writeln(t("task.no_prints"), "muted")
        self.console.writeln(t("task.finished_ms", ms=f"{secs * 1000:.0f}"), "muted")

    def run_tests(self) -> None:
        if self._busy or not self.task:
            return
        task = self.task
        source = self.editor.get_code()
        self.console.clear()
        self.console.writeln(t("task.running_tests") + "\n", "muted")
        self.status.configure(text="")
        self.editor.mark_error_line(None)
        self._set_busy(True)

        def work():
            report = runner.run_tests(source, task.func, task.cases, task.checker_src)
            self.after(0, lambda: self._show_report(report))

        threading.Thread(target=work, daemon=True).start()

    def _show_report(self, report: runner.TestReport) -> None:
        self._set_busy(False)
        task = self.task
        if task is None:
            return
        c = self.console

        if report.timed_out:
            c.writeln(t("task.timeout_big"), "err")
            c.writeln(t("task.timeout_why"), "muted")
            self.status.configure(text=t("task.status_timeout"), fg=T.RED)
            return

        if report.import_error:
            c.writeln(t("task.crash_intro"), "err")
            c.writeln(report.import_error.rstrip(), "err")
            line = runner.error_line(report.import_error)
            if line:
                self.editor.mark_error_line(line)
                c.writeln(t("task.crash_line", line=line), "warn")
            self.status.configure(text=t("task.status_crash"), fg=T.RED)
            return

        if report.stdout.strip():
            c.writeln(t("task.your_prints"), "muted")
            c.writeln(report.stdout.rstrip(), "muted")
            c.writeln("")

        for i, case in enumerate(report.cases, 1):
            tag_ok = "ok" if case.passed else "err"
            mark = t("task.pass") if case.passed else t("task.fail")
            name = case.label or (t("task.hidden_test") if case.hidden else t("task.test"))
            c.write(f"{mark:>4}  ", tag_ok)
            c.write(f"#{i} {name}\n", "muted")
            if not case.passed:
                if case.hidden and not case.error:
                    c.writeln(t("task.hidden_input"), "muted")
                else:
                    c.writeln(t("task.input", value=pretty_args(case.args)), "muted")
                if case.error:
                    c.writeln(t("task.crashed", value=case.error), "err")
                elif task.checker_src:
                    c.writeln(t("task.checker_fail"), "err")
                else:
                    c.writeln(t("task.expected", value=case.expected), "warn")
                    c.writeln(t("task.got", value=case.got), "err")

        c.writeln("")
        if report.ok:
            c.writeln(t("task.all_passed", n=report.total,
                        ms=f"{report.elapsed * 1000:.0f}"), "ok")
            if task.complexity:
                c.writeln(t("task.complexity_check", value=task.complexity), "info")
            if task.notes:
                c.writeln(f"\n   {task.notes}", "info")
            self.status.configure(text=t("task.status_solved"), fg=T.GREEN)
            if self.on_solved:
                self.on_solved(task)
        else:
            c.writeln(t("task.some_passed", passed=report.passed, total=report.total),
                      "err")
            hint = self._diagnose(report)
            if hint:
                c.writeln(f"   {hint}", "warn")
            self.status.configure(
                text=t("task.status_passing", passed=report.passed, total=report.total),
                fg=T.YELLOW)

    @staticmethod
    def _diagnose(report: runner.TestReport) -> str:
        errors = [c.error for c in report.cases if c.error]
        if errors:
            first = errors[0]
            if "NoneType" in first:
                return t("diag.none")
            if first.startswith("IndexError"):
                return t("diag.index")
            if first.startswith("KeyError"):
                return t("diag.key")
            if first.startswith("TypeError"):
                return t("diag.type")
            if first.startswith("ZeroDivisionError"):
                return t("diag.zero")
            return t("diag.crash")
        empties = [c for c in report.cases if not c.passed and c.args in ("([],)", "('',)")]
        if empties:
            return t("diag.empty")
        if all(c.got == "None" for c in report.cases if not c.passed):
            return t("diag.all_none")
        return ""

    # ----------------------------------------------------------------- timer
    def _tick(self) -> None:
        if not self.show_timer or not self.winfo_exists():
            return
        elapsed = int(time.time() - self._start_time)
        self.timer_label.configure(text=f"{elapsed // 60:02d}:{elapsed % 60:02d}")
        self._timer_job = self.after(1000, self._tick)

    def stop_timer(self) -> None:
        if self._timer_job:
            self.after_cancel(self._timer_job)
            self._timer_job = None
