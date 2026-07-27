"""Randomised practice drills.

Every drill is a GENERATOR: each time you ask for it you get a fresh statement
with different numbers, different words and freshly computed test cases. That
is the point — you can grind the same concept twenty times without ever
memorising the answer.

Because the statements interpolate their random values, the German version has
to be written right next to the English one (the `de=` argument) rather than in
a separate translation file like the lessons and interview problems.
"""
from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Callable

import i18n
from tasks import CITIES, NAMES, WORDS, Task, make_cases, starter_for

REGISTRY: list["Drill"] = []


@dataclass
class Drill:
    id: str
    title: str
    title_de: str
    topic: str
    difficulty: str
    build: Callable[[random.Random], Task]


def drill(did: str, title: str, title_de: str, topic: str, difficulty: str = "Easy"):
    def wrap(fn):
        REGISTRY.append(Drill(did, title, title_de, topic, difficulty, fn))
        return fn
    return wrap


def _task(rng, did, title, topic, difficulty, func, statement, params, ref,
          samples, hints, solution, doc="", de=None) -> Task:
    task = Task(
        id=f"drill_{did}_{rng.randrange(10**6)}",
        title=title, func=func, statement=statement.strip(),
        starter=starter_for(func, params, doc),
        cases=make_cases(ref, samples, hidden_from=3),
        hints=hints, solution=solution, difficulty=difficulty, topic=topic,
        source="drill",
    )
    if de and de.get("statement"):
        de = dict(de)
        de["statement"] = de["statement"].strip()
    return i18n.localize_task(task, de)


def rand_list(rng, n=None, lo=-20, hi=40):
    n = n if n is not None else rng.randint(4, 9)
    return [rng.randint(lo, hi) for _ in range(n)]


def rand_word(rng):
    return rng.choice(WORDS)


def rand_text(rng, n=None):
    n = n or rng.randint(3, 6)
    return " ".join(rng.choice(WORDS) for _ in range(n))


# =========================================================== BASICS / NUMBERS
@drill("mult_table", "Multiplication row", "Reihe im Einmaleins", "Basics")
def _mult_table(rng):
    k = rng.randint(3, 12)
    limit = rng.choice([5, 8, 10, 12])

    def ref(n):
        return [n * i for i in range(1, limit + 1)]

    return _task(rng, "mult_table", f"Times table up to {limit}", "Basics", "Easy",
                 "table", f"""
Write table(n) that returns the first {limit} multiples of n as a list.

  table({k}) -> {ref(k)}

Start at 1 * n, end at {limit} * n.""",
                 "n", ref, [(k,), (1,), (0,), (rng.randint(2, 9),),
                            (-3,), (rng.randint(20, 50),)],
                 [f"range(1, {limit + 1}) gives you 1..{limit}",
                  "A list comprehension does this in one line"],
                 f"def table(n):\n    return [n * i for i in range(1, {limit + 1})]\n",
                 de={
                     "title": f"Einmaleins bis {limit}",
                     "statement": f"""
Schreib table(n), das die ersten {limit} Vielfachen von n als Liste zurückgibt.

  table({k}) -> {ref(k)}

Fang bei 1 * n an und hör bei {limit} * n auf.""",
                     "hints": [f"range(1, {limit + 1}) liefert dir 1..{limit}",
                               "Eine List Comprehension erledigt das in einer Zeile"],
                 })


@drill("discount", "Price after discount", "Preis nach Rabatt", "Basics")
def _discount(rng):
    pct = rng.choice([5, 10, 15, 20, 25, 30, 40])
    price = rng.choice([19.99, 49.5, 120.0, 8.75, 250.0])

    def ref(price, percent):
        return round(price * (1 - percent / 100), 2)

    return _task(rng, "discount", f"Apply a {pct}% discount", "Basics", "Easy",
                 "final_price", f"""
Write final_price(price, percent) returning the price after a percentage
discount, rounded to 2 decimals.

  final_price({price}, {pct}) -> {ref(price, pct)}

percent is a whole number like {pct}, meaning {pct}%.""",
                 "price, percent", ref,
                 [(price, pct), (100.0, 50), (10.0, 0),
                  (rng.choice([33.33, 7.5]), rng.choice([12, 60])),
                  (0.0, 25), (999.99, 100)],
                 ["A discount of p% leaves you (100 - p)% of the price",
                  "price * (1 - percent / 100)",
                  "round(value, 2) at the end"],
                 "def final_price(price, percent):\n"
                 "    return round(price * (1 - percent / 100), 2)\n",
                 de={
                     "title": f"{pct} % Rabatt anwenden",
                     "statement": f"""
Schreib final_price(price, percent), das den Preis nach einem prozentualen
Rabatt zurückgibt, auf 2 Nachkommastellen gerundet.

  final_price({price}, {pct}) -> {ref(price, pct)}

percent ist eine ganze Zahl wie {pct} und bedeutet {pct} %.""",
                     "hints": ["Ein Rabatt von p % lässt dir (100 - p) % des Preises",
                               "price * (1 - percent / 100)",
                               "Am Ende round(wert, 2)"],
                 })


@drill("digit_sum", "Digit sum / digital root", "Quersumme / Ziffernwurzel", "Basics")
def _digit_sum(rng):
    n = rng.randint(1000, 999999)
    root = rng.random() < 0.5
    if root:
        def ref(n):
            n = abs(n)
            while n > 9:
                n = sum(int(d) for d in str(n))
            return n
        goal = ("keeps adding the digits until a single digit is left "
                "(the 'digital root')")
        goal_de = ("die Ziffern so lange addiert, bis nur noch eine einzige "
                   "übrig ist (die 'Ziffernwurzel')")
        sol = ("def digit_sum(n):\n    n = abs(n)\n    while n > 9:\n"
               "        n = sum(int(d) for d in str(n))\n    return n\n")
        hint3, hint3_de = "while n > 9: repeat", "while n > 9: wiederholen"
    else:
        def ref(n):
            return sum(int(d) for d in str(abs(n)))
        goal = "adds up the digits once"
        goal_de = "die Ziffern einmal aufaddiert"
        sol = "def digit_sum(n):\n    return sum(int(d) for d in str(abs(n)))\n"
        hint3 = "sum(...) over a generator"
        hint3_de = "sum(...) über einen Generator"

    return _task(rng, "digit_sum", "Digital root" if root else "Digit sum",
                 "Basics", "Easy", "digit_sum", f"""
Write digit_sum(n) that {goal}.

  digit_sum({n}) -> {ref(n)}

Negative numbers count as positive: digit_sum(-45) -> {ref(-45)}.""",
                 "n", ref, [(n,), (0,), (-45,), (rng.randint(10, 99),),
                            (999999999,), (7,)],
                 ["str(n) lets you walk over the digits",
                  "int(d) turns one digit-character back into a number", hint3],
                 sol,
                 de={
                     "title": "Ziffernwurzel" if root else "Quersumme",
                     "statement": f"""
Schreib digit_sum(n), das {goal_de}.

  digit_sum({n}) -> {ref(n)}

Negative Zahlen zählen als positiv: digit_sum(-45) -> {ref(-45)}.""",
                     "hints": ["str(n) lässt dich über die Ziffern laufen",
                               "int(d) macht aus einem Ziffernzeichen wieder eine Zahl",
                               hint3_de],
                 })


