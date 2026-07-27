"""Interface languages for CodeForge.

English is the source of truth. Every other language may be partial — `pick()`
and `t()` fall back to English for anything missing, so an unfinished
translation degrades into a readable app instead of a broken one.

Internally everything stays English: topic names are dict keys in progress.json
and difficulty strings drive the XP table, so those are translated only at the
moment they are drawn.
"""
from __future__ import annotations

LANG = "en"
LANGUAGES = ("en", "de", "fr", "es")
LANGUAGE_NAMES = {
    "en": "English",
    "de": "Deutsch",
    "fr": "Français",
    "es": "Español",
}


def set_language(lang: str) -> str:
    global LANG
    LANG = lang if lang in LANGUAGES else "en"
    return LANG


def is_de() -> bool:
    return LANG == "de"


def pick(table, fallback=""):
    """Take the active language out of a {lang: value} mapping, else English."""
    if not isinstance(table, dict):
        return table if table is not None else fallback
    value = table.get(LANG)
    if value:
        return value
    return table.get("en", fallback)


# ===========================================================================
#  UI strings
# ===========================================================================
UI: dict[str, dict[str, str]] = {
    # ---------------------------------------------------------------- shell
    "app.tagline": {
        "en": "Learn to code, then pass the interview",
        "de": "Programmieren lernen, Interview bestehen",
        "fr": "Apprendre à coder, puis réussir l'entretien",
        "es": "Aprende a programar y aprueba la entrevista"},
    "nav.learn": {"en": "Learn", "de": "Lernen", "fr": "Apprendre", "es": "Aprender"},
    "nav.learn.sub": {
        "en": "Read, run, then solve", "de": "Lesen, ausführen, lösen",
        "fr": "Lire, exécuter, résoudre", "es": "Leer, ejecutar, resolver"},
    "nav.practice": {"en": "Practice", "de": "Üben", "fr": "S'entraîner",
                     "es": "Practicar"},
    "nav.practice.sub": {
        "en": "Endless random drills", "de": "Endlose Zufallsübungen",
        "fr": "Exercices aléatoires sans fin", "es": "Ejercicios aleatorios sin fin"},
    "nav.interview": {"en": "Interview", "de": "Interview", "fr": "Entretien",
                      "es": "Entrevista"},
    "nav.interview.sub": {
        "en": "Codility + LeetCode bank", "de": "Codility- und LeetCode-Sammlung",
        "fr": "Banque Codility et LeetCode", "es": "Colección Codility y LeetCode"},
    "nav.playground": {"en": "Playground", "de": "Spielwiese", "fr": "Bac à sable",
                       "es": "Área de pruebas"},
    "nav.playground.sub": {
        "en": "Scratch editor", "de": "Freier Editor",
        "fr": "Éditeur libre", "es": "Editor libre"},
    "nav.progress": {"en": "Progress", "de": "Fortschritt", "fr": "Progression",
                     "es": "Progreso"},
    "nav.progress.sub": {
        "en": "XP, streaks, stats", "de": "XP, Serien, Statistik",
        "fr": "XP, séries, statistiques", "es": "XP, rachas, estadísticas"},
    "shell.level": {"en": "Level {n}", "de": "Level {n}", "fr": "Niveau {n}",
                    "es": "Nivel {n}"},
    "shell.xp": {
        "en": "{xp} XP  ·  {left} to next level",
        "de": "{xp} XP  ·  noch {left} bis Level-up",
        "fr": "{xp} XP  ·  {left} avant le niveau suivant",
        "es": "{xp} XP  ·  {left} para el siguiente nivel"},
    "shell.gained": {"en": "+{n} XP", "de": "+{n} XP", "fr": "+{n} XP", "es": "+{n} XP"},
    "shell.shortcuts": {
        "en": "Ctrl+Enter runs · Ctrl+1..5 switches tab",
        "de": "Strg+Enter führt aus · Strg+1..5 wechselt den Tab",
        "fr": "Ctrl+Entrée exécute · Ctrl+1..5 change d'onglet",
        "es": "Ctrl+Intro ejecuta · Ctrl+1..5 cambia de pestaña"},
    "shell.lang_hint": {
        "en": "Click the flag to change the language",
        "de": "Klick auf die Flagge, um die Sprache zu wechseln",
        "fr": "Cliquez sur le drapeau pour changer de langue",
        "es": "Haz clic en la bandera para cambiar de idioma"},
    "shell.choose_language": {
        "en": "Interface language", "de": "Sprache der Oberfläche",
        "fr": "Langue de l'interface", "es": "Idioma de la interfaz"},

    # ---------------------------------------------------------------- learn
    "learn.curriculum": {"en": "CURRICULUM", "de": "LEHRPLAN", "fr": "PROGRAMME",
                         "es": "TEMARIO"},
    "learn.done": {
        "en": "{done} / {total} lessons done", "de": "{done} / {total} Lektionen geschafft",
        "fr": "{done} / {total} leçons terminées", "es": "{done} / {total} lecciones hechas"},
    "learn.tab.theory": {
        "en": "1 · Read & experiment", "de": "1 · Lesen & ausprobieren",
        "fr": "1 · Lire et expérimenter", "es": "1 · Leer y experimentar"},
    "learn.tab.task": {"en": "2 · Exercise", "de": "2 · Übung", "fr": "2 · Exercice",
                       "es": "2 · Ejercicio"},
    "learn.next": {"en": "Next lesson  →", "de": "Nächste Lektion  →",
                   "fr": "Leçon suivante  →", "es": "Lección siguiente  →"},
    "learn.prev": {"en": "←  Previous", "de": "←  Zurück", "fr": "←  Précédent",
                   "es": "←  Anterior"},
    "learn.theory": {"en": "THEORY", "de": "THEORIE", "fr": "THÉORIE", "es": "TEORÍA"},
    "learn.example": {
        "en": "LIVE EXAMPLE — change it, break it, re-run it",
        "de": "LIVE-BEISPIEL — ändere es, mach es kaputt, führ es neu aus",
        "fr": "EXEMPLE VIVANT — modifiez-le, cassez-le, relancez-le",
        "es": "EJEMPLO EN VIVO — cámbialo, rómpelo, vuelve a ejecutarlo"},
    "learn.run_example": {
        "en": "▶  Run example   (Ctrl+Enter)", "de": "▶  Beispiel ausführen   (Strg+Enter)",
        "fr": "▶  Exécuter l'exemple   (Ctrl+Entrée)",
        "es": "▶  Ejecutar ejemplo   (Ctrl+Intro)"},
    "learn.reset_example": {
        "en": "Reset example", "de": "Beispiel zurücksetzen",
        "fr": "Réinitialiser l'exemple", "es": "Restablecer ejemplo"},
    "learn.to_exercise": {"en": "Go to exercise  →", "de": "Zur Übung  →",
                          "fr": "Vers l'exercice  →", "es": "Ir al ejercicio  →"},
    "learn.press_run": {
        "en": "Press Ctrl+Enter (or the Run button) to execute this example.",
        "de": "Drücke Strg+Enter (oder den Ausführen-Knopf), um dieses Beispiel "
              "laufen zu lassen.",
        "fr": "Appuyez sur Ctrl+Entrée (ou le bouton Exécuter) pour lancer cet exemple.",
        "es": "Pulsa Ctrl+Intro (o el botón Ejecutar) para lanzar este ejemplo."},
    "learn.position": {
        "en": "{section}  ·  lesson {index} of {total}",
        "de": "{section}  ·  Lektion {index} von {total}",
        "fr": "{section}  ·  leçon {index} sur {total}",
        "es": "{section}  ·  lección {index} de {total}"},

    # ------------------------------------------------------------- practice
    "practice.topic": {"en": "Topic", "de": "Thema", "fr": "Thème", "es": "Tema"},
    "practice.level": {"en": "Level", "de": "Stufe", "fr": "Niveau", "es": "Nivel"},
    "practice.new": {
        "en": "⟳  New random task", "de": "⟳  Neue Zufallsaufgabe",
        "fr": "⟳  Nouvel exercice aléatoire", "es": "⟳  Nuevo ejercicio aleatorio"},
    "practice.another": {"en": "Another one", "de": "Noch eine", "fr": "Encore un",
                         "es": "Otro más"},
    "practice.blurb": {
        "en": "Every task is generated fresh — new numbers, new words, new tests. "
              "Grind the same topic until it is boring.",
        "de": "Jede Aufgabe wird neu erzeugt — neue Zahlen, neue Wörter, neue Tests. "
              "Übe dasselbe Thema, bis es langweilig wird.",
        "fr": "Chaque exercice est généré à neuf — nouveaux nombres, nouveaux mots, "
              "nouveaux tests. Travaillez le même thème jusqu'à l'ennui.",
        "es": "Cada ejercicio se genera de nuevo — nuevos números, nuevas palabras, "
              "nuevas pruebas. Repite el mismo tema hasta que aburra."},
    "practice.stats": {
        "en": "drills solved: {solved}   ·   day streak: {streak}",
        "de": "gelöste Übungen: {solved}   ·   Tagesserie: {streak}",
        "fr": "exercices résolus : {solved}   ·   série de jours : {streak}",
        "es": "ejercicios resueltos: {solved}   ·   racha de días: {streak}"},

    # ------------------------------------------------------------ interview
    "interview.bank": {"en": "PROBLEM BANK", "de": "AUFGABENSAMMLUNG",
                       "fr": "BANQUE D'EXERCICES", "es": "COLECCIÓN DE PROBLEMAS"},
    "interview.solved": {
        "en": "{solved} / {shown} solved   ({total} total)",
        "de": "{solved} / {shown} gelöst   ({total} insgesamt)",
        "fr": "{solved} / {shown} résolus   ({total} au total)",
        "es": "{solved} / {shown} resueltos   ({total} en total)"},
    "interview.search": {"en": "search problems…", "de": "Aufgaben suchen…",
                         "fr": "rechercher des exercices…", "es": "buscar problemas…"},
    "interview.random": {
        "en": "🎲  Random problem", "de": "🎲  Zufällige Aufgabe",
        "fr": "🎲  Exercice au hasard", "es": "🎲  Problema al azar"},
    # Kept short on purpose: this sits in a crowded action row next to four
    # other buttons, and the longer wordings clipped in French and German.
    "interview.next": {"en": "Random next", "de": "Nächste", "fr": "Au hasard",
                       "es": "Al azar"},

    # ----------------------------------------------------------- playground
    "play.title": {"en": "Playground", "de": "Spielwiese", "fr": "Bac à sable",
                   "es": "Área de pruebas"},
    "play.sub": {
        "en": "A real {label} program, compiled and run by the real toolchain. "
              "Endless loops get killed, so experiment freely.",
        "de": "Ein echtes {label}-Programm, von der echten Toolchain übersetzt und "
              "ausgeführt. Endlosschleifen werden beendet — probier ruhig alles aus.",
        "fr": "Un vrai programme {label}, compilé et exécuté par la vraie chaîne "
              "d'outils. Les boucles infinies sont arrêtées, expérimentez librement.",
        "es": "Un programa {label} de verdad, compilado y ejecutado por las "
              "herramientas reales. Los bucles infinitos se detienen; experimenta "
              "con libertad."},
    "play.run": {"en": "▶  Run   (Ctrl+Enter)", "de": "▶  Ausführen   (Strg+Enter)",
                 "fr": "▶  Exécuter   (Ctrl+Entrée)", "es": "▶  Ejecutar   (Ctrl+Intro)"},
    "play.clear_out": {"en": "Clear output", "de": "Ausgabe leeren",
                       "fr": "Vider la sortie", "es": "Limpiar salida"},
    "play.clear_editor": {"en": "Clear editor", "de": "Editor leeren",
                          "fr": "Vider l'éditeur", "es": "Limpiar editor"},
    "play.stdin": {"en": "INPUT (stdin)", "de": "EINGABE (stdin)",
                   "fr": "ENTRÉE (stdin)", "es": "ENTRADA (stdin)"},
    "play.stdin_hint": {
        "en": "Whatever you type here is piped into your program, so input() and "
              "sys.stdin.read() work exactly as they do on Codility.",
        "de": "Was du hier eintippst, wird in dein Programm geleitet. input() und "
              "sys.stdin.read() funktionieren also genau wie bei Codility.",
        "fr": "Ce que vous tapez ici est transmis à votre programme : input() et "
              "sys.stdin.read() se comportent exactement comme chez Codility.",
        "es": "Lo que escribas aquí se envía a tu programa, así que input() y "
              "sys.stdin.read() funcionan igual que en Codility."},
    "play.no_output": {"en": "(no output)", "de": "(keine Ausgabe)",
                       "fr": "(aucune sortie)", "es": "(sin salida)"},

    # ------------------------------------------------------------- progress
    "prog.title": {"en": "Your progress", "de": "Dein Fortschritt",
                   "fr": "Votre progression", "es": "Tu progreso"},
    "prog.sub": {
        "en": "Everything is stored locally in progress.json next to the app.",
        "de": "Alles wird lokal in progress.json neben der App gespeichert.",
        "fr": "Tout est enregistré localement dans progress.json à côté de l'application.",
        "es": "Todo se guarda localmente en progress.json junto a la aplicación."},
    "prog.level": {"en": "LEVEL", "de": "LEVEL", "fr": "NIVEAU", "es": "NIVEL"},
    "prog.level.sub": {
        "en": "{into}/{need} xp to next", "de": "{into}/{need} XP bis Level-up",
        "fr": "{into}/{need} XP avant le suivant",
        "es": "{into}/{need} XP para el siguiente"},
    "prog.xp": {"en": "TOTAL XP", "de": "XP GESAMT", "fr": "XP TOTAL", "es": "XP TOTAL"},
    "prog.xp.sub": {"en": "keep going", "de": "weiter so", "fr": "continuez",
                    "es": "sigue así"},
    "prog.streak": {"en": "DAY STREAK", "de": "TAGESSERIE", "fr": "SÉRIE DE JOURS",
                    "es": "RACHA DE DÍAS"},
    "prog.streak.sub": {"en": "best {best}", "de": "Rekord {best}",
                        "fr": "record {best}", "es": "récord {best}"},
    "prog.lessons": {"en": "LESSONS", "de": "LEKTIONEN", "fr": "LEÇONS",
                     "es": "LECCIONES"},
    "prog.lessons.sub": {"en": "curriculum", "de": "Lehrplan", "fr": "programme",
                         "es": "temario"},
    "prog.problems": {"en": "PROBLEMS", "de": "AUFGABEN", "fr": "EXERCICES",
                      "es": "PROBLEMAS"},
    "prog.problems.sub": {"en": "interview bank", "de": "Interview-Sammlung",
                          "fr": "banque d'entretien", "es": "colección de entrevista"},
    "prog.drills": {"en": "DRILLS", "de": "ÜBUNGEN", "fr": "EXERCICES",
                    "es": "PRÁCTICAS"},
    "prog.drills.sub": {"en": "randomised", "de": "zufällig erzeugt",
                        "fr": "générés au hasard", "es": "generados al azar"},
    "prog.by_topic": {"en": "SOLVED BY TOPIC", "de": "GELÖST NACH THEMA",
                      "fr": "RÉSOLUS PAR THÈME", "es": "RESUELTOS POR TEMA"},
    "prog.nothing": {
        "en": "Nothing solved yet — go break something in Learn.",
        "de": "Noch nichts gelöst — geh und mach im Lern-Tab etwas kaputt.",
        "fr": "Rien de résolu pour l'instant — allez casser quelque chose dans Apprendre.",
        "es": "Nada resuelto todavía — ve a romper algo en Aprender."},
    "prog.last14": {"en": "LAST 14 DAYS", "de": "LETZTE 14 TAGE",
                    "fr": "14 DERNIERS JOURS", "es": "ÚLTIMOS 14 DÍAS"},
    "prog.no_activity": {
        "en": "No activity recorded yet.", "de": "Noch keine Aktivität erfasst.",
        "fr": "Aucune activité enregistrée.", "es": "Aún no hay actividad registrada."},
    "prog.recent": {"en": "RECENTLY SOLVED", "de": "ZULETZT GELÖST",
                    "fr": "RÉSOLUS RÉCEMMENT", "es": "RESUELTOS HACE POCO"},
    "prog.reset": {"en": "Reset all progress", "de": "Fortschritt zurücksetzen",
                   "fr": "Réinitialiser la progression", "es": "Restablecer el progreso"},
    "prog.reset_note": {
        "en": "   (this cannot be undone)",
        "de": "   (das lässt sich nicht rückgängig machen)",
        "fr": "   (action irréversible)", "es": "   (no se puede deshacer)"},
    "prog.reset_title": {"en": "Reset progress", "de": "Fortschritt zurücksetzen",
                         "fr": "Réinitialiser la progression",
                         "es": "Restablecer el progreso"},
    "prog.reset_ask": {
        "en": "Delete all XP, streaks and solved marks?",
        "de": "Alle XP, Serien und Lösungshaken löschen?",
        "fr": "Supprimer tous les XP, séries et exercices résolus ?",
        "es": "¿Borrar todos los XP, rachas y marcas de resueltos?"},
    "prog.reset_yes": {"en": "Yes, wipe it", "de": "Ja, alles löschen",
                       "fr": "Oui, tout effacer", "es": "Sí, borrarlo todo"},
    "prog.reset_no": {"en": "Cancel", "de": "Abbrechen", "fr": "Annuler",
                      "es": "Cancelar"},
    "prog.kind.lesson": {"en": "lesson", "de": "Lektion", "fr": "leçon",
                         "es": "lección"},
    "prog.kind.interview": {"en": "interview", "de": "Interview", "fr": "entretien",
                            "es": "entrevista"},
    "prog.kind.drill": {"en": "drill", "de": "Übung", "fr": "exercice",
                        "es": "práctica"},

    # ------------------------------------------------------------- taskview
    "task.header": {"en": "TASK", "de": "AUFGABE", "fr": "EXERCICE", "es": "EJERCICIO"},
    "task.solved_pill": {"en": "✓ SOLVED", "de": "✓ GELÖST", "fr": "✓ RÉSOLU",
                         "es": "✓ RESUELTO"},
    "task.complexity": {
        "en": "Target complexity: {value}", "de": "Ziel-Komplexität: {value}",
        "fr": "Complexité visée : {value}", "es": "Complejidad objetivo: {value}"},
    "task.examples": {"en": "Example tests", "de": "Beispieltests",
                      "fr": "Tests d'exemple", "es": "Pruebas de ejemplo"},
    "task.hidden_note": {
        "en": "\n+ {n} hidden test(s) run when you submit.\n",
        "de": "\n+ {n} versteckte Test(s) laufen beim Absenden mit.\n",
        "fr": "\n+ {n} test(s) caché(s) s'exécutent à la soumission.\n",
        "es": "\n+ {n} prueba(s) oculta(s) se ejecutan al enviar.\n"},
    "task.loaded": {
        "en": "{n} test cases loaded  ({shown} shown, {hidden} hidden).",
        "de": "{n} Testfälle geladen  ({shown} sichtbar, {hidden} versteckt).",
        "fr": "{n} cas de test chargés  ({shown} visibles, {hidden} cachés).",
        "es": "{n} casos de prueba cargados  ({shown} visibles, {hidden} ocultos)."},
    "task.write": {
        "en": "Write your function, then press Ctrl+Enter.",
        "de": "Schreib deine Funktion und drücke dann Strg+Enter.",
        "fr": "Écrivez votre fonction, puis appuyez sur Ctrl+Entrée.",
        "es": "Escribe tu función y luego pulsa Ctrl+Intro."},
    "task.run_tests": {
        "en": "▶  Run tests   (Ctrl+Enter)", "de": "▶  Tests starten   (Strg+Enter)",
        "fr": "▶  Lancer les tests   (Ctrl+Entrée)",
        "es": "▶  Ejecutar pruebas   (Ctrl+Intro)"},
    "task.running": {"en": "Running…", "de": "Läuft…", "fr": "Exécution…",
                     "es": "Ejecutando…"},
    "task.run_code": {"en": "Run code", "de": "Code ausführen",
                      "fr": "Exécuter le code", "es": "Ejecutar código"},
    "task.hint": {"en": "Hint", "de": "Tipp", "fr": "Indice", "es": "Pista"},
    "task.hint_n": {"en": "Hint ({i}/{total})", "de": "Tipp ({i}/{total})",
                    "fr": "Indice ({i}/{total})", "es": "Pista ({i}/{total})"},
    "task.hint_line": {
        "en": "\nHint {i}: {text}\n", "de": "\nTipp {i}: {text}\n",
        "fr": "\nIndice {i} : {text}\n", "es": "\nPista {i}: {text}\n"},
    "task.no_hints": {
        "en": "No hints for this one — you've got it.",
        "de": "Für diese Aufgabe gibt es keine Tipps — du schaffst das.",
        "fr": "Pas d'indice pour celui-ci — vous y arriverez.",
        "es": "Sin pistas para este — tú puedes."},
    "task.last_hint": {"en": "That was the last hint.", "de": "Das war der letzte Tipp.",
                       "fr": "C'était le dernier indice.",
                       "es": "Esa era la última pista."},
    "task.solution": {"en": "Solution", "de": "Lösung", "fr": "Solution",
                      "es": "Solución"},
    "task.load_solution": {"en": "Load into editor", "de": "In den Editor laden",
                           "fr": "Charger dans l'éditeur", "es": "Cargar en el editor"},
    "task.solution_intro": {
        "en": "Reference solution — read it, then close it and type it yourself "
              "from memory:",
        "de": "Musterlösung — lies sie, schließ sie und tipp sie dann aus dem Kopf "
              "selbst:",
        "fr": "Solution de référence — lisez-la, fermez-la, puis retapez-la de mémoire :",
        "es": "Solución de referencia — léela, ciérrala y escríbela tú de memoria:"},
    "task.no_solution": {"en": "(no solution recorded)",
                         "de": "(keine Lösung hinterlegt)",
                         "fr": "(aucune solution enregistrée)",
                         "es": "(no hay solución registrada)"},
    "task.solution_loaded": {
        "en": "\nLoaded into the editor. Run it, then reset and redo it yourself.",
        "de": "\nIn den Editor geladen. Führ sie aus, setz dann zurück und mach es "
              "selbst noch einmal.",
        "fr": "\nChargée dans l'éditeur. Exécutez-la, puis réinitialisez et "
              "refaites-la vous-même.",
        "es": "\nCargada en el editor. Ejecútala, luego restablece y hazla tú mismo."},
    "task.reset": {"en": "Reset", "de": "Reset", "fr": "Réinit.",
                   "es": "Reiniciar"},
    "task.script_run": {
        "en": "Running your code as a script…", "de": "Dein Code läuft als Skript…",
        "fr": "Exécution de votre code comme script…",
        "es": "Ejecutando tu código como script…"},
    "task.timeout_10": {
        "en": "Timed out after 10s — is there an endless loop?",
        "de": "Nach 10 s abgebrochen — steckt da eine Endlosschleife drin?",
        "fr": "Arrêté après 10 s — y a-t-il une boucle infinie ?",
        "es": "Detenido tras 10 s — ¿hay un bucle infinito?"},
    "task.no_prints": {
        "en": "(no output — your code defines things but prints nothing, which is fine)",
        "de": "(keine Ausgabe — dein Code definiert nur etwas und gibt nichts aus, "
              "das ist völlig in Ordnung)",
        "fr": "(aucune sortie — votre code définit des choses sans rien afficher, "
              "c'est normal)",
        "es": "(sin salida — tu código define cosas pero no imprime nada, es normal)"},
    "task.finished_ms": {"en": "\nFinished in {ms} ms", "de": "\nFertig in {ms} ms",
                         "fr": "\nTerminé en {ms} ms", "es": "\nTerminado en {ms} ms"},
    "task.running_tests": {"en": "Running tests…", "de": "Tests laufen…",
                           "fr": "Tests en cours…", "es": "Ejecutando pruebas…"},
    "task.timeout_big": {
        "en": "⏱  TIMEOUT — your code ran for over 10 seconds.",
        "de": "⏱  ZEITÜBERSCHREITUNG — dein Code lief über 10 Sekunden.",
        "fr": "⏱  DÉLAI DÉPASSÉ — votre code a tourné plus de 10 secondes.",
        "es": "⏱  TIEMPO AGOTADO — tu código se ejecutó más de 10 segundos."},
    "task.timeout_why": {
        "en": "Either there is an endless loop, or the algorithm is too slow for the "
              "big hidden test.",
        "de": "Entweder steckt da eine Endlosschleife drin, oder der Algorithmus ist "
              "für den großen versteckten Test zu langsam.",
        "fr": "Soit il y a une boucle infinie, soit l'algorithme est trop lent pour le "
              "grand test caché.",
        "es": "O hay un bucle infinito, o el algoritmo es demasiado lento para la "
              "prueba oculta grande."},
    "task.status_timeout": {"en": "Timed out", "de": "Zeit überschritten",
                            "fr": "Délai dépassé", "es": "Tiempo agotado"},
    "task.crash_intro": {
        "en": "💥  Your code raised an error before the tests could run:\n",
        "de": "💥  Dein Code hat einen Fehler ausgelöst, bevor die Tests starten "
              "konnten:\n",
        "fr": "💥  Votre code a levé une erreur avant même les tests :\n",
        "es": "💥  Tu código lanzó un error antes de que las pruebas se ejecutaran:\n"},
    "task.crash_line": {
        "en": "\n→ look at line {line} in the editor (highlighted).",
        "de": "\n→ schau dir Zeile {line} im Editor an (hervorgehoben).",
        "fr": "\n→ regardez la ligne {line} dans l'éditeur (surlignée).",
        "es": "\n→ mira la línea {line} en el editor (resaltada)."},
    "task.status_crash": {"en": "Error before testing", "de": "Fehler vor dem Test",
                          "fr": "Erreur avant les tests", "es": "Error antes de probar"},
    "task.your_prints": {"en": "Your prints:", "de": "Deine Ausgaben:",
                         "fr": "Vos affichages :", "es": "Tus impresiones:"},
    "task.pass": {"en": "PASS", "de": "OK", "fr": "OK", "es": "OK"},
    "task.fail": {"en": "FAIL", "de": "FEHL", "fr": "ÉCHEC", "es": "FALLO"},
    "task.hidden_test": {"en": "hidden test", "de": "versteckter Test",
                         "fr": "test caché", "es": "prueba oculta"},
    "task.test": {"en": "test", "de": "Test", "fr": "test", "es": "prueba"},
    "task.hidden_input": {
        "en": "        (hidden input)", "de": "        (versteckte Eingabe)",
        "fr": "        (entrée cachée)", "es": "        (entrada oculta)"},
    "task.input": {"en": "        input:    {value}", "de": "        Eingabe:   {value}",
                   "fr": "        entrée :   {value}", "es": "        entrada:   {value}"},
    "task.crashed": {"en": "        crashed:  {value}", "de": "        Absturz:   {value}",
                     "fr": "        erreur :   {value}", "es": "        error:     {value}"},
    "task.expected": {"en": "        expected: {value}",
                      "de": "        erwartet:  {value}",
                      "fr": "        attendu :  {value}",
                      "es": "        esperado:  {value}"},
    "task.got": {"en": "        got:      {value}", "de": "        bekommen:  {value}",
                 "fr": "        obtenu :   {value}", "es": "        obtenido:  {value}"},
    "task.checker_fail": {
        "en": "        the object your function returned did not behave as specified",
        "de": "        das von deiner Funktion zurückgegebene Objekt hat sich nicht "
              "wie verlangt verhalten",
        "fr": "        l'objet renvoyé par votre fonction ne s'est pas comporté comme "
              "demandé",
        "es": "        el objeto que devolvió tu función no se comportó como se pedía"},
    "task.all_passed": {
        "en": "✓  ALL {n} TESTS PASSED   ({ms} ms)",
        "de": "✓  ALLE {n} TESTS BESTANDEN   ({ms} ms)",
        "fr": "✓  LES {n} TESTS SONT PASSÉS   ({ms} ms)",
        "es": "✓  LAS {n} PRUEBAS PASARON   ({ms} ms)"},
    "task.complexity_check": {
        "en": "   Target complexity was {value} — is that what you wrote?",
        "de": "   Die Ziel-Komplexität war {value} — hast du das auch geschrieben?",
        "fr": "   La complexité visée était {value} — est-ce bien ce que vous avez "
              "écrit ?",
        "es": "   La complejidad objetivo era {value} — ¿es lo que escribiste?"},
    "task.status_solved": {"en": "Solved!", "de": "Gelöst!", "fr": "Résolu !",
                           "es": "¡Resuelto!"},
    "task.some_passed": {
        "en": "✗  {passed} of {total} tests passed.",
        "de": "✗  {passed} von {total} Tests bestanden.",
        "fr": "✗  {passed} tests sur {total} sont passés.",
        "es": "✗  {passed} de {total} pruebas pasaron."},
    "task.status_passing": {
        "en": "{passed}/{total} passing", "de": "{passed}/{total} bestanden",
        "fr": "{passed}/{total} réussis", "es": "{passed}/{total} correctas"},

    # ------------------------------------------------------------ diagnoses
    "diag.none": {
        "en": "A 'NoneType' error usually means a missing `return`.",
        "de": "Ein 'NoneType'-Fehler heißt meistens: da fehlt ein `return`.",
        "fr": "Une erreur « NoneType » signifie presque toujours qu'il manque un "
              "`return`.",
        "es": "Un error «NoneType» casi siempre significa que falta un `return`."},
    "diag.index": {
        "en": "IndexError: check your loop bounds and the empty-input case.",
        "de": "IndexError: prüf deine Schleifengrenzen und den Fall der leeren Eingabe.",
        "fr": "IndexError : vérifiez les bornes de vos boucles et le cas de l'entrée "
              "vide.",
        "es": "IndexError: revisa los límites del bucle y el caso de entrada vacía."},
    "diag.key": {
        "en": "KeyError: use dict.get(key, default) instead of dict[key].",
        "de": "KeyError: nimm dict.get(key, default) statt dict[key].",
        "fr": "KeyError : utilisez dict.get(clé, défaut) plutôt que dict[clé].",
        "es": "KeyError: usa dict.get(clave, valor) en vez de dict[clave]."},
    "diag.type": {
        "en": "TypeError: check the types you are mixing (int vs str vs None).",
        "de": "TypeError: schau nach, welche Typen du mischst (int, str, None).",
        "fr": "TypeError : regardez les types que vous mélangez (int, str, None).",
        "es": "TypeError: mira qué tipos estás mezclando (int, str, None)."},
    "diag.zero": {
        "en": "Guard the empty / zero case before dividing.",
        "de": "Fang den leeren bzw. Null-Fall ab, bevor du teilst.",
        "fr": "Traitez le cas vide ou nul avant de diviser.",
        "es": "Controla el caso vacío o cero antes de dividir."},
    "diag.crash": {
        "en": "Fix the crash first, then re-run.",
        "de": "Behebe erst den Absturz, dann noch mal ausführen.",
        "fr": "Corrigez d'abord l'erreur, puis relancez.",
        "es": "Arregla primero el fallo y vuelve a ejecutar."},
    "diag.empty": {
        "en": "The empty input is failing — handle it explicitly at the top.",
        "de": "Die leere Eingabe schlägt fehl — behandle sie gleich am Anfang.",
        "fr": "L'entrée vide échoue — traitez-la explicitement au début.",
        "es": "La entrada vacía falla — trátala explícitamente al principio."},
    "diag.all_none": {
        "en": "Everything returns None — did you forget to `return` the result?",
        "de": "Alles liefert None — hast du vergessen, das Ergebnis mit `return` "
              "zurückzugeben?",
        "fr": "Tout renvoie None — auriez-vous oublié de `return` le résultat ?",
        "es": "Todo devuelve None — ¿olvidaste hacer `return` del resultado?"},

    # ---------------------------------------------------- programming language
    "lang.section": {"en": "LANGUAGE", "de": "SPRACHE", "fr": "LANGAGE",
                     "es": "LENGUAJE"},
    "lang.ready": {"en": "ready", "de": "bereit", "fr": "prêt", "es": "listo"},
    "lang.missing": {"en": "not installed", "de": "nicht installiert",
                     "fr": "non installé", "es": "no instalado"},
    "lang.bundled": {"en": "built in", "de": "eingebaut", "fr": "intégré",
                     "es": "integrado"},
    "lang.detect": {"en": "Re-check toolchains", "de": "Toolchains neu prüfen",
                    "fr": "Revérifier les outils", "es": "Volver a comprobar"},
    "lang.missing_title": {
        "en": "{label} is not installed", "de": "{label} ist nicht installiert",
        "fr": "{label} n'est pas installé", "es": "{label} no está instalado"},
    "lang.missing_body": {
        "en": "CodeForge runs your code with the real {label} toolchain, and it could "
              "not find it on this machine.\n\n{hint}\n\nOnce it is installed, press "
              "“{button}”.",
        "de": "CodeForge führt deinen Code mit der echten {label}-Toolchain aus und "
              "hat sie auf diesem Rechner nicht gefunden.\n\n{hint}\n\nWenn sie "
              "installiert ist, drück auf „{button}“.",
        "fr": "CodeForge exécute votre code avec la vraie chaîne d'outils {label}, et "
              "ne l'a pas trouvée sur cette machine.\n\n{hint}\n\nUne fois installée, "
              "cliquez sur « {button} ».",
        "es": "CodeForge ejecuta tu código con las herramientas reales de {label}, y no "
              "las encontró en este equipo.\n\n{hint}\n\nCuando estén instaladas, pulsa "
              "«{button}»."},
    "lang.python_only_title": {
        "en": "Only available for Python so far", "de": "Bisher nur für Python verfügbar",
        "fr": "Disponible seulement pour Python", "es": "Solo disponible para Python"},
    "lang.python_only_body": {
        "en": "This part of CodeForge — the {area} — is written for Python at the "
              "moment. The Interview tab already works in {label}, with the same "
              "problems and generated starter code.\n\nSwitch the language back to "
              "Python to use this tab.",
        "de": "Dieser Teil von CodeForge — {area} — gibt es zurzeit nur für Python. Der "
              "Interview-Tab funktioniert in {label} bereits, mit denselben Aufgaben "
              "und erzeugtem Startcode.\n\nStell die Sprache auf Python zurück, um "
              "diesen Tab zu nutzen.",
        "fr": "Cette partie de CodeForge — {area} — n'existe pour l'instant qu'en "
              "Python. L'onglet Entretien fonctionne déjà en {label}, avec les mêmes "
              "exercices et un code de départ généré.\n\nRepassez le langage sur Python "
              "pour utiliser cet onglet.",
        "es": "Esta parte de CodeForge — {area} — está escrita solo para Python por "
              "ahora. La pestaña Entrevista ya funciona en {label}, con los mismos "
              "problemas y código inicial generado.\n\nVuelve a poner el lenguaje en "
              "Python para usar esta pestaña."},
    "lang.area_curriculum": {"en": "lesson curriculum", "de": "der Lehrplan",
                             "fr": "le programme de leçons", "es": "el temario"},
    "lang.area_drills": {"en": "randomised drills", "de": "die Zufallsübungen",
                         "fr": "les exercices aléatoires",
                         "es": "los ejercicios aleatorios"},
    "lang.area_playground": {"en": "playground", "de": "die Spielwiese",
                             "fr": "le bac à sable", "es": "el área de pruebas"},
    "lang.build_failed": {
        "en": "🔨  It did not compile:", "de": "🔨  Es lässt sich nicht übersetzen:",
        "fr": "🔨  La compilation a échoué :", "es": "🔨  No compiló:"},
    "lang.compiled_in": {
        "en": "compiled and ran in {ms} ms", "de": "übersetzt und ausgeführt in {ms} ms",
        "fr": "compilé et exécuté en {ms} ms", "es": "compilado y ejecutado en {ms} ms"},

    # --------------------------------------------------------------- shared
    "common.all_topics": {"en": "All topics", "de": "Alle Themen",
                          "fr": "Tous les thèmes", "es": "Todos los temas"},
    "common.any": {"en": "Any", "de": "Beliebig", "fr": "Tous", "es": "Cualquiera"},
    "common.timed_out": {
        "en": "⏱  Timed out after 10 seconds.", "de": "⏱  Nach 10 Sekunden abgebrochen.",
        "fr": "⏱  Arrêté après 10 secondes.", "es": "⏱  Detenido tras 10 segundos."},
    "common.running": {"en": "Running…", "de": "Läuft…", "fr": "Exécution…",
                       "es": "Ejecutando…"},
    "common.finished": {
        "en": "\n[finished in {ms} ms]", "de": "\n[fertig in {ms} ms]",
        "fr": "\n[terminé en {ms} ms]", "es": "\n[terminado en {ms} ms]"},
}


