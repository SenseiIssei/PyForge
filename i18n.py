"""Language handling for PyForge.

The app ships in English and German. English is the source of truth: every
lesson, drill and problem is authored in English, and the German version lives
in a parallel dict (lessons_de.py / problems_de.py, and inline for the drills,
which have to interpolate their random values into both languages).

Internally everything stays English — topic names are dict keys in progress.json
and difficulty strings drive the XP table, so those are translated only at the
moment they are drawn.
"""
from __future__ import annotations

LANG = "en"
LANGUAGES = ("en", "de")


def set_language(lang: str) -> None:
    global LANG
    LANG = lang if lang in LANGUAGES else "en"


def is_de() -> bool:
    return LANG == "de"


def pick(en, de):
    """Return whichever of the two matches the current language."""
    return de if LANG == "de" and de is not None else en


# ===========================================================================
#  UI strings  —  key: (english, german)
# ===========================================================================
UI: dict[str, tuple[str, str]] = {
    # ---------------------------------------------------------------- shell
    "app.tagline": ("Learn to code, then pass the interview",
                    "Programmieren lernen, Interview bestehen"),
    "nav.learn": ("Learn", "Lernen"),
    "nav.learn.sub": ("Read, run, then solve", "Lesen, ausführen, lösen"),
    "nav.practice": ("Practice", "Üben"),
    "nav.practice.sub": ("Endless random drills", "Endlose Zufallsübungen"),
    "nav.interview": ("Interview", "Interview"),
    "nav.interview.sub": ("Codility + LeetCode bank", "Codility- und LeetCode-Sammlung"),
    "nav.playground": ("Playground", "Spielwiese"),
    "nav.playground.sub": ("Scratch editor", "Freier Editor"),
    "nav.progress": ("Progress", "Fortschritt"),
    "nav.progress.sub": ("XP, streaks, stats", "XP, Serien, Statistik"),
    "shell.level": ("Level {n}", "Level {n}"),
    "shell.xp": ("{xp} XP  ·  {left} to next level",
                 "{xp} XP  ·  noch {left} bis Level-up"),
    "shell.gained": ("+{n} XP", "+{n} XP"),
    "shell.shortcuts": ("Ctrl+Enter runs · Ctrl+1..5 switches tab",
                        "Strg+Enter führt aus · Strg+1..5 wechselt den Tab"),
    "shell.lang_hint": ("Switch the whole app to German",
                        "Die ganze App auf Englisch umstellen"),

    # ---------------------------------------------------------------- learn
    "learn.curriculum": ("CURRICULUM", "LEHRPLAN"),
    "learn.done": ("{done} / {total} lessons done",
                   "{done} / {total} Lektionen geschafft"),
    "learn.tab.theory": ("1 · Read & experiment", "1 · Lesen & ausprobieren"),
    "learn.tab.task": ("2 · Exercise", "2 · Übung"),
    "learn.next": ("Next lesson  →", "Nächste Lektion  →"),
    "learn.prev": ("←  Previous", "←  Zurück"),
    "learn.theory": ("THEORY", "THEORIE"),
    "learn.example": ("LIVE EXAMPLE — change it, break it, re-run it",
                      "LIVE-BEISPIEL — ändere es, mach es kaputt, führ es neu aus"),
    "learn.run_example": ("▶  Run example   (Ctrl+Enter)",
                          "▶  Beispiel ausführen   (Strg+Enter)"),
    "learn.reset_example": ("Reset example", "Beispiel zurücksetzen"),
    "learn.to_exercise": ("Go to exercise  →", "Zur Übung  →"),
    "learn.press_run": ("Press Ctrl+Enter (or the Run button) to execute this example.",
                        "Drücke Strg+Enter (oder den Ausführen-Knopf), um dieses "
                        "Beispiel laufen zu lassen."),
    "learn.position": ("{section}  ·  lesson {index} of {total}",
                       "{section}  ·  Lektion {index} von {total}"),

    # ------------------------------------------------------------- practice
    "practice.topic": ("Topic", "Thema"),
    "practice.level": ("Level", "Stufe"),
    "practice.new": ("⟳  New random task", "⟳  Neue Zufallsaufgabe"),
    "practice.another": ("Another one", "Noch eine"),
    "practice.blurb": ("Every task is generated fresh — new numbers, new words, "
                       "new tests. Grind the same topic until it is boring.",
                       "Jede Aufgabe wird neu erzeugt — neue Zahlen, neue Wörter, "
                       "neue Tests. Übe dasselbe Thema, bis es langweilig wird."),
    "practice.stats": ("drills solved: {solved}   ·   day streak: {streak}",
                       "gelöste Übungen: {solved}   ·   Tagesserie: {streak}"),

    # ------------------------------------------------------------ interview
    "interview.bank": ("PROBLEM BANK", "AUFGABENSAMMLUNG"),
    "interview.solved": ("{solved} / {shown} solved   ({total} total)",
                         "{solved} / {shown} gelöst   ({total} insgesamt)"),
    "interview.search": ("search problems…", "Aufgaben suchen…"),
    "interview.random": ("🎲  Random problem", "🎲  Zufällige Aufgabe"),
    "interview.next": ("Random next", "Nächste zufällig"),

    # ----------------------------------------------------------- playground
    "play.title": ("Playground", "Spielwiese"),
    "play.sub": ("A real Python process. Endless loops get killed after 10 "
                 "seconds, so experiment freely.",
                 "Ein echter Python-Prozess. Endlosschleifen werden nach 10 "
                 "Sekunden beendet — probier also ruhig alles aus."),
    "play.run": ("▶  Run   (Ctrl+Enter)", "▶  Ausführen   (Strg+Enter)"),
    "play.clear_out": ("Clear output", "Ausgabe leeren"),
    "play.clear_editor": ("Clear editor", "Editor leeren"),
    "play.stdin": ("INPUT (stdin)", "EINGABE (stdin)"),
    "play.stdin_hint": ("Whatever you type here is piped into your program, so "
                        "input() and sys.stdin.read() work exactly as they do "
                        "on Codility.",
                        "Was du hier eintippst, wird in dein Programm geleitet. "
                        "input() und sys.stdin.read() funktionieren also genau "
                        "wie bei Codility."),
    "play.no_output": ("(no output)", "(keine Ausgabe)"),

    # ------------------------------------------------------------- progress
    "prog.title": ("Your progress", "Dein Fortschritt"),
    "prog.sub": ("Everything is stored locally in progress.json next to the app.",
                 "Alles wird lokal in progress.json neben der App gespeichert."),
    "prog.level": ("LEVEL", "LEVEL"),
    "prog.level.sub": ("{into}/{need} xp to next", "{into}/{need} XP bis Level-up"),
    "prog.xp": ("TOTAL XP", "XP GESAMT"),
    "prog.xp.sub": ("keep going", "weiter so"),
    "prog.streak": ("DAY STREAK", "TAGESSERIE"),
    "prog.streak.sub": ("best {best}", "Rekord {best}"),
    "prog.lessons": ("LESSONS", "LEKTIONEN"),
    "prog.lessons.sub": ("curriculum", "Lehrplan"),
    "prog.problems": ("PROBLEMS", "AUFGABEN"),
    "prog.problems.sub": ("interview bank", "Interview-Sammlung"),
    "prog.drills": ("DRILLS", "ÜBUNGEN"),
    "prog.drills.sub": ("randomised", "zufällig erzeugt"),
    "prog.by_topic": ("SOLVED BY TOPIC", "GELÖST NACH THEMA"),
    "prog.nothing": ("Nothing solved yet — go break something in Learn.",
                     "Noch nichts gelöst — geh und mach im Lern-Tab etwas kaputt."),
    "prog.last14": ("LAST 14 DAYS", "LETZTE 14 TAGE"),
    "prog.no_activity": ("No activity recorded yet.", "Noch keine Aktivität erfasst."),
    "prog.recent": ("RECENTLY SOLVED", "ZULETZT GELÖST"),
    "prog.reset": ("Reset all progress", "Fortschritt zurücksetzen"),
    "prog.reset_note": ("   (this cannot be undone)",
                        "   (das lässt sich nicht rückgängig machen)"),
    "prog.reset_title": ("Reset progress", "Fortschritt zurücksetzen"),
    "prog.reset_ask": ("Delete all XP, streaks and solved marks?",
                       "Alle XP, Serien und Lösungshaken löschen?"),
    "prog.reset_yes": ("Yes, wipe it", "Ja, alles löschen"),
    "prog.reset_no": ("Cancel", "Abbrechen"),
    "prog.kind.lesson": ("lesson", "Lektion"),
    "prog.kind.interview": ("interview", "Interview"),
    "prog.kind.drill": ("drill", "Übung"),

    # ------------------------------------------------------------- taskview
    "task.header": ("TASK", "AUFGABE"),
    "task.solved_pill": ("✓ SOLVED", "✓ GELÖST"),
    "task.complexity": ("Target complexity: {value}",
                        "Ziel-Komplexität: {value}"),
    "task.examples": ("Example tests", "Beispieltests"),
    "task.hidden_note": ("\n+ {n} hidden test(s) run when you submit.\n",
                         "\n+ {n} versteckte Test(s) laufen beim Absenden mit.\n"),
    "task.loaded": ("{n} test cases loaded  ({shown} shown, {hidden} hidden).",
                    "{n} Testfälle geladen  ({shown} sichtbar, {hidden} versteckt)."),
    "task.write": ("Write your function, then press Ctrl+Enter.",
                   "Schreib deine Funktion und drücke dann Strg+Enter."),
    "task.run_tests": ("▶  Run tests   (Ctrl+Enter)", "▶  Tests starten   (Strg+Enter)"),
    "task.running": ("Running…", "Läuft…"),
    "task.run_code": ("Run code", "Code ausführen"),
    "task.hint": ("Hint", "Tipp"),
    "task.hint_n": ("Hint ({i}/{total})", "Tipp ({i}/{total})"),
    "task.hint_line": ("\nHint {i}: {text}\n", "\nTipp {i}: {text}\n"),
    "task.no_hints": ("No hints for this one — you've got it.",
                      "Für diese Aufgabe gibt es keine Tipps — du schaffst das."),
    "task.last_hint": ("That was the last hint.", "Das war der letzte Tipp."),
    "task.solution": ("Solution", "Lösung"),
    "task.load_solution": ("Load into editor", "In den Editor laden"),
    "task.solution_intro": ("Reference solution — read it, then close it and type "
                            "it yourself from memory:",
                            "Musterlösung — lies sie, schließ sie und tipp sie dann "
                            "aus dem Kopf selbst:"),
    "task.no_solution": ("(no solution recorded)", "(keine Lösung hinterlegt)"),
    "task.solution_loaded": ("\nLoaded into the editor. Run it, then reset and redo "
                             "it yourself.",
                             "\nIn den Editor geladen. Führ sie aus, setz dann zurück "
                             "und mach es selbst noch einmal."),
    "task.reset": ("Reset", "Zurücksetzen"),
    "task.script_run": ("Running your code as a script…",
                        "Dein Code läuft als Skript…"),
    "task.timeout_10": ("Timed out after 10s — is there an endless loop?",
                        "Nach 10 s abgebrochen — steckt da eine Endlosschleife drin?"),
    "task.no_prints": ("(no output — your code defines things but prints nothing, "
                       "which is fine)",
                       "(keine Ausgabe — dein Code definiert nur etwas und gibt "
                       "nichts aus, das ist völlig in Ordnung)"),
    "task.finished_ms": ("\nFinished in {ms} ms", "\nFertig in {ms} ms"),
    "task.running_tests": ("Running tests…", "Tests laufen…"),
    "task.timeout_big": ("⏱  TIMEOUT — your code ran for over 10 seconds.",
                         "⏱  ZEITÜBERSCHREITUNG — dein Code lief über 10 Sekunden."),
    "task.timeout_why": ("Either there is an endless loop, or the algorithm is too "
                         "slow for the big hidden test.",
                         "Entweder steckt da eine Endlosschleife drin, oder der "
                         "Algorithmus ist für den großen versteckten Test zu langsam."),
    "task.status_timeout": ("Timed out", "Zeit überschritten"),
    "task.crash_intro": ("💥  Your code raised an error before the tests could run:\n",
                         "💥  Dein Code hat einen Fehler ausgelöst, bevor die Tests "
                         "starten konnten:\n"),
    "task.crash_line": ("\n→ look at line {line} in the editor (highlighted).",
                        "\n→ schau dir Zeile {line} im Editor an (hervorgehoben)."),
    "task.status_crash": ("Error before testing", "Fehler vor dem Test"),
    "task.your_prints": ("Your prints:", "Deine Ausgaben:"),
    "task.pass": ("PASS", "OK"),
    "task.fail": ("FAIL", "FEHL"),
    "task.hidden_test": ("hidden test", "versteckter Test"),
    "task.test": ("test", "Test"),
    "task.hidden_input": ("        (hidden input)", "        (versteckte Eingabe)"),
    "task.input": ("        input:    {value}", "        Eingabe:   {value}"),
    "task.crashed": ("        crashed:  {value}", "        Absturz:   {value}"),
    "task.expected": ("        expected: {value}", "        erwartet:  {value}"),
    "task.got": ("        got:      {value}", "        bekommen:  {value}"),
    "task.checker_fail": ("        the object your function returned did not behave "
                          "as specified",
                          "        das von deiner Funktion zurückgegebene Objekt hat "
                          "sich nicht wie verlangt verhalten"),
    "task.all_passed": ("✓  ALL {n} TESTS PASSED   ({ms} ms)",
                        "✓  ALLE {n} TESTS BESTANDEN   ({ms} ms)"),
    "task.complexity_check": ("   Target complexity was {value} — is that what you "
                              "wrote?",
                              "   Die Ziel-Komplexität war {value} — hast du das "
                              "auch geschrieben?"),
    "task.status_solved": ("Solved!", "Gelöst!"),
    "task.some_passed": ("✗  {passed} of {total} tests passed.",
                         "✗  {passed} von {total} Tests bestanden."),
    "task.status_passing": ("{passed}/{total} passing", "{passed}/{total} bestanden"),

    # ------------------------------------------------------------ diagnoses
    "diag.none": ("A 'NoneType' error usually means a missing `return`.",
                  "Ein 'NoneType'-Fehler heißt meistens: da fehlt ein `return`."),
    "diag.index": ("IndexError: check your loop bounds and the empty-input case.",
                   "IndexError: prüf deine Schleifengrenzen und den Fall der "
                   "leeren Eingabe."),
    "diag.key": ("KeyError: use dict.get(key, default) instead of dict[key].",
                 "KeyError: nimm dict.get(key, default) statt dict[key]."),
    "diag.type": ("TypeError: check the types you are mixing (int vs str vs None).",
                  "TypeError: schau nach, welche Typen du mischst (int, str, None)."),
    "diag.zero": ("Guard the empty / zero case before dividing.",
                  "Fang den leeren bzw. Null-Fall ab, bevor du teilst."),
    "diag.crash": ("Fix the crash first, then re-run.",
                   "Behebe erst den Absturz, dann noch mal ausführen."),
    "diag.empty": ("The empty input is failing — handle it explicitly at the top.",
                   "Die leere Eingabe schlägt fehl — behandle sie gleich am Anfang."),
    "diag.all_none": ("Everything returns None — did you forget to `return` the "
                      "result?",
                      "Alles liefert None — hast du vergessen, das Ergebnis mit "
                      "`return` zurückzugeben?"),

    # ---------------------------------------------------- programming language
    "lang.section": ("LANGUAGE", "SPRACHE"),
    "lang.ready": ("ready", "bereit"),
    "lang.missing": ("not installed", "nicht installiert"),
    "lang.bundled": ("built in", "eingebaut"),
    "lang.detect": ("Re-check toolchains", "Toolchains neu prüfen"),
    "lang.missing_title": ("{label} is not installed", "{label} ist nicht installiert"),
    "lang.missing_body": ("CodeForge runs your code with the real {label} toolchain, "
                          "and it could not find it on this machine.\n\n{hint}\n\n"
                          "Once it is installed, press “{button}”.",
                          "CodeForge führt deinen Code mit der echten "
                          "{label}-Toolchain aus und hat sie auf diesem Rechner "
                          "nicht gefunden.\n\n{hint}\n\nWenn sie installiert ist, "
                          "drück auf „{button}“."),
    "lang.python_only_title": ("Only available for Python so far",
                               "Bisher nur für Python verfügbar"),
    "lang.python_only_body": ("This part of CodeForge — the {area} — is written for "
                              "Python at the moment. The Interview tab already works "
                              "in {label}, with the same problems and generated "
                              "starter code.\n\nSwitch the language back to Python to "
                              "use this tab.",
                              "Dieser Teil von CodeForge — {area} — gibt es zurzeit "
                              "nur für Python. Der Interview-Tab funktioniert in "
                              "{label} bereits, mit denselben Aufgaben und erzeugtem "
                              "Startcode.\n\nStell die Sprache auf Python zurück, um "
                              "diesen Tab zu nutzen."),
    "lang.area_curriculum": ("lesson curriculum", "der Lehrplan"),
    "lang.area_drills": ("randomised drills", "die Zufallsübungen"),
    "lang.area_playground": ("playground", "die Spielwiese"),
    "lang.build_failed": ("🔨  It did not compile:", "🔨  Es lässt sich nicht übersetzen:"),
    "lang.compiled_in": ("compiled and ran in {ms} ms", "übersetzt und ausgeführt in {ms} ms"),

    # --------------------------------------------------------------- shared
    "common.all_topics": ("All topics", "Alle Themen"),
    "common.any": ("Any", "Beliebig"),
    "common.timed_out": ("⏱  Timed out after 10 seconds.",
                         "⏱  Nach 10 Sekunden abgebrochen."),
    "common.running": ("Running…", "Läuft…"),
    "common.finished": ("\n[finished in {ms} ms]", "\n[fertig in {ms} ms]"),
}


