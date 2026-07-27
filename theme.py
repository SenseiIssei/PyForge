"""Central place for colors, fonts and ttk styling.

Everything visual in CodeForge goes through here so the whole app stays
consistent and a palette swap is a one-file change.
"""
from __future__ import annotations

import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk

# --------------------------------------------------------------------------
# palette (dark, high contrast, low saturation background)
# --------------------------------------------------------------------------
BG = "#0d0f14"          # app background
PANEL = "#141821"       # cards / side panels
ELEV = "#1b2029"        # elevated surface (editor, inputs)
ELEV2 = "#232936"       # hover surface
BORDER = "#2a3140"      # hairlines
TEXT = "#e7eaf0"        # primary text
MUTED = "#8b94a8"       # secondary text
FAINT = "#5b6478"       # tertiary / line numbers

ACCENT = "#7c5cff"      # primary brand (violet)
ACCENT_HOVER = "#8f74ff"
CYAN = "#31d0e0"
GREEN = "#3ddc97"
RED = "#ff6b6b"
YELLOW = "#ffc857"
ORANGE = "#ff9f5a"
PINK = "#ff7ab6"

DIFF_COLORS = {"Easy": GREEN, "Medium": YELLOW, "Hard": RED}

# --------------------------------------------------------------------------
# syntax colors
# --------------------------------------------------------------------------
SYN = {
    "keyword": "#c792ea",
    "builtin": "#82aaff",
    "string": "#c3e88d",
    "comment": "#5f6b82",
    "number": "#f78c6c",
    "decorator": "#ffcb6b",
    "defname": "#ffd479",
    "self": "#ff7ab6",
    "operator": "#89ddff",
}

_fonts: dict[str, tkfont.Font] = {}


def _pick(root: tk.Misc, candidates: list[str], fallback: str) -> str:
    available = set(tkfont.families(root))
    for name in candidates:
        if name in available:
            return name
    return fallback


def init_fonts(root: tk.Misc) -> dict[str, tkfont.Font]:
    """Create the app font objects once and cache them."""
    if _fonts:
        return _fonts

    ui = _pick(root, ["Segoe UI Variable Text", "Segoe UI", "Inter", "Helvetica"], "TkDefaultFont")
    mono = _pick(root, ["Cascadia Code", "Cascadia Mono", "JetBrains Mono",
                        "Consolas", "Courier New"], "TkFixedFont")

    _fonts.update({
        "ui": tkfont.Font(family=ui, size=10),
        "ui_bold": tkfont.Font(family=ui, size=10, weight="bold"),
        "small": tkfont.Font(family=ui, size=9),
        "small_bold": tkfont.Font(family=ui, size=9, weight="bold"),
        "tiny": tkfont.Font(family=ui, size=8),
        "h1": tkfont.Font(family=ui, size=19, weight="bold"),
        "h2": tkfont.Font(family=ui, size=13, weight="bold"),
        "h3": tkfont.Font(family=ui, size=11, weight="bold"),
        "logo": tkfont.Font(family=ui, size=16, weight="bold"),
        "code": tkfont.Font(family=mono, size=11),
        "code_small": tkfont.Font(family=mono, size=10),
        "code_bold": tkfont.Font(family=mono, size=11, weight="bold"),
    })
    return _fonts


def fonts() -> dict[str, tkfont.Font]:
    return _fonts