def t(key: str, **kw) -> str:
    entry = UI.get(key)
    if entry is None:
        return key
    text = pick(entry, key)
    return text.format(**kw) if kw else text


# ===========================================================================
#  Topics, difficulties, complexity notes
# ===========================================================================
TOPICS_BY_LANG: dict[str, dict[str, str]] = {
    "de": {
        "General": "Allgemein", "Basics": "Grundlagen", "Strings": "Zeichenketten",
        "Lists": "Listen", "Sets": "Mengen", "Sorting": "Sortieren",
        "Hash map": "Hash-Map", "Prefix sums": "Präfixsummen",
        "Two pointers": "Zwei Zeiger", "Sliding window": "Schiebefenster",
        "Matrix": "Matrix", "Bit tricks": "Bit-Tricks", "Errors": "Fehler",
        "Arrays": "Arrays", "Math": "Mathe", "Stack": "Stapel", "Counting": "Zählen",
        "Greedy": "Greedy", "Dynamic programming": "Dynamische Programmierung",
        "Binary search": "Binäre Suche", "Graphs": "Graphen", "Recursion": "Rekursion",
        "Functions": "Funktionen", "OOP": "Objektorientierung",
        "Debugging": "Fehlersuche",
    },
    "fr": {
        "General": "Général", "Basics": "Bases", "Strings": "Chaînes",
        "Lists": "Listes", "Sets": "Ensembles", "Sorting": "Tri",
        "Hash map": "Table de hachage", "Prefix sums": "Sommes préfixes",
        "Two pointers": "Deux pointeurs", "Sliding window": "Fenêtre glissante",
        "Matrix": "Matrice", "Bit tricks": "Astuces binaires", "Errors": "Erreurs",
        "Arrays": "Tableaux", "Math": "Maths", "Stack": "Pile", "Counting": "Comptage",
        "Greedy": "Glouton", "Dynamic programming": "Programmation dynamique",
        "Binary search": "Recherche binaire", "Graphs": "Graphes",
        "Recursion": "Récursion", "Functions": "Fonctions", "OOP": "Objet",
        "Debugging": "Débogage",
    },
    "es": {
        "General": "General", "Basics": "Fundamentos", "Strings": "Cadenas",
        "Lists": "Listas", "Sets": "Conjuntos", "Sorting": "Ordenación",
        "Hash map": "Tabla hash", "Prefix sums": "Sumas prefijas",
        "Two pointers": "Dos punteros", "Sliding window": "Ventana deslizante",
        "Matrix": "Matriz", "Bit tricks": "Trucos de bits", "Errors": "Errores",
        "Arrays": "Arreglos", "Math": "Matemáticas", "Stack": "Pila",
        "Counting": "Conteo", "Greedy": "Voraz",
        "Dynamic programming": "Programación dinámica",
        "Binary search": "Búsqueda binaria", "Graphs": "Grafos",
        "Recursion": "Recursión", "Functions": "Funciones", "OOP": "Objetos",
        "Debugging": "Depuración",
    },
}

