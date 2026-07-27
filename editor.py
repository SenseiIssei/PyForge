"""A small but real Python code editor widget.

Features: line numbers, syntax highlighting, current-line marker, auto-indent,
bracket/quote completion, block indent/dedent, comment toggle, undo/redo.
Pure tkinter, no dependencies.
"""
from __future__ import annotations

import keyword
import re
import tkinter as tk
from tkinter import ttk

import theme as T

BUILTINS = {
    "abs", "all", "any", "bin", "bool", "bytes", "callable", "chr", "dict", "dir",
    "divmod", "enumerate", "eval", "filter", "float", "format", "frozenset",
    "getattr", "hasattr", "hash", "hex", "id", "input", "int", "isinstance",
    "issubclass", "iter", "len", "list", "map", "max", "min", "next", "object",
    "oct", "open", "ord", "pow", "print", "range", "repr", "reversed", "round",
    "set", "setattr", "slice", "sorted", "str", "sum", "tuple", "type", "zip",
    "Exception", "ValueError", "TypeError", "KeyError", "IndexError",
    "ZeroDivisionError", "StopIteration", "NotImplementedError", "True", "False", "None",
}

_KW = sorted(set(keyword.kwlist) - {"True", "False", "None"}, key=len, reverse=True)

PATTERNS: list[tuple[str, str]] = [
    ("number", r"\b(0[xXbBoO][0-9a-fA-F_]+|\d[\d_]*\.?[\d_]*(?:[eE][+-]?\d+)?)\b"),
    ("keyword", r"\b(?:" + "|".join(_KW) + r")\b"),
    ("builtin", r"\b(?:" + "|".join(sorted(BUILTINS, key=len, reverse=True)) + r")\b"),
    ("self", r"\bself\b"),
    ("defname", r"(?<=\bdef )\s*\w+|(?<=\bclass )\s*\w+"),
    ("decorator", r"^[ \t]*@\w[\w.]*"),
    ("operator", r"[+\-*/%=<>!&|^~]+"),
    # strings & comments last so they win over everything above
    ("string", r"(?s)('''.*?'''|\"\"\".*?\"\"\")"),
    ("string", r"([frbFRB]{0,2}'(?:\\.|[^'\\\n])*'|[frbFRB]{0,2}\"(?:\\.|[^\"\\\n])*\")"),
    ("comment", r"#[^\n]*"),
]
_COMPILED = [(tag, re.compile(pat, re.MULTILINE)) for tag, pat in PATTERNS]

PAIRS = {"(": ")", "[": "]", "{": "}", "'": "'", '"': '"'}
CLOSERS = set(PAIRS.values())
INDENT = "    "