@drill("gcd_lcm", "GCD and LCM", "ggT und kgV", "Basics", "Medium")
def _gcd(rng):
    a, b = rng.randint(12, 200), rng.randint(12, 200)

    def ref(a, b):
        x, y = abs(a), abs(b)
        while y:
            x, y = y, x % y
        return [x, abs(a * b) // x if x else 0]

    return _task(rng, "gcd_lcm", "GCD and LCM", "Basics", "Medium",
                 "gcd_lcm", f"""
Write gcd_lcm(a, b) that returns [gcd, lcm] as a two-element list.

  gcd_lcm({a}, {b}) -> {ref(a, b)}

Implement Euclid's algorithm yourself (no math.gcd for this drill):
repeatedly replace (a, b) with (b, a % b) until b is 0.
Then lcm = a * b // gcd.""",
                 "a, b", ref, [(a, b), (12, 18), (7, 13),
                               (rng.randint(2, 50), rng.randint(2, 50)),
                               (100, 100), (1, 999)],
                 ["while b: a, b = b, a % b", "After the loop, a IS the gcd",
                  "lcm = abs(a * b) // gcd, computed from the ORIGINAL values"],
                 "def gcd_lcm(a, b):\n    x, y = abs(a), abs(b)\n    while y:\n"
                 "        x, y = y, x % y\n    return [x, abs(a * b) // x if x else 0]\n",
                 de={
                     "title": "ggT und kgV",
                     "statement": f"""
Schreib gcd_lcm(a, b), das [ggT, kgV] als zweielementige Liste zurückgibt.

  gcd_lcm({a}, {b}) -> {ref(a, b)}

Implementier Euklids Algorithmus selbst (kein math.gcd bei dieser Übung):
ersetz (a, b) immer wieder durch (b, a % b), bis b null ist.
Dann ist kgV = a * b // ggT.""",
                     "hints": ["while b: a, b = b, a % b",
                               "Nach der Schleife IST a der ggT",
                               "kgV = abs(a * b) // ggT, berechnet aus den URSPRÜNGLICHEN Werten"],
                 })


@drill("fizz_variant", "Custom FizzBuzz", "Eigenes FizzBuzz", "Basics")
def _fizz(rng):
    d1, d2 = rng.sample([2, 3, 4, 5, 6, 7], 2)
    w1, w2 = rng.sample(["Pling", "Plang", "Plong", "Zip", "Zap", "Boom", "Woof"], 2)
    n = rng.randint(10, 20)

    def ref(n):
        out = []
        for i in range(1, n + 1):
            word = ""
            if i % d1 == 0:
                word += w1
            if i % d2 == 0:
                word += w2
            out.append(word or i)
        return out

    return _task(rng, "fizz_variant", f"{w1}/{w2} for {d1} and {d2}", "Basics", "Easy",
                 "play", f"""
Write play(n) returning a list for 1..n where:

  * multiples of {d1} become "{w1}"
  * multiples of {d2} become "{w2}"
  * multiples of BOTH become "{w1}{w2}" (glued together, {w1} first)
  * everything else stays the number itself (an int)

  play(10) -> {ref(10)}""",
                 "n", ref, [(n,), (1,), (d1 * d2,), (0,), (25,), (d1,)],
                 [f"Build the word: start empty, add \"{w1}\" if i % {d1} == 0, "
                  f"then \"{w2}\" if i % {d2} == 0",
                  "An empty string is falsy: `word or i` picks the number when no word matched"],
                 f'def play(n):\n    out = []\n    for i in range(1, n + 1):\n'
                 f'        word = ""\n        if i % {d1} == 0:\n            word += "{w1}"\n'
                 f'        if i % {d2} == 0:\n            word += "{w2}"\n'
                 f'        out.append(word or i)\n    return out\n',
                 de={
                     "title": f"{w1}/{w2} für {d1} und {d2}",
                     "statement": f"""
Schreib play(n), das eine Liste für 1..n zurückgibt, wobei:

  * Vielfache von {d1} zu "{w1}" werden
  * Vielfache von {d2} zu "{w2}" werden
  * Vielfache von BEIDEN zu "{w1}{w2}" werden (aneinandergehängt, {w1} zuerst)
  * alles andere die Zahl selbst bleibt (als int)

  play(10) -> {ref(10)}""",
                     "hints": [f'Bau das Wort auf: leer anfangen, "{w1}" anhängen wenn '
                               f'i % {d1} == 0, dann "{w2}" wenn i % {d2} == 0',
                               "Ein leerer String ist falsy: `word or i` nimmt die Zahl, "
                               "wenn kein Wort gepasst hat"],
                 })


# ==================================================================== STRINGS
@drill("count_char", "Count a character", "Ein Zeichen zählen", "Strings")
def _count_char(rng):
    ch = rng.choice("aeioustrn")
    text = rand_text(rng)
    ignore_case = rng.random() < 0.5

    def ref(text):
        return (text.lower() if ignore_case else text).count(ch)

    extra = "\nUpper and lower case both count." if ignore_case else \
            "\nOnly lower-case matches count."
    extra_de = "\nGroß- und Kleinschreibung zählen beide." if ignore_case else \
               "\nNur Treffer in Kleinschreibung zählen."
    return _task(rng, "count_char", f"Count '{ch}'", "Strings", "Easy",
                 "count_it", f"""
Write count_it(text) that returns how many times the letter '{ch}' appears.

  count_it({text!r}) -> {ref(text)}
{extra}""",
                 "text", ref, [(text,), ("", ), (ch * 4,),
                               (rand_text(rng),), (rand_text(rng).upper(),),
                               (rand_word(rng),)],
                 ["str.count(sub) does the counting for you",
                  "text.lower() first if case must be ignored" if ignore_case
                  else "No case conversion needed here"],
                 f'def count_it(text):\n    return text{".lower()" if ignore_case else ""}'
                 f'.count("{ch}")\n',
                 de={
                     "title": f"'{ch}' zählen",
                     "statement": f"""
Schreib count_it(text), das zurückgibt, wie oft der Buchstabe '{ch}' vorkommt.

  count_it({text!r}) -> {ref(text)}
{extra_de}""",
                     "hints": ["str.count(teil) übernimmt das Zählen für dich",
                               "Erst text.lower(), wenn die Groß-/Kleinschreibung egal ist"
                               if ignore_case else
                               "Hier ist keine Umwandlung der Groß-/Kleinschreibung nötig"],
                 })


@drill("caesar", "Caesar cipher", "Caesar-Verschlüsselung", "Strings", "Medium")
def _caesar(rng):
    shift = rng.randint(1, 25)
    word = rand_word(rng)

    def ref(text):
        out = []
        for ch in text:
            if ch.isalpha():
                base = ord("a") if ch.islower() else ord("A")
                out.append(chr((ord(ch) - base + shift) % 26 + base))
            else:
                out.append(ch)
        return "".join(out)

    return _task(rng, "caesar", f"Caesar shift by {shift}", "Strings", "Medium",
                 "encode", f"""
Write encode(text) that shifts every LETTER {shift} places forward in the
alphabet, wrapping z -> a. Non-letters stay untouched, and upper/lower case
is preserved.

  encode({word!r}) -> {ref(word)!r}
  encode("Hello, World!") -> {ref("Hello, World!")!r}""",
                 "text", ref, [(word,), ("Hello, World!",), ("",),
                               ("xyz XYZ",), (rand_text(rng),), ("123 !?",)],
                 ["ord(ch) gives the character code, chr(n) turns it back",
                  'base = ord("a") for lower case, ord("A") for upper',
                  "(ord(ch) - base + shift) % 26 + base does the wrap-around"],
                 f'def encode(text):\n    out = []\n    for ch in text:\n'
                 f'        if ch.isalpha():\n'
                 f'            base = ord("a") if ch.islower() else ord("A")\n'
                 f'            out.append(chr((ord(ch) - base + {shift}) % 26 + base))\n'
                 f'        else:\n            out.append(ch)\n    return "".join(out)\n',
                 de={
                     "title": f"Caesar-Verschiebung um {shift}",
                     "statement": f"""
Schreib encode(text), das jeden BUCHSTABEN {shift} Stellen im Alphabet nach
vorne schiebt, mit Umlauf z -> a. Nicht-Buchstaben bleiben unangetastet, und
Groß-/Kleinschreibung bleibt erhalten.

  encode({word!r}) -> {ref(word)!r}
  encode("Hello, World!") -> {ref("Hello, World!")!r}""",
                     "hints": ["ord(ch) liefert den Zeichencode, chr(n) macht ihn zurück",
                               'base = ord("a") für Klein-, ord("A") für Großbuchstaben',
                               "(ord(ch) - base + verschiebung) % 26 + base erledigt den Umlauf"],
                 })


@drill("vowels", "Vowels vs consonants", "Vokale und Konsonanten", "Strings")
def _vowels(rng):
    text = rand_text(rng)

    def ref(text):
        vowels = sum(1 for c in text.lower() if c in "aeiou")
        cons = sum(1 for c in text.lower() if c.isalpha() and c not in "aeiou")
        return {"vowels": vowels, "consonants": cons}

    return _task(rng, "vowels", "Vowel / consonant tally", "Strings", "Easy",
                 "tally", f"""
Write tally(text) returning a dict {{"vowels": v, "consonants": c}}.

Only letters count — digits, spaces and punctuation are ignored.
Case does not matter.

  tally({text!r}) -> {ref(text)}""",
                 "text", ref, [(text,), ("AEIOU xyz",), ("",),
                               ("hello world 123!",), (rand_word(rng),),
                               ("Rhythm",)],
                 ['Work on text.lower() so you only check "aeiou"',
                  "c.isalpha() filters out spaces, digits and punctuation",
                  "sum(1 for c in ... if ...) counts in one line"],
                 'def tally(text):\n    low = text.lower()\n'
                 '    vowels = sum(1 for c in low if c in "aeiou")\n'
                 '    consonants = sum(1 for c in low if c.isalpha() and c not in "aeiou")\n'
                 '    return {"vowels": vowels, "consonants": consonants}\n',
                 de={
                     "title": "Vokale / Konsonanten zählen",
                     "statement": f"""
Schreib tally(text), das ein dict {{"vowels": v, "consonants": c}} zurückgibt.

Nur Buchstaben zählen — Ziffern, Leerzeichen und Satzzeichen werden ignoriert.
Groß-/Kleinschreibung spielt keine Rolle.

  tally({text!r}) -> {ref(text)}

(Die Schlüssel bleiben englisch, weil die Tests sie so erwarten.)""",
                     "hints": ['Arbeite auf text.lower(), dann musst du nur "aeiou" prüfen',
                               "c.isalpha() filtert Leerzeichen, Ziffern und Satzzeichen heraus",
                               "sum(1 for c in ... if ...) zählt in einer Zeile"],
                 })


@drill("palindrome", "Palindrome check", "Palindrom-Prüfung", "Strings")
def _palindrome(rng):
    samples = ["A man, a plan, a canal: Panama", "race a car", "", "No 'x' in Nixon",
               rand_word(rng), "Was it a car or a cat I saw?"]
    rng.shuffle(samples)

    def ref(text):
        cleaned = [c.lower() for c in text if c.isalnum()]
        return cleaned == cleaned[::-1]

    return _task(rng, "palindrome", "Palindrome check", "Strings", "Easy",
                 "is_palindrome", f"""
Write is_palindrome(text) -> True if the text reads the same backwards,
IGNORING case, spaces and punctuation.

  is_palindrome("A man, a plan, a canal: Panama") -> True
  is_palindrome("race a car") -> False

The empty string counts as a palindrome.""",
                 "text", ref, [(s,) for s in samples],
                 ["Build a cleaned list: [c.lower() for c in text if c.isalnum()]",
                  "cleaned[::-1] is the reverse",
                  "Compare the cleaned version with its reverse"],
                 "def is_palindrome(text):\n"
                 "    cleaned = [c.lower() for c in text if c.isalnum()]\n"
                 "    return cleaned == cleaned[::-1]\n",
                 de={
                     "title": "Palindrom-Prüfung",
                     "statement": """
Schreib is_palindrome(text) -> True, wenn sich der Text rückwärts gleich liest,
wobei Groß-/Kleinschreibung, Leerzeichen und Satzzeichen IGNORIERT werden.

  is_palindrome("A man, a plan, a canal: Panama") -> True
  is_palindrome("race a car") -> False

Der leere String gilt als Palindrom.""",
                     "hints": ["Bau eine bereinigte Liste: [c.lower() for c in text if c.isalnum()]",
                               "cleaned[::-1] ist die Umkehrung",
                               "Vergleich die bereinigte Fassung mit ihrer Umkehrung"],
                 })


@drill("anagram", "Anagram check", "Anagramm-Prüfung", "Strings")
def _anagram(rng):
    w = rand_word(rng)
    shuffled = list(w)
    rng.shuffle(shuffled)
    scrambled = "".join(shuffled)

    def ref(a, b):
        return sorted(a.lower().replace(" ", "")) == sorted(b.lower().replace(" ", ""))

    return _task(rng, "anagram", "Anagram check", "Strings", "Easy",
                 "is_anagram", f"""
Write is_anagram(a, b) -> True if the two words use exactly the same letters.
Ignore case and spaces.

  is_anagram({w!r}, {scrambled!r}) -> {ref(w, scrambled)}
  is_anagram("Listen", "Silent") -> True
  is_anagram("abc", "abd") -> False""",
                 "a, b", ref, [(w, scrambled), ("Listen", "Silent"), ("abc", "abd"),
                               ("", ""), ("Dormitory", "Dirty Room"),
                               (rand_word(rng), rand_word(rng))],
                 ["sorted('cab') -> ['a','b','c'] — sort both and compare",
                  '.lower() and .replace(" ", "") normalise first'],
                 "def is_anagram(a, b):\n"
                 "    norm = lambda s: sorted(s.lower().replace(' ', ''))\n"
                 "    return norm(a) == norm(b)\n",
                 de={
                     "title": "Anagramm-Prüfung",
                     "statement": f"""
Schreib is_anagram(a, b) -> True, wenn beide Wörter aus genau denselben
Buchstaben bestehen. Groß-/Kleinschreibung und Leerzeichen ignorieren.

  is_anagram({w!r}, {scrambled!r}) -> {ref(w, scrambled)}
  is_anagram("Listen", "Silent") -> True
  is_anagram("abc", "abd") -> False""",
                     "hints": ["sorted('cab') -> ['a','b','c'] — beide sortieren und vergleichen",
                               '.lower() und .replace(" ", "") normalisieren vorher'],
                 })


@drill("rle", "Run-length encoding", "Lauflängenkodierung", "Strings", "Medium")
def _rle(rng):
    base = "".join(rng.choice("aabbccdxyz") for _ in range(rng.randint(6, 12)))

    def ref(text):
        if not text:
            return ""
        out, count = [], 1
        for i in range(1, len(text) + 1):
            if i < len(text) and text[i] == text[i - 1]:
                count += 1
            else:
                out.append(text[i - 1] + (str(count) if count > 1 else ""))
                count = 1
        return "".join(out)

    return _task(rng, "rle", "Run-length encoding", "Strings", "Medium",
                 "encode_runs", f"""
Write encode_runs(text) that compresses runs of identical characters.
A run of length 1 keeps NO number.

  encode_runs("aaabbc")  -> "a3b2c"
  encode_runs({base!r}) -> {ref(base)!r}
  encode_runs("")        -> ""

Build the result in a list and "".join it at the end.""",
                 "text", ref, [(base,), ("aaabbc",), ("",), ("abc",),
                               ("zzzzzzzzzzzz",),
                               ("".join(rng.choice("ab") for _ in range(10)),)],
                 ["Walk with an index and keep a `count` of the current run",
                  "When the next char differs (or you ran out), flush the run",
                  'Append char + (str(count) if count > 1 else "")'],
                 'def encode_runs(text):\n    if not text:\n        return ""\n'
                 '    out, count = [], 1\n    for i in range(1, len(text) + 1):\n'
                 '        if i < len(text) and text[i] == text[i - 1]:\n'
                 '            count += 1\n        else:\n'
                 '            out.append(text[i - 1] + (str(count) if count > 1 else ""))\n'
                 '            count = 1\n    return "".join(out)\n',
                 de={
                     "title": "Lauflängenkodierung",
                     "statement": f"""
Schreib encode_runs(text), das Folgen identischer Zeichen komprimiert.
Eine Folge der Länge 1 bekommt KEINE Zahl.

  encode_runs("aaabbc")  -> "a3b2c"
  encode_runs({base!r}) -> {ref(base)!r}
  encode_runs("")        -> ""

Bau das Ergebnis in einer Liste auf und mach am Ende "".join.""",
                     "hints": ["Lauf mit einem Index und führ einen `count` für die aktuelle Folge",
                               "Wenn das nächste Zeichen anders ist (oder der Text zu Ende), "
                               "schreib die Folge raus",
                               'Häng zeichen + (str(count) if count > 1 else "") an'],
                 })


@drill("title_words", "Word surgery", "Wort-Operationen", "Strings")
def _title_words(rng):
    mode = rng.choice(["reverse_each", "reverse_order", "capitalise_long", "drop_short"])
    limit = rng.randint(4, 6)
    text = rand_text(rng, 5)

    if mode == "reverse_each":
        desc = "reverses every word but keeps the word order"
        desc_de = "jedes Wort umdreht, aber die Wortreihenfolge beibehält"
        ref = lambda t: " ".join(w[::-1] for w in t.split())
        sol = 'return " ".join(w[::-1] for w in text.split())'
    elif mode == "reverse_order":
        desc = "reverses the ORDER of the words (each word itself unchanged)"
        desc_de = "die REIHENFOLGE der Wörter umdreht (jedes Wort selbst bleibt gleich)"
        ref = lambda t: " ".join(t.split()[::-1])
        sol = 'return " ".join(text.split()[::-1])'
    elif mode == "capitalise_long":
        desc = f"UPPER-CASES every word longer than {limit} characters, leaves the rest alone"
        desc_de = (f"jedes Wort mit mehr als {limit} Zeichen in GROSSBUCHSTABEN setzt "
                   f"und den Rest in Ruhe lässt")
        ref = lambda t: " ".join(w.upper() if len(w) > limit else w for w in t.split())
        sol = (f'return " ".join(w.upper() if len(w) > {limit} else w '
               f'for w in text.split())')
    else:
        desc = f"drops every word shorter than {limit} characters"
        desc_de = f"jedes Wort mit weniger als {limit} Zeichen weglässt"
        ref = lambda t: " ".join(w for w in t.split() if len(w) >= limit)
        sol = f'return " ".join(w for w in text.split() if len(w) >= {limit})'

    return _task(rng, "title_words", "Word surgery", "Strings", "Easy",
                 "transform", f"""
Write transform(text) that {desc}.

  transform({text!r})
    -> {ref(text)!r}

Words are separated by single spaces in the output.""",
                 "text", ref, [(text,), ("",), (rand_word(rng),),
                               (rand_text(rng, 3),), ("  padded   out  ",),
                               (rand_text(rng, 7),)],
                 ["text.split() gives you the words",
                  '" ".join(...) glues them back together',
                  "A generator expression inside join keeps it to one line"],
                 f"def transform(text):\n    {sol}\n",
                 de={
                     "title": "Wort-Operationen",
                     "statement": f"""
Schreib transform(text), das {desc_de}.

  transform({text!r})
    -> {ref(text)!r}

In der Ausgabe sind die Wörter durch einzelne Leerzeichen getrennt.""",
                     "hints": ["text.split() liefert dir die Wörter",
                               '" ".join(...) klebt sie wieder zusammen',
                               "Ein Generator-Ausdruck in join hält es bei einer Zeile"],
                 })


# ====================================================================== LISTS
@drill("filter_list", "Filter a list", "Eine Liste filtern", "Lists")
def _filter_list(rng):
    mode = rng.choice(["divisible", "greater", "even_index", "negative", "range"])
    k = rng.randint(2, 9)
    t = rng.randint(0, 20)
    lo, hi = sorted((rng.randint(-10, 5), rng.randint(6, 30)))
    data = rand_list(rng)

    if mode == "divisible":
        desc = f"keeps only the values divisible by {k}"
        desc_de = f"nur die durch {k} teilbaren Werte behält"
        ref = lambda nums: [n for n in nums if n % k == 0]
        sol = f"return [n for n in nums if n % {k} == 0]"
    elif mode == "greater":
        desc = f"keeps only the values strictly greater than {t}"
        desc_de = f"nur die Werte behält, die echt größer als {t} sind"
        ref = lambda nums: [n for n in nums if n > t]
        sol = f"return [n for n in nums if n > {t}]"
    elif mode == "even_index":
        desc = "keeps the values at EVEN indices (0, 2, 4, ...)"
        desc_de = "die Werte an GERADEN Indizes behält (0, 2, 4, ...)"
        ref = lambda nums: nums[::2]
        sol = "return nums[::2]"
    elif mode == "negative":
        desc = "keeps only the negative values, in their original order"
        desc_de = "nur die negativen Werte behält, in ihrer ursprünglichen Reihenfolge"
        ref = lambda nums: [n for n in nums if n < 0]
        sol = "return [n for n in nums if n < 0]"
    else:
        desc = f"keeps the values between {lo} and {hi} inclusive"
        desc_de = f"die Werte zwischen {lo} und {hi} einschließlich behält"
        ref = lambda nums: [n for n in nums if lo <= n <= hi]
        sol = f"return [n for n in nums if {lo} <= n <= {hi}]"

    return _task(rng, "filter_list", "Filter a list", "Lists", "Easy",
                 "keep", f"""
Write keep(nums) that {desc}.

  keep({data}) -> {ref(data)}

Return a NEW list; do not modify the input.""",
                 "nums", ref, [(data,), ([],), (rand_list(rng, 3),),
                               (rand_list(rng, 12),), ([0, 0, 0],),
                               (rand_list(rng, 6, -50, 50),)],
                 ["A list comprehension with an `if` filter is the whole job",
                  "[value for value in nums if CONDITION]"],
                 f"def keep(nums):\n    {sol}\n",
                 de={
                     "title": "Eine Liste filtern",
                     "statement": f"""
Schreib keep(nums), das {desc_de}.

  keep({data}) -> {ref(data)}

Gib eine NEUE Liste zurück; verändere die Eingabe nicht.""",
                     "hints": ["Eine List Comprehension mit einem `if`-Filter ist die ganze Arbeit",
                               "[wert for wert in nums if BEDINGUNG]"],
                 })


@drill("chunk", "Chunk a list", "Eine Liste stückeln", "Lists", "Medium")
def _chunk(rng):
    size = rng.randint(2, 5)
    data = rand_list(rng, rng.randint(7, 13), 1, 30)

    def ref(nums):
        return [nums[i:i + size] for i in range(0, len(nums), size)]

    return _task(rng, "chunk", f"Chunks of {size}", "Lists", "Medium",
                 "chunk", f"""
Write chunk(nums) that splits a list into consecutive pieces of {size}.
The final piece may be shorter.

  chunk({data})
    -> {ref(data)}
  chunk([]) -> []""",
                 "nums", ref, [(data,), ([],), (list(range(size)),),
                               (rand_list(rng, size * 3, 0, 9),),
                               (rand_list(rng, 1),), (list(range(20)),)],
                 [f"range(0, len(nums), {size}) jumps {size} at a time",
                  f"nums[i:i + {size}] takes one chunk (slices never go out of range)",
                  "One list comprehension is enough"],
                 f"def chunk(nums):\n"
                 f"    return [nums[i:i + {size}] for i in range(0, len(nums), {size})]\n",
                 de={
                     "title": f"Stücke zu {size}",
                     "statement": f"""
Schreib chunk(nums), das eine Liste in aufeinanderfolgende Stücke zu je {size}
zerlegt. Das letzte Stück darf kürzer sein.

  chunk({data})
    -> {ref(data)}
  chunk([]) -> []""",
                     "hints": [f"range(0, len(nums), {size}) springt in {size}er-Schritten",
                               f"nums[i:i + {size}] holt ein Stück (Slices laufen nie über den Rand)",
                               "Eine einzige List Comprehension reicht"],
                 })


@drill("sort_key", "Sort with a key", "Mit Schlüssel sortieren", "Sorting", "Medium")
def _sort_key(rng):
    mode = rng.choice(["len_then_alpha", "abs_value", "last_char", "digit_sum", "desc"])
    words = rng.sample(WORDS, 6)
    nums = rand_list(rng, 7, -40, 40)

    if mode == "len_then_alpha":
        desc = "sorts words by LENGTH (short first), ties broken alphabetically"
        desc_de = ("Wörter nach LÄNGE sortiert (kurze zuerst), bei Gleichstand "
                   "alphabetisch")
        ref = lambda items: sorted(items, key=lambda w: (len(w), w))
        sol = "return sorted(items, key=lambda w: (len(w), w))"
        samples = [(words,), ([],), (["bb", "a", "cc"],),
                   (rng.sample(WORDS, 4),), (["x"],), (rng.sample(WORDS, 8),)]
    elif mode == "abs_value":
        desc = "sorts numbers by ABSOLUTE value, smallest first"
        desc_de = "Zahlen nach ihrem BETRAG sortiert, kleinste zuerst"
        ref = lambda items: sorted(items, key=abs)
        sol = "return sorted(items, key=abs)"
        samples = [(nums,), ([],), ([-1, 1],), (rand_list(rng, 5, -9, 9),),
                   ([0],), (rand_list(rng, 10, -100, 100),)]
    elif mode == "last_char":
        desc = "sorts words by their LAST character (a-z)"
        desc_de = "Wörter nach ihrem LETZTEN Zeichen sortiert (a-z)"
        ref = lambda items: sorted(items, key=lambda w: w[-1])
        sol = "return sorted(items, key=lambda w: w[-1])"
        samples = [(words,), ([],), (["ab", "ba"],),
                   (rng.sample(WORDS, 4),), (["z"],), (rng.sample(WORDS, 7),)]
    elif mode == "digit_sum":
        desc = "sorts numbers by the sum of their digits (smallest first, ties keep original order)"
        desc_de = ("Zahlen nach ihrer Quersumme sortiert (kleinste zuerst, bei "
                   "Gleichstand bleibt die ursprüngliche Reihenfolge)")
        ref = lambda items: sorted(items, key=lambda n: sum(int(d) for d in str(abs(n))))
        sol = ("return sorted(items, key=lambda n: sum(int(d) for d in str(abs(n))))")
        samples = [(rand_list(rng, 6, 1, 999),), ([],), ([10, 9],),
                   (rand_list(rng, 5, 1, 99),), ([100, 2],),
                   (rand_list(rng, 8, 1, 500),)]
    else:
        desc = "sorts numbers from largest to smallest"
        desc_de = "Zahlen von der größten zur kleinsten sortiert"
        ref = lambda items: sorted(items, reverse=True)
        sol = "return sorted(items, reverse=True)"
        samples = [(nums,), ([],), ([1],), (rand_list(rng, 5),),
                   ([2, 2, 2],), (rand_list(rng, 9, -5, 5),)]

    return _task(rng, "sort_key", "Sort with a key", "Sorting", "Medium",
                 "arrange", f"""
Write arrange(items) that {desc}.

  arrange({samples[0][0]})
    -> {ref(list(samples[0][0]))}

Return a NEW list — use sorted(), not .sort().""",
                 "items", ref, samples,
                 ["sorted(items, key=...) takes a function that maps each item to its sort value",
                  "A tuple key sorts by the first element, then the second",
                  "reverse=True flips the order"],
                 f"def arrange(items):\n    {sol}\n",
                 de={
                     "title": "Mit Schlüssel sortieren",
                     "statement": f"""
Schreib arrange(items), das {desc_de} zurückgibt.

  arrange({samples[0][0]})
    -> {ref(list(samples[0][0]))}

Gib eine NEUE Liste zurück — nimm sorted(), nicht .sort().""",
                     "hints": ["sorted(items, key=...) nimmt eine Funktion, die jedes Element "
                               "auf seinen Sortierwert abbildet",
                               "Ein Tupel als Schlüssel sortiert nach dem ersten Element, "
                               "dann nach dem zweiten",
                               "reverse=True dreht die Reihenfolge um"],
                 })


@drill("running", "Running totals", "Laufende Werte", "Prefix sums", "Medium")
def _running(rng):
    mode = rng.choice(["sum", "max", "product"])
    data = rand_list(rng, 7, 1, 12)

    if mode == "sum":
        desc, desc_de = "running SUM", "laufende SUMME"
        def ref(nums):
            out, acc = [], 0
            for n in nums:
                acc += n
                out.append(acc)
            return out
        sol = ("out, acc = [], 0\n    for n in nums:\n        acc += n\n"
               "        out.append(acc)\n    return out")
    elif mode == "max":
        desc = "running MAXIMUM (the biggest value seen so far)"
        desc_de = "laufendes MAXIMUM (der bisher größte gesehene Wert)"
        def ref(nums):
            out, best = [], None
            for n in nums:
                best = n if best is None else max(best, n)
                out.append(best)
            return out
        sol = ("out, best = [], None\n    for n in nums:\n"
               "        best = n if best is None else max(best, n)\n"
               "        out.append(best)\n    return out")
    else:
        desc, desc_de = "running PRODUCT", "laufendes PRODUKT"
        def ref(nums):
            out, acc = [], 1
            for n in nums:
                acc *= n
                out.append(acc)
            return out
        sol = ("out, acc = [], 1\n    for n in nums:\n        acc *= n\n"
               "        out.append(acc)\n    return out")

    return _task(rng, "running", f"Running {mode}", "Prefix sums", "Medium",
                 "running", f"""
Write running(nums) returning the {desc} at every position.
The result has the same length as the input.

  running({data})
    -> {ref(data)}
  running([]) -> []""",
                 "nums", ref, [(data,), ([],), ([5],),
                               (rand_list(rng, 4, 1, 6),), ([1, 1, 1, 1],),
                               (rand_list(rng, 9, 1, 5),)],
                 ["Keep one accumulator variable outside the loop",
                  "Append the accumulator AFTER updating it",
                  "itertools.accumulate does this too — but write the loop first"],
                 f"def running(nums):\n    {sol}\n",
                 de={
                     "title": f"Laufendes {desc_de.split()[-1].capitalize()}",
                     "statement": f"""
Schreib running(nums), das an jeder Position das {desc_de} zurückgibt.
Das Ergebnis hat dieselbe Länge wie die Eingabe.

  running({data})
    -> {ref(data)}
  running([]) -> []""",
                     "hints": ["Führ eine Sammelvariable außerhalb der Schleife",
                               "Häng die Sammelvariable an, NACHDEM du sie aktualisiert hast",
                               "itertools.accumulate kann das auch — schreib aber erst die Schleife"],
                 })


@drill("remove_value", "Remove in place", "Werte nach hinten schieben", "Lists")
def _remove_value(rng):
    target = rng.randint(0, 5)
    data = [rng.randint(0, 5) for _ in range(rng.randint(6, 11))]

    def ref(nums):
        return [n for n in nums if n != target] + [0] * nums.count(target)

    return _task(rng, "remove_value", f"Push {target}s to the end", "Lists", "Medium",
                 "shift_out", f"""
Write shift_out(nums) that removes every {target} and pads the list back to its
ORIGINAL length with zeros at the end. The order of the other values must be
preserved.

  shift_out({data})
    -> {ref(list(data))}

(This is the classic "move zeroes" pattern with a random target.)""",
                 "nums", ref, [(data,), ([],), ([target] * 4,),
                               ([rng.randint(0, 5) for _ in range(5)],),
                               ([9, 9, 9],),
                               ([rng.randint(0, 5) for _ in range(12)],)],
                 [f"kept = [n for n in nums if n != {target}]",
                  "The number removed is len(nums) - len(kept)",
                  "Return kept + [0] * removed"],
                 f"def shift_out(nums):\n    kept = [n for n in nums if n != {target}]\n"
                 f"    return kept + [0] * (len(nums) - len(kept))\n",
                 de={
                     "title": f"Alle {target}en nach hinten",
                     "statement": f"""
Schreib shift_out(nums), das jede {target} entfernt und die Liste am Ende mit
Nullen wieder auf ihre URSPRÜNGLICHE Länge auffüllt. Die Reihenfolge der
übrigen Werte muss erhalten bleiben.

  shift_out({data})
    -> {ref(list(data))}

(Das ist das klassische "Nullen nach hinten"-Muster mit einem zufälligen Wert.)""",
                     "hints": [f"behalten = [n for n in nums if n != {target}]",
                               "Die Anzahl der entfernten ist len(nums) - len(behalten)",
                               "Gib behalten + [0] * entfernt zurück"],
                 })


@drill("interleave", "Interleave two lists", "Zwei Listen verzahnen", "Lists", "Medium")
def _interleave(rng):
    a = rand_list(rng, rng.randint(3, 6), 1, 20)
    b = rand_list(rng, rng.randint(3, 6), 21, 40)

    def ref(a, b):
        out = []
        for i in range(max(len(a), len(b))):
            if i < len(a):
                out.append(a[i])
            if i < len(b):
                out.append(b[i])
        return out

    return _task(rng, "interleave", "Interleave two lists", "Lists", "Medium",
                 "interleave", f"""
Write interleave(a, b) that alternates the elements of two lists, starting with
a. When one list runs out, the rest of the other is appended.

  interleave({a}, {b})
    -> {ref(a, b)}
  interleave([1, 2, 3], []) -> [1, 2, 3]""",
                 "a, b", ref, [(a, b), ([1, 2, 3], []), ([], []),
                               ([1], [2, 3, 4]),
                               (rand_list(rng, 4, 1, 9), rand_list(rng, 4, 10, 19)),
                               ([0, 0], [1])],
                 ["Loop i over range(max(len(a), len(b)))",
                  "Guard each append with `if i < len(...)`",
                  "itertools.zip_longest is the fancy alternative"],
                 "def interleave(a, b):\n    out = []\n"
                 "    for i in range(max(len(a), len(b))):\n"
                 "        if i < len(a):\n            out.append(a[i])\n"
                 "        if i < len(b):\n            out.append(b[i])\n    return out\n",
                 de={
                     "title": "Zwei Listen verzahnen",
                     "statement": f"""
Schreib interleave(a, b), das die Elemente zweier Listen abwechselnd
aneinanderreiht, beginnend mit a. Geht eine Liste aus, wird der Rest der
anderen angehängt.

  interleave({a}, {b})
    -> {ref(a, b)}
  interleave([1, 2, 3], []) -> [1, 2, 3]""",
                     "hints": ["Lauf i über range(max(len(a), len(b)))",
                               "Sicher jedes Anhängen mit `if i < len(...)` ab",
                               "itertools.zip_longest ist die elegante Alternative"],
                 })


@drill("nth_smallest", "N-th smallest", "Der n-kleinste Wert", "Sorting")
def _nth(rng):
    k = rng.randint(1, 4)
    data = rand_list(rng, rng.randint(6, 10), 1, 50)

    def ref(nums):
        distinct = sorted(set(nums))
        return distinct[k - 1] if len(distinct) >= k else None

    return _task(rng, "nth_smallest", f"{k}-th smallest distinct", "Sorting", "Easy",
                 "nth_smallest", f"""
Write nth_smallest(nums) that returns the {k}-th smallest DISTINCT value.
Return None if there are fewer than {k} distinct values.

  nth_smallest({data}) -> {ref(data)}
  nth_smallest([]) -> None""",
                 "nums", ref, [(data,), ([],), ([5, 5, 5],),
                               (rand_list(rng, 5, 1, 10),),
                               (list(range(k)),), (rand_list(rng, 12, 1, 8),)],
                 ["set(nums) removes duplicates",
                  f"sorted(...) then index {k - 1}",
                  "Check the length BEFORE indexing"],
                 f"def nth_smallest(nums):\n    distinct = sorted(set(nums))\n"
                 f"    return distinct[{k - 1}] if len(distinct) >= {k} else None\n",
                 de={
                     "title": f"{k}-kleinster verschiedener Wert",
                     "statement": f"""
Schreib nth_smallest(nums), das den {k}-kleinsten VERSCHIEDENEN Wert zurückgibt.
Gib None zurück, wenn es weniger als {k} verschiedene Werte gibt.

  nth_smallest({data}) -> {ref(data)}
  nth_smallest([]) -> None""",
                     "hints": ["set(nums) entfernt die Duplikate",
                               f"sorted(...) und dann Index {k - 1}",
                               "Prüf die Länge, BEVOR du indizierst"],
                 })


# ================================================================= DICT / SET
@drill("group_by", "Group items", "Elemente gruppieren", "Hash map", "Medium")
def _group_by(rng):
    mode = rng.choice(["first_letter", "length", "parity"])
    words = rng.sample(WORDS + NAMES, 7)
    nums = rand_list(rng, 8, 1, 40)

    if mode == "first_letter":
        desc = "groups words by their first letter (lower-cased)"
        desc_de = "Wörter nach ihrem ersten Buchstaben gruppiert (kleingeschrieben)"
        def ref(items):
            out = {}
            for w in items:
                out.setdefault(w[0].lower(), []).append(w)
            return out
        sol = ('out = {}\n    for w in items:\n'
               '        out.setdefault(w[0].lower(), []).append(w)\n    return out')
        samples = [(words,), ([],), (["Ada", "alan"],),
                   (rng.sample(WORDS, 5),), (["x"],), (rng.sample(NAMES, 6),)]
    elif mode == "length":
        desc = "groups words by their length"
        desc_de = "Wörter nach ihrer Länge gruppiert"
        def ref(items):
            out = {}
            for w in items:
                out.setdefault(len(w), []).append(w)
            return out
        sol = ('out = {}\n    for w in items:\n'
               '        out.setdefault(len(w), []).append(w)\n    return out')
        samples = [(words,), ([],), (["ab", "cd", "e"],),
                   (rng.sample(WORDS, 5),), ([""],), (rng.sample(WORDS, 9),)]
    else:
        desc = 'groups numbers under the keys "even" and "odd"'
        desc_de = 'Zahlen unter den Schlüsseln "even" und "odd" gruppiert'
        def ref(items):
            out = {}
            for n in items:
                out.setdefault("even" if n % 2 == 0 else "odd", []).append(n)
            return out
        sol = ('out = {}\n    for n in items:\n'
               '        out.setdefault("even" if n % 2 == 0 else "odd", []).append(n)\n'
               '    return out')
        samples = [(nums,), ([],), ([2, 4],), (rand_list(rng, 5, 1, 9),),
                   ([1],), (rand_list(rng, 10, -9, 9),)]

    return _task(rng, "group_by", "Group items", "Hash map", "Medium",
                 "group", f"""
Write group(items) that returns a dict which {desc}.
Each value is a list, in the original order. Groups appear in the order they
were first seen.

  group({samples[0][0]})
    -> {ref(list(samples[0][0]))}""",
                 "items", ref, samples,
                 ["d.setdefault(key, []).append(value) creates the list if missing",
                  "collections.defaultdict(list) does the same thing more elegantly",
                  "Dicts keep insertion order, so 'first seen' is free"],
                 f"def group(items):\n    {sol}\n",
                 de={
                     "title": "Elemente gruppieren",
                     "statement": f"""
Schreib group(items), das ein dict zurückgibt, welches {desc_de}.
Jeder Wert ist eine Liste in der ursprünglichen Reihenfolge. Die Gruppen
erscheinen in der Reihenfolge, in der sie zuerst aufgetaucht sind.

  group({samples[0][0]})
    -> {ref(list(samples[0][0]))}""",
                     "hints": ["d.setdefault(schluessel, []).append(wert) legt die Liste "
                               "an, falls sie fehlt",
                               "collections.defaultdict(list) macht dasselbe eleganter",
                               "Dicts behalten die Einfügereihenfolge, 'zuerst gesehen' "
                               "bekommst du also geschenkt"],
                 })


@drill("invert_dict", "Invert a mapping", "Eine Zuordnung umdrehen", "Hash map", "Medium")
def _invert(rng):
    keys = rng.sample(NAMES, 4)
    values = [rng.choice(CITIES) for _ in keys]
    data = dict(zip(keys, values))

    def ref(mapping):
        out = {}
        for k, v in mapping.items():
            out.setdefault(v, []).append(k)
        return out

    return _task(rng, "invert_dict", "Invert a mapping", "Hash map", "Medium",
                 "invert", f"""
Write invert(mapping) that flips a dict around. Because several keys can share
a value, every value in the result is a LIST of the original keys, in
insertion order.

  invert({data})
    -> {ref(data)}
  invert({{}}) -> {{}}""",
                 "mapping", ref, [(data,), ({},), ({"a": 1, "b": 1},),
                                  (dict(zip(rng.sample(NAMES, 3), ["X", "Y", "X"])),),
                                  ({"solo": "one"},),
                                  (dict(zip(rng.sample(WORDS, 5),
                                            [rng.choice("AB") for _ in range(5)])),)],
                 ["Loop over mapping.items()",
                  "out.setdefault(value, []).append(key)",
                  "Never assign out[value] = key — you would lose the collisions"],
                 "def invert(mapping):\n    out = {}\n"
                 "    for key, value in mapping.items():\n"
                 "        out.setdefault(value, []).append(key)\n    return out\n",
                 de={
                     "title": "Eine Zuordnung umdrehen",
                     "statement": f"""
Schreib invert(mapping), das ein dict umdreht. Weil sich mehrere Schlüssel
einen Wert teilen können, ist jeder Wert im Ergebnis eine LISTE der
ursprünglichen Schlüssel, in Einfügereihenfolge.

  invert({data})
    -> {ref(data)}
  invert({{}}) -> {{}}""",
                     "hints": ["Lauf über mapping.items()",
                               "out.setdefault(wert, []).append(schluessel)",
                               "Schreib bloß nie out[wert] = schluessel — damit "
                               "verlierst du die Kollisionen"],
                 })


@drill("merge_totals", "Merge two tallies", "Zwei Zählungen zusammenführen", "Hash map")
def _merge(rng):
    keys = rng.sample(WORDS, 5)
    a = {k: rng.randint(1, 9) for k in keys[:3]}
    b = {k: rng.randint(1, 9) for k in keys[2:]}

    def ref(a, b):
        out = dict(a)
        for k, v in b.items():
            out[k] = out.get(k, 0) + v
        return out

    return _task(rng, "merge_totals", "Merge two tallies", "Hash map", "Easy",
                 "merge", f"""
Write merge(a, b) that adds two count-dicts together. Keys present in both get
their values SUMMED. Keys from `a` keep their position, new keys from `b` are
appended.

  merge({a}, {b})
    -> {ref(a, b)}""",
                 "a, b", ref, [(a, b), ({}, {}), ({"x": 1}, {"x": 2}),
                               ({"p": 5}, {"q": 5}),
                               ({k: 1 for k in rng.sample(WORDS, 3)}, {}),
                               ({}, {"only": 7})],
                 ["Start from a COPY: out = dict(a)",
                  "out[k] = out.get(k, 0) + v for every item of b",
                  "collections.Counter(a) + Counter(b) is the shortcut"],
                 "def merge(a, b):\n    out = dict(a)\n    for key, value in b.items():\n"
                 "        out[key] = out.get(key, 0) + value\n    return out\n",
                 de={
                     "title": "Zwei Zählungen zusammenführen",
                     "statement": f"""
Schreib merge(a, b), das zwei Zähl-dicts addiert. Schlüssel, die in beiden
vorkommen, bekommen ihre Werte SUMMIERT. Die Schlüssel aus `a` behalten ihre
Position, neue Schlüssel aus `b` werden hinten angehängt.

  merge({a}, {b})
    -> {ref(a, b)}""",
                     "hints": ["Fang mit einer KOPIE an: out = dict(a)",
                               "out[k] = out.get(k, 0) + v für jeden Eintrag von b",
                               "collections.Counter(a) + Counter(b) ist die Abkürzung"],
                 })


@drill("most_common", "Most common item", "Häufigstes Element", "Hash map")
def _most_common(rng):
    pool = rng.sample(WORDS, 4)
    data = [rng.choice(pool) for _ in range(rng.randint(7, 14))]

    def ref(items):
        if not items:
            return None
        counts = {}
        for item in items:
            counts[item] = counts.get(item, 0) + 1
        best = max(counts.values())
        return min(k for k, v in counts.items() if v == best)

    return _task(rng, "most_common", "Most common item", "Hash map", "Easy",
                 "most_common", f"""
Write most_common(items) returning the value that appears most often.
If several tie, return the alphabetically smallest of them.
Return None for an empty list.

  most_common({data})
    -> {ref(data)!r}""",
                 "items", ref, [(data,), ([],), (["b", "a"],),
                                ([rng.choice(pool) for _ in range(5)],),
                                (["solo"],),
                                ([rng.choice(pool) for _ in range(20)],)],
                 ["Count into a dict first",
                  "best = max(counts.values()) is the winning count",
                  "min(...) over the keys that reached that count breaks the tie"],
                 "def most_common(items):\n    if not items:\n        return None\n"
                 "    counts = {}\n    for item in items:\n"
                 "        counts[item] = counts.get(item, 0) + 1\n"
                 "    best = max(counts.values())\n"
                 "    return min(k for k, v in counts.items() if v == best)\n",
                 de={
                     "title": "Häufigstes Element",
                     "statement": f"""
Schreib most_common(items), das den Wert zurückgibt, der am häufigsten vorkommt.
Bei Gleichstand den alphabetisch kleinsten davon.
Für eine leere Liste None.

  most_common({data})
    -> {ref(data)!r}""",
                     "hints": ["Zähl zuerst in ein dict",
                               "best = max(counts.values()) ist die Siegeranzahl",
                               "min(...) über die Schlüssel mit dieser Anzahl löst den Gleichstand"],
                 })


# ======================================================= WINDOWS & TWO POINTER
@drill("window_sum", "Best window of k", "Bestes Fenster der Größe k",
       "Two pointers", "Medium")
def _window(rng):
    k = rng.randint(2, 4)
    data = rand_list(rng, rng.randint(7, 12), -10, 25)

    def ref(nums):
        if len(nums) < k:
            return None
        window = sum(nums[:k])
        best = window
        for i in range(k, len(nums)):
            window += nums[i] - nums[i - k]
            best = max(best, window)
        return best

    return _task(rng, "window_sum", f"Best window of {k}", "Two pointers", "Medium",
                 "best_window", f"""
Write best_window(nums) returning the largest sum of {k} CONSECUTIVE values.
Return None if the list is shorter than {k}.

  best_window({data}) -> {ref(data)}

Do it in one pass: slide the window by adding the entering value and
subtracting the leaving one. Re-summing each window is O(n*k) — too slow.""",
                 "nums", ref, [(data,), ([1],), (list(range(k)),),
                               (rand_list(rng, 6, 1, 9),),
                               ([-5] * (k + 2),),
                               (rand_list(rng, 20, -30, 30),)],
                 [f"window = sum(nums[:{k}]) is the first window",
                  f"Sliding: window += nums[i] - nums[i - {k}]",
                  "Track best = max(best, window) each step"],
                 f"def best_window(nums):\n    if len(nums) < {k}:\n        return None\n"
                 f"    window = sum(nums[:{k}])\n    best = window\n"
                 f"    for i in range({k}, len(nums)):\n"
                 f"        window += nums[i] - nums[i - {k}]\n"
                 f"        best = max(best, window)\n    return best\n",
                 de={
                     "title": f"Bestes Fenster der Größe {k}",
                     "statement": f"""
Schreib best_window(nums), das die größte Summe von {k} AUFEINANDERFOLGENDEN
Werten zurückgibt. Gib None zurück, wenn die Liste kürzer als {k} ist.

  best_window({data}) -> {ref(data)}

Mach es in einem Durchlauf: schieb das Fenster, indem du den eintretenden Wert
addierst und den austretenden abziehst. Jedes Fenster neu zu summieren ist
O(n*k) — zu langsam.""",
                     "hints": [f"window = sum(nums[:{k}]) ist das erste Fenster",
                               f"Schieben: window += nums[i] - nums[i - {k}]",
                               "Führ in jedem Schritt best = max(best, window) mit"],
                 })


@drill("pair_sum", "Pair that sums to target", "Paar mit Zielsumme",
       "Two pointers", "Medium")
def _pair(rng):
    data = sorted(rand_list(rng, rng.randint(6, 10), 1, 40))
    i, j = sorted(rng.sample(range(len(data)), 2))
    target = data[i] + data[j]

    def ref(nums, target):
        seen = set()
        for n in nums:
            if target - n in seen:
                return True
            seen.add(n)
        return False

    return _task(rng, "pair_sum", f"Two values summing to {target}", "Two pointers",
                 "Medium", "has_pair", f"""
Write has_pair(nums, target) -> True if ANY two DIFFERENT positions in the list
add up to target.

  has_pair({data}, {target}) -> True
  has_pair([1, 2], 100) -> False

O(n) with a set. (An O(n log n) two-pointer solution on the sorted list is
equally acceptable — but the set version is shorter.)""",
                 "nums, target", ref,
                 [(data, target), ([1, 2], 100), ([], 0),
                  ([3, 3], 6), ([5], 10),
                  (rand_list(rng, 12, 1, 20), rng.randint(5, 35))],
                 ["Keep a `seen` set of the values you already passed",
                  "For each n, ask: is (target - n) already in seen?",
                  "Add n to seen AFTER the check, so one element cannot pair with itself"],
                 "def has_pair(nums, target):\n    seen = set()\n    for n in nums:\n"
                 "        if target - n in seen:\n            return True\n"
                 "        seen.add(n)\n    return False\n",
                 de={
                     "title": f"Zwei Werte mit Summe {target}",
                     "statement": f"""
Schreib has_pair(nums, target) -> True, wenn IRGENDWELCHE zwei
VERSCHIEDENEN Positionen der Liste zusammen target ergeben.

  has_pair({data}, {target}) -> True
  has_pair([1, 2], 100) -> False

O(n) mit einem set. (Eine O(n log n)-Lösung mit zwei Zeigern auf der sortierten
Liste ist genauso in Ordnung — die set-Variante ist aber kürzer.)""",
                     "hints": ["Führ ein `gesehen`-Set mit den Werten, an denen du vorbei bist",
                               "Frag für jedes n: steckt (target - n) schon in gesehen?",
                               "Füg n erst NACH der Prüfung hinzu, damit sich ein Element "
                               "nicht mit sich selbst paart"],
                 })


@drill("split_balance", "Best split point", "Beste Teilungsstelle",
       "Prefix sums", "Medium")
def _split(rng):
    data = rand_list(rng, rng.randint(5, 10), -15, 25)

    def ref(nums):
        if len(nums) < 2:
            return None
        total, left, best = sum(nums), 0, None
        for i in range(len(nums) - 1):
            left += nums[i]
            diff = abs(left - (total - left))
            best = diff if best is None else min(best, diff)
        return best

    return _task(rng, "split_balance", "Best split point", "Prefix sums", "Medium",
                 "best_split", f"""
Cut the list into two non-empty parts. Write best_split(nums) returning the
SMALLEST possible |sum(left) - sum(right)|.
Return None if the list is shorter than 2.

  best_split({data}) -> {ref(data)}

O(n): keep a running left sum, right = total - left. This is Codility's
TapeEquilibrium.""",
                 "nums", ref, [(data,), ([1, 1],), ([5],),
                               (rand_list(rng, 6, 1, 10),),
                               ([-1000, 1000],),
                               (rand_list(rng, 15, -50, 50),)],
                 ["total = sum(nums) once, up front",
                  "Loop i from 0 to len(nums) - 2 (the left part must not be empty)",
                  "left += nums[i]; then diff = abs(left - (total - left))"],
                 "def best_split(nums):\n    if len(nums) < 2:\n        return None\n"
                 "    total, left, best = sum(nums), 0, None\n"
                 "    for i in range(len(nums) - 1):\n        left += nums[i]\n"
                 "        diff = abs(left - (total - left))\n"
                 "        best = diff if best is None else min(best, diff)\n    return best\n",
                 de={
                     "title": "Beste Teilungsstelle",
                     "statement": f"""
Zerschneide die Liste in zwei nicht leere Teile. Schreib best_split(nums), das
das KLEINSTMÖGLICHE |summe(links) - summe(rechts)| zurückgibt.
Gib None zurück, wenn die Liste kürzer als 2 ist.

  best_split({data}) -> {ref(data)}

O(n): führ eine laufende linke Summe, rechts = gesamt - links. Das ist
Codilitys TapeEquilibrium.""",
                     "hints": ["gesamt = sum(nums) einmal, ganz am Anfang",
                               "Lauf i von 0 bis len(nums) - 2 (der linke Teil darf nicht leer sein)",
                               "links += nums[i]; dann diff = abs(links - (gesamt - links))"],
                 })


# ==================================================================== MATRICES
@drill("matrix_op", "Matrix operation", "Matrix-Operation", "Matrix", "Medium")
def _matrix(rng):
    mode = rng.choice(["row_sums", "diagonal", "transpose", "spiral_first_col"])
    n = rng.randint(2, 4)
    m = [[rng.randint(1, 9) for _ in range(n)] for _ in range(n)]

    if mode == "row_sums":
        desc = "returns the sum of each ROW as a list"
        desc_de = "die Summe jeder ZEILE als Liste zurückgibt"
        ref = lambda grid: [sum(row) for row in grid]
        sol = "return [sum(row) for row in grid]"
    elif mode == "diagonal":
        desc = "returns the main diagonal (top-left to bottom-right) as a list"
        desc_de = ("die Hauptdiagonale (links oben nach rechts unten) als Liste "
                   "zurückgibt")
        ref = lambda grid: [grid[i][i] for i in range(len(grid))]
        sol = "return [grid[i][i] for i in range(len(grid))]"
    elif mode == "transpose":
        desc = "returns the TRANSPOSED grid (rows become columns), as a list of lists"
        desc_de = ("das TRANSPONIERTE Gitter zurückgibt (Zeilen werden zu Spalten), "
                   "als Liste von Listen")
        ref = lambda grid: [list(col) for col in zip(*grid)]
        sol = "return [list(col) for col in zip(*grid)]"
    else:
        desc = "returns the FIRST COLUMN as a list"
        desc_de = "die ERSTE SPALTE als Liste zurückgibt"
        ref = lambda grid: [row[0] for row in grid]
        sol = "return [row[0] for row in grid]"

    other = [[rng.randint(1, 9) for _ in range(3)] for _ in range(3)]
    return _task(rng, "matrix_op", "Matrix operation", "Matrix", "Medium",
                 "solve", f"""
The input is a square grid (a list of lists of numbers).

Write solve(grid) that {desc}.

  solve({m})
    -> {ref([row[:] for row in m])}
  solve([]) -> []""",
                 "grid", ref, [(m,), ([],), ([[1]],), (other,),
                               ([[0, 0], [0, 0]],),
                               ([[rng.randint(-9, 9) for _ in range(4)] for _ in range(4)],)],
                 ["Iterate rows with `for row in grid`",
                  "grid[i][j] is row i, column j",
                  "zip(*grid) transposes — the star unpacks the rows as arguments"],
                 f"def solve(grid):\n    {sol}\n",
                 de={
                     "title": "Matrix-Operation",
                     "statement": f"""
Die Eingabe ist ein quadratisches Gitter (eine Liste von Zahlenlisten).

Schreib solve(grid), das {desc_de}.

  solve({m})
    -> {ref([row[:] for row in m])}
  solve([]) -> []""",
                     "hints": ["Lauf über die Zeilen mit `for zeile in grid`",
                               "grid[i][j] ist Zeile i, Spalte j",
                               "zip(*grid) transponiert — der Stern entpackt die Zeilen "
                               "als Argumente"],
                 })


@drill("temp_convert", "Unit conversion", "Einheiten umrechnen", "Basics")
def _temp(rng):
    mode = rng.choice(["c2f", "f2c", "km2mi", "kg2lb"])
    if mode == "c2f":
        desc, f, unit = "Celsius to Fahrenheit", lambda v: round(v * 9 / 5 + 32, 2), "°C"
        desc_de = "Celsius in Fahrenheit"
        sol = "return round(value * 9 / 5 + 32, 2)"
        vals = [0, 100, -40, 37, 21.5, -273.15]
    elif mode == "f2c":
        desc, f, unit = "Fahrenheit to Celsius", lambda v: round((v - 32) * 5 / 9, 2), "°F"
        desc_de = "Fahrenheit in Celsius"
        sol = "return round((value - 32) * 5 / 9, 2)"
        vals = [32, 212, -40, 98.6, 0, 72]
    elif mode == "km2mi":
        desc, f, unit = "kilometres to miles", lambda v: round(v * 0.621371, 2), "km"
        desc_de = "Kilometer in Meilen"
        sol = "return round(value * 0.621371, 2)"
        vals = [1, 42.195, 0, 100, 5.5, 1609.34]
    else:
        desc, f, unit = "kilograms to pounds", lambda v: round(v * 2.20462, 2), "kg"
        desc_de = "Kilogramm in Pfund"
        sol = "return round(value * 2.20462, 2)"
        vals = [1, 0, 70, 2.5, 100, 13.6]
    rng.shuffle(vals)

    return _task(rng, "temp_convert", f"Convert {desc}", "Basics", "Easy",
                 "convert", f"""
Write convert(value) that converts {desc}, rounded to 2 decimals.

  convert({vals[0]}) -> {f(vals[0])}
  convert({vals[1]}) -> {f(vals[1])}

The input is in {unit}.""",
                 "value", f, [(v,) for v in vals],
                 ["Write the formula out, then wrap it in round(..., 2)",
                  "Careful with operator precedence — use parentheses"],
                 f"def convert(value):\n    {sol}\n",
                 de={
                     "title": f"{desc_de} umrechnen",
                     "statement": f"""
Schreib convert(value), das {desc_de} umrechnet, auf 2 Nachkommastellen gerundet.

  convert({vals[0]}) -> {f(vals[0])}
  convert({vals[1]}) -> {f(vals[1])}

Die Eingabe ist in {unit}.""",
                     "hints": ["Schreib die Formel hin und pack sie dann in round(..., 2)",
                               "Achte auf die Punkt-vor-Strich-Regel — setz Klammern"],
                 })


@drill("binary_ops", "Binary representation", "Binärdarstellung", "Bit tricks", "Medium")
def _binary(rng):
    mode = rng.choice(["count_ones", "to_binary", "is_power_two", "reverse_bits"])
    n = rng.randint(5, 500)

    if mode == "count_ones":
        desc = "counts how many 1-bits the number has in binary"
        desc_de = "zählt, wie viele 1-Bits die Zahl in Binärdarstellung hat"
        ref = lambda n: bin(n).count("1")
        sol = 'return bin(n).count("1")'
    elif mode == "to_binary":
        desc = 'returns the binary representation as a string WITHOUT the "0b" prefix'
        desc_de = 'gibt die Binärdarstellung als String OHNE das "0b" davor zurück'
        ref = lambda n: bin(n)[2:]
        sol = "return bin(n)[2:]"
    elif mode == "is_power_two":
        desc = "returns True if the number is an exact power of two (1, 2, 4, 8, ...)"
        desc_de = ("gibt True zurück, wenn die Zahl eine exakte Zweierpotenz ist "
                   "(1, 2, 4, 8, ...)")
        ref = lambda n: n > 0 and n & (n - 1) == 0
        sol = "return n > 0 and n & (n - 1) == 0"
    else:
        desc = ("returns the number you get by reversing its binary digits "
                "(e.g. 6 = '110' -> '011' = 3)")
        desc_de = ("gibt die Zahl zurück, die entsteht, wenn man ihre Binärziffern "
                   "umdreht (z. B. 6 = '110' -> '011' = 3)")
        ref = lambda n: int(bin(n)[2:][::-1], 2) if n else 0
        sol = "return int(bin(n)[2:][::-1], 2) if n else 0"

    return _task(rng, "binary_ops", "Binary bits", "Bit tricks", "Medium",
                 "solve", f"""
Write solve(n) that {desc}.

  solve({n}) -> {ref(n)!r}
  solve(1)  -> {ref(1)!r}
  solve(0)  -> {ref(0)!r}

bin(n) gives you a string like '0b1011'.""",
                 "n", ref, [(n,), (1,), (0,), (rng.choice([16, 64, 1024]),),
                            (rng.randint(2, 100),), (255,)],
                 ["bin(n) -> '0b101'; slice [2:] to drop the prefix",
                  "int('101', 2) parses a binary string back to a number",
                  "n & (n - 1) clears the lowest set bit"],
                 f"def solve(n):\n    {sol}\n",
                 de={
                     "title": "Binäre Bits",
                     "statement": f"""
Schreib solve(n), das {desc_de}.

  solve({n}) -> {ref(n)!r}
  solve(1)  -> {ref(1)!r}
  solve(0)  -> {ref(0)!r}

bin(n) liefert dir einen String wie '0b1011'.""",
                     "hints": ["bin(n) -> '0b101'; mit [2:] schneidest du das Präfix ab",
                               "int('101', 2) macht aus einem Binärstring wieder eine Zahl",
                               "n & (n - 1) löscht das niedrigste gesetzte Bit"],
                 })


@drill("word_freq", "Word frequency report", "Wörter zählen", "Hash map", "Medium")
def _word_freq(rng):
    text = " ".join(rng.choice(WORDS[:8]) for _ in range(rng.randint(8, 15)))
    k = rng.randint(2, 3)

    def ref(text):
        counts = {}
        for w in text.lower().split():
            counts[w] = counts.get(w, 0) + 1
        ordered = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
        return ordered[:k]

    return _task(rng, "word_freq", f"Top {k} words", "Hash map", "Medium",
                 "top_words", f"""
Write top_words(text) returning the {k} most frequent words as a list of
(word, count) TUPLES, most frequent first. Ties are broken alphabetically.
Words are separated by whitespace and compared lower-cased.

  top_words({text!r})
    -> {ref(text)}""",
                 "text", ref, [(text,), ("",), ("a a b b c",),
                               (rand_text(rng, 6),),
                               ("Same same SAME",),
                               (" ".join(rng.choice(WORDS[:4]) for _ in range(20)),)],
                 ["counts[w] = counts.get(w, 0) + 1 over text.lower().split()",
                  "sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))",
                  f"Slice the first {k}"],
                 f"def top_words(text):\n    counts = {{}}\n"
                 f"    for word in text.lower().split():\n"
                 f"        counts[word] = counts.get(word, 0) + 1\n"
                 f"    ordered = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))\n"
                 f"    return ordered[:{k}]\n",
                 de={
                     "title": f"Die {k} häufigsten Wörter",
                     "statement": f"""
Schreib top_words(text), das die {k} häufigsten Wörter als Liste von
(wort, anzahl)-TUPELN zurückgibt, das häufigste zuerst. Gleichstand wird
alphabetisch aufgelöst. Wörter sind durch Leerraum getrennt und werden
kleingeschrieben verglichen.

  top_words({text!r})
    -> {ref(text)}""",
                     "hints": ["counts[w] = counts.get(w, 0) + 1 über text.lower().split()",
                               "sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))",
                               f"Schneid die ersten {k} heraus"],
                 })


@drill("validate", "Validate input", "Eingaben prüfen", "Errors", "Medium")
def _validate(rng):
    lo, hi = rng.choice([(1, 100), (0, 255), (18, 99), (1, 12)])

    def ref(items):
        good, bad = [], 0
        for item in items:
            try:
                value = int(item)
            except (ValueError, TypeError):
                bad += 1
                continue
            if lo <= value <= hi:
                good.append(value)
            else:
                bad += 1
        return [good, bad]

    sample = [str(rng.randint(lo - 5, hi + 5)) for _ in range(4)] + ["oops", None]
    return _task(rng, "validate", f"Validate {lo}..{hi}", "Errors", "Medium",
                 "validate", f"""
Write validate(items) that checks a list of raw values. A value is GOOD if it
converts to an int AND falls between {lo} and {hi} inclusive.

Return [good_values, bad_count] — a two-element list where the first element is
the list of accepted ints in order.

  validate({sample!r})
    -> {ref(sample)}

Nothing may crash: some items are not numbers at all.""",
                 "items", ref, [(sample,), ([],), ([str(lo), str(hi)],),
                                (["abc", "1.5", None],),
                                ([str(hi + 1), str(lo - 1)],),
                                ([str(rng.randint(lo, hi)) for _ in range(5)],)],
                 ["try: value = int(item) / except (ValueError, TypeError): bad += 1; continue",
                  f"Then the range check: if {lo} <= value <= {hi}",
                  "Return [good, bad] as a list, not a tuple"],
                 f"def validate(items):\n    good, bad = [], 0\n    for item in items:\n"
                 f"        try:\n            value = int(item)\n"
                 f"        except (ValueError, TypeError):\n            bad += 1\n"
                 f"            continue\n        if {lo} <= value <= {hi}:\n"
                 f"            good.append(value)\n        else:\n            bad += 1\n"
                 f"    return [good, bad]\n",
                 de={
                     "title": f"Werte von {lo} bis {hi} prüfen",
                     "statement": f"""
Schreib validate(items), das eine Liste roher Werte prüft. Ein Wert ist GUT,
wenn er sich in ein int umwandeln lässt UND zwischen {lo} und {hi}
einschließlich liegt.

Gib [gute_werte, anzahl_schlechte] zurück — eine zweielementige Liste, deren
erstes Element die Liste der akzeptierten ints in Reihenfolge ist.

  validate({sample!r})
    -> {ref(sample)}

Nichts darf abstürzen: einige Einträge sind überhaupt keine Zahlen.""",
                     "hints": ["try: wert = int(item) / except (ValueError, TypeError): "
                               "schlecht += 1; continue",
                               f"Dann die Bereichsprüfung: if {lo} <= wert <= {hi}",
                               "Gib [gut, schlecht] als Liste zurück, nicht als Tupel"],
                 })


TOPICS: list[str] = []
for _d in REGISTRY:
    if _d.topic not in TOPICS:
        TOPICS.append(_d.topic)
TOPICS.sort()


def generate(topic: str | None = None, difficulty: str | None = None,
             rng: random.Random | None = None) -> Task:
    """Pick a matching drill and build a fresh randomised instance of it."""
    rng = rng or random.Random()
    pool = REGISTRY
    if topic and topic != "All topics":
        pool = [d for d in pool if d.topic == topic]
    if difficulty and difficulty != "Any":
        narrowed = [d for d in pool if d.difficulty == difficulty]
        pool = narrowed or pool
    if not pool:
        pool = REGISTRY
    return rng.choice(pool).build(rng)