def t(key: str, **kw) -> str:
    entry = UI.get(key)
    if entry is None:
        return key
    text = entry[1] if LANG == "de" else entry[0]
    return text.format(**kw) if kw else text


# ===========================================================================
#  Topics, difficulties, complexity notes
# ===========================================================================
TOPIC_DE = {
    "General": "Allgemein",
    "Basics": "Grundlagen",
    "Strings": "Zeichenketten",
    "Lists": "Listen",
    "Sets": "Mengen",
    "Sorting": "Sortieren",
    "Hash map": "Hash-Map",
    "Prefix sums": "Präfixsummen",
    "Two pointers": "Zwei Zeiger",
    "Sliding window": "Schiebefenster",
    "Matrix": "Matrix",
    "Bit tricks": "Bit-Tricks",
    "Errors": "Fehler",
    "Arrays": "Arrays",
    "Math": "Mathe",
    "Stack": "Stapel",
    "Counting": "Zählen",
    "Greedy": "Greedy",
    "Dynamic programming": "Dynamische Programmierung",
    "Binary search": "Binäre Suche",
    "Graphs": "Graphen",
    "Recursion": "Rekursion",
    "Functions": "Funktionen",
    "OOP": "Objektorientierung",
    "Debugging": "Fehlersuche",
}