DIFFICULTY_BY_LANG: dict[str, dict[str, str]] = {
    "de": {"Easy": "Leicht", "Medium": "Mittel", "Hard": "Schwer"},
    "fr": {"Easy": "Facile", "Medium": "Moyen", "Hard": "Difficile"},
    "es": {"Easy": "Fácil", "Medium": "Medio", "Hard": "Difícil"},
}

_COMPLEXITY_BY_LANG: dict[str, list[tuple[str, str]]] = {
    "de": [(" time, ", " Zeit, "), (" space", " Speicher"),
           (", one pass", ", ein Durchlauf"),
           ("O(total characters)", "O(Zeichen insgesamt)"),
           ("O(rows * cols)", "O(Zeilen * Spalten)"),
           ("O(amount * len(coins))", "O(Betrag * Anzahl Münzsorten)"),
           ("O(n) with a set / O(n log n) sorted",
            "O(n) mit einem Set / O(n log n) mit Sortieren"),
           ("O(n log k) with a heap", "O(n log k) mit einem Heap"),
           ("O(n log n) — O(n) with bucket sort", "O(n log n) — O(n) mit Bucket-Sort"),
           ("O(n) with a set", "O(n) mit einem Set"),
           ("O(n log log n)", "O(n log log n)"), ("O(sqrt n)", "O(Wurzel n)"),
           ("O(n) extra", "O(n) zusätzlich"), ("O(1) extra", "O(1) zusätzlich")],
    "fr": [(" time, ", " en temps, "), (" space", " en mémoire"),
           (", one pass", ", un seul passage"),
           ("O(total characters)", "O(nombre total de caractères)"),
           ("O(rows * cols)", "O(lignes * colonnes)"),
           ("O(amount * len(coins))", "O(montant * nombre de pièces)"),
           ("O(n) with a set / O(n log n) sorted",
            "O(n) avec un ensemble / O(n log n) avec un tri"),
           ("O(n log k) with a heap", "O(n log k) avec un tas"),
           ("O(n log n) — O(n) with bucket sort",
            "O(n log n) — O(n) avec un tri par paquets"),
           ("O(n) with a set", "O(n) avec un ensemble"),
           ("O(sqrt n)", "O(racine de n)"),
           ("O(n) extra", "O(n) supplémentaire"),
           ("O(1) extra", "O(1) supplémentaire")],
    "es": [(" time, ", " en tiempo, "), (" space", " en memoria"),
           (", one pass", ", una sola pasada"),
           ("O(total characters)", "O(caracteres en total)"),
           ("O(rows * cols)", "O(filas * columnas)"),
           ("O(amount * len(coins))", "O(importe * número de monedas)"),
           ("O(n) with a set / O(n log n) sorted",
            "O(n) con un conjunto / O(n log n) ordenando"),
           ("O(n log k) with a heap", "O(n log k) con un montículo"),
           ("O(n log n) — O(n) with bucket sort",
            "O(n log n) — O(n) con ordenación por cubos"),
           ("O(n) with a set", "O(n) con un conjunto"),
           ("O(sqrt n)", "O(raíz de n)"),
           ("O(n) extra", "O(n) extra"), ("O(1) extra", "O(1) extra")],
}


def topic(name: str) -> str:
    return TOPICS_BY_LANG.get(LANG, {}).get(name, name)


def difficulty(name: str) -> str:
    return DIFFICULTY_BY_LANG.get(LANG, {}).get(name, name)


def complexity(text: str) -> str:
    rules = _COMPLEXITY_BY_LANG.get(LANG)
    if not rules or not text:
        return text
    out = text
    for source, target in rules:
        out = out.replace(source, target)
    return out


def topic_choices(topics: list[str]) -> tuple[list[str], list[str]]:
    """(internal values, displayed labels) with 'All topics' in front."""
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
def localize_task(task, table: dict | None, language: str = "de"):
    """Swap a task's title/statement/hints/notes to the active language.

    `table` holds the translation for `language` (or None). It is applied only
    when that language is the active one — otherwise a French user would get
    the German text handed to them. Anything without a translation stays
    English, which is the intended fallback.

    The task object is mutated in place; every caller builds a fresh Task first.
    """
    task.complexity = complexity(task.complexity)
    if LANG != language or not table:
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
    return task