def apply_ttk_theme(root: tk.Misc) -> None:
    f = fonts()
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    style.configure(".", background=BG, foreground=TEXT, font=f["ui"],
                    borderwidth=0, focuscolor=BG)

    style.configure("TFrame", background=BG)
    style.configure("Panel.TFrame", background=PANEL)
    style.configure("Elev.TFrame", background=ELEV)
    style.configure("TLabel", background=BG, foreground=TEXT, font=f["ui"])
    style.configure("Muted.TLabel", background=BG, foreground=MUTED, font=f["small"])

    # thin, flat scrollbars
    for orient in ("Vertical", "Horizontal"):
        style.configure(f"{orient}.TScrollbar", background=BORDER, troughcolor=BG,
                        bordercolor=BG, arrowcolor=MUTED, gripcount=0,
                        darkcolor=BORDER, lightcolor=BORDER, arrowsize=11)
        style.map(f"{orient}.TScrollbar",
                  background=[("active", FAINT), ("pressed", ACCENT)])

    style.configure("TPanedwindow", background=BG)
    style.configure("Sash", sashthickness=6, gripcount=0)

    style.configure("TCombobox", fieldbackground=ELEV, background=ELEV,
                    foreground=TEXT, arrowcolor=MUTED, bordercolor=BORDER,
                    lightcolor=ELEV, darkcolor=ELEV, selectbackground=ELEV,
                    selectforeground=TEXT, padding=5)
    style.map("TCombobox", fieldbackground=[("readonly", ELEV)],
              background=[("readonly", ELEV)])
    root.option_add("*TCombobox*Listbox.background", ELEV)
    root.option_add("*TCombobox*Listbox.foreground", TEXT)
    root.option_add("*TCombobox*Listbox.selectBackground", ACCENT)
    root.option_add("*TCombobox*Listbox.selectForeground", "#ffffff")
    root.option_add("*TCombobox*Listbox.font", f["ui"])

    style.configure("TProgressbar", background=ACCENT, troughcolor=ELEV,
                    bordercolor=ELEV, lightcolor=ACCENT, darkcolor=ACCENT,
                    thickness=6)
    style.configure("Green.Horizontal.TProgressbar", background=GREEN,
                    troughcolor=ELEV, bordercolor=ELEV,
                    lightcolor=GREEN, darkcolor=GREEN, thickness=6)

    style.configure("TSeparator", background=BORDER)


# --------------------------------------------------------------------------
# small widget helpers (flat "modern" look, no external deps)
# --------------------------------------------------------------------------
class Button(tk.Label):
    """Flat clickable pill. Variants: primary / ghost / success / danger / soft."""

    VARIANTS = {
        "primary": (ACCENT, "#ffffff", ACCENT_HOVER),
        "success": (GREEN, "#06241a", "#5ae8ad"),
        "danger": (RED, "#2b0f0f", "#ff8585"),
        "soft": (ELEV2, TEXT, "#2e3646"),
        "ghost": (PANEL, MUTED, ELEV2),
    }

    def __init__(self, master, text: str, command=None, variant: str = "soft",
                 padx: int = 14, pady: int = 7, font_key: str = "small_bold", **kw):
        bg, fg, hover = self.VARIANTS.get(variant, self.VARIANTS["soft"])
        self._bg, self._fg, self._hover = bg, fg, hover
        self._command = command
        self._enabled = True
        super().__init__(master, text=text, bg=bg, fg=fg, padx=padx, pady=pady,
                         font=fonts()[font_key], cursor="hand2", **kw)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)

    def _on_enter(self, _=None):
        if self._enabled:
            self.configure(bg=self._hover)

    def _on_leave(self, _=None):
        if self._enabled:
            self.configure(bg=self._bg)

    def _on_click(self, _=None):
        if self._enabled and self._command:
            self._command()

    def set_command(self, command):
        self._command = command

    def set_enabled(self, value: bool):
        self._enabled = value
        if value:
            self.configure(cursor="hand2", bg=self._bg, fg=self._fg)
        else:
            self.configure(cursor="arrow", bg=PANEL, fg=FAINT)