DIFF_DE = {"Easy": "Leicht", "Medium": "Mittel", "Hard": "Schwer"}

_COMPLEXITY_DE = [
    (" time, ", " Zeit, "),
    (" space", " Speicher"),
    (", one pass", ", ein Durchlauf"),
    ("O(total characters)", "O(Zeichen insgesamt)"),
    ("O(rows * cols)", "O(Zeilen * Spalten)"),
    ("O(amount * len(coins))", "O(Betrag * Anzahl Münzsorten)"),
    ("O(n) with a set / O(n log n) sorted",
     "O(n) mit einem Set / O(n log n) mit Sortieren"),
    ("O(n log k) with a heap", "O(n log k) mit einem Heap"),
    ("O(n log n) — O(n) with bucket sort",
     "O(n log n) — O(n) mit Bucket-Sort"),
    ("O(n) with a set", "O(n) mit einem Set"),
    ("O(n + m)", "O(n + m)"),
    ("O(n * k log k)", "O(n * k log k)"),
    ("O(sqrt n)", "O(Wurzel n)"),
    ("O(n) extra", "O(n) zusätzlich"),
    ("O(1) extra", "O(1) zusätzlich"),
]


def topic(name: str) -> str:
    return TOPIC_DE.get(name, name) if LANG == "de" else name


