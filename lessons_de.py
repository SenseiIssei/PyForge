"""German translation of the Learn curriculum.

Keyed by lesson id. Each entry may provide: section, title, theory, takeaway,
example, and a `task` dict with title / statement / hints.

The example CODE is translated too (comments and printed labels), because the
whole point of the German mode is being able to learn without switching
languages in your head.
"""

SECTIONS_DE = {
    "Foundations": "Grundlagen",
    "Data structures": "Datenstrukturen",
    "Functions & structure": "Funktionen & Struktur",
    "Interview technique": "Interview-Technik",
}

LESSONS_DE = {

# ============================================================ 1. GRUNDLAGEN
"vars": {
 "section": "Grundlagen",
 "title": "Variablen & Typen",
 "theory": """In Python werden Typen nicht deklariert. Eine Variable ist nur ein Name, der auf
ein Objekt zeigt, und das Objekt kennt seinen Typ selbst.

    age = 30            # int   (ganze Zahl)
    price = 4.99        # float (Kommazahl)
    name = "Ada"        # str   (Text)
    is_ready = True     # bool  (großes T bzw. F!)
    nothing = None      # das "kein Wert"-Objekt

Dinge, die du ständig brauchst:
  * type(x)      -> der Typ von x
  * int("42")    -> Text in eine Zahl umwandeln
  * str(42)      -> Zahl in Text umwandeln
  * f-Strings    -> f"{name} ist {age}" baut Text mit Werten darin

Ganzzahldivision und Rest kommen in jedem Interview vor:
  7 / 2  -> 3.5     (echte Division, immer ein float)
  7 // 2 -> 3       (Ganzzahldivision, schneidet ab)
  7 %  2 -> 1       (Rest — der Schlüssel zu gerade/ungerade und Zyklen)
  2 ** 10 -> 1024   (Potenz)

Namen schreibt man snake_case, Konstanten in GROSSBUCHSTABEN. Darauf achtet
Python nicht technisch, aber die Community sehr wohl.""",
 "takeaway": "Eine Variable ist ein Etikett auf einem Objekt. % und // sind deine Interview-Werkzeuge.",
 "example": '''name = "Ada"
age = 36
height = 1.68
likes_python = True

print(f"{name} ist {age} Jahre alt und {height} m groß.")
print("Typ von age:", type(age))
print("age als Text:", str(age) + " Jahre")

print("7 / 2  =", 7 / 2)
print("7 // 2 =", 7 // 2)
print("7 % 2  =", 7 % 2)
print("2 ** 10 =", 2 ** 10)

# Mehrfachzuweisung / Tauschen ohne Hilfsvariable
a, b = 1, 2
a, b = b, a
print("getauscht:", a, b)
''',
 "task": {
  "title": "Sekunden als Uhrzeit",
  "statement": """Schreib to_clock(seconds), das eine Anzahl Sekunden in einen "H:MM:SS"-String
verwandelt.

Regeln:
  * Stunden ohne führende Null, Minuten und Sekunden immer zweistellig
  * to_clock(3661) -> "1:01:01"
  * to_clock(59)   -> "0:00:59"

Tipp: // liefert dir ganze Einheiten, % liefert den Rest.""",
  "hints": ["hours = seconds // 3600",
            "minutes = (seconds % 3600) // 60",
            'f-Strings können auffüllen: f"{m:02d}" ergibt "07" für 7'],
 },
},

"strings": {
 "section": "Grundlagen",
 "title": "Zeichenketten (Strings)",
 "theory": """Strings sind unveränderliche Folgen von Zeichen. Jede "verändernde" Methode gibt
einen NEUEN String zurück.

    s = "  Hallo, Welt  "
    s.strip()          -> "Hallo, Welt"
    s.lower()          -> "  hallo, welt  "
    s.replace("l","L") -> neuer String
    s.split(",")       -> ['  Hallo', ' Welt  ']
    ",".join(teile)    -> eine Liste wieder zusammenkleben
    s.startswith("H"), s.endswith("t"), "Welt" in s

Indizieren und Slicing (die mit Abstand nützlichste Python-Fähigkeit):

    s[0]      erstes Zeichen
    s[-1]     letztes Zeichen
    s[2:5]    Zeichen 2,3,4      (Start dabei, Ende NICHT)
    s[:3]     die ersten drei
    s[3:]     alles ab 3
    s[::-1]   das Ganze rückwärts

Einen String in einer Schleife mit += zu bauen ist O(n^2). Sammle die Teile in
einer Liste und mach "".join(teile) — das fällt Interviewern auf.""",
 "takeaway": "Strings sind unveränderlich. Slicing mit [start:ende:schritt]. join statt +=.",
 "example": '''s = "  Hallo, Python Welt  "

print(repr(s.strip()))
print(s.strip().lower())
print(s.strip().split())
print("-".join(["a", "b", "c"]))

wort = "interview"
print("erstes:", wort[0], "| letztes:", wort[-1])
print("Ausschnitt 2:5 ->", wort[2:5])
print("rückwärts ->", wort[::-1])
print("jedes 2. ->", wort[::2])

print("steckt 'view' drin?", "view" in wort)
print("Anzahl 'e':", wort.count("e"))

# effizient einen String zusammenbauen
teile = []
for i in range(5):
    teile.append(str(i * i))
print(", ".join(teile))
''',
 "task": {
  "title": "Namen normalisieren",
  "statement": """Schreib normalise(text), das einen unordentlichen Namen aufräumt:

  * Leerzeichen am Anfang und Ende entfernen
  * mehrfache Leerzeichen im Inneren auf eines reduzieren
  * jedes Wort groß schreiben (erster Buchstabe groß, Rest klein)

normalise("  aDA   LOVElace ") -> "Ada Lovelace"

Tipp: text.split() ohne Argument trennt bereits an beliebig vielen Leerzeichen.""",
  "hints": ["woerter = text.split() entfernt die überflüssigen Leerzeichen schon für dich",
            "wort.capitalize() macht den ersten Buchstaben groß und den Rest klein",
            'return " ".join(...)'],
 },
},

"lists": {
 "section": "Grundlagen",
 "title": "Listen",
 "theory": """Eine Liste ist eine geordnete, veränderbare Folge. Sie ist der Standard-Behälter
in Python.

    nums = [3, 1, 4, 1, 5]
    nums.append(9)        hinten anhängen              O(1)
    nums.pop()            letztes entfernen+liefern    O(1)
    nums.pop(0)           erstes entfernen+liefern     O(n)  <- Vorsicht!
    nums.insert(0, 7)     vorne einfügen               O(n)
    nums.remove(1)        die ERSTE 1 entfernen        O(n)
    len(nums), sum(nums), min(nums), max(nums)
    nums.sort()           sortiert an Ort und Stelle, liefert None
    sorted(nums)          liefert eine NEUE sortierte Liste
    nums[::-1]            umgedrehte Kopie

Die klassische Anfängerfalle:

    a = [1, 2, 3]
    b = a          # b ist DIESELBE Liste, keine Kopie
    b.append(4)    # a ist jetzt auch [1, 2, 3, 4]!
    c = a[:]       # DAS ist eine Kopie (oder a.copy() / list(a))

Sortieren mit key ist Interview-Grundhandwerk:

    leute.sort(key=lambda p: p[1])                 nach zweitem Element
    woerter.sort(key=len, reverse=True)            längste zuerst
    items.sort(key=lambda x: (-x.score, x.name))   Punkte absteigend, dann Name""",
 "takeaway": "Listen sind veränderbar und werden per Referenz geteilt. sort() ändert, sorted() kopiert.",
 "example": '''nums = [3, 1, 4, 1, 5, 9, 2, 6]

print("Länge:", len(nums), "| Summe:", sum(nums), "| Maximum:", max(nums))
nums.append(5)
print("nach append:", nums)
print("entnommen:", nums.pop(), "->", nums)

print("sortierte Kopie:", sorted(nums))
print("Original unverändert:", nums)
nums.sort()
print("an Ort und Stelle sortiert:", nums)

woerter = ["Birne", "Fei", "Banane", "Kiwi"]
woerter.sort(key=len)
print("nach Länge:", woerter)
woerter.sort(key=lambda w: (-len(w), w))
print("lang->kurz, dann a-z:", woerter)

# Referenz vs. Kopie
a = [1, 2, 3]
verweis, kopie = a, a[:]
verweis.append(99)
print("a:", a, "| Kopie:", kopie)
''',
 "task": {
  "title": "Zweitgrößter Wert",
  "statement": """Schreib second_largest(nums), das den zweitgrößten UNTERSCHIEDLICHEN Wert einer
Liste zurückgibt.

  second_largest([3, 1, 4, 4, 5]) -> 4
  second_largest([7, 7, 7])       -> None   (es gibt keinen zweiten Wert)

Gib None zurück, wenn es weniger als zwei verschiedene Werte gibt.""",
  "hints": ["set(nums) wirft die Duplikate weg",
            "sorted(...) und dann Index -2 nehmen",
            "Fang den kurzen Fall zuerst ab: if len(distinct) < 2: return None"],
 },
},

"control": {
 "section": "Grundlagen",
 "title": "if / else & Schleifen",
 "theory": """Die Einrückung IST der Block. Vier Leerzeichen, immer.

    if punkte >= 90:
        note = "A"
    elif punkte >= 80:
        note = "B"
    else:
        note = "C"

Iteriere über die ELEMENTE, nicht über die Indizes, wann immer es geht:

    for wort in woerter:            # gut
    for i in range(len(woerter)):   # nur, wenn du i wirklich brauchst
    for i, wort in enumerate(woerter):      # Index UND Element
    for name, punkte in zip(namen, punkte): # zwei Listen im Gleichschritt

while-Schleifen laufen, bis eine Bedingung kippt:

    while low <= high:            # die Form der binären Suche
        ...

Schleifensteuerung:
    break      die Schleife sofort verlassen
    continue   zum nächsten Durchlauf springen
    for...else das else läuft nur, wenn NICHT mit break abgebrochen wurde

range(start, stop, schritt) — stop gehört NICHT dazu:
    range(5)        0 1 2 3 4
    range(2, 8, 2)  2 4 6
    range(5, 0, -1) 5 4 3 2 1""",
 "takeaway": "Iteriere über Elemente; greif zu enumerate/zip, bevor du range(len(x)) schreibst.",
 "example": '''punkte = [92, 78, 85, 61, 99]
namen = ["Ada", "Linus", "Grace", "Guido", "Hedy"]

for name, p in zip(namen, punkte):
    if p >= 90:
        note = "A"
    elif p >= 80:
        note = "B"
    else:
        note = "C"
    print(f"{name:<6} {p:>3}  {note}")

print("---")
for i, name in enumerate(namen, start=1):
    print(i, name)

print("--- erste Punktzahl über 95")
for p in punkte:
    if p > 95:
        print("gefunden:", p)
        break
else:
    print("keine gefunden")

n, schritte = 27, 0
while n != 1:                 # Collatz-Folge
    n = n // 2 if n % 2 == 0 else 3 * n + 1
    schritte += 1
print("Collatz-Schritte für 27:", schritte)
''',
 "task": {
  "title": "FizzBuzz — zurückgeben statt ausgeben",
  "statement": """Der Klassiker — aber gib eine LISTE zurück, statt zu drucken.

fizzbuzz(n) liefert eine Liste für die Zahlen 1..n, wobei:
  * Vielfache von 3 und 5 -> "FizzBuzz"
  * Vielfache von 3       -> "Fizz"
  * Vielfache von 5       -> "Buzz"
  * alles andere          -> die Zahl selbst, als int

fizzbuzz(5) -> [1, 2, "Fizz", 4, "Buzz"]

Prüf den 15er-Fall ZUERST, sonst kann er nie eintreten.""",
  "hints": ["Bau eine Ergebnisliste und häng daran an",
            "range(1, n + 1) liefert dir 1..n einschließlich",
            "if i % 15 == 0 erledigt beide Fälle auf einmal"],
 },
},

# ======================================================= 2. DATENSTRUKTUREN
"dicts": {
 "section": "Datenstrukturen",
 "title": "Dictionaries",
 "theory": """Ein dict bildet Schlüssel auf Werte ab, mit O(1) Zugriff im Mittel. Es ist DAS
Werkzeug, um aus einer O(n^2)-Schleife eine O(n)-Schleife zu machen — und genau
das wird in Coding-Interviews belohnt.

    alter = {"Ada": 36, "Linus": 54}
    alter["Grace"] = 85         einfügen / überschreiben
    alter["Ada"]                KeyError, wenn nicht vorhanden
    alter.get("Niemand")        -> None  (kein Absturz)
    alter.get("Niemand", 0)     -> 0     (Vorgabewert)
    "Ada" in alter              Mitgliedschaftstest, O(1)
    del alter["Ada"]
    alter.keys() / .values() / .items()

Zähl-Muster, vom allgemeinen zum eleganten:

    counts[c] = counts.get(c, 0) + 1        funktioniert überall
    from collections import Counter
    counts = Counter(text)                  Batterien inklusive
    counts.most_common(3)

Gruppieren:

    from collections import defaultdict
    gruppen = defaultdict(list)
    for wort in woerter:
        gruppen[len(wort)].append(wort)

Seit Python 3.7 behalten dicts ihre Einfügereihenfolge.""",
 "takeaway": "dict-Zugriff ist O(1). Counter und defaultdict sparen dir echte Zeit.",
 "example": '''from collections import Counter, defaultdict

text = "mississippi"

counts = {}
for ch in text:
    counts[ch] = counts.get(ch, 0) + 1
print("von Hand:", counts)

print("Counter:", Counter(text))
print("Top 2:", Counter(text).most_common(2))

woerter = ["Fei", "Birne", "Kiwi", "Pflaume", "Apfel"]
nach_laenge = defaultdict(list)
for wort in woerter:
    nach_laenge[len(wort)].append(wort)
print("gruppiert:", dict(nach_laenge))

lager = {"Apfel": 3, "Birne": 0, "Feige": 7}
for name, menge in lager.items():
    print(f"{name:<7} {menge}")
print("vorrätig:", [n for n, m in lager.items() if m > 0])
print("fehlender Schlüssel, gefahrlos:", lager.get("Banane", 0))
''',
 "task": {
  "title": "Erstes Zeichen ohne Wiederholung",
  "statement": """Schreib first_unique(text), das das erste Zeichen zurückgibt, das genau einmal
vorkommt. Gib None zurück, wenn sich jedes Zeichen wiederholt.

  first_unique("swiss")    -> "w"
  first_unique("aabbcc")   -> None

Mach es in zwei Durchläufen: erst zählen, dann der Reihe nach durchgehen. Das
ist O(n) — eine verschachtelte O(n^2)-Schleife ist NICHT die gewünschte Antwort.""",
  "hints": ["Erste Schleife: counts[ch] = counts.get(ch, 0) + 1 aufbauen",
            "Zweite Schleife: nochmal über text, das erste ch mit counts[ch] == 1 zurückgeben",
            "Geh im zweiten Durchlauf über den TEXT, nicht über das dict — die Reihenfolge zählt"],
 },
},

"sets": {
 "section": "Datenstrukturen",
 "title": "Mengen & Tupel",
 "theory": """Ein set ist eine ungeordnete Sammlung eindeutiger Elemente mit O(1)-Mitgliedschaft.

    gesehen = set()
    gesehen.add(3)
    3 in gesehen         O(1)  <- gegenüber O(n) bei einer Liste!
    gesehen.discard(3)   kein Fehler, wenn nicht vorhanden
    a | b   Vereinigung      a & b  Schnittmenge
    a - b   Differenz        a ^ b  symmetrische Differenz

Aus `if x in grosse_liste` ein `if x in grosses_set` zu machen ist die
häufigste "mach es schneller"-Korrektur in Coding-Tests überhaupt.

Ein Tupel ist eine unveränderliche Liste: (3, 4). Weil es unveränderlich ist,
ist es hashbar — Tupel können also dict-Schlüssel und set-Elemente sein,
Listen nicht.

    punkt = (3, 4)
    x, y = punkt                 entpacken
    gitter[(zeile, spalte)] = wert   Tupel als dict-Schlüssel
    besucht.add((zeile, spalte))     das "besuchte Felder"-Muster

Achtung: {} ist ein leeres DICT. Ein leeres set schreibt man set().""",
 "takeaway": "`in` ist bei einem set O(1), bei einer Liste O(n). Tupel sind hashbar, Listen nicht.",
 "example": '''nums = [3, 1, 4, 1, 5, 9, 2, 6, 5]

print("eindeutig:", set(nums))
print("enthält 4?", 4 in set(nums))
print("Duplikate weg, Reihenfolge bleibt:", list(dict.fromkeys(nums)))

a, b = {1, 2, 3, 4}, {3, 4, 5}
print("Vereinigung:", a | b, "| Schnittmenge:", a & b)
print("nur in a:", a - b, "| in genau einem:", a ^ b)

# das "habe ich das schon gesehen"-Muster
gesehen, doppelte = set(), []
for n in nums:
    if n in gesehen:
        doppelte.append(n)
    gesehen.add(n)
print("Duplikate:", doppelte)

# Tupel: unveränderlich, hashbar, entpackbar
punkt = (3, 4)
x, y = punkt
print("x =", x, "y =", y)
besucht = {(0, 0), (1, 2)}
print("(1,2) besucht?", (1, 2) in besucht)
''',
 "task": {
  "title": "Haben zwei Listen etwas gemeinsam?",
  "statement": """Schreib common_items(a, b), das die Werte zurückgibt, die in BEIDEN Listen
vorkommen — aufsteigend sortiert und ohne Duplikate.

  common_items([1, 2, 2, 3], [3, 4, 2]) -> [2, 3]
  common_items([1], [2])                -> []

Ziel ist O(n + m), keine verschachtelte Schleife.""",
  "hints": ["set(a) & set(b) liefert die gemeinsamen Werte",
            "sorted(...) macht daraus eine geordnete Liste"],
 },
},

"comprehensions": {
 "section": "Datenstrukturen",
 "title": "Comprehensions",
 "theory": """Eine Comprehension ist eine Schleife, die einen Behälter baut — geschrieben als
ein einziger Ausdruck.

    quadrate = [n * n for n in range(10)]
    gerade   = [n for n in nums if n % 2 == 0]
    labels   = [f"#{i}" for i in ids]
    lookup   = {wort: len(wort) for wort in woerter}    dict-Comprehension
    eindeutig = {w.lower() for w in woerter}            set-Comprehension
    summe    = sum(n * n for n in nums)                 Generator, keine Liste

Die Form zum Merken:

    [ WAS_BEHALTEN   for ELEMENT in ITERIERBARES   if BEDINGUNG ]

Verschachtelt (von links nach rechts lesen, genau wie verschachtelte
for-Schleifen):

    flach = [x for zeile in matrix for x in zeile]

Bedingter WERT (dieses if/else steht vorne und ist KEIN Filter):

    art = ["gerade" if n % 2 == 0 else "ungerade" for n in nums]

Faustregel: Passt es nicht bequem in eine Zeile, nimm eine richtige Schleife.""",
 "takeaway": "[ausdruck for element in it if bedingung]. In sum/any/all einen Generator nehmen.",
 "example": '''nums = [1, 2, 3, 4, 5, 6, 7, 8]

print([n * n for n in nums])
print([n for n in nums if n % 2 == 0])
print(["gerade" if n % 2 == 0 else "ungerade" for n in nums])

woerter = ["Fei", "Banane", "Kiwi"]
print({w: len(w) for w in woerter})
print({w[0] for w in woerter})

matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print("flachgeklopft:", [x for zeile in matrix for x in zeile])
print("Diagonale:", [matrix[i][i] for i in range(len(matrix))])
print("transponiert:", [list(spalte) for spalte in zip(*matrix)])

# Generator-Ausdruck: keine Zwischenliste im Speicher
print("Summe der Quadrate:", sum(n * n for n in range(1000)))
print("irgendetwas negativ?", any(n < 0 for n in nums))
print("alles positiv?", all(n > 0 for n in nums))
''',
 "task": {
  "title": "Spaltensummen einer Matrix",
  "statement": """Schreib col_sums(matrix), das die Summe jeder SPALTE einer rechteckigen
Liste-von-Listen zurückgibt.

  col_sums([[1, 2], [3, 4], [5, 6]]) -> [9, 12]
  col_sums([])                       -> []

zip(*matrix) transponiert eine Matrix — das plus eine Comprehension ist ein
Einzeiler.""",
  "hints": ["zip(*matrix) liefert ein Tupel pro Spalte",
            "[sum(spalte) for spalte in zip(*matrix)]",
            "zip(*[]) ist leer, der leere Fall funktioniert also schon von allein"],
 },
},

# ==================================================== 3. FUNKTIONEN/STRUKTUR
"functions": {
 "section": "Funktionen & Struktur",
 "title": "Funktionen",
 "theory": """    def greet(name, greeting="Hallo", *, loud=False):
        text = f"{greeting}, {name}!"
        return text.upper() if loud else text

  * `greeting="Hallo"` ist ein Vorgabewert — beim Aufruf optional
  * alles nach `*` muss als Schlüsselwort übergeben werden: greet("Ada", loud=True)
  * eine Funktion ohne `return` liefert None
  * `return a, b` gibt ein Tupel zurück, das der Aufrufer entpacken kann

DIE klassische Python-Falle — nie einen veränderbaren Vorgabewert nutzen:

    def schlecht(item, eimer=[]):   # DIESELBE Liste wird bei allen Aufrufen benutzt!
        eimer.append(item)
        return eimer

    def gut(item, eimer=None):
        if eimer is None:
            eimer = []
        eimer.append(item)
        return eimer

Gültigkeitsbereich: ein Name, dem in einer Funktion etwas zugewiesen wird, ist
lokal. Eine äußere Variable zu LESEN ist in Ordnung; sie neu zu binden bräuchte
`global` (was du fast nie willst — übergib sie lieber und gib sie zurück).

Typ-Hinweise sind optional und werden nie erzwungen, dokumentieren aber die
Absicht:

    def total(prices: list[float]) -> float: ...""",
 "takeaway": "Vorgabewerte werden einmal ausgewertet. Niemals [] oder {} als Vorgabe.",
 "example": '''def greet(name, greeting="Hallo", *, loud=False):
    text = f"{greeting}, {name}!"
    return text.upper() if loud else text

print(greet("Ada"))
print(greet("Linus", "Hi"))
print(greet("Grace", loud=True))

def min_max(nums):
    return min(nums), max(nums)

klein, gross = min_max([4, 9, 1, 7])
print("kleinstes:", klein, "größtes:", gross)

def schlecht(item, eimer=[]):
    eimer.append(item)
    return eimer

print("schlechter Aufruf 1:", schlecht(1))
print("schlechter Aufruf 2:", schlecht(2), "  <- die Liste hat überlebt!")

def gut(item, eimer=None):
    eimer = [] if eimer is None else eimer
    eimer.append(item)
    return eimer

print("guter Aufruf 1:", gut(1))
print("guter Aufruf 2:", gut(2))

def zweimal_anwenden(fn, wert):
    return fn(fn(wert))
print("zweimal_anwenden:", zweimal_anwenden(lambda x: x * 3, 2))
''',
 "task": {
  "title": "Flexibler Durchschnitt",
  "statement": """Schreib average(nums, ndigits=2), das den Mittelwert einer Zahlenliste auf
`ndigits` Nachkommastellen gerundet zurückgibt. Für eine leere Liste 0.0.

  average([1, 2, 3, 4])       -> 2.5
  average([1, 2], ndigits=0)  -> 2.0

Nutze round(wert, ndigits). Fang die leere Liste ab, BEVOR du teilst!""",
  "hints": ["if not nums: return 0.0",
            "mittel = sum(nums) / len(nums)",
            "return round(mittel, ndigits)"],
 },
},

"errors": {
 "section": "Funktionen & Struktur",
 "title": "Fehler & Ausnahmen",
 "theory": """    try:
        wert = int(text)
    except ValueError:
        wert = 0
    else:
        print("hat geklappt:", wert)   # nur wenn keine Ausnahme kam
    finally:
        print("läuft immer")           # Aufräumen

Fang die KONKRETE Ausnahme. Ein nacktes `except:` schluckt Tippfehler, Strg-C
und echte Bugs gleichermaßen.

Die, denen du begegnen wirst:
    ValueError        int("abc")
    TypeError         "a" + 1
    KeyError          d["fehlt"]
    IndexError        lst[99]
    ZeroDivisionError 1 / 0
    AttributeError    None.strip()

Wirf selbst eine, wenn ein Argument keinen Sinn ergibt:

    if n < 0:
        raise ValueError(f"n muss >= 0 sein, war aber {n}")

Der Python-Stil heißt EAFP — "lieber um Verzeihung bitten als um Erlaubnis".
Es zu versuchen und abzufangen ist idiomatisch; jede Vorbedingung vorher zu
prüfen ist es nicht.

    try:                        # EAFP, pythonisch
        return d[key]
    except KeyError:
        return default""",
 "takeaway": "Fang konkrete Ausnahmen. Wirf ValueError bei ungültiger Eingabe.",
 "example": '''def safe_int(text, default=0):
    try:
        return int(text)
    except (ValueError, TypeError):
        return default

print(safe_int("42"), safe_int("nix"), safe_int(None, -1))

def teile(a, b):
    try:
        ergebnis = a / b
    except ZeroDivisionError:
        print("  -> durch null kann man nicht teilen")
        return None
    else:
        return ergebnis
    finally:
        print("  (teile ist fertig)")

print("10/2 =", teile(10, 2))
print("10/0 =", teile(10, 0))

def wurzel_von(n):
    if n < 0:
        raise ValueError(f"n muss >= 0 sein, war aber {n}")
    return n ** 0.5

try:
    wurzel_von(-4)
except ValueError as exc:
    print("abgefangen:", exc)
''',
 "task": {
  "title": "Eine Zahlenliste einlesen",
  "statement": """Schreib parse_numbers(items), das eine Liste von Strings in ints umwandelt und
(numbers, bad_count) zurückgibt:

  * numbers   — die erfolgreich umgewandelten ints, in der Reihenfolge
  * bad_count — wie viele Einträge sich nicht umwandeln ließen

parse_numbers(["1", "x", "3"]) -> ([1, 3], 1)

Gib ein echtes Tupel zurück. Ein fehlerhafter Eintrag darf die Funktion nicht
zum Absturz bringen.""",
  "hints": ["Schleife, und pack int(item) in ein try/except ValueError",
            'int("3.5") wirft einen ValueError — das ist hier so gewollt',
            "return numbers, bad  baut das Tupel automatisch"],
 },
},

"oop": {
 "section": "Funktionen & Struktur",
 "title": "Klassen & Objekte",
 "theory": """Eine Klasse bündelt Daten mit den Funktionen, die damit arbeiten.

    class Konto:
        def __init__(self, inhaber, stand=0):   # läuft bei Konto("Ada")
            self.inhaber = inhaber              # Instanz-Attribute
            self.stand = stand

        def einzahlen(self, betrag):            # self = dieses Objekt
            if betrag <= 0:
                raise ValueError("Betrag muss positiv sein")
            self.stand += betrag
            return self.stand

        def __repr__(self):                     # wie es gedruckt wird
            return f"Konto({self.inhaber!r}, {self.stand})"

`self` ist der erste Parameter jeder Instanzmethode, und Python übergibt ihn
für dich: k.einzahlen(50) ruft einzahlen(k, 50) auf.

Dunder-Methoden klinken sich in die Sprache ein:
    __init__  Erzeugung        __repr__  Text für Entwickler
    __str__   Text für Nutzer  __len__   len(obj)
    __eq__    ==               __lt__    < , womit sort() funktioniert

Vererbung:

    class Sparkonto(Konto):
        def __init__(self, inhaber, stand=0, zins=0.02):
            super().__init__(inhaber, stand)
            self.zins = zins

Für reine Datenbündel nimm eine dataclass — sie schreibt __init__ und __repr__
für dich:

    from dataclasses import dataclass
    @dataclass
    class Punkt:
        x: int
        y: int""",
 "takeaway": "__init__ baut es, self ist das Objekt, super() erreicht die Elternklasse.",
 "example": '''from dataclasses import dataclass

class Konto:
    def __init__(self, inhaber, stand=0):
        self.inhaber = inhaber
        self.stand = stand

    def einzahlen(self, betrag):
        if betrag <= 0:
            raise ValueError("Betrag muss positiv sein")
        self.stand += betrag
        return self.stand

    def abheben(self, betrag):
        if betrag > self.stand:
            raise ValueError("nicht genug Guthaben")
        self.stand -= betrag
        return self.stand

    def __repr__(self):
        return f"Konto({self.inhaber!r}, {self.stand})"

k = Konto("Ada", 100)
k.einzahlen(50)
print(k, "| Stand:", k.stand)
try:
    k.abheben(1000)
except ValueError as exc:
    print("abgefangen:", exc)

class Sparkonto(Konto):
    def __init__(self, inhaber, stand=0, zins=0.02):
        super().__init__(inhaber, stand)
        self.zins = zins

    def zinsen_gutschreiben(self):
        return self.einzahlen(self.stand * self.zins)

s = Sparkonto("Grace", 1000)
s.zinsen_gutschreiben()
print(s, "| Zins:", s.zins)

@dataclass
class Punkt:
    x: int
    y: int
    def abstand(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

p = Punkt(3, 4)
print(p, "| Abstand:", p.abstand())
''',
 "task": {
  "title": "Eine kleine Stack-Klasse",
  "statement": """Bau eine Klasse Stack und eine Fabrikfunktion make_stack(items), die einen
bereits mit `items` gefüllten Stack zurückgibt (von links nach rechts gepusht).

Dein Stack braucht:
  * push(x)   oben drauflegen
  * pop()     das oberste entfernen und zurückgeben, oder None wenn leer
  * peek()    das oberste zurückgeben, ohne es zu entfernen, oder None wenn leer
  * size()    Anzahl der Elemente

make_stack([1, 2, 3]).pop() -> 3

Die Tests rufen make_stack(...) auf und stochern dann in dem Objekt herum, das
zurückkommt.""",
  "hints": ["push -> self.items.append(x)",
            "pop -> if not self.items: return None, sonst self.items.pop()",
            "make_stack: einen Stack bauen, über items laufen, jedes pushen, zurückgeben"],
 },
},

"modules": {
 "section": "Funktionen & Struktur",
 "title": "Module & die Standardbibliothek",
 "theory": """    import math                      math.sqrt(16)
    from math import sqrt, pi        sqrt(16)
    import statistics as stats       stats.mean(nums)

Die Batterien, zu denen du in einem Coding-Test wirklich greifst:

  collections   Counter, defaultdict, deque, namedtuple
  itertools     accumulate, combinations, permutations, groupby, product
  math          gcd, sqrt, ceil, floor, inf, comb, isclose
  heapq         heappush/heappop — eine Prioritätswarteschlange (Top-K-Aufgaben)
  bisect        binäre Suche in einer sortierten Liste
  functools     lru_cache (Memoisierung!), reduce
  re            reguläre Ausdrücke

deque ist das, was alle vergessen: vorne aus einer Liste zu entfernen ist O(n),
aus einer deque O(1). Das ist der Unterschied zwischen bestanden und Zeitlimit
bei einer BFS- oder Schiebefenster-Aufgabe.

    from collections import deque
    q = deque([1, 2, 3])
    q.append(4); q.appendleft(0)
    q.popleft()      # O(1)

Jede Datei, die du schreibst, ist selbst ein Modul. `if __name__ == "__main__":`
schützt Code, der nur laufen soll, wenn die Datei direkt ausgeführt wird.""",
 "takeaway": "deque für O(1) vorne, lru_cache für gratis Memoisierung, Counter fürs Zählen.",
 "example": '''import math
from collections import deque, Counter
from itertools import accumulate, combinations
from functools import lru_cache
import bisect, heapq

print("ggT(84, 36):", math.gcd(84, 36))
print("ceil(2.1):", math.ceil(2.1), "| floor(2.9):", math.floor(2.9))
print("comb(5, 2):", math.comb(5, 2))

q = deque([1, 2, 3])
q.appendleft(0)
print("deque:", q, "| popleft ->", q.popleft(), q)

print("laufende Summen:", list(accumulate([1, 2, 3, 4])))
print("Paare:", list(combinations("abc", 2)))
print("Counter:", Counter("banane").most_common())

nums = [1, 3, 5, 7, 9]
print("6 einfügen an Index:", bisect.bisect_left(nums, 6))
print("die 3 größten:", heapq.nlargest(3, [5, 1, 9, 3, 7]))

@lru_cache(maxsize=None)
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)
print("fib(60) sofort:", fib(60))

if __name__ == "__main__":
    print("diese Datei wurde direkt ausgeführt")
''',
 "task": {
  "title": "Die k häufigsten Wörter",
  "statement": """Schreib top_k(words, k), das die k häufigsten Wörter zurückgibt, das häufigste
zuerst. Gleichstand wird alphabetisch aufgelöst.

  top_k(["a", "b", "a", "c", "b", "a"], 2) -> ["a", "b"]

collections.Counter erledigt das Zählen; für den Gleichstand brauchst du einen
Sortierschlüssel (-anzahl, wort).""",
  "hints": ["counts = Counter(words)",
            "ordered = sorted(counts, key=lambda w: (-counts[w], w))",
            "return ordered[:k]"],
 },
},

# ==================================================== 4. INTERVIEW-TECHNIK
"complexity": {
 "section": "Interview-Technik",
 "title": "Big-O in der Praxis",
 "theory": """Codility und Konsorten prüfen nicht nur, ob deine Antwort richtig ist — sie
prüfen, ob sie schnell genug ist. Lern, die Kosten deines eigenen Codes zu lesen.

  O(1)        feste Anzahl Schritte         d[key], lst[i], Rechnen
  O(log n)    halbiert bei jedem Schritt    binäre Suche
  O(n)        ein Durchlauf                 sum(lst), eine einzelne for-Schleife
  O(n log n)  Sortieren                     sorted(lst), lst.sort()
  O(n^2)      Schleife in einer Schleife    zwei verschachtelte for-Schleifen
  O(2^n)      naive Rekursion über Teilmengen   die "zu langsam"-Klippe

Versteckte Kosten, die oft übersehen werden:
    x in liste       O(n)      aber  x in set / dict  ist O(1)
    liste.pop(0)     O(n)      aber  deque.popleft()  ist O(1)
    liste.insert(0,x) O(n)
    s += "x" in Schleife  O(n^2)   bau eine Liste und "".join sie
    Sortieren        O(n log n) — oft die gewollte Antwort, kein Versagen

Faustregel für 1 Sekunde Limit: etwa 10^7 bis 10^8 einfache Operationen. Für
n = 100000 läuft eine O(n^2)-Lösung (10^10 Schritte) also ins Zeitlimit,
O(n log n) ist problemlos.

Der Interview-Zug: sag die Komplexität laut, und dann, was sie verbessern würde.
"Das ist O(n^2); mit einem Hash-Set wird es O(n)." Dieser Satz bringt Punkte.""",
 "takeaway": "n^2 stirbt oberhalb von ~10k Elementen. Sets, Sortieren und ein sauberer Durchlauf sind die Rettung.",
 "example": '''import time

n = 20000
daten = list(range(n))
als_set = set(daten)

start = time.perf_counter()
treffer = sum(1 for x in range(0, n, 200) if x in daten)      # O(n) pro Suche
listen_zeit = time.perf_counter() - start

start = time.perf_counter()
treffer = sum(1 for x in range(0, n, 200) if x in als_set)    # O(1) pro Suche
set_zeit = time.perf_counter() - start

print(f"Suchen in der Liste: {listen_zeit * 1000:8.2f} ms")
print(f"Suchen im Set:       {set_zeit * 1000:8.2f} ms")
print(f"Beschleunigung: {listen_zeit / max(set_zeit, 1e-9):.0f}x")

# String-Aufbau
start = time.perf_counter()
s = ""
for i in range(20000):
    s += "x"
verketten = time.perf_counter() - start

start = time.perf_counter()
s = "".join("x" for _ in range(20000))
gejoint = time.perf_counter() - start
print(f"\\n+= verketten: {verketten * 1000:6.2f} ms | join: {gejoint * 1000:6.2f} ms")
''',
 "task": {
  "title": "Gibt es ein Duplikat? (muss O(n) sein)",
  "statement": """Schreib has_duplicate(nums) -> True, wenn irgendein Wert mehr als einmal vorkommt.

  has_duplicate([1, 2, 3, 1]) -> True
  has_duplicate([1, 2, 3])    -> False

Einer der versteckten Tests wirft dir 200 000 Zahlen hin, bei etwa einer Sekunde
Budget — eine verschachtelte Schleife fällt also durch. Nimm ein set (oder
vergleiche len(set(nums)) mit len(nums)).""",
  "hints": ["len(set(nums)) != len(nums) ist der Einzeiler",
            "Oder: ein `gesehen`-Set führen und True zurückgeben, sobald ein Wert erneut auftaucht",
            "Schreib hier bloß kein `for i ... for j ...`"],
 },
},

"twopointer": {
 "section": "Interview-Technik",
 "title": "Zwei Zeiger & Schiebefenster",
 "theory": """Zwei Indizes, die durch ein Array laufen, ersetzen eine verschachtelte Schleife
und machen aus O(n^2) ein O(n). Zwei Formen decken die meisten Aufgaben ab.

1) Von beiden Enden (braucht ein SORTIERTES Array):

    links, rechts = 0, len(nums) - 1
    while links < rechts:
        summe = nums[links] + nums[rechts]
        if summe == ziel: return (links, rechts)
        if summe < ziel:  links += 1      # mehr nötig
        else:             rechts -= 1     # weniger nötig

2) Schiebefenster (zusammenhängender Teilbereich):

    links = 0
    for rechts, wert in enumerate(nums):
        fenster_summe += wert
        while fenster_summe > limit:      # schrumpfen, bis es wieder passt
            fenster_summe -= nums[links]
            links += 1
        best = max(best, rechts - links + 1)

Jeder Index wandert nur vorwärts, deshalb ist das Ganze O(n), obwohl da zwei
Schleifen stehen.

Signale, dass eine Aufgabe das will: "zusammenhängend", "Teilarray",
"Teilstring", "Paar mit Summe", "längstes/kürzestes Fenster, sodass",
"sortiertes Array".""",
 "takeaway": "'zusammenhängend' oder 'sortiertes Paar' => zwei Zeiger. Beide Indizes laufen nur vorwärts.",
 "example": '''def two_sum_sorted(nums, ziel):
    links, rechts = 0, len(nums) - 1
    while links < rechts:
        summe = nums[links] + nums[rechts]
        if summe == ziel:
            return (links, rechts)
        if summe < ziel:
            links += 1
        else:
            rechts -= 1
    return None

print(two_sum_sorted([1, 3, 4, 7, 11], 10))

def laengster_eindeutiger(text):
    """Längster Teilstring ohne wiederholtes Zeichen."""
    zuletzt, links, best = {}, 0, 0
    for rechts, ch in enumerate(text):
        if ch in zuletzt and zuletzt[ch] >= links:
            links = zuletzt[ch] + 1
        zuletzt[ch] = rechts
        best = max(best, rechts - links + 1)
    return best

print("längster eindeutiger in 'abcabcbb':", laengster_eindeutiger("abcabcbb"))

def max_fenster_summe(nums, k):
    """Größte Summe von k aufeinanderfolgenden Werten — festes Fenster."""
    fenster = sum(nums[:k])
    best = fenster
    for i in range(k, len(nums)):
        fenster += nums[i] - nums[i - k]
        best = max(best, fenster)
    return best

print("größte Summe von 3 in Folge:", max_fenster_summe([2, 1, 5, 1, 3, 2], 3))
''',
 "task": {
  "title": "Längste Serie gleicher Werte",
  "statement": """Schreib longest_run(nums), das die Länge der längsten Serie IDENTISCHER
aufeinanderfolgender Werte zurückgibt.

  longest_run([1, 1, 2, 2, 2, 3]) -> 3
  longest_run([])                 -> 0

Ein Durchlauf, ein Zähler. Keine verschachtelten Schleifen.""",
  "hints": ["Führ `aktuell` (Serie bisher) und `best` mit",
            "Wenn nums[i] == nums[i-1]: aktuell += 1, sonst aktuell = 1",
            "best = max(best, aktuell) in jedem Schritt"],
 },
},

"prefix": {
 "section": "Interview-Technik",
 "title": "Präfixsummen & Zähltricks",
 "theory": """Einmal vorberechnen, dann jede Anfrage in O(1) beantworten. Das ist der Trick
hinter einem großen Teil von Codilitys "Prefix Sums"- und "Counting
Elements"-Aufgaben.

Präfixsummen:

    prefix = [0] * (len(nums) + 1)
    for i, wert in enumerate(nums):
        prefix[i + 1] = prefix[i] + wert

    # Summe von nums[a..b] einschließlich, in O(1):
    summe = prefix[b + 1] - prefix[a]

Oder einfach: from itertools import accumulate.

Counting Sort / Eimer-Zählen — wenn die Werte kleine ganze Zahlen sind, zähl sie
in ein festes Array, statt zu sortieren:

    counts = [0] * (max_wert + 1)
    for wert in nums:
        counts[wert] += 1

Das "Array aufteilen"-Muster (Codilitys TapeEquilibrium und die halbe
"finde den Drehpunkt"-Familie): einmal von links nach rechts laufen, dabei die
linke Summe mitführen und die rechte als gesamt - links ableiten. Ein
Durchlauf, O(n).

    gesamt = sum(nums)
    links = 0
    for i in range(len(nums) - 1):
        links += nums[i]
        rechts = gesamt - links
        best = min(best, abs(links - rechts))""",
 "takeaway": "Präfixsummen einmal bauen, Bereichsanfragen dann in O(1). gesamt - links = rechts.",
 "example": '''from itertools import accumulate

nums = [3, 1, 4, 1, 5, 9, 2, 6]

prefix = [0]
for wert in nums:
    prefix.append(prefix[-1] + wert)
print("Präfix:", prefix)

def bereichssumme(a, b):
    return prefix[b + 1] - prefix[a]

print("Summe nums[2..5] =", bereichssumme(2, 5), "(Probe:", sum(nums[2:6]), ")")
print("accumulate:", list(accumulate(nums)))

# kleinstmöglicher Unterschied beim Zweiteilen des Arrays
gesamt, links, best = sum(nums), 0, float("inf")
for i in range(len(nums) - 1):
    links += nums[i]
    best = min(best, abs(links - (gesamt - links)))
print("bester Teilungsunterschied:", best)

# Zählen statt Sortieren, wenn die Werte klein sind
werte = [3, 1, 2, 3, 3, 1]
counts = [0] * (max(werte) + 1)
for w in werte:
    counts[w] += 1
print("Anzahl je Wert:", counts)
print("häufigster Wert:", counts.index(max(counts)))
''',
 "task": {
  "title": "Gleichgewichtsindex",
  "statement": """Ein Gleichgewichtsindex ist eine Position, an der die Summe von allem LINKS
davon gleich der Summe von allem RECHTS davon ist (das Element selbst zählt zu
keiner Seite).

Schreib equilibrium(nums), das den KLEINSTEN solchen Index zurückgibt, oder -1,
wenn es keinen gibt.

  equilibrium([-1, 3, -4, 5, 1, -6, 2, 1]) -> 1
  equilibrium([1, 2, 3])                   -> -1

Muss O(n) sein: eine laufende linke Summe führen und die rechte Seite aus der
Gesamtsumme ableiten.""",
  "hints": ["gesamt = sum(nums); links = 0",
            "An Index i: rechts = gesamt - links - nums[i]",
            "Erst vergleichen, dann links += nums[i] — in dieser Reihenfolge"],
 },
},

"recursion": {
 "section": "Interview-Technik",
 "title": "Rekursion & Memoisierung",
 "theory": """Eine rekursive Funktion ruft sich selbst mit einer kleineren Version des
Problems auf. Immer zwei Teile:

    def fakultaet(n):
        if n <= 1:          # 1. BASISFALL — beendet die Rekursion
            return 1
        return n * fakultaet(n - 1)   # 2. SCHRITT — geht Richtung Basisfall

Naive Rekursion kann explodieren. fib(35) macht ~30 Millionen Aufrufe, weil es
dieselben Werte immer wieder neu berechnet. Memoisierung repariert das gratis:

    from functools import lru_cache

    @lru_cache(maxsize=None)
    def fib(n):
        return n if n < 2 else fib(n - 1) + fib(n - 2)

Dieser eine Dekorator macht aus O(2^n) ein O(n). Das ist die billigste
dynamische Programmierung, die du je schreiben wirst.

Pythons Rekursionslimit liegt bei etwa 1000 Ebenen, tiefe Rekursion über eine
große Liste läuft also in einen RecursionError — solche Fälle schreibt man
iterativ mit einem eigenen Stapel.

Bottom-up-DP ist dieselbe Idee ohne Aufrufstapel:

    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]""",
 "takeaway": "Basisfall zuerst. @lru_cache macht aus exponentieller Rekursion lineare.",
 "example": '''from functools import lru_cache
import time

def fib_langsam(n):
    return n if n < 2 else fib_langsam(n - 1) + fib_langsam(n - 2)

@lru_cache(maxsize=None)
def fib_schnell(n):
    return n if n < 2 else fib_schnell(n - 1) + fib_schnell(n - 2)

start = time.perf_counter()
fib_langsam(28)
langsam = time.perf_counter() - start
start = time.perf_counter()
fib_schnell(28)
schnell = time.perf_counter() - start
print(f"fib(28) naiv: {langsam*1000:.1f} ms | memoisiert: {schnell*1000:.4f} ms")
print("fib(200) memoisiert:", fib_schnell(200))

def flach_machen(verschachtelt):
    out = []
    for item in verschachtelt:
        if isinstance(item, list):
            out.extend(flach_machen(item))
        else:
            out.append(item)
    return out

print("flach:", flach_machen([1, [2, [3, [4, 5]], 6], 7]))

# Bottom-up: wie viele Wege gibt es, n Stufen mit 1er- oder 2er-Schritten zu nehmen
def steigen(n):
    dp = [0] * (n + 1)
    dp[0] = 1
    for i in range(1, n + 1):
        dp[i] = dp[i - 1] + (dp[i - 2] if i >= 2 else 0)
    return dp[n]

print("Wege für 10 Stufen:", steigen(10))
''',
 "task": {
  "title": "Tief verschachtelte Liste summieren",
  "statement": """Schreib deep_sum(nested), das alle Zahlen in einer beliebig tief verschachtelten
Liste aus Zahlen und Listen aufaddiert.

  deep_sum([1, [2, [3, [4]]], 5]) -> 15
  deep_sum([])                    -> 0

Nutze isinstance(item, list), um zu entscheiden, ob du rekursiv weitergehst.""",
  "hints": ["gesamt = 0, dann über die Elemente laufen",
            "if isinstance(item, list): gesamt += deep_sum(item)",
            "else: gesamt += item"],
 },
},

"io": {
 "section": "Interview-Technik",
 "title": "Eingabe lesen & Ausgabe schreiben",
 "theory": """Manche Prüfsysteme geben dir eine Funktion zum Ausfüllen (so macht es Codility).
Andere füttern dich über stdin und lesen dein stdout. Kenn beides.

Von stdin lesen:

    zeile = input()                      eine Zeile, als String
    n = int(input())                     eine Zahl
    nums = list(map(int, input().split()))   "3 1 4" -> [3, 1, 4]

    import sys
    daten = sys.stdin.read().split()     alles auf einmal — viel schneller
    for zeile in sys.stdin:              Zeile für Zeile

Ausgeben:

    print(a, b)              -> "a b"
    print(*nums)             -> entpackt die Liste: "1 2 3"
    print(", ".join(map(str, nums)))
    print(f"{wert:.2f}")     zwei Nachkommastellen
    print(x, end="")         kein Zeilenumbruch

Formatier-Spickzettel:
    f"{n:5d}"     rechtsbündig in 5 Spalten
    f"{n:<5}"     linksbündig
    f"{n:05d}"    mit Nullen aufgefüllt  -> 00042
    f"{x:.3f}"    3 Nachkommastellen
    f"{x:,}"      Tausendertrenner -> 1,234,567
    f"{p:.1%}"    Prozent -> 42.0%

In dieser App: der Spielwiesen-Tab hat ein stdin-Feld, du kannst den
stdin-Lesestil also genau so üben, wie ein Prüfsystem ihn ausführt.""",
 "takeaway": "list(map(int, input().split())) liest eine Zahlenzeile. f-Strings formatieren sie zurück.",
 "example": '''# Dieses Beispiel benutzt eine feste Eingabe, damit es ohne Tippen läuft.
roh = """3
5 3 8
Ada
"""
zeilen = roh.strip().split("\\n")

n = int(zeilen[0])
nums = list(map(int, zeilen[1].split()))
name = zeilen[2]

print("n =", n)
print("nums =", nums, "Summe =", sum(nums))
print("name =", name)

print("entpackt:", *nums)
print("verbunden:", ", ".join(map(str, nums)))

print()
print(f"{'Artikel':<12}{'Anz':>5}{'Preis':>10}")
for artikel, anzahl, preis in [("Apfel", 3, 1.5), ("Wassermelone", 12, 4.25)]:
    print(f"{artikel:<12}{anzahl:>5}{preis:>10.2f}")

print()
print(f"aufgefüllt: {42:05d} | Prozent: {0.4237:.1%} | groß: {1234567:,}")
''',
 "task": {
  "title": "Eine Kassenbon-Zeile formatieren",
  "statement": """Schreib receipt_line(name, qty, price), das eine formatierte Zeile zurückgibt:

  * name linksbündig in 12 Spalten
  * qty rechtsbündig in 4 Spalten
  * die Zeilensumme (qty * price) rechtsbündig in 10 Spalten mit 2 Nachkommastellen

receipt_line("apple", 3, 1.5) -> "apple          3      4.50"

(das sind 12 + 4 + 10 = 26 Zeichen)""",
  "hints": ['f"{name:<12}" richtet in 12 Spalten linksbündig aus',
            'f"{qty:>4}" richtet in 4 Spalten rechtsbündig aus',
            'f"{qty * price:>10.2f}" für die Summe'],
 },
},

"debug": {
 "section": "Interview-Technik",
 "title": "Einen Traceback lesen",
 "theory": """Ein Traceback wird von UNTEN nach OBEN gelesen. Die letzte Zeile sagt, was
schiefging; die Zeile darüber, wo.

    Traceback (most recent call last):
      File "your_code.py", line 7, in <module>
        print(total(prices))
      File "your_code.py", line 4, in total
        return sum(p["cost"] for p in prices)
    KeyError: 'cost'

Lies es als: "KeyError 'cost'" passierte in total() in Zeile 4.

Die häufigen Fehler und ihre übliche Ursache:

  IndexError: list index out of range   -> Zähler um eins daneben, oder leere Liste
  KeyError: 'x'                         -> fehlender dict-Schlüssel; nimm .get()
  TypeError: 'NoneType' object is not subscriptable
                                        -> eine Funktion lieferte None (return vergessen!)
  TypeError: unsupported operand type(s) for +: 'int' and 'str'
                                        -> Zahl mit Text vermischt
  ValueError: invalid literal for int() -> int("12a")
  UnboundLocalError                     -> Variable benutzt, bevor sie zugewiesen wurde
  IndentationError / SyntaxError        -> das Dach ^ zeigt auf die Stelle

Debuggen ohne Debugger: gib die FORM deiner Daten aus, nicht nur den Wert.

    print(f"{i=} {links=} {rechts=} {fenster=}")     # ab 3.8, selbstdokumentierend

Dieses `=` im f-String druckt "i=3 links=0" — das schnellste Debug-Werkzeug der
ganzen Sprache.""",
 "takeaway": "Tracebacks von unten lesen. `TypeError: NoneType` heißt fast immer: return vergessen.",
 "example": '''def summe(preise):
    return sum(p["kosten"] for p in preise)

artikel = [{"name": "Feige", "kosten": 2}, {"name": "Birne", "preis": 3}]

try:
    print(summe(artikel))
except KeyError as exc:
    print("KeyError beim Schlüssel:", exc, "-> ein dict nutzt 'preis', nicht 'kosten'")

def sichere_summe(preise):
    return sum(p.get("kosten", p.get("preis", 0)) for p in preise)
print("korrigierte Summe:", sichere_summe(artikel))

# der "return vergessen"-Fehler
def verdoppeln_kaputt(n):
    n * 2          # kein return -> None

ergebnis = verdoppeln_kaputt(5)
print("ergebnis ist", ergebnis, "vom Typ", type(ergebnis).__name__)

# selbstdokumentierende f-Strings
links, rechts, fenster = 0, 4, [1, 2, 3]
print(f"{links=} {rechts=} {fenster=} {len(fenster)=}")

nums = [1, 2, 3]
for i in range(len(nums)):
    print(f"Index {i} -> {nums[i]}")
print("der klassische Fehler um eins wäre range(len(nums) + 1)")
''',
 "task": {
  "title": "Repariere die kaputte Funktion",
  "statement": """Die Funktion unten SOLL den Durchschnitt der Punktzahlen einer Liste von
Studenten-dicts zurückgeben, auf 1 Nachkommastelle gerundet, und 0.0 für eine
leere Liste. Sie hat drei Fehler.

Repariere sie:

    def average_score(students):
        total = 0
        for s in students:
            total += s["score"]
        return round(total / len(students), 1)

Zu findende Fehler: sie stürzt bei einer leeren Liste ab, sie stürzt ab, wenn
ein Student keinen "score"-Schlüssel hat (eine fehlende Punktzahl zählt als 0),
und sie muss auch dann einen float liefern, wenn der Durchschnitt glatt ist.""",
  "hints": ["if not students: return 0.0  — noch vor der Division",
            's.get("score", 0) statt s["score"]',
            "round(x, 1) liefert bereits einen float, wenn x einer ist — teile mit /"],
 },
},
}