class FlagButton(tk.Frame):
    """Language switch. Draws the flags itself on a Canvas, because Windows
    does not render regional-indicator flag emoji as actual flags."""

    def __init__(self, master, get_lang, command, bg: str = PANEL):
        super().__init__(master, bg=bg, cursor="hand2")
        self.get_lang = get_lang
        self.command = command
        self._bg = bg

        self.canvas = tk.Canvas(self, width=26, height=17, bg=bg,
                                highlightthickness=0, bd=0)
        self.canvas.pack(side="left")
        self.label = tk.Label(self, text="", bg=bg, fg=MUTED, font=fonts()["tiny"],
                              padx=5)
        self.label.pack(side="left")

        for widget in (self, self.canvas, self.label):
            widget.bind("<Button-1>", lambda e: self.command())
            widget.bind("<Enter>", lambda e: self._hover(True))
            widget.bind("<Leave>", lambda e: self._hover(False))
        self.refresh()

    def _hover(self, entering: bool):
        color = ELEV2 if entering else self._bg
        self.configure(bg=color)
        self.canvas.configure(bg=color)
        self.label.configure(bg=color, fg=TEXT if entering else MUTED)

    def refresh(self):
        """Show the flag of the language clicking would switch TO."""
        target = "de" if self.get_lang() == "en" else "en"
        self.canvas.delete("all")
        if target == "de":
            self._draw_german()
            self.label.configure(text="DE")
        else:
            self._draw_uk()
            self.label.configure(text="EN")

    def _draw_german(self):
        c, w, h = self.canvas, 24, 15
        x, y = 1, 1
        c.create_rectangle(x, y, x + w, y + h / 3, fill="#000000", outline="")
        c.create_rectangle(x, y + h / 3, x + w, y + 2 * h / 3, fill="#DD0000", outline="")
        c.create_rectangle(x, y + 2 * h / 3, x + w, y + h, fill="#FFCE00", outline="")
        c.create_rectangle(x, y, x + w, y + h, outline=BORDER)

    def _draw_uk(self):
        c, w, h = self.canvas, 24, 15
        x, y = 1, 1
        c.create_rectangle(x, y, x + w, y + h, fill="#012169", outline="")
        # white diagonals, then red diagonals on top
        for width, color in ((4, "#FFFFFF"), (2, "#C8102E")):
            c.create_line(x, y, x + w, y + h, fill=color, width=width)
            c.create_line(x + w, y, x, y + h, fill=color, width=width)
        # white cross, then red cross
        for width, color in ((6, "#FFFFFF"), (3, "#C8102E")):
            c.create_line(x + w / 2, y, x + w / 2, y + h, fill=color, width=width)
            c.create_line(x, y + h / 2, x + w, y + h / 2, fill=color, width=width)
        c.create_rectangle(x, y, x + w, y + h, outline=BORDER)


def hline(master, color: str = BORDER, bg: str | None = None) -> tk.Frame:
    return tk.Frame(master, height=1, bg=color, bd=0, highlightthickness=0)


def card(master, bg: str = PANEL, **kw) -> tk.Frame:
    """A flat surface with a hairline border."""
    outer = tk.Frame(master, bg=BORDER, bd=0, highlightthickness=0, **kw)
    inner = tk.Frame(outer, bg=bg, bd=0, highlightthickness=0)
    inner.pack(fill="both", expand=True, padx=1, pady=1)
    outer.inner = inner  # type: ignore[attr-defined]
    return outer


def scrolled_frame(master, bg: str = BG):
    """Returns (container, inner_frame) with a vertical scrollbar + mousewheel."""
    container = tk.Frame(master, bg=bg)
    canvas = tk.Canvas(container, bg=bg, highlightthickness=0, bd=0)
    vbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    inner = tk.Frame(canvas, bg=bg)

    window = canvas.create_window((0, 0), window=inner, anchor="nw")
    canvas.configure(yscrollcommand=vbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    vbar.pack(side="right", fill="y")

    def _on_configure(_=None):
        canvas.configure(scrollregion=canvas.bbox("all"))
    inner.bind("<Configure>", _on_configure)
    canvas.bind("<Configure>", lambda e: canvas.itemconfigure(window, width=e.width))

    def _wheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _bind(_=None):
        canvas.bind_all("<MouseWheel>", _wheel)

    def _unbind(_=None):
        canvas.unbind_all("<MouseWheel>")

    for w in (canvas, inner):
        w.bind("<Enter>", _bind)
        w.bind("<Leave>", _unbind)

    return container, inner