def difficulty(name: str) -> str:
    return DIFF_DE.get(name, name) if LANG == "de" else name


def complexity(text: str) -> str:
    if LANG != "de" or not text:
        return text
    out = text
    for src, dst in _COMPLEXITY_DE:
        out = out.replace(src, dst)
    return out


def topic_choices(topics: list[str]) -> tuple[list[str], list[str]]:
    """(internal values, displayed values) with 'All topics' in front."""
    values = ["All topics"] + list(topics)
    labels = [t("common.all_topics")] + [topic(x) for x in topics]
    return values, labels


def difficulty_choices(levels: list[str]) -> tuple[list[str], list[str]]:
    values = ["Any"] + list(levels)
    labels = [t("common.any")] + [difficulty(x) for x in levels]
    return values, labels


# ===========================================================================
#  Content localisation
# ===========================================================================
def localize_task(task, table: dict | None):
    """Return `task` with its German title/statement/hints/notes swapped in.

    `table` is the German entry for this task (or None). The task object is
    mutated in place — every caller builds a fresh Task first.
    """
    if LANG != "de" or not table:
        return task
    task.title = table.get("title", task.title)
    task.statement = table.get("statement", task.statement)
    if table.get("hints"):
        task.hints = list(table["hints"])
    if table.get("notes"):
        task.notes = table["notes"]
    if table.get("starter"):
        task.starter = table["starter"]
    if table.get("solution"):
        task.solution = table["solution"]
    task.complexity = complexity(task.complexity)
    return task