class CodeEditor(tk.Frame):
    def __init__(self, master, height: int = 18, readonly: bool = False,
                 on_run=None, font_key: str = "code", show_numbers: bool = True):
        super().__init__(master, bg=T.BORDER, bd=0, highlightthickness=0)
        self.on_run = on_run
        self.readonly = readonly
        self._hl_job = None

        wrap = tk.Frame(self, bg=T.ELEV)
        wrap.pack(fill="both", expand=True, padx=1, pady=1)

        f = T.fonts()
        self.font = f[font_key]

        self.gutter = tk.Canvas(wrap, width=48, bg=T.ELEV, highlightthickness=0, bd=0)
        if show_numbers:
            self.gutter.pack(side="left", fill="y")

        self.vbar = ttk.Scrollbar(wrap, orient="vertical", command=self._yview)
        self.vbar.pack(side="right", fill="y")

        self.text = tk.Text(
            wrap, bg=T.ELEV, fg=T.TEXT, insertbackground=T.CYAN, insertwidth=2,
            font=self.font, bd=0, highlightthickness=0, wrap="none", undo=True,
            maxundo=-1, autoseparators=True, tabs=self.font.measure(" " * 4),
            selectbackground="#33405c", selectforeground=T.TEXT,
            padx=10, pady=8, height=height, spacing1=1, spacing3=1,
        )
        self.text.pack(side="left", fill="both", expand=True)
        self.text.configure(yscrollcommand=self._on_yscroll)

        for tag, color in T.SYN.items():
            self.text.tag_configure(tag, foreground=color)
        self.text.tag_configure("comment", foreground=T.SYN["comment"])
        self.text.tag_configure("errline", background="#3a1f26")
        self.text.tag_lower("errline")

        if readonly:
            self.text.configure(insertwidth=0, bg=T.PANEL)
            self.text.bind("<Key>", self._block_keys)
        else:
            self._bind_editing()

        self.text.bind("<<Modified>>", self._on_modified)
        self.text.bind("<KeyRelease>", lambda e: self._refresh(), add="+")
        self.text.bind("<ButtonRelease>", lambda e: self._refresh(), add="+")
        self.text.bind("<Configure>", lambda e: self._draw_gutter(), add="+")
        self.text.bind("<MouseWheel>", self._on_wheel, add="+")

    # ---------------------------------------------------------------- public
    def get_code(self) -> str:
        return self.text.get("1.0", "end-1c")

    def set_code(self, code: str, keep_undo: bool = False) -> None:
        state = self.text.cget("state")
        self.text.configure(state="normal")
        self.text.delete("1.0", "end")
        self.text.insert("1.0", code.replace("\t", INDENT))
        if not keep_undo:
            self.text.edit_reset()
        self.text.edit_modified(False)
        if self.readonly:
            self.text.configure(state=state)
        self.highlight()
        self._draw_gutter()

    def mark_error_line(self, lineno: int | None) -> None:
        self.text.tag_remove("errline", "1.0", "end")
        if lineno:
            self.text.tag_add("errline", f"{lineno}.0", f"{lineno}.end+1c")
            self.text.see(f"{lineno}.0")

    def focus_code(self) -> None:
        self.text.focus_set()

    # -------------------------------------------------------------- internal
    def _block_keys(self, event):
        allowed = ("Up", "Down", "Left", "Right", "Prior", "Next", "Home", "End")
        if event.keysym in allowed or (event.state & 4):  # allow ctrl combos (copy)
            return None
        return "break"

    def _bind_editing(self):
        t = self.text
        t.bind("<Return>", self._on_return)
        t.bind("<Tab>", self._on_tab)
        t.bind("<Shift-Tab>", self._on_shift_tab)
        t.bind("<BackSpace>", self._on_backspace)
        t.bind("<Control-slash>", self._toggle_comment)
        t.bind("<Control-d>", self._duplicate_line)
        t.bind("<Control-a>", self._select_all)
        for opener in PAIRS:
            t.bind(f"<KeyPress-{self._keysym(opener)}>", self._on_open_char)
        for closer in CLOSERS:
            if closer not in ("'", '"'):
                t.bind(f"<KeyPress-{self._keysym(closer)}>", self._on_close_char)
        if self.on_run:
            t.bind("<Control-Return>", lambda e: (self.on_run(), "break")[1])

    @staticmethod
    def _keysym(ch: str) -> str:
        return {"(": "parenleft", ")": "parenright", "[": "bracketleft",
                "]": "bracketright", "{": "braceleft", "}": "braceright",
                "'": "apostrophe", '"': "quotedbl"}.get(ch, ch)

    def _select_all(self, _):
        self.text.tag_add("sel", "1.0", "end-1c")
        return "break"

    def _cur_line(self) -> str:
        return self.text.get("insert linestart", "insert")

    def _on_return(self, _):
        line = self.text.get("insert linestart", "insert lineend")
        before = self._cur_line()
        indent = re.match(r"[ \t]*", before).group(0)
        stripped = before.rstrip()
        if stripped.endswith(":"):
            indent += INDENT
        elif re.match(r"\s*(return|pass|break|continue|raise)\b", stripped) and len(indent) >= 4:
            indent = indent[:-4]
        after = self.text.get("insert", "insert lineend")
        self.text.insert("insert", "\n" + indent)
        # opening brace right before cursor and closer right after -> expand block
        if before[-1:] in "([{" and after[:1] in ")]}":
            self.text.insert("insert", "\n" + indent[:-4] if indent else "\n")
            self.text.mark_set("insert", f"insert -{len(indent[:-4] if indent else '')+1}c")
        self.text.see("insert")
        self._refresh()
        return "break"

    def _sel_lines(self):
        try:
            first = int(self.text.index("sel.first").split(".")[0])
            last_idx = self.text.index("sel.last")
            last = int(last_idx.split(".")[0])
            if last_idx.split(".")[1] == "0" and last > first:
                last -= 1
            return first, last
        except tk.TclError:
            return None

    def _on_tab(self, _):
        rng = self._sel_lines()
        if rng:
            for ln in range(rng[0], rng[1] + 1):
                self.text.insert(f"{ln}.0", INDENT)
        else:
            col = int(self.text.index("insert").split(".")[1])
            self.text.insert("insert", " " * (4 - col % 4))
        self._refresh()
        return "break"

    def _on_shift_tab(self, _):
        rng = self._sel_lines() or (int(self.text.index("insert").split(".")[0]),) * 2
        for ln in range(rng[0], rng[1] + 1):
            head = self.text.get(f"{ln}.0", f"{ln}.4")
            strip = len(head) - len(head.lstrip(" "))
            if strip:
                self.text.delete(f"{ln}.0", f"{ln}.{min(strip, 4)}")
        self._refresh()
        return "break"

    def _on_backspace(self, _):
        if self.text.tag_ranges("sel"):
            return None
        before = self._cur_line()
        if before and not before.strip() and len(before) % 4 == 0:
            self.text.delete("insert -4c", "insert")
            return "break"
        pair = self.text.get("insert -1c", "insert +1c")
        if len(pair) == 2 and PAIRS.get(pair[0]) == pair[1]:
            self.text.delete("insert -1c", "insert +1c")
            return "break"
        return None

    def _on_open_char(self, event):
        ch = event.char
        if ch not in PAIRS:
            return None
        if self.text.tag_ranges("sel"):  # wrap selection
            s, e = self.text.index("sel.first"), self.text.index("sel.last")
            body = self.text.get(s, e)
            self.text.delete(s, e)
            self.text.insert(s, ch + body + PAIRS[ch])
            self._refresh()
            return "break"
        nxt = self.text.get("insert", "insert +1c")
        if ch in ("'", '"'):
            prev = self.text.get("insert -1c", "insert")
            if prev.isalnum() or prev == ch or nxt == ch:
                return None
        if nxt and (nxt.isalnum() or nxt in "\"'"):
            return None
        self.text.insert("insert", ch + PAIRS[ch])
        self.text.mark_set("insert", "insert -1c")
        self._refresh()
        return "break"

    def _on_close_char(self, event):
        if self.text.get("insert", "insert +1c") == event.char:
            self.text.mark_set("insert", "insert +1c")
            self._refresh()
            return "break"
        return None

    def _toggle_comment(self, _):
        rng = self._sel_lines() or (int(self.text.index("insert").split(".")[0]),) * 2
        lines = [self.text.get(f"{ln}.0", f"{ln}.end") for ln in range(rng[0], rng[1] + 1)]
        meaningful = [l for l in lines if l.strip()]
        commented = meaningful and all(l.lstrip().startswith("#") for l in meaningful)
        for i, ln in enumerate(range(rng[0], rng[1] + 1)):
            line = lines[i]
            if not line.strip():
                continue
            pad = len(line) - len(line.lstrip())
            if commented:
                body = line.lstrip()[1:]
                body = body[1:] if body.startswith(" ") else body
                self.text.delete(f"{ln}.0", f"{ln}.end")
                self.text.insert(f"{ln}.0", " " * pad + body)
            else:
                self.text.insert(f"{ln}.{pad}", "# ")
        self._refresh()
        return "break"

    def _duplicate_line(self, _):
        line = self.text.get("insert linestart", "insert lineend")
        self.text.insert("insert lineend", "\n" + line)
        self._refresh()
        return "break"

    # ------------------------------------------------------- highlight/gutter
    def _on_modified(self, _):
        if self.text.edit_modified():
            self.text.edit_modified(False)
            self._refresh()

    def _refresh(self):
        if self._hl_job:
            self.after_cancel(self._hl_job)
        self._hl_job = self.after(40, self._do_refresh)

    def _do_refresh(self):
        self._hl_job = None
        self.highlight()
        self._draw_gutter()

    def highlight(self):
        src = self.text.get("1.0", "end-1c")
        for tag in T.SYN:
            self.text.tag_remove(tag, "1.0", "end")
        if len(src) > 40000:
            return
        # map absolute offsets -> tk indices quickly via line starts
        starts, pos = [0], 0
        for line in src.split("\n"):
            pos += len(line) + 1
            starts.append(pos)

        def idx(offset: int) -> str:
            lo, hi = 0, len(starts) - 1
            while lo < hi:
                mid = (lo + hi + 1) // 2
                if starts[mid] <= offset:
                    lo = mid
                else:
                    hi = mid - 1
            return f"{lo + 1}.{offset - starts[lo]}"

        taken: list[tuple[int, int]] = []
        for tag, rx in _COMPILED:
            for m in rx.finditer(src):
                s, e = m.span()
                if any(s < te and e > ts for ts, te in taken):
                    continue
                if tag in ("string", "comment"):
                    for other in T.SYN:
                        self.text.tag_remove(other, idx(s), idx(e))
                    taken.append((s, e))
                self.text.tag_add(tag, idx(s), idx(e))

    def _draw_gutter(self):
        g = self.gutter
        g.delete("all")
        try:
            first = self.text.index("@0,0")
        except tk.TclError:
            return
        cur_line = self.text.index("insert").split(".")[0]
        i = first
        while True:
            info = self.text.dlineinfo(i)
            if info is None:
                break
            y = info[1]
            num = i.split(".")[0]
            g.create_text(38, y + info[3] // 2, anchor="e", text=num,
                          fill=T.CYAN if num == cur_line else T.FAINT,
                          font=T.fonts()["code_small"])
            i = self.text.index(f"{i}+1line")
            if int(i.split(".")[0]) > int(self.text.index("end-1c").split(".")[0]):
                break

    def _yview(self, *args):
        self.text.yview(*args)
        self._draw_gutter()

    def _on_yscroll(self, *args):
        self.vbar.set(*args)
        self._draw_gutter()

    def _on_wheel(self, event):
        self.text.yview_scroll(int(-1 * (event.delta / 120)), "units")
        self._draw_gutter()
        return "break"


class Console(tk.Frame):
    """Read-only, colorised output pane."""

    def __init__(self, master, height: int = 8):
        super().__init__(master, bg=T.BORDER)
        wrap = tk.Frame(self, bg="#0a0c10")
        wrap.pack(fill="both", expand=True, padx=1, pady=1)

        self.vbar = ttk.Scrollbar(wrap, orient="vertical")
        self.vbar.pack(side="right", fill="y")
        self.text = tk.Text(wrap, bg="#0a0c10", fg=T.TEXT, font=T.fonts()["code_small"],
                            bd=0, highlightthickness=0, wrap="word", height=height,
                            padx=10, pady=8, insertwidth=0,
                            yscrollcommand=self.vbar.set, state="disabled",
                            selectbackground="#33405c")
        self.text.pack(side="left", fill="both", expand=True)
        self.vbar.configure(command=self.text.yview)

        for name, color in (("ok", T.GREEN), ("err", T.RED), ("warn", T.YELLOW),
                            ("info", T.CYAN), ("muted", T.MUTED), ("accent", T.ACCENT),
                            ("plain", T.TEXT)):
            self.text.tag_configure(name, foreground=color)
        self.text.tag_configure("bold", font=T.fonts()["code_bold"])
        self.text.bind("<MouseWheel>",
                       lambda e: (self.text.yview_scroll(int(-e.delta / 120), "units"), "break")[1])

    def clear(self):
        self.text.configure(state="normal")
        self.text.delete("1.0", "end")
        self.text.configure(state="disabled")

    def write(self, text: str, tag: str = "plain"):
        self.text.configure(state="normal")
        self.text.insert("end", text, tag)
        self.text.see("end")
        self.text.configure(state="disabled")

    def writeln(self, text: str = "", tag: str = "plain"):
        self.write(text + "\n", tag)
