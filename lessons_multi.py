"""Short courses for the non-Python languages.

Four lessons each: the syntax you need to read anything, the collection type
you will reach for constantly, the language's own defining idea, and the string
handling that interview questions actually demand.

These are deliberately not a replacement for learning the language properly —
they are the shortest path to being able to solve the Interview problems in it.

Theory is written in English and German; French and Spanish fall back to
English, same as anywhere else in the app.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import i18n
import languages as LG
from languages import BOOL, INT, L, STR, Sig
from tasks import Task, case

REGISTRY: list["LangLesson"] = []


@dataclass
class LangLesson:
    id: str
    language: str
    section: dict[str, str]
    title: dict[str, str]
    theory: dict[str, str]
    takeaway: dict[str, str]
    example: str
    func: str
    sig: Sig
    statement: dict[str, str]
    cases: list[dict]
    solution: str
    hints: dict[str, list[str]] = field(default_factory=dict)

    def build(self) -> Task:
        backend = LG.get(self.language)
        return Task(
            id=self.id,
            title=i18n.pick(self.title, self.id),
            func=self.func,
            statement=i18n.pick(self.statement, "").strip(),
            starter=backend.starter(self.func, self.sig),
            cases=list(self.cases),
            hints=list(i18n.pick(self.hints, []) or []),
            solution=self.solution,
            difficulty="Easy",
            topic="Basics",
            source="lesson",
            sig=self.sig,
            language=self.language,
        )


def L_(lesson_id, language, section, title, theory, takeaway, example,
       func, sig, statement, cases, solution, hints=None) -> LangLesson:
    lesson = LangLesson(
        id=f"lesson_{language}_{lesson_id}", language=language, section=section,
        title=title, theory=theory, takeaway=takeaway, example=example,
        func=func, sig=sig, statement=statement, cases=cases,
        solution=solution, hints=hints or {})
    REGISTRY.append(lesson)
    return lesson


def for_language(language_id: str) -> list[LangLesson]:
    return [lesson for lesson in REGISTRY if lesson.language == language_id]


SEC_SYNTAX = {"en": "Syntax", "de": "Syntax", "fr": "Syntaxe", "es": "Sintaxis"}
SEC_DATA = {"en": "Collections", "de": "Sammlungen", "fr": "Collections",
            "es": "Colecciones"}
SEC_CORE = {"en": "What makes it different", "de": "Was es besonders macht",
            "fr": "Ce qui le distingue", "es": "Lo que lo distingue"}
SEC_STRINGS = {"en": "Strings & interviews", "de": "Strings & Interviews",
               "fr": "Chaînes et entretiens", "es": "Cadenas y entrevistas"}


# ===========================================================================
#  JAVASCRIPT
# ===========================================================================
L_("syntax", "javascript", SEC_SYNTAX,
   {"en": "Values and let/const", "de": "Werte und let/const"},
   {"en": """JavaScript has one number type. 7 / 2 is 3.5, and there is no separate integer,
so use Math.floor or the bitwise | 0 when you want truncation.

    let count = 0;         // can be reassigned
    const name = "Ada";    // cannot be reassigned
    var old = 1;           // function-scoped, from before 2015 — avoid it

`const` does not freeze the contents: const nums = [1]; nums.push(2) is legal.
It only stops you from pointing the name at something else.

Equality has two forms and you want the strict one:

    1 == "1"     true    // converts before comparing — a source of real bugs
    1 === "1"    false   // no conversion; use this one

Values that count as false: false, 0, "", null, undefined, NaN. Everything else
is true, including [] and {} — an empty array is truthy, so check .length.

Template literals build strings with backticks:

    `${name} is ${age}`""",
    "de": """JavaScript hat nur einen Zahlentyp. 7 / 2 ergibt 3.5, es gibt keine eigene
Ganzzahl — für Abschneiden nimmst du Math.floor oder das bitweise | 0.

    let count = 0;         // kann neu zugewiesen werden
    const name = "Ada";    // kann nicht neu zugewiesen werden
    var old = 1;           // funktionsweit, von vor 2015 — meide es

`const` friert den Inhalt nicht ein: const nums = [1]; nums.push(2) ist erlaubt.
Es verhindert nur, dass der Name auf etwas anderes zeigt.

Gleichheit gibt es zweimal, und du willst die strikte:

    1 == "1"     true    // wandelt vorher um — eine echte Fehlerquelle
    1 === "1"    false   // keine Umwandlung; nimm diese

Als falsch gelten: false, 0, "", null, undefined, NaN. Alles andere ist wahr,
auch [] und {} — ein leeres Array ist truthy, prüf also .length.

Template-Literale bauen Strings mit Backticks:

    `${name} ist ${age}`"""},
   {"en": "Use === and const by default. An empty array is truthy — check .length.",
    "de": "Nimm standardmäßig === und const. Ein leeres Array ist truthy — prüf .length."},
   '''const name = "Ada";
let age = 36;

console.log(`${name} is ${age}`);
console.log("7 / 2 =", 7 / 2, "| floored:", Math.floor(7 / 2));
console.log("7 % 2 =", 7 % 2);

console.log("1 == '1'  ->", 1 == "1");
console.log("1 === '1' ->", 1 === "1");

const nums = [3, 1, 4];
nums.push(1);                 // allowed: const pins the name, not the contents
console.log("nums:", nums, "length:", nums.length);

console.log("[] is truthy:", Boolean([]));
console.log("but [].length is", [].length);

const [first, ...rest] = nums;
console.log("first:", first, "rest:", rest);
''',
   "clock", Sig([("seconds", INT)], STR),
   {"en": """Write clock(seconds) turning a number of seconds into "H:MM:SS".

  clock(3661) -> "1:01:01"
  clock(59)   -> "0:00:59"

Hours have no leading zero; minutes and seconds always have two digits.
Math.floor gives you whole units and % gives the remainder.""",
    "de": """Schreib clock(seconds), das Sekunden in "H:MM:SS" verwandelt.

  clock(3661) -> "1:01:01"
  clock(59)   -> "0:00:59"

Stunden ohne führende Null, Minuten und Sekunden immer zweistellig.
Math.floor liefert ganze Einheiten, % den Rest."""},
   [case(3661, "1:01:01"), case(59, "0:00:59"), case(0, "0:00:00"),
    case(86399, "23:59:59", hidden=True), case(600, "0:10:00", hidden=True)],
   '''function clock(seconds) {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = seconds % 60;
  return `${h}:${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
}
''',
   {"en": ["Math.floor(seconds / 3600) gives the hours",
           "String(m).padStart(2, \"0\") pads a number to two digits",
           "Build the result with a template literal"],
    "de": ["Math.floor(seconds / 3600) ergibt die Stunden",
           "String(m).padStart(2, \"0\") füllt eine Zahl auf zwei Stellen auf",
           "Bau das Ergebnis mit einem Template-Literal"]})

L_("collections", "javascript", SEC_DATA,
   {"en": "Arrays, Map and Set", "de": "Arrays, Map und Set"},
   {"en": """An array is the workhorse. The methods you will actually use:

    nums.push(x) / nums.pop()          add / remove at the end     O(1)
    nums.shift()                       remove from the front       O(n)
    nums.slice(1, 3)                   a copy of part of it
    nums.map(f)  .filter(f)  .reduce(f, start)
    nums.includes(x)                   O(n)
    [...nums]                          a shallow copy

Sorting is the trap. Array.sort compares as TEXT by default:

    [10, 9, 1].sort()               ->  [1, 10, 9]     wrong
    [10, 9, 1].sort((a, b) => a - b) ->  [1, 9, 10]    right

For lookups use Set and Map — both O(1), both keep insertion order:

    const seen = new Set([1, 2]);   seen.has(1)   seen.add(3)   seen.size
    const counts = new Map();       counts.get(k) ?? 0          counts.set(k, v)

A plain object works as a map too, but its keys are always strings, so
obj[1] and obj["1"] are the same entry. Map does not do that.""",
    "de": """Das Array ist das Arbeitspferd. Die Methoden, die du wirklich brauchst:

    nums.push(x) / nums.pop()          hinten anfügen / entfernen  O(1)
    nums.shift()                       vorne entfernen             O(n)
    nums.slice(1, 3)                   eine Teilkopie
    nums.map(f)  .filter(f)  .reduce(f, start)
    nums.includes(x)                   O(n)
    [...nums]                          flache Kopie

Sortieren ist die Falle. Array.sort vergleicht standardmäßig als TEXT:

    [10, 9, 1].sort()               ->  [1, 10, 9]     falsch
    [10, 9, 1].sort((a, b) => a - b) ->  [1, 9, 10]    richtig

Für Nachschlagen nimm Set und Map — beide O(1), beide mit Einfügereihenfolge:

    const seen = new Set([1, 2]);   seen.has(1)   seen.add(3)   seen.size
    const counts = new Map();       counts.get(k) ?? 0          counts.set(k, v)

Ein einfaches Objekt geht auch als Map, aber seine Schlüssel sind immer
Strings — obj[1] und obj["1"] sind derselbe Eintrag. Map macht das nicht."""},
   {"en": "sort() compares as text. Always pass (a, b) => a - b for numbers.",
    "de": "sort() vergleicht als Text. Gib für Zahlen immer (a, b) => a - b mit."},
   '''const nums = [10, 9, 1, 4];

console.log("default sort:", [...nums].sort());
console.log("numeric sort:", [...nums].sort((a, b) => a - b));

console.log("doubled:", nums.map(n => n * 2));
console.log("evens:", nums.filter(n => n % 2 === 0));
console.log("sum:", nums.reduce((a, b) => a + b, 0));

const seen = new Set(nums);
console.log("set:", seen, "has 9:", seen.has(9), "size:", seen.size);

const counts = new Map();
for (const ch of "mississippi") counts.set(ch, (counts.get(ch) ?? 0) + 1);
console.log("counts:", counts);

const byCount = [...counts.entries()].sort((a, b) => b[1] - a[1]);
console.log("most common:", byCount[0]);
''',
   "second_largest", Sig([("nums", L(INT))], INT),
   {"en": """Write second_largest(nums) returning the second largest DISTINCT value.
Return -1 if there are fewer than two distinct values.

  second_largest([3, 1, 4, 4, 5]) -> 4
  second_largest([7, 7, 7])       -> -1

A Set removes the duplicates. Remember that sort needs a comparator.""",
    "de": """Schreib second_largest(nums), das den zweitgrößten VERSCHIEDENEN Wert liefert.
Gib -1 zurück, wenn es weniger als zwei verschiedene Werte gibt.

  second_largest([3, 1, 4, 4, 5]) -> 4
  second_largest([7, 7, 7])       -> -1

Ein Set entfernt die Duplikate. Denk daran, dass sort einen Vergleicher braucht."""},
   [case([3, 1, 4, 4, 5], 4), case([7, 7, 7], -1), case([2, 1], 1),
    case([], -1, hidden=True), case([-5, -2, -9, -2], -5, hidden=True)],
   '''function second_largest(nums) {
  const distinct = [...new Set(nums)].sort((a, b) => a - b);
  return distinct.length < 2 ? -1 : distinct[distinct.length - 2];
}
''',
   {"en": ["new Set(nums) throws away the duplicates",
           "Spread it back into an array with [...set]",
           "sort((a, b) => a - b), then take the second from the end"],
    "de": ["new Set(nums) wirft die Duplikate weg",
           "Mit [...set] wieder in ein Array ausbreiten",
           "sort((a, b) => a - b), dann das zweitletzte nehmen"]})

L_("functions", "javascript", SEC_CORE,
   {"en": "Functions are values", "de": "Funktionen sind Werte"},
   {"en": """A function in JavaScript is an ordinary value: you can store it, pass it and
return it. That is why map/filter/reduce look the way they do.

    function named(a) { return a * 2; }      // hoisted
    const arrow = a => a * 2;                // concise, no own `this`
    const block = (a, b) => { return a + b; };

A closure is a function that remembers the variables around it, even after the
outer call has finished. This is the single most-asked JavaScript concept:

    function counter() {
      let n = 0;
      return () => ++n;          // still sees n
    }
    const next = counter();
    next(); next();              // 1, then 2

Useful shorthands you will read everywhere:

    a ?? b         b only when a is null or undefined (0 and "" survive)
    a?.b           undefined instead of throwing when a is null/undefined
    const {x, y} = point;        destructuring
    f(...args)                   spread""",
    "de": """Eine Funktion ist in JavaScript ein ganz normaler Wert: du kannst sie
speichern, übergeben und zurückgeben. Deshalb sehen map/filter/reduce so aus.

    function named(a) { return a * 2; }      // wird hochgezogen
    const arrow = a => a * 2;                // kurz, ohne eigenes `this`
    const block = (a, b) => { return a + b; };

Eine Closure ist eine Funktion, die sich die Variablen um sie herum merkt —
auch nachdem der äußere Aufruf beendet ist. Das ist das meistgefragte
JavaScript-Konzept überhaupt:

    function counter() {
      let n = 0;
      return () => ++n;          // sieht n weiterhin
    }
    const next = counter();
    next(); next();              // 1, dann 2

Kurzschreibweisen, die dir überall begegnen:

    a ?? b         b nur, wenn a null oder undefined ist (0 und "" bleiben)
    a?.b           undefined statt Absturz, wenn a null/undefined ist
    const {x, y} = point;        Destrukturierung
    f(...args)                   Spread"""},
   {"en": "A closure keeps the variables it was created with. That is the whole trick.",
    "de": "Eine Closure behält die Variablen, mit denen sie entstand. Das ist der ganze Trick."},
   '''const double = n => n * 2;
const apply = (fn, value) => fn(fn(value));
console.log("apply twice:", apply(double, 3));

function counter() {
  let n = 0;
  return () => ++n;
}
const next = counter();
console.log(next(), next(), next());

const other = counter();          // its own private n
console.log("a fresh counter:", other());

console.log("?? keeps 0:", 0 ?? 99, "| || does not:", 0 || 99);

const point = { x: 3, y: 4 };
const { x, y } = point;
console.log("destructured:", x, y);
console.log("optional chain on missing:", point.z?.deep);

const nums = [5, 3, 9];
console.log("spread into Math.max:", Math.max(...nums));
''',
   "running_max", Sig([("nums", L(INT))], L(INT)),
   {"en": """Write running_max(nums) returning the biggest value seen so far at every
position. The result has the same length as the input.

  running_max([1, 3, 2, 5]) -> [1, 3, 3, 5]
  running_max([])           -> []

Keep one variable outside the loop and update it as you go.""",
    "de": """Schreib running_max(nums), das an jeder Position den bisher größten Wert
zurückgibt. Das Ergebnis hat dieselbe Länge wie die Eingabe.

  running_max([1, 3, 2, 5]) -> [1, 3, 3, 5]
  running_max([])           -> []

Führ eine Variable außerhalb der Schleife und aktualisier sie unterwegs."""},
   [case([1, 3, 2, 5], [1, 3, 3, 5]), case([], []), case([4], [4]),
    case([5, 4, 3], [5, 5, 5], hidden=True),
    case([-3, -1, -2], [-3, -1, -1], hidden=True)],
   '''function running_max(nums) {
  const out = [];
  let best = null;
  for (const n of nums) {
    best = best === null ? n : Math.max(best, n);
    out.push(best);
  }
  return out;
}
''',
   {"en": ["Hold the best value in a variable outside the loop",
           "Push the accumulator AFTER updating it",
           "The empty input must give an empty array"],
    "de": ["Halt den besten Wert in einer Variablen außerhalb der Schleife",
           "Häng den Akkumulator an, NACHDEM du ihn aktualisiert hast",
           "Die leere Eingabe muss ein leeres Array ergeben"]})

L_("strings", "javascript", SEC_STRINGS,
   {"en": "Strings", "de": "Zeichenketten"},
   {"en": """Strings are immutable: every method returns a new one.

    s.length                       not a method
    s[0]  or  s.charAt(0)
    s.slice(1, 4)                  s.slice(-3) takes the last three
    s.toUpperCase() / .toLowerCase()
    s.trim()  .split(" ")  .includes("x")  .indexOf("x")
    arr.join("-")

There is no built-in reverse for strings — go through an array:

    [...s].reverse().join("")

Building a string in a loop with += is fine in modern engines, but collecting
into an array and joining once is still the habit interviewers expect.

For counting characters, a Map beats an object because it keeps non-string keys
and has a clean .get default with ?? 0.""",
    "de": """Strings sind unveränderlich: jede Methode gibt einen neuen zurück.

    s.length                       keine Methode
    s[0]  oder  s.charAt(0)
    s.slice(1, 4)                  s.slice(-3) nimmt die letzten drei
    s.toUpperCase() / .toLowerCase()
    s.trim()  .split(" ")  .includes("x")  .indexOf("x")
    arr.join("-")

Für Strings gibt es kein eingebautes reverse — geh über ein Array:

    [...s].reverse().join("")

Einen String in einer Schleife mit += zu bauen ist in modernen Engines in
Ordnung, aber in ein Array zu sammeln und einmal zu joinen ist weiterhin die
Gewohnheit, die Interviewer erwarten.

Zum Zeichenzählen ist eine Map besser als ein Objekt: sie behält
Nicht-String-Schlüssel und hat mit ?? 0 einen sauberen Vorgabewert."""},
   {"en": "No string reverse — spread into an array first. Count with a Map.",
    "de": "Kein reverse für Strings — erst in ein Array ausbreiten. Zählen mit einer Map."},
   '''const s = "  Hello, World  ";

console.log(JSON.stringify(s.trim()));
console.log("upper:", s.trim().toUpperCase());
console.log("split:", s.trim().split(", "));
console.log("last three:", s.trim().slice(-3));
console.log("reversed:", [...s.trim()].reverse().join(""));

const counts = new Map();
for (const ch of "mississippi") counts.set(ch, (counts.get(ch) ?? 0) + 1);
console.log("counts:", [...counts]);

const firstUnique = [..."swiss"].find(ch =>
  [..."swiss"].filter(c => c === ch).length === 1);
console.log("first unique in 'swiss':", firstUnique);

const parts = [];
for (let i = 0; i < 5; i++) parts.push(i * i);
console.log(parts.join(", "));
''',
   "normalise", Sig([("text", STR)], STR),
   {"en": """Write normalise(text) that cleans up a messy name:

  * trim both ends
  * collapse any run of inner whitespace to a single space
  * capitalise each word: first letter upper, the rest lower

  normalise("  aDA   LOVElace ") -> "Ada Lovelace"
  normalise("   ")               -> ""

split(/\\s+/) on a trimmed string gives you the words.""",
    "de": """Schreib normalise(text), das einen unordentlichen Namen aufräumt:

  * an beiden Enden trimmen
  * jede Folge innerer Leerzeichen auf eines reduzieren
  * jedes Wort groß schreiben: erster Buchstabe groß, Rest klein

  normalise("  aDA   LOVElace ") -> "Ada Lovelace"
  normalise("   ")               -> ""

split(/\\s+/) auf einem getrimmten String liefert dir die Wörter."""},
   [case("  aDA   LOVElace ", "Ada Lovelace"),
    case("guido van ROSSUM", "Guido Van Rossum"), case("   ", ""),
    case("a", "A", hidden=True),
    case("  linus     TORVALDS  ", "Linus Torvalds", hidden=True)],
   '''function normalise(text) {
  const words = text.trim().split(/\\s+/).filter(Boolean);
  return words
    .map(w => w[0].toUpperCase() + w.slice(1).toLowerCase())
    .join(" ");
}
''',
   {"en": ["trim() first, then split on /\\s+/",
           "filter(Boolean) drops the empty piece an all-space string leaves",
           "w[0].toUpperCase() + w.slice(1).toLowerCase() capitalises one word"],
    "de": ["Erst trim(), dann an /\\s+/ trennen",
           "filter(Boolean) wirft das leere Stück weg, das ein reiner Leerstring lässt",
           "w[0].toUpperCase() + w.slice(1).toLowerCase() macht ein Wort groß"]})


# ===========================================================================
#  JAVA
# ===========================================================================
L_("syntax", "java", SEC_SYNTAX,
   {"en": "Types and integer maths", "de": "Typen und Ganzzahlrechnung"},
   {"en": """Java declares the type of everything. That is the biggest change coming from
Python, and it is also what lets the compiler catch your mistakes.

    int count = 0;
    long big = 3_000_000_000L;     // int stops at about 2.1 billion
    double ratio = 7 / 2.0;
    boolean ready = true;
    String name = "Ada";           // capital S — it is a class
    var guessed = 42;              // the compiler infers int

Integer division truncates and does NOT become a fraction:

    7 / 2    ->  3        both operands are int
    7 / 2.0  ->  3.5      one is a double, so the result is
    7 % 2    ->  1

That first line bites everyone once. If you want a real quotient, make one side
a double.

Overflow is silent: int arithmetic wraps around instead of raising. When a
problem multiplies values, use long — the exercises here already do.

Every program lives in a class, and printing is System.out.println(...).""",
    "de": """Java deklariert den Typ von allem. Das ist die größte Umstellung von Python
her, und genau das lässt den Compiler deine Fehler finden.

    int count = 0;
    long big = 3_000_000_000L;     // int endet bei etwa 2,1 Milliarden
    double ratio = 7 / 2.0;
    boolean ready = true;
    String name = "Ada";           // großes S — es ist eine Klasse
    var guessed = 42;              // der Compiler folgert int

Ganzzahldivision schneidet ab und wird NICHT zum Bruch:

    7 / 2    ->  3        beide Operanden sind int
    7 / 2.0  ->  3.5      einer ist double, also ist es das Ergebnis auch
    7 % 2    ->  1

Diese erste Zeile erwischt jeden einmal. Willst du einen echten Quotienten,
mach eine Seite zu double.

Überlauf passiert lautlos: int-Rechnung läuft über, statt einen Fehler zu
werfen. Wenn eine Aufgabe multipliziert, nimm long — die Übungen hier tun das.

Jedes Programm lebt in einer Klasse, und ausgegeben wird mit
System.out.println(...)."""},
   {"en": "int / int stays an int. Use long when anything gets multiplied.",
    "de": "int / int bleibt int. Nimm long, sobald irgendetwas multipliziert wird."},
   '''public class Main {
    public static void main(String[] args) {
        int count = 7;
        long big = 3_000_000_000L;
        String name = "Ada";

        System.out.println(name + " has " + count);
        System.out.println("7 / 2   = " + (7 / 2));
        System.out.println("7 / 2.0 = " + (7 / 2.0));
        System.out.println("7 % 2   = " + (7 % 2));
        System.out.println("big     = " + big);

        int overflows = Integer.MAX_VALUE;
        System.out.println("int max + 1 = " + (overflows + 1));
        System.out.println("as long     = " + ((long) overflows + 1));

        System.out.printf("%s is %d, padded %05d%n", name, count, count);
        System.out.println(String.format("%.3f", 2.0 / 3));
    }
}
''',
   "clock", Sig([("seconds", INT)], STR),
   {"en": """Write clock(seconds) turning a number of seconds into "H:MM:SS".

  clock(3661) -> "1:01:01"
  clock(59)   -> "0:00:59"

Hours have no leading zero; minutes and seconds always have two digits.
Integer division gives whole units, % gives the remainder, and
String.format("%02d", n) pads to two digits.""",
    "de": """Schreib clock(seconds), das Sekunden in "H:MM:SS" verwandelt.

  clock(3661) -> "1:01:01"
  clock(59)   -> "0:00:59"

Stunden ohne führende Null, Minuten und Sekunden immer zweistellig.
Ganzzahldivision liefert ganze Einheiten, % den Rest, und
String.format("%02d", n) füllt auf zwei Stellen auf."""},
   [case(3661, "1:01:01"), case(59, "0:00:59"), case(0, "0:00:00"),
    case(86399, "23:59:59", hidden=True), case(600, "0:10:00", hidden=True)],
   '''class Solution {
    static String clock(long seconds) {
        long h = seconds / 3600;
        long m = (seconds % 3600) / 60;
        long s = seconds % 60;
        return String.format("%d:%02d:%02d", h, m, s);
    }
}
''',
   {"en": ["seconds / 3600 already truncates — that is the hours",
           "(seconds % 3600) / 60 gives the minutes",
           "String.format(\"%d:%02d:%02d\", h, m, s) does the padding"],
    "de": ["seconds / 3600 schneidet schon ab — das sind die Stunden",
           "(seconds % 3600) / 60 ergibt die Minuten",
           "String.format(\"%d:%02d:%02d\", h, m, s) füllt auf"]})

L_("collections", "java", SEC_DATA,
   {"en": "Arrays, List, Map, Set", "de": "Arrays, List, Map, Set"},
   {"en": """An array has a fixed length and a bare syntax:

    long[] nums = {3, 1, 4};
    nums.length            a field, not a method
    Arrays.sort(nums);     sorts in place
    Arrays.toString(nums)  because printing an array shows its address

For anything that grows, use the collections:

    List<Long> list = new ArrayList<>();
    list.add(5L);  list.get(0);  list.size();
    Map<String, Integer> counts = new HashMap<>();
    counts.merge(key, 1, Integer::sum);        the idiomatic counter
    counts.getOrDefault(key, 0)
    Set<Long> seen = new HashSet<>();
    seen.add(x)            returns false if it was already there

Generics cannot hold primitives, so it is List<Long>, not List<long>. Java
boxes and unboxes for you, which is convenient and occasionally slow.

The trap: == on objects compares identity, not contents. Use .equals for
String and boxed numbers. For arrays use Arrays.equals.""",
    "de": """Ein Array hat feste Länge und eine nackte Syntax:

    long[] nums = {3, 1, 4};
    nums.length            ein Feld, keine Methode
    Arrays.sort(nums);     sortiert an Ort und Stelle
    Arrays.toString(nums)  denn ein Array auszugeben zeigt seine Adresse

Für alles, was wächst, nimm die Collections:

    List<Long> list = new ArrayList<>();
    list.add(5L);  list.get(0);  list.size();
    Map<String, Integer> counts = new HashMap<>();
    counts.merge(key, 1, Integer::sum);        der idiomatische Zähler
    counts.getOrDefault(key, 0)
    Set<Long> seen = new HashSet<>();
    seen.add(x)            liefert false, wenn es schon drin war

Generics können keine primitiven Typen halten, also List<Long>, nicht
List<long>. Java packt für dich ein und aus — bequem und gelegentlich langsam.

Die Falle: == vergleicht bei Objekten die Identität, nicht den Inhalt. Nimm
.equals für String und eingepackte Zahlen, Arrays.equals für Arrays."""},
   {"en": "== compares identity for objects. Use .equals, and Arrays.equals for arrays.",
    "de": "== vergleicht bei Objekten die Identität. Nimm .equals, für Arrays Arrays.equals."},
   '''import java.util.*;

public class Main {
    public static void main(String[] args) {
        long[] nums = {10, 9, 1, 4};
        Arrays.sort(nums);
        System.out.println("sorted: " + Arrays.toString(nums));

        List<Long> list = new ArrayList<>();
        for (long n : nums) list.add(n * 2);
        System.out.println("doubled: " + list);

        Map<Character, Integer> counts = new HashMap<>();
        for (char c : "mississippi".toCharArray())
            counts.merge(c, 1, Integer::sum);
        System.out.println("counts: " + counts);

        Set<Long> seen = new HashSet<>();
        for (long n : new long[]{1, 2, 1}) {
            if (!seen.add(n)) System.out.println("duplicate: " + n);
        }

        String a = "ab", b = "a" + "b";
        System.out.println("a.equals(b): " + a.equals(b));
        System.out.println("new String comparison with ==: "
            + (a == new String("ab")));
    }
}
''',
   "second_largest", Sig([("nums", L(INT))], INT),
   {"en": """Write second_largest(nums) returning the second largest DISTINCT value.
Return -1 if there are fewer than two distinct values.

  second_largest([3, 1, 4, 4, 5]) -> 4
  second_largest([7, 7, 7])       -> -1

A TreeSet keeps values sorted and unique, which does most of the work.""",
    "de": """Schreib second_largest(nums), das den zweitgrößten VERSCHIEDENEN Wert liefert.
Gib -1 zurück, wenn es weniger als zwei verschiedene Werte gibt.

  second_largest([3, 1, 4, 4, 5]) -> 4
  second_largest([7, 7, 7])       -> -1

Ein TreeSet hält Werte sortiert und eindeutig — das erledigt die meiste Arbeit."""},
   [case([3, 1, 4, 4, 5], 4), case([7, 7, 7], -1), case([2, 1], 1),
    case([], -1, hidden=True), case([-5, -2, -9, -2], -5, hidden=True)],
   '''import java.util.TreeSet;

class Solution {
    static long second_largest(long[] nums) {
        TreeSet<Long> distinct = new TreeSet<>();
        for (long n : nums) distinct.add(n);
        if (distinct.size() < 2) return -1;
        distinct.pollLast();
        return distinct.last();
    }
}
''',
   {"en": ["A TreeSet is sorted and holds each value once",
           "pollLast() removes and returns the biggest",
           "Check size() before you reach for anything"],
    "de": ["Ein TreeSet ist sortiert und hält jeden Wert einmal",
           "pollLast() entfernt das größte und gibt es zurück",
           "Prüf size(), bevor du auf etwas zugreifst"]})

L_("classes", "java", SEC_CORE,
   {"en": "Classes and objects", "de": "Klassen und Objekte"},
   {"en": """Everything in Java lives in a class, so knowing how to write a small one is not
optional even for a coding test.

    class Student {
        final String name;         // final = assigned once
        int score;

        Student(String name, int score) {   // constructor: same name, no return
            this.name = name;
            this.score = score;
        }

        boolean beats(Student other) { return this.score > other.score; }

        @Override
        public String toString() { return name + "(" + score + ")"; }
    }

`static` means "belongs to the class, not to an instance" — that is why the
exercises here are static methods: the harness calls Solution.method(...)
without creating an object.

A record is the short form for a plain data holder, and gives you the
constructor, equals, hashCode and toString for free:

    record Point(int x, int y) {}""",
    "de": """In Java lebt alles in einer Klasse — eine kleine schreiben zu können ist also
auch für einen Coding-Test nicht optional.

    class Student {
        final String name;         // final = einmal zugewiesen
        int score;

        Student(String name, int score) {   // Konstruktor: gleicher Name, kein return
            this.name = name;
            this.score = score;
        }

        boolean beats(Student other) { return this.score > other.score; }

        @Override
        public String toString() { return name + "(" + score + ")"; }
    }

`static` heißt „gehört zur Klasse, nicht zu einer Instanz" — deshalb sind die
Übungen hier statische Methoden: der Testrahmen ruft Solution.methode(...) auf,
ohne ein Objekt zu erzeugen.

Ein record ist die Kurzform für einen reinen Datenhalter und schenkt dir
Konstruktor, equals, hashCode und toString:

    record Point(int x, int y) {}"""},
   {"en": "static belongs to the class; this.field is the instance. record is the short form.",
    "de": "static gehört zur Klasse, this.feld zur Instanz. record ist die Kurzform."},
   '''import java.util.*;

public class Main {
    record Point(int x, int y) {}

    static class Student {
        final String name;
        int score;

        Student(String name, int score) {
            this.name = name;
            this.score = score;
        }

        @Override
        public String toString() { return name + "(" + score + ")"; }
    }

    public static void main(String[] args) {
        List<Student> students = new ArrayList<>();
        students.add(new Student("Ada", 92));
        students.add(new Student("Linus", 78));
        students.add(new Student("Grace", 99));

        students.sort(Comparator.comparingInt(s -> -s.score));
        System.out.println("by score: " + students);
        System.out.println("winner: " + students.get(0).name);

        Point p = new Point(3, 4);
        System.out.println("record prints itself: " + p);
        System.out.println("and compares by value: " + p.equals(new Point(3, 4)));
    }
}
''',
   "top_scorer", Sig([("names", L(STR)), ("scores", L(INT))], STR),
   {"en": """Two lists of the same length: names[i] scored scores[i]. Return the name with
the highest score. If several tie, return the one that comes first in the list.
Return "" for empty input.

  top_scorer(["Ada", "Linus"], [92, 78]) -> "Ada"

Write it however you like — but this is a good place to try a small helper
class, because that is what Java expects of you.""",
    "de": """Zwei gleich lange Listen: names[i] hat scores[i] Punkte. Gib den Namen mit der
höchsten Punktzahl zurück. Bei Gleichstand den, der zuerst in der Liste steht.
Für leere Eingaben "".

  top_scorer(["Ada", "Linus"], [92, 78]) -> "Ada"

Schreib es, wie du willst — aber hier lohnt sich eine kleine Hilfsklasse, denn
genau das erwartet Java von dir."""},
   [case((["Ada", "Linus"], [92, 78]), "Ada"),
    case((["Ada", "Grace"], [92, 99]), "Grace"),
    case(([], []), ""),
    case((["a", "b", "c"], [5, 5, 1]), "a", hidden=True),
    case((["solo"], [0]), "solo", hidden=True)],
   '''class Solution {
    static String top_scorer(String[] names, long[] scores) {
        if (names.length == 0) return "";
        int best = 0;
        for (int i = 1; i < names.length; i++) {
            if (scores[i] > scores[best]) best = i;
        }
        return names[best];
    }
}
''',
   {"en": ["Track the index of the best score, not the score itself",
           "Use a strict > so the earliest of a tie wins",
           "Guard the empty input before touching index 0"],
    "de": ["Merk dir den Index der besten Punktzahl, nicht die Punktzahl",
           "Nimm ein striktes >, damit bei Gleichstand der frühere gewinnt",
           "Fang die leere Eingabe ab, bevor du auf Index 0 zugreifst"]})

L_("strings", "java", SEC_STRINGS,
   {"en": "Strings and StringBuilder", "de": "Strings und StringBuilder"},
   {"en": """String is immutable. Every "change" makes a new object, which is why building
one in a loop with += is O(n^2) and why StringBuilder exists.

    s.length()             a method here, unlike arrays
    s.charAt(0)            there is no s[0]
    s.substring(1, 4)      start inclusive, end exclusive
    s.toUpperCase()  .trim()  .isEmpty()  .contains("x")  .indexOf("x")
    s.split("\\\\s+")        takes a REGULAR EXPRESSION, not a plain string
    String.join("-", parts)

    StringBuilder sb = new StringBuilder();
    sb.append("x");
    sb.reverse();
    sb.toString();

Two traps worth remembering: split takes a regex, so split(".") splits on every
character and gives you nothing; and comparing with == checks identity, so
always use .equals for text.""",
    "de": """String ist unveränderlich. Jede „Änderung" erzeugt ein neues Objekt — deshalb
ist der Aufbau in einer Schleife mit += O(n^2), und deshalb gibt es
StringBuilder.

    s.length()             hier eine Methode, anders als bei Arrays
    s.charAt(0)            ein s[0] gibt es nicht
    s.substring(1, 4)      Start dabei, Ende nicht
    s.toUpperCase()  .trim()  .isEmpty()  .contains("x")  .indexOf("x")
    s.split("\\\\s+")        nimmt einen REGULÄREN AUSDRUCK, keinen einfachen String
    String.join("-", parts)

    StringBuilder sb = new StringBuilder();
    sb.append("x");
    sb.reverse();
    sb.toString();

Zwei Fallen zum Merken: split nimmt einen Regex, split(".") trennt also an
jedem Zeichen und liefert nichts; und == vergleicht die Identität — für Text
also immer .equals."""},
   {"en": "split takes a regex. Use .equals for text and StringBuilder in loops.",
    "de": "split nimmt einen Regex. Für Text .equals, in Schleifen StringBuilder."},
   '''import java.util.*;

public class Main {
    public static void main(String[] args) {
        String s = "  Hello, World  ";

        System.out.println("[" + s.trim() + "]");
        System.out.println("upper: " + s.trim().toUpperCase());
        System.out.println("substring: " + s.trim().substring(0, 5));
        System.out.println("split: " + Arrays.toString(s.trim().split(",\\\\s*")));
        System.out.println("joined: " + String.join("-", "a", "b", "c"));

        System.out.println("reversed: "
            + new StringBuilder("interview").reverse());

        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < 5; i++) sb.append(i * i).append(" ");
        System.out.println("built: " + sb.toString().trim());

        System.out.println("split(\\".\\") gives "
            + "hello".split("\\\\.").length + " part(s) with an escaped dot");
    }
}
''',
   "normalise", Sig([("text", STR)], STR),
   {"en": """Write normalise(text) that cleans up a messy name:

  * trim both ends
  * collapse any run of inner whitespace to a single space
  * capitalise each word: first letter upper, the rest lower

  normalise("  aDA   LOVElace ") -> "Ada Lovelace"
  normalise("   ")               -> ""

trim() then split("\\\\s+") gives you the words — mind the regex.""",
    "de": """Schreib normalise(text), das einen unordentlichen Namen aufräumt:

  * an beiden Enden trimmen
  * jede Folge innerer Leerzeichen auf eine reduzieren
  * jedes Wort groß schreiben: erster Buchstabe groß, Rest klein

  normalise("  aDA   LOVElace ") -> "Ada Lovelace"
  normalise("   ")               -> ""

trim() und dann split("\\\\s+") liefert die Wörter — achte auf den Regex."""},
   [case("  aDA   LOVElace ", "Ada Lovelace"),
    case("guido van ROSSUM", "Guido Van Rossum"), case("   ", ""),
    case("a", "A", hidden=True),
    case("  linus     TORVALDS  ", "Linus Torvalds", hidden=True)],
   '''class Solution {
    static String normalise(String text) {
        String trimmed = text.trim();
        if (trimmed.isEmpty()) return "";
        StringBuilder out = new StringBuilder();
        for (String word : trimmed.split("\\\\s+")) {
            if (out.length() > 0) out.append(' ');
            out.append(Character.toUpperCase(word.charAt(0)));
            out.append(word.substring(1).toLowerCase());
        }
        return out.toString();
    }
}
''',
   {"en": ["trim() first, and return early when nothing is left",
           "split(\"\\\\s+\") on the trimmed text gives the words",
           "Build the answer in a StringBuilder"],
    "de": ["Erst trim(), und früh zurückkehren, wenn nichts übrig bleibt",
           "split(\"\\\\s+\") auf dem getrimmten Text liefert die Wörter",
           "Bau die Antwort in einem StringBuilder"]})


# ===========================================================================
#  C#
# ===========================================================================
L_("syntax", "csharp", SEC_SYNTAX,
   {"en": "Types and var", "de": "Typen und var"},
   {"en": """C# is statically typed, but `var` lets the compiler work the type out for you.
The variable still has one fixed type — this is not Python's dynamism.

    int count = 0;
    long big = 3_000_000_000L;
    double ratio = 7 / 2.0;
    bool ready = true;
    string name = "Ada";           // lower-case string, an alias for String
    var inferred = 42;             // int, decided at compile time

Integer division truncates, exactly as in Java:

    7 / 2    ->  3
    7 / 2.0  ->  3.5
    7 % 2    ->  1

String interpolation is the nicest of the C-family:

    $"{name} is {count}"           and $"{value,5:F2}" aligns and rounds

Two things you will meet constantly: `?` marks a nullable type (int? may be
null), and `??` supplies a fallback when something is null.""",
    "de": """C# ist statisch typisiert, aber `var` lässt den Compiler den Typ herleiten. Die
Variable hat trotzdem einen festen Typ — das ist nicht Pythons Dynamik.

    int count = 0;
    long big = 3_000_000_000L;
    double ratio = 7 / 2.0;
    bool ready = true;
    string name = "Ada";           // kleingeschriebenes string, Alias für String
    var inferred = 42;             // int, zur Übersetzungszeit entschieden

Ganzzahldivision schneidet ab, genau wie in Java:

    7 / 2    ->  3
    7 / 2.0  ->  3.5
    7 % 2    ->  1

String-Interpolation ist die angenehmste der C-Familie:

    $"{name} ist {count}"          und $"{value,5:F2}" richtet aus und rundet

Zwei Dinge begegnen dir ständig: `?` markiert einen nullbaren Typ (int? darf
null sein), und `??` liefert einen Ersatzwert, wenn etwas null ist."""},
   {"en": "var is inference, not dynamic typing. int / int still truncates.",
    "de": "var ist Herleitung, keine dynamische Typisierung. int / int schneidet weiter ab."},
   '''using System;

class Program
{
    static void Main()
    {
        var name = "Ada";
        int count = 7;
        long big = 3_000_000_000L;

        Console.WriteLine($"{name} has {count}");
        Console.WriteLine($"7 / 2   = {7 / 2}");
        Console.WriteLine($"7 / 2.0 = {7 / 2.0}");
        Console.WriteLine($"7 % 2   = {7 % 2}");
        Console.WriteLine($"big     = {big}");

        Console.WriteLine($"padded: {count:D5}  aligned: |{count,6}|");
        Console.WriteLine($"rounded: {2.0 / 3:F3}");

        int? maybe = null;
        Console.WriteLine($"?? fallback: {maybe ?? -1}");

        string text = null;
        Console.WriteLine($"?. on null: {text?.Length ?? 0}");
    }
}
''',
   "clock", Sig([("seconds", INT)], STR),
   {"en": """Write clock(seconds) turning a number of seconds into "H:MM:SS".

  clock(3661) -> "1:01:01"
  clock(59)   -> "0:00:59"

Hours have no leading zero; minutes and seconds always have two digits.
Interpolation can pad for you: $"{m:D2}".""",
    "de": """Schreib clock(seconds), das Sekunden in "H:MM:SS" verwandelt.

  clock(3661) -> "1:01:01"
  clock(59)   -> "0:00:59"

Stunden ohne führende Null, Minuten und Sekunden immer zweistellig.
Die Interpolation füllt für dich auf: $"{m:D2}"."""},
   [case(3661, "1:01:01"), case(59, "0:00:59"), case(0, "0:00:00"),
    case(86399, "23:59:59", hidden=True), case(600, "0:10:00", hidden=True)],
   '''public static class Solution
{
    public static string clock(long seconds)
    {
        long h = seconds / 3600;
        long m = (seconds % 3600) / 60;
        long s = seconds % 60;
        return $"{h}:{m:D2}:{s:D2}";
    }
}
''',
   {"en": ["seconds / 3600 truncates — those are the hours",
           "(seconds % 3600) / 60 gives the minutes",
           "$\"{m:D2}\" pads a number to two digits"],
    "de": ["seconds / 3600 schneidet ab — das sind die Stunden",
           "(seconds % 3600) / 60 ergibt die Minuten",
           "$\"{m:D2}\" füllt eine Zahl auf zwei Stellen auf"]})

L_("collections", "csharp", SEC_DATA,
   {"en": "Arrays, List, Dictionary", "de": "Arrays, List, Dictionary"},
   {"en": """    long[] nums = {3, 1, 4};       fixed length
    nums.Length                    a property
    Array.Sort(nums);              in place

    var list = new List<long>();
    list.Add(5);  list[0];  list.Count;  list.Contains(5);

    var counts = new Dictionary<string, int>();
    counts["a"] = counts.GetValueOrDefault("a") + 1;
    if (counts.TryGetValue(key, out var n)) { ... }

    var seen = new HashSet<long>();
    seen.Add(x)                    returns false if it was already there

Note the capitals: C# methods and properties are PascalCase, so it is
`Count`, not `count`, and `Add`, not `add`.

The `out var n` pattern above is worth learning — it does the lookup and the
"was it there?" check in one step, without hashing twice.""",
    "de": """    long[] nums = {3, 1, 4};       feste Länge
    nums.Length                    eine Property
    Array.Sort(nums);              an Ort und Stelle

    var list = new List<long>();
    list.Add(5);  list[0];  list.Count;  list.Contains(5);

    var counts = new Dictionary<string, int>();
    counts["a"] = counts.GetValueOrDefault("a") + 1;
    if (counts.TryGetValue(key, out var n)) { ... }

    var seen = new HashSet<long>();
    seen.Add(x)                    liefert false, wenn es schon drin war

Achte auf die Großschreibung: Methoden und Properties sind in C# PascalCase,
also `Count`, nicht `count`, und `Add`, nicht `add`.

Das `out var n` oben lohnt sich zu lernen — es macht Nachschlagen und die
Frage „war es da?" in einem Schritt, ohne zweimal zu hashen."""},
   {"en": "PascalCase everywhere. TryGetValue with out does lookup and test in one.",
    "de": "Überall PascalCase. TryGetValue mit out macht Nachschlagen und Prüfen in einem."},
   '''using System;
using System.Collections.Generic;

class Program
{
    static void Main()
    {
        long[] nums = {10, 9, 1, 4};
        Array.Sort(nums);
        Console.WriteLine("sorted: [" + string.Join(", ", nums) + "]");

        var list = new List<long>();
        foreach (var n in nums) list.Add(n * 2);
        Console.WriteLine("doubled: [" + string.Join(", ", list) + "]");

        var counts = new Dictionary<char, int>();
        foreach (var c in "mississippi")
            counts[c] = counts.GetValueOrDefault(c) + 1;
        foreach (var pair in counts)
            Console.WriteLine($"  {pair.Key} -> {pair.Value}");

        var seen = new HashSet<long>();
        foreach (var n in new long[]{1, 2, 1})
            if (!seen.Add(n)) Console.WriteLine($"duplicate: {n}");

        if (counts.TryGetValue('s', out var s))
            Console.WriteLine($"found s = {s} in one lookup");
    }
}
''',
   "second_largest", Sig([("nums", L(INT))], INT),
   {"en": """Write second_largest(nums) returning the second largest DISTINCT value.
Return -1 if there are fewer than two distinct values.

  second_largest([3, 1, 4, 4, 5]) -> 4
  second_largest([7, 7, 7])       -> -1

A HashSet removes the duplicates; sorting the rest finishes it.""",
    "de": """Schreib second_largest(nums), das den zweitgrößten VERSCHIEDENEN Wert liefert.
Gib -1 zurück, wenn es weniger als zwei verschiedene Werte gibt.

  second_largest([3, 1, 4, 4, 5]) -> 4
  second_largest([7, 7, 7])       -> -1

Ein HashSet entfernt die Duplikate; das Sortieren des Rests erledigt den Rest."""},
   [case([3, 1, 4, 4, 5], 4), case([7, 7, 7], -1), case([2, 1], 1),
    case([], -1, hidden=True), case([-5, -2, -9, -2], -5, hidden=True)],
   '''using System;
using System.Collections.Generic;

public static class Solution
{
    public static long second_largest(long[] nums)
    {
        var distinct = new List<long>(new HashSet<long>(nums));
        if (distinct.Count < 2) return -1;
        distinct.Sort();
        return distinct[distinct.Count - 2];
    }
}
''',
   {"en": ["new HashSet<long>(nums) drops the duplicates",
           "Put it back in a List so you can sort it",
           "Check Count before indexing"],
    "de": ["new HashSet<long>(nums) wirft die Duplikate weg",
           "Pack es in eine List, damit du sortieren kannst",
           "Prüf Count, bevor du indizierst"]})

L_("linq", "csharp", SEC_CORE,
   {"en": "LINQ", "de": "LINQ"},
   {"en": """LINQ is the reason a lot of C# reads almost like a list comprehension. Add
`using System.Linq;` and every collection gains a set of chainable operations:

    nums.Where(n => n % 2 == 0)          filter
    nums.Select(n => n * n)              map
    nums.OrderBy(n => n)                 sort ascending
    nums.OrderByDescending(n => n)
    nums.Distinct()  .Take(3)  .Skip(2)  .Reverse()
    nums.Sum()  .Max()  .Min()  .Average()  .Count()
    nums.Any(n => n < 0)   .All(n => n > 0)   .First()  .FirstOrDefault()
    nums.GroupBy(n => n % 2)

These are lazy: nothing runs until you enumerate. Finish a chain with
.ToArray() or .ToList() when you need a concrete result — and the exercises
here do, because the harness compares arrays.

Careful with .First() on an empty sequence: it throws. .FirstOrDefault()
returns 0 or null instead.""",
    "de": """LINQ ist der Grund, warum sich viel C# fast wie eine List Comprehension liest.
Mit `using System.Linq;` bekommt jede Collection verkettbare Operationen:

    nums.Where(n => n % 2 == 0)          filtern
    nums.Select(n => n * n)              abbilden
    nums.OrderBy(n => n)                 aufsteigend sortieren
    nums.OrderByDescending(n => n)
    nums.Distinct()  .Take(3)  .Skip(2)  .Reverse()
    nums.Sum()  .Max()  .Min()  .Average()  .Count()
    nums.Any(n => n < 0)   .All(n => n > 0)   .First()  .FirstOrDefault()
    nums.GroupBy(n => n % 2)

Sie sind faul: nichts läuft, bis du durchgehst. Schließ eine Kette mit
.ToArray() oder .ToList() ab, wenn du ein konkretes Ergebnis brauchst — und die
Übungen hier brauchen das, weil der Testrahmen Arrays vergleicht.

Vorsicht mit .First() auf einer leeren Folge: das wirft. .FirstOrDefault()
liefert stattdessen 0 oder null."""},
   {"en": "LINQ is lazy — finish with .ToArray(). .First() throws when empty.",
    "de": "LINQ ist faul — schließ mit .ToArray() ab. .First() wirft bei leer."},
   '''using System;
using System.Linq;

class Program
{
    static void Main()
    {
        var nums = new long[] {5, 3, 9, 3, 1, 8};

        Console.WriteLine("evens: [" +
            string.Join(", ", nums.Where(n => n % 2 == 0)) + "]");
        Console.WriteLine("squares: [" +
            string.Join(", ", nums.Select(n => n * n)) + "]");
        Console.WriteLine("distinct sorted: [" +
            string.Join(", ", nums.Distinct().OrderBy(n => n)) + "]");
        Console.WriteLine("top 3: [" +
            string.Join(", ", nums.OrderByDescending(n => n).Take(3)) + "]");

        Console.WriteLine($"sum {nums.Sum()}  max {nums.Max()}  avg {nums.Average():F2}");
        Console.WriteLine($"any negative? {nums.Any(n => n < 0)}");

        var groups = nums.GroupBy(n => n % 2 == 0 ? "even" : "odd");
        foreach (var g in groups)
            Console.WriteLine($"  {g.Key}: [{string.Join(", ", g)}]");

        var empty = new long[0];
        Console.WriteLine($"FirstOrDefault on empty: {empty.FirstOrDefault()}");
    }
}
''',
   "distinct_sorted", Sig([("nums", L(INT))], L(INT)),
   {"en": """Write distinct_sorted(nums) returning each value once, sorted ascending.

  distinct_sorted([5, 3, 5, 1]) -> [1, 3, 5]
  distinct_sorted([])           -> []

This is one LINQ chain. Remember to finish it with .ToArray().""",
    "de": """Schreib distinct_sorted(nums), das jeden Wert einmal zurückgibt, aufsteigend
sortiert.

  distinct_sorted([5, 3, 5, 1]) -> [1, 3, 5]
  distinct_sorted([])           -> []

Das ist eine LINQ-Kette. Denk daran, sie mit .ToArray() abzuschließen."""},
   [case([5, 3, 5, 1], [1, 3, 5]), case([], []), case([2, 2], [2]),
    case([-1, 3, -1, 0], [-1, 0, 3], hidden=True),
    case([9, 8, 7], [7, 8, 9], hidden=True)],
   '''using System.Linq;

public static class Solution
{
    public static long[] distinct_sorted(long[] nums)
    {
        return nums.Distinct().OrderBy(n => n).ToArray();
    }
}
''',
   {"en": ["Distinct() removes the repeats",
           "OrderBy(n => n) sorts ascending",
           "ToArray() turns the lazy chain into a real array"],
    "de": ["Distinct() entfernt die Wiederholungen",
           "OrderBy(n => n) sortiert aufsteigend",
           "ToArray() macht aus der faulen Kette ein echtes Array"]})

L_("strings", "csharp", SEC_STRINGS,
   {"en": "Strings", "de": "Zeichenketten"},
   {"en": """string is immutable, so every method returns a new one.

    s.Length                       a property
    s[0]                           indexing works, unlike Java
    s.Substring(1, 3)              start and COUNT, not start and end
    s.ToUpperInvariant()  .Trim()  .Contains("x")  .IndexOf("x")
    s.Split(' ')                   plain characters, not a regex
    string.Join("-", parts)
    string.IsNullOrWhiteSpace(s)

Substring is the one that catches people: the second argument is a LENGTH, so
"interview".Substring(2, 3) is "ter", not "terv".

For splitting on any run of whitespace, pass null and drop the empties:

    text.Split((char[])null, StringSplitOptions.RemoveEmptyEntries)

Build strings in a loop with StringBuilder, same reason as Java.""",
    "de": """string ist unveränderlich, jede Methode gibt also einen neuen zurück.

    s.Length                       eine Property
    s[0]                           Indizieren geht, anders als in Java
    s.Substring(1, 3)              Start und ANZAHL, nicht Start und Ende
    s.ToUpperInvariant()  .Trim()  .Contains("x")  .IndexOf("x")
    s.Split(' ')                   einfache Zeichen, kein Regex
    string.Join("-", parts)
    string.IsNullOrWhiteSpace(s)

Substring ist die Falle: das zweite Argument ist eine LÄNGE, also ist
"interview".Substring(2, 3) gleich "ter", nicht "terv".

Um an beliebigen Leerraumfolgen zu trennen, übergib null und wirf die Leeren weg:

    text.Split((char[])null, StringSplitOptions.RemoveEmptyEntries)

Strings in Schleifen baust du mit StringBuilder, aus demselben Grund wie in Java."""},
   {"en": "Substring takes a length, not an end index. Split(null, RemoveEmptyEntries) for whitespace.",
    "de": "Substring nimmt eine Länge, keinen Endindex. Für Leerraum Split(null, RemoveEmptyEntries)."},
   '''using System;
using System.Text;

class Program
{
    static void Main()
    {
        var s = "  Hello, World  ";

        Console.WriteLine($"[{s.Trim()}]");
        Console.WriteLine("upper: " + s.Trim().ToUpperInvariant());
        Console.WriteLine("Substring(0, 5): " + s.Trim().Substring(0, 5));
        Console.WriteLine("first char: " + s.Trim()[0]);

        var words = "  many   spaces here ".Split((char[])null,
            StringSplitOptions.RemoveEmptyEntries);
        Console.WriteLine($"{words.Length} words: " + string.Join("|", words));

        var reversed = new char[] {'a', 'b', 'c'};
        Array.Reverse(reversed);
        Console.WriteLine("reversed: " + new string(reversed));

        var sb = new StringBuilder();
        for (int i = 0; i < 5; i++) sb.Append(i * i).Append(' ');
        Console.WriteLine("built: " + sb.ToString().Trim());
    }
}
''',
   "normalise", Sig([("text", STR)], STR),
   {"en": """Write normalise(text) that cleans up a messy name:

  * trim both ends
  * collapse any run of inner whitespace to a single space
  * capitalise each word: first letter upper, the rest lower

  normalise("  aDA   LOVElace ") -> "Ada Lovelace"
  normalise("   ")               -> ""

Split(null, RemoveEmptyEntries) hands you the words already cleaned up.""",
    "de": """Schreib normalise(text), das einen unordentlichen Namen aufräumt:

  * an beiden Enden trimmen
  * jede Folge innerer Leerzeichen auf eine reduzieren
  * jedes Wort groß schreiben: erster Buchstabe groß, Rest klein

  normalise("  aDA   LOVElace ") -> "Ada Lovelace"
  normalise("   ")               -> ""

Split(null, RemoveEmptyEntries) liefert dir die Wörter schon aufgeräumt."""},
   [case("  aDA   LOVElace ", "Ada Lovelace"),
    case("guido van ROSSUM", "Guido Van Rossum"), case("   ", ""),
    case("a", "A", hidden=True),
    case("  linus     TORVALDS  ", "Linus Torvalds", hidden=True)],
   '''using System;
using System.Linq;

public static class Solution
{
    public static string normalise(string text)
    {
        var words = text.Split((char[])null,
            StringSplitOptions.RemoveEmptyEntries);
        return string.Join(" ", words.Select(w =>
            char.ToUpperInvariant(w[0]) + w.Substring(1).ToLowerInvariant()));
    }
}
''',
   {"en": ["Split(null, RemoveEmptyEntries) trims and collapses in one step",
           "char.ToUpperInvariant(w[0]) + w.Substring(1).ToLowerInvariant()",
           "string.Join(\" \", ...) puts it back together"],
    "de": ["Split(null, RemoveEmptyEntries) trimmt und reduziert in einem Schritt",
           "char.ToUpperInvariant(w[0]) + w.Substring(1).ToLowerInvariant()",
           "string.Join(\" \", ...) setzt es wieder zusammen"]})


# ===========================================================================
#  GO
# ===========================================================================
L_("syntax", "go", SEC_SYNTAX,
   {"en": "Declarations and zero values", "de": "Deklarationen und Nullwerte"},
   {"en": """Go has one short form for declaring and one long one:

    count := 0                 inside a function; the type is inferred
    var total int              at package level, or when you want the zero value
    const Limit = 100

Every type has a ZERO VALUE and a variable always has it before you assign:
0 for numbers, "" for strings, false for bool, nil for slices and maps. There is
no undefined and no None to trip over.

The compiler refuses to build if a local variable or an import is unused. That
feels harsh for ten minutes and then saves you for years.

Integer division truncates; there is no implicit conversion at all, so you must
write the cast:

    total := 7 / 2                 3
    ratio := float64(7) / 2        3.5

Formatting is one function with verbs: %d %s %v %q %T, and Printf needs the
\\n you would get free from Println.""",
    "de": """Go hat eine kurze Deklarationsform und eine lange:

    count := 0                 in einer Funktion; der Typ wird hergeleitet
    var total int              auf Paketebene, oder wenn du den Nullwert willst
    const Limit = 100

Jeder Typ hat einen NULLWERT, und eine Variable hat ihn vor jeder Zuweisung:
0 bei Zahlen, "" bei Strings, false bei bool, nil bei Slices und Maps. Es gibt
kein undefined und kein None, über das man stolpern könnte.

Der Compiler verweigert den Bau, wenn eine lokale Variable oder ein Import
unbenutzt ist. Das fühlt sich zehn Minuten lang hart an und rettet dich dann
jahrelang.

Ganzzahldivision schneidet ab, und es gibt überhaupt keine implizite Umwandlung
— du musst den Cast hinschreiben:

    total := 7 / 2                 3
    ratio := float64(7) / 2        3.5

Formatiert wird mit einer Funktion und Verben: %d %s %v %q %T — und Printf
braucht das \\n, das dir Println schenkt."""},
   {"en": "Zero values instead of null. No implicit conversion — write float64(x).",
    "de": "Nullwerte statt null. Keine implizite Umwandlung — schreib float64(x)."},
   '''package main

import "fmt"

func main() {
	name := "Ada"
	var count int // zero value: 0
	count = 7

	fmt.Printf("%s has %d\\n", name, count)
	fmt.Println("7 / 2        =", 7/2)
	fmt.Println("float64(7)/2 =", float64(7)/2)
	fmt.Println("7 %% 2        =", 7%2)

	var emptyString string
	var emptySlice []int
	var emptyMap map[string]int
	fmt.Printf("zero values: %q %v %v\\n", emptyString, emptySlice, emptyMap)
	fmt.Println("nil slice has len", len(emptySlice), "and appends fine")

	emptySlice = append(emptySlice, 1)
	fmt.Println("after append:", emptySlice)

	fmt.Printf("%v is a %T, quoted %q\\n", count, count, name)
	fmt.Printf("padded |%5d| left |%-5d|\\n", count, count)
}
''',
   "clock", Sig([("seconds", INT)], STR),
   {"en": """Write clock(seconds) turning a number of seconds into "H:MM:SS".

  clock(3661) -> "1:01:01"
  clock(59)   -> "0:00:59"

Hours have no leading zero; minutes and seconds always have two digits.
fmt.Sprintf("%d:%02d:%02d", h, m, s) builds the string.""",
    "de": """Schreib clock(seconds), das Sekunden in "H:MM:SS" verwandelt.

  clock(3661) -> "1:01:01"
  clock(59)   -> "0:00:59"

Stunden ohne führende Null, Minuten und Sekunden immer zweistellig.
fmt.Sprintf("%d:%02d:%02d", h, m, s) baut den String."""},
   [case(3661, "1:01:01"), case(59, "0:00:59"), case(0, "0:00:00"),
    case(86399, "23:59:59", hidden=True), case(600, "0:10:00", hidden=True)],
   '''package main

import "fmt"

func clock(seconds int) string {
	h := seconds / 3600
	m := (seconds % 3600) / 60
	s := seconds % 60
	return fmt.Sprintf("%d:%02d:%02d", h, m, s)
}
''',
   {"en": ["seconds / 3600 truncates — those are the hours",
           "Sprintf returns the string instead of printing it",
           "%02d pads a number to two digits"],
    "de": ["seconds / 3600 schneidet ab — das sind die Stunden",
           "Sprintf gibt den String zurück, statt ihn auszugeben",
           "%02d füllt eine Zahl auf zwei Stellen auf"]})

L_("slices", "go", SEC_DATA,
   {"en": "Slices and maps", "de": "Slices und Maps"},
   {"en": """A slice is Go's list. It is a view onto an array, with a length and a capacity.

    nums := []int{3, 1, 4}
    nums = append(nums, 5)         append RETURNS the slice — reassign it
    len(nums)   cap(nums)
    nums[1:3]                      a view, NOT a copy
    copy(dst, src)                 an actual copy
    sort.Ints(nums)                sorts in place

That "not a copy" matters: two slices can share the same backing array, so
writing through one changes the other. When you need independence, copy.

Maps are the hash table:

    counts := map[string]int{}
    counts["a"]++                  missing keys read as the zero value
    value, ok := counts["a"]       ok tells you whether it was really there
    delete(counts, "a")

Iterating a map gives a RANDOM order on purpose, so you cannot accidentally
depend on it. Sort the keys when order matters.""",
    "de": """Ein Slice ist Gos Liste. Es ist eine Sicht auf ein Array, mit Länge und
Kapazität.

    nums := []int{3, 1, 4}
    nums = append(nums, 5)         append LIEFERT das Slice — weise es neu zu
    len(nums)   cap(nums)
    nums[1:3]                      eine Sicht, KEINE Kopie
    copy(dst, src)                 eine echte Kopie
    sort.Ints(nums)                sortiert an Ort und Stelle

Dieses „keine Kopie" ist wichtig: zwei Slices können dasselbe Array darunter
teilen, ein Schreibzugriff durch das eine ändert also das andere. Wenn du
Unabhängigkeit brauchst, kopiere.

Maps sind die Hashtabelle:

    counts := map[string]int{}
    counts["a"]++                  fehlende Schlüssel lesen sich als Nullwert
    value, ok := counts["a"]       ok sagt dir, ob er wirklich da war
    delete(counts, "a")

Eine Map durchläuft man absichtlich in ZUFÄLLIGER Reihenfolge, damit man sich
nicht versehentlich darauf verlässt. Sortier die Schlüssel, wenn es zählt."""},
   {"en": "append returns the slice — reassign it. A sub-slice shares memory.",
    "de": "append liefert das Slice zurück — weise es neu zu. Ein Teil-Slice teilt Speicher."},
   '''package main

import (
	"fmt"
	"sort"
)

func main() {
	nums := []int{10, 9, 1, 4}
	nums = append(nums, 7)
	fmt.Println("nums:", nums, "len", len(nums), "cap", cap(nums))

	sort.Ints(nums)
	fmt.Println("sorted:", nums)

	view := nums[1:3]
	view[0] = 999
	fmt.Println("writing through a sub-slice changed the original:", nums)

	safe := make([]int, len(nums))
	copy(safe, nums)
	safe[0] = -1
	fmt.Println("after copying, original is untouched:", nums)

	counts := map[rune]int{}
	for _, r := range "mississippi" {
		counts[r]++
	}
	keys := []string{}
	for r := range counts {
		keys = append(keys, string(r))
	}
	sort.Strings(keys)
	for _, k := range keys {
		fmt.Printf("  %s -> %d\\n", k, counts[rune(k[0])])
	}

	if v, ok := counts['z']; !ok {
		fmt.Println("no z; reading it anyway gives", v)
	}
}
''',
   "second_largest", Sig([("nums", L(INT))], INT),
   {"en": """Write second_largest(nums) returning the second largest DISTINCT value.
Return -1 if there are fewer than two distinct values.

  second_largest([3, 1, 4, 4, 5]) -> 4
  second_largest([7, 7, 7])       -> -1

A map[int]bool works as a set; collect the keys, sort them, take the second
from the end.""",
    "de": """Schreib second_largest(nums), das den zweitgrößten VERSCHIEDENEN Wert liefert.
Gib -1 zurück, wenn es weniger als zwei verschiedene Werte gibt.

  second_largest([3, 1, 4, 4, 5]) -> 4
  second_largest([7, 7, 7])       -> -1

Ein map[int]bool dient als Set; sammle die Schlüssel, sortier sie und nimm das
zweitletzte."""},
   [case([3, 1, 4, 4, 5], 4), case([7, 7, 7], -1), case([2, 1], 1),
    case([], -1, hidden=True), case([-5, -2, -9, -2], -5, hidden=True)],
   '''package main

import "sort"

func second_largest(nums []int) int {
	seen := map[int]bool{}
	distinct := []int{}
	for _, n := range nums {
		if !seen[n] {
			seen[n] = true
			distinct = append(distinct, n)
		}
	}
	if len(distinct) < 2 {
		return -1
	}
	sort.Ints(distinct)
	return distinct[len(distinct)-2]
}
''',
   {"en": ["map[int]bool is the usual stand-in for a set",
           "Collect the unseen values into a slice as you go",
           "sort.Ints, then index len-2"],
    "de": ["map[int]bool ist der übliche Ersatz für ein Set",
           "Sammle die noch nicht gesehenen Werte unterwegs in ein Slice",
           "sort.Ints, dann Index len-2"]})

L_("errors", "go", SEC_CORE,
   {"en": "Multiple returns and errors", "de": "Mehrfache Rückgaben und Fehler"},
   {"en": """Go has no exceptions. A function that can fail returns its result AND an error,
and you check it right there:

    value, err := strconv.Atoi("42")
    if err != nil {
        return 0, fmt.Errorf("bad number: %w", err)
    }

That `if err != nil` block is the most-typed thing in Go. It looks repetitive
and it is — the trade is that every failure is visible in the code path instead
of flying past you.

Multiple return values are not only for errors:

    func minMax(nums []int) (int, int) { ... }
    lo, hi := minMax(nums)
    lo, _ := minMax(nums)          _ discards a value you do not want

For the genuinely exceptional there is panic/recover, but idiomatic Go reserves
it for programmer error, not for "the file was missing".

defer runs a call when the function exits, in reverse order — the usual way to
close things.""",
    "de": """Go hat keine Ausnahmen. Eine Funktion, die scheitern kann, gibt ihr Ergebnis
UND einen Fehler zurück, und du prüfst ihn direkt dort:

    value, err := strconv.Atoi("42")
    if err != nil {
        return 0, fmt.Errorf("ungültige Zahl: %w", err)
    }

Dieser `if err != nil`-Block ist das meistgetippte in Go. Er wirkt repetitiv,
und das ist er auch — dafür ist jeder Fehlerfall im Code sichtbar, statt an dir
vorbeizufliegen.

Mehrfache Rückgabewerte gibt es nicht nur für Fehler:

    func minMax(nums []int) (int, int) { ... }
    lo, hi := minMax(nums)
    lo, _ := minMax(nums)          _ verwirft einen Wert, den du nicht willst

Für wirklich Außergewöhnliches gibt es panic/recover, aber idiomatisches Go
hebt sich das für Programmierfehler auf, nicht für „die Datei fehlte".

defer führt einen Aufruf beim Verlassen der Funktion aus, in umgekehrter
Reihenfolge — der übliche Weg, Dinge zu schließen."""},
   {"en": "if err != nil is the whole error model. _ discards a return you do not need.",
    "de": "if err != nil ist das ganze Fehlermodell. _ verwirft einen Rückgabewert."},
   '''package main

import (
	"errors"
	"fmt"
	"strconv"
)

func minMax(nums []int) (int, int) {
	lo, hi := nums[0], nums[0]
	for _, n := range nums {
		if n < lo {
			lo = n
		}
		if n > hi {
			hi = n
		}
	}
	return lo, hi
}

func parse(text string) (int, error) {
	n, err := strconv.Atoi(text)
	if err != nil {
		return 0, fmt.Errorf("parsing %q: %w", text, err)
	}
	return n, nil
}

func main() {
	lo, hi := minMax([]int{4, 9, 1, 7})
	fmt.Println("lo:", lo, "hi:", hi)

	onlyLow, _ := minMax([]int{4, 9, 1, 7})
	fmt.Println("discarding the second value:", onlyLow)

	if n, err := parse("42"); err == nil {
		fmt.Println("parsed:", n)
	}
	if _, err := parse("nope"); err != nil {
		fmt.Println("failed as expected:", err)
		fmt.Println("unwrapped kind:", errors.Unwrap(err))
	}

	defer fmt.Println("deferred: this prints last")
	fmt.Println("end of main")
}
''',
   "min_max", Sig([("nums", L(INT))], L(INT)),
   {"en": """Write min_max(nums) returning [smallest, largest] as a two-element slice.
Return an empty slice for empty input.

  min_max([4, 9, 1, 7]) -> [1, 9]
  min_max([5])          -> [5, 5]
  min_max([])           -> []

Compute both in a single pass. This is the shape multiple return values exist
for — the harness just wants them collected into a slice.""",
    "de": """Schreib min_max(nums), das [kleinster, größter] als zweielementiges Slice
zurückgibt. Für leere Eingaben ein leeres Slice.

  min_max([4, 9, 1, 7]) -> [1, 9]
  min_max([5])          -> [5, 5]
  min_max([])           -> []

Berechne beides in einem Durchlauf. Genau dafür gibt es mehrfache
Rückgabewerte — der Testrahmen will sie nur als Slice gesammelt haben."""},
   [case([4, 9, 1, 7], [1, 9]), case([5], [5, 5]), case([], []),
    case([-3, -1, -9], [-9, -1], hidden=True),
    case([2, 2, 2], [2, 2], hidden=True)],
   '''package main

func min_max(nums []int) []int {
	if len(nums) == 0 {
		return []int{}
	}
	lo, hi := nums[0], nums[0]
	for _, n := range nums {
		if n < lo {
			lo = n
		}
		if n > hi {
			hi = n
		}
	}
	return []int{lo, hi}
}
''',
   {"en": ["Start both lo and hi at the first element, not at 0",
           "One loop updates both",
           "Return an empty slice, not nil-with-a-crash, for empty input"],
    "de": ["Starte lo und hi beim ersten Element, nicht bei 0",
           "Eine Schleife aktualisiert beide",
           "Gib bei leerer Eingabe ein leeres Slice zurück, statt abzustürzen"]})

L_("strings", "go", SEC_STRINGS,
   {"en": "Strings, bytes and runes", "de": "Strings, Bytes und Runes"},
   {"en": """A Go string is an immutable sequence of BYTES holding UTF-8. That distinction
matters the moment a character is not ASCII.

    len(s)               the number of BYTES
    s[0]                 one byte, printed as a number
    for i, r := range s  gives runes (characters) and their byte offsets
    []rune(s)            a slice of characters, indexable properly

The strings package has everything else:

    strings.ToUpper, .TrimSpace, .Contains, .HasPrefix, .Index
    strings.Split(s, ",")        strings.Fields(s) splits on any whitespace
    strings.Join(parts, "-")
    strings.Repeat("ab", 3)

strings.Fields is the one to remember: it trims and collapses runs of
whitespace in a single call.

Build strings with strings.Builder in a loop — concatenating with + allocates
a new string every time.""",
    "de": """Ein Go-String ist eine unveränderliche Folge von BYTES mit UTF-8-Inhalt. Dieser
Unterschied zählt, sobald ein Zeichen nicht ASCII ist.

    len(s)               die Anzahl der BYTES
    s[0]                 ein Byte, als Zahl ausgegeben
    for i, r := range s  liefert Runes (Zeichen) und ihre Byte-Positionen
    []rune(s)            ein Slice von Zeichen, richtig indizierbar

Das strings-Paket hat alles Weitere:

    strings.ToUpper, .TrimSpace, .Contains, .HasPrefix, .Index
    strings.Split(s, ",")        strings.Fields(s) trennt an beliebigem Leerraum
    strings.Join(parts, "-")
    strings.Repeat("ab", 3)

strings.Fields ist das, was man sich merkt: es trimmt und reduziert Leerraum in
einem einzigen Aufruf.

Bau Strings in Schleifen mit strings.Builder — Verketten mit + legt jedes Mal
einen neuen String an."""},
   {"en": "len() counts bytes, range gives runes. strings.Fields trims and splits at once.",
    "de": "len() zählt Bytes, range liefert Runes. strings.Fields trimmt und trennt zugleich."},
   '''package main

import (
	"fmt"
	"strings"
)

func main() {
	s := "  Hello, World  "

	fmt.Printf("[%s]\\n", strings.TrimSpace(s))
	fmt.Println("upper:", strings.ToUpper(strings.TrimSpace(s)))
	fmt.Println("split:", strings.Split(strings.TrimSpace(s), ", "))
	fmt.Println("fields on messy input:", strings.Fields("  many   spaces here "))
	fmt.Println("joined:", strings.Join([]string{"a", "b", "c"}, "-"))

	word := "Grüße"
	fmt.Println("len in bytes:", len(word))
	fmt.Println("len in runes:", len([]rune(word)))
	for i, r := range word {
		fmt.Printf("  byte %d -> %q\\n", i, r)
	}

	var b strings.Builder
	for i := 0; i < 5; i++ {
		fmt.Fprintf(&b, "%d ", i*i)
	}
	fmt.Println("built:", strings.TrimSpace(b.String()))
}
''',
   "normalise", Sig([("text", STR)], STR),
   {"en": """Write normalise(text) that cleans up a messy name:

  * trim both ends
  * collapse any run of inner whitespace to a single space
  * capitalise each word: first letter upper, the rest lower

  normalise("  aDA   LOVElace ") -> "Ada Lovelace"
  normalise("   ")               -> ""

strings.Fields does the trimming and collapsing for you in one call.""",
    "de": """Schreib normalise(text), das einen unordentlichen Namen aufräumt:

  * an beiden Enden trimmen
  * jede Folge innerer Leerzeichen auf eine reduzieren
  * jedes Wort groß schreiben: erster Buchstabe groß, Rest klein

  normalise("  aDA   LOVElace ") -> "Ada Lovelace"
  normalise("   ")               -> ""

strings.Fields erledigt Trimmen und Reduzieren in einem Aufruf."""},
   [case("  aDA   LOVElace ", "Ada Lovelace"),
    case("guido van ROSSUM", "Guido Van Rossum"), case("   ", ""),
    case("a", "A", hidden=True),
    case("  linus     TORVALDS  ", "Linus Torvalds", hidden=True)],
   '''package main

import "strings"

func normalise(text string) string {
	words := strings.Fields(text)
	for i, w := range words {
		runes := []rune(strings.ToLower(w))
		runes[0] = []rune(strings.ToUpper(string(runes[0])))[0]
		words[i] = string(runes)
	}
	return strings.Join(words, " ")
}
''',
   {"en": ["strings.Fields trims and collapses whitespace in one call",
           "Lower-case the whole word, then upper-case its first rune",
           "strings.Join(words, \" \") puts it back together"],
    "de": ["strings.Fields trimmt und reduziert Leerraum in einem Aufruf",
           "Mach das ganze Wort klein und dann die erste Rune groß",
           "strings.Join(words, \" \") setzt es wieder zusammen"]})


# ===========================================================================
#  RUST
# ===========================================================================
L_("syntax", "rust", SEC_SYNTAX,
   {"en": "let, mut and types", "de": "let, mut und Typen"},
   {"en": """Bindings are immutable unless you say otherwise. That is the opposite default
from every language you already know, and it is deliberate.

    let count = 0;             cannot be changed
    let mut total = 0;         can
    let name: &str = "Ada";
    let owned: String = name.to_string();

Shadowing lets you reuse a name with a new type, which reads better than
inventing text2:

    let value = "42";
    let value: i64 = value.parse().unwrap();

There is no implicit numeric conversion at all — not even widening:

    let a: i64 = 7;
    let b = a as f64 / 2.0;    the `as` is required

Integer division truncates, and integer overflow PANICS in debug builds
instead of wrapping silently.

Printing uses format strings with positional braces:
println!("{} is {}", name, count) and {:?} for the debug view of a collection.""",
    "de": """Bindungen sind unveränderlich, solange du nichts anderes sagst. Das ist die
umgekehrte Vorgabe zu jeder Sprache, die du kennst, und sie ist Absicht.

    let count = 0;             kann nicht geändert werden
    let mut total = 0;         kann es
    let name: &str = "Ada";
    let owned: String = name.to_string();

Shadowing erlaubt, einen Namen mit neuem Typ wiederzuverwenden — das liest sich
besser, als text2 zu erfinden:

    let value = "42";
    let value: i64 = value.parse().unwrap();

Implizite Zahlenumwandlung gibt es überhaupt nicht — nicht einmal Erweiterung:

    let a: i64 = 7;
    let b = a as f64 / 2.0;    das `as` ist Pflicht

Ganzzahldivision schneidet ab, und Ganzzahlüberlauf PANICKT in Debug-Builds,
statt lautlos umzulaufen.

Ausgegeben wird mit Formatstrings und Klammern:
println!("{} ist {}", name, count), und {:?} für die Debug-Ansicht."""},
   {"en": "Immutable by default; add mut. No implicit conversion — write `as`.",
    "de": "Standardmäßig unveränderlich; mut hinzufügen. Keine implizite Umwandlung — `as`."},
   '''fn main() {
    let name = "Ada";
    let mut count = 0;
    count += 7;

    println!("{} has {}", name, count);
    println!("7 / 2          = {}", 7 / 2);
    println!("7 as f64 / 2.0 = {}", 7 as f64 / 2.0);
    println!("7 % 2          = {}", 7 % 2);

    // shadowing: same name, new type
    let value = "42";
    let value: i64 = value.parse().unwrap();
    println!("parsed {} of type i64", value);

    let nums = vec![3, 1, 4];
    println!("debug view: {:?}", nums);
    println!("padded |{:>5}| left |{:<5}|", count, count);
    println!("rounded {:.3}", 2.0 / 3.0);

    let maybe: Option<i64> = None;
    println!("unwrap_or: {}", maybe.unwrap_or(-1));
}
''',
   "clock", Sig([("seconds", INT)], STR),
   {"en": """Write clock(seconds) turning a number of seconds into "H:MM:SS".

  clock(3661) -> "1:01:01"
  clock(59)   -> "0:00:59"

Hours have no leading zero; minutes and seconds always have two digits.
format!("{}:{:02}:{:02}", h, m, s) builds the String.""",
    "de": """Schreib clock(seconds), das Sekunden in "H:MM:SS" verwandelt.

  clock(3661) -> "1:01:01"
  clock(59)   -> "0:00:59"

Stunden ohne führende Null, Minuten und Sekunden immer zweistellig.
format!("{}:{:02}:{:02}", h, m, s) baut den String."""},
   [case(3661, "1:01:01"), case(59, "0:00:59"), case(0, "0:00:00"),
    case(86399, "23:59:59", hidden=True), case(600, "0:10:00", hidden=True)],
   '''fn clock(seconds: i64) -> String {
    let h = seconds / 3600;
    let m = (seconds % 3600) / 60;
    let s = seconds % 60;
    format!("{}:{:02}:{:02}", h, m, s)
}
''',
   {"en": ["format! returns a String; println! prints one",
           "{:02} pads a number to two digits",
           "The last expression is the return value — no semicolon"],
    "de": ["format! liefert einen String, println! gibt ihn aus",
           "{:02} füllt eine Zahl auf zwei Stellen auf",
           "Der letzte Ausdruck ist der Rückgabewert — ohne Semikolon"]})

L_("collections", "rust", SEC_DATA,
   {"en": "Vec and HashMap", "de": "Vec und HashMap"},
   {"en": """    let mut nums = vec![3, 1, 4];
    nums.push(5);
    nums.len();  nums.is_empty();
    nums.sort();                     in place, needs `mut`
    nums.contains(&5);               note the &
    let slice: &[i64] = &nums;       a borrowed view

Iterators are where Rust gets pleasant, and they are lazy until collected:

    nums.iter().map(|n| n * 2).collect::<Vec<i64>>()
    nums.iter().filter(|n| **n > 2).count()
    nums.iter().sum::<i64>()
    nums.iter().max()                returns Option — there may be nothing

    use std::collections::{HashMap, HashSet};
    let mut counts: HashMap<char, i64> = HashMap::new();
    *counts.entry(c).or_insert(0) += 1;      the idiomatic counter
    let mut seen = HashSet::new();
    seen.insert(x)                   returns false if it was already there

The `::<Vec<i64>>` on collect is the turbofish: collect can build many things,
so sometimes you have to say which.""",
    "de": """    let mut nums = vec![3, 1, 4];
    nums.push(5);
    nums.len();  nums.is_empty();
    nums.sort();                     an Ort und Stelle, braucht `mut`
    nums.contains(&5);               beachte das &
    let slice: &[i64] = &nums;       eine geliehene Sicht

Bei Iteratoren wird Rust angenehm, und sie sind faul bis zum Einsammeln:

    nums.iter().map(|n| n * 2).collect::<Vec<i64>>()
    nums.iter().filter(|n| **n > 2).count()
    nums.iter().sum::<i64>()
    nums.iter().max()                liefert Option — es könnte nichts da sein

    use std::collections::{HashMap, HashSet};
    let mut counts: HashMap<char, i64> = HashMap::new();
    *counts.entry(c).or_insert(0) += 1;      der idiomatische Zähler
    let mut seen = HashSet::new();
    seen.insert(x)                   liefert false, wenn es schon drin war

Das `::<Vec<i64>>` an collect ist der Turbofish: collect kann vieles bauen,
manchmal musst du sagen, was."""},
   {"en": "*map.entry(k).or_insert(0) += 1 is the counter. .max() returns an Option.",
    "de": "*map.entry(k).or_insert(0) += 1 ist der Zähler. .max() liefert ein Option."},
   '''use std::collections::{HashMap, HashSet};

fn main() {
    let mut nums = vec![10, 9, 1, 4];
    nums.push(7);
    nums.sort();
    println!("sorted: {:?}", nums);

    let doubled: Vec<i64> = nums.iter().map(|n| n * 2).collect();
    println!("doubled: {:?}", doubled);
    println!("sum: {}", nums.iter().sum::<i64>());
    println!("max: {:?}", nums.iter().max());

    let mut counts: HashMap<char, i64> = HashMap::new();
    for c in "mississippi".chars() {
        *counts.entry(c).or_insert(0) += 1;
    }
    let mut keys: Vec<&char> = counts.keys().collect();
    keys.sort();
    for k in keys {
        println!("  {} -> {}", k, counts[k]);
    }

    let mut seen = HashSet::new();
    for n in [1, 2, 1] {
        if !seen.insert(n) {
            println!("duplicate: {}", n);
        }
    }
}
''',
   "second_largest", Sig([("nums", L(INT))], INT),
   {"en": """Write second_largest(nums) returning the second largest DISTINCT value.
Return -1 if there are fewer than two distinct values.

  second_largest([3, 1, 4, 4, 5]) -> 4
  second_largest([7, 7, 7])       -> -1

Collect into a Vec, sort it, then dedup() — which only removes CONSECUTIVE
duplicates, so it has to come after the sort.""",
    "de": """Schreib second_largest(nums), das den zweitgrößten VERSCHIEDENEN Wert liefert.
Gib -1 zurück, wenn es weniger als zwei verschiedene Werte gibt.

  second_largest([3, 1, 4, 4, 5]) -> 4
  second_largest([7, 7, 7])       -> -1

Sammle in ein Vec, sortier es und dann dedup() — das entfernt nur
AUFEINANDERFOLGENDE Duplikate, muss also nach dem Sortieren kommen."""},
   [case([3, 1, 4, 4, 5], 4), case([7, 7, 7], -1), case([2, 1], 1),
    case([], -1, hidden=True), case([-5, -2, -9, -2], -5, hidden=True)],
   '''fn second_largest(nums: &[i64]) -> i64 {
    let mut distinct: Vec<i64> = nums.to_vec();
    distinct.sort();
    distinct.dedup();
    if distinct.len() < 2 {
        return -1;
    }
    distinct[distinct.len() - 2]
}
''',
   {"en": ["to_vec() gives you an owned, mutable copy",
           "dedup() only removes neighbours — sort first",
           "Check len() before indexing; there is no negative indexing"],
    "de": ["to_vec() liefert eine eigene, veränderbare Kopie",
           "dedup() entfernt nur Nachbarn — erst sortieren",
           "Prüf len() vor dem Indizieren; negative Indizes gibt es nicht"]})

L_("ownership", "rust", SEC_CORE,
   {"en": "Ownership and borrowing", "de": "Ownership und Borrowing"},
   {"en": """This is the idea the whole language is built on, and the reason Rust needs no
garbage collector.

Every value has exactly ONE owner. When the owner goes out of scope, the value
is freed. Assigning a non-Copy value MOVES it:

    let a = String::from("hi");
    let b = a;              // moved
    // println!("{}", a);   // compile error: a no longer owns anything

Numbers and bools are Copy, so they are duplicated instead of moved. Strings
and Vecs are not.

Instead of moving, you can BORROW with &:

    fn length(s: &String) -> usize { s.len() }   // shared borrow, read-only
    fn push(v: &mut Vec<i64>) { v.push(1); }     // exclusive borrow, can write

The rule the compiler enforces: at any moment you may have EITHER any number of
shared borrows OR exactly one mutable borrow — never both. That single rule is
what makes data races impossible.

This is why the exercises take &[i64] rather than Vec<i64>: they only need to
read, so borrowing is enough and the caller keeps its data.""",
    "de": """Das ist die Idee, auf der die ganze Sprache steht, und der Grund, warum Rust
keinen Garbage Collector braucht.

Jeder Wert hat genau EINEN Besitzer. Verlässt der Besitzer den Gültigkeitsbereich,
wird der Wert freigegeben. Ein nicht-Copy-Wert wird beim Zuweisen VERSCHOBEN:

    let a = String::from("hi");
    let b = a;              // verschoben
    // println!("{}", a);   // Übersetzungsfehler: a besitzt nichts mehr

Zahlen und bools sind Copy, werden also kopiert statt verschoben. Strings und
Vecs nicht.

Statt zu verschieben, kannst du mit & AUSLEIHEN:

    fn length(s: &String) -> usize { s.len() }   // geteilte Leihe, nur lesen
    fn push(v: &mut Vec<i64>) { v.push(1); }     // exklusive Leihe, schreibend

Die Regel, die der Compiler erzwingt: zu jedem Zeitpunkt darfst du ENTWEDER
beliebig viele geteilte Leihen ODER genau eine veränderbare haben — nie beides.
Diese eine Regel macht Data Races unmöglich.

Deshalb nehmen die Übungen &[i64] statt Vec<i64>: sie müssen nur lesen, Leihen
genügt, und der Aufrufer behält seine Daten."""},
   {"en": "One owner. Borrow with & to read, &mut to write — never both at once.",
    "de": "Ein Besitzer. Mit & leihen zum Lesen, &mut zum Schreiben — nie beides zugleich."},
   '''fn length(s: &String) -> usize {
    s.len()                     // shared borrow: we may read
}

fn add_one(v: &mut Vec<i64>) {
    v.push(1);                  // exclusive borrow: we may write
}

fn main() {
    let a = String::from("hello");
    let b = a.clone();          // an explicit copy, because a move would end `a`
    println!("a = {}, b = {}", a, b);
    println!("length via borrow: {}", length(&a));
    println!("a still usable afterwards: {}", a);

    let moved = a;              // now `a` is moved out
    println!("moved owns it now: {}", moved);

    let mut nums = vec![1, 2];
    add_one(&mut nums);
    println!("after &mut: {:?}", nums);

    let first = &nums[0];       // shared borrow
    println!("reading through the borrow: {}", first);
    nums.push(9);               // the borrow above already ended, so this is fine
    println!("{:?}", nums);

    let n = 5;                  // i64 is Copy
    let m = n;
    println!("both still valid: {} {}", n, m);
}
''',
   "dedup_keep_order", Sig([("nums", L(INT))], L(INT)),
   {"en": """Write dedup_keep_order(nums) returning each value once, in the order it first
appeared.

  dedup_keep_order([3, 1, 3, 2, 1]) -> [3, 1, 2]
  dedup_keep_order([])              -> []

Note that Vec::dedup is no help here: it only removes neighbours. Use a HashSet
to remember what you have already emitted. The parameter is a borrow, so you
build a new Vec rather than modifying the caller's data.""",
    "de": """Schreib dedup_keep_order(nums), das jeden Wert einmal zurückgibt, in der
Reihenfolge seines ersten Auftretens.

  dedup_keep_order([3, 1, 3, 2, 1]) -> [3, 1, 2]
  dedup_keep_order([])              -> []

Vec::dedup hilft hier nicht: es entfernt nur Nachbarn. Nimm ein HashSet, um dir
zu merken, was du schon ausgegeben hast. Der Parameter ist geliehen — du baust
also ein neues Vec, statt die Daten des Aufrufers zu ändern."""},
   [case([3, 1, 3, 2, 1], [3, 1, 2]), case([], []), case([5, 5, 5], [5]),
    case([1, 2, 3], [1, 2, 3], hidden=True),
    case([-1, 0, -1, 0], [-1, 0], hidden=True)],
   '''use std::collections::HashSet;

fn dedup_keep_order(nums: &[i64]) -> Vec<i64> {
    let mut seen = HashSet::new();
    let mut out = Vec::new();
    for &n in nums {
        if seen.insert(n) {
            out.push(n);
        }
    }
    out
}
''',
   {"en": ["seen.insert(n) returns true the first time and false afterwards",
           "`for &n in nums` destructures the reference into a value",
           "Push into a new Vec — you only borrowed the input"],
    "de": ["seen.insert(n) liefert beim ersten Mal true und danach false",
           "`for &n in nums` löst die Referenz in einen Wert auf",
           "Häng an ein neues Vec an — die Eingabe hast du nur geliehen"]})

L_("strings", "rust", SEC_STRINGS,
   {"en": "String, &str and Option", "de": "String, &str und Option"},
   {"en": """Rust has two string types and the difference is ownership, not content:

    &str      a borrowed view — string literals, slices of a String
    String    an owned, growable buffer

    let borrowed: &str = "Ada";
    let owned: String = borrowed.to_string();
    let back: &str = &owned;

Strings are UTF-8, so you cannot index by number: s[0] does not compile. Go
through chars:

    s.chars().count()             s.chars().rev().collect::<String>()
    s.chars().nth(0)              returns Option<char>
    s.to_uppercase()  .trim()  .contains("x")  .starts_with("A")
    s.split_whitespace()          trims and collapses, like Go's Fields
    parts.join("-")

Anything that can be absent is an Option, and the compiler makes you deal with
it:

    match s.chars().next() {
        Some(c) => ...,
        None => ...,
    }
    s.chars().next().unwrap_or('?')""",
    "de": """Rust hat zwei String-Typen, und der Unterschied ist Besitz, nicht Inhalt:

    &str      eine geliehene Sicht — Literale, Ausschnitte eines String
    String    ein eigener, wachsender Puffer

    let borrowed: &str = "Ada";
    let owned: String = borrowed.to_string();
    let back: &str = &owned;

Strings sind UTF-8, du kannst also nicht mit Zahlen indizieren: s[0] übersetzt
nicht. Geh über chars:

    s.chars().count()             s.chars().rev().collect::<String>()
    s.chars().nth(0)              liefert Option<char>
    s.to_uppercase()  .trim()  .contains("x")  .starts_with("A")
    s.split_whitespace()          trimmt und reduziert, wie Gos Fields
    parts.join("-")

Alles, was fehlen kann, ist ein Option, und der Compiler zwingt dich, damit
umzugehen:

    match s.chars().next() {
        Some(c) => ...,
        None => ...,
    }
    s.chars().next().unwrap_or('?')"""},
   {"en": "&str borrows, String owns. No s[0] — go through .chars(). Absence is Option.",
    "de": "&str leiht, String besitzt. Kein s[0] — über .chars(). Fehlen ist ein Option."},
   '''fn main() {
    let s = "  Hello, World  ";

    println!("[{}]", s.trim());
    println!("upper: {}", s.trim().to_uppercase());
    println!("split: {:?}", s.trim().split(", ").collect::<Vec<&str>>());
    println!("fields: {:?}", "  many   spaces here ".split_whitespace()
        .collect::<Vec<&str>>());
    println!("joined: {}", ["a", "b", "c"].join("-"));

    let reversed: String = "interview".chars().rev().collect();
    println!("reversed: {}", reversed);

    let owned: String = s.trim().to_string();
    let borrowed: &str = &owned;
    println!("owned {} chars, borrowed view {}", owned.chars().count(), borrowed);

    match "".chars().next() {
        Some(c) => println!("first char {}", c),
        None => println!("empty string has no first char"),
    }
    println!("with a fallback: {}", "".chars().next().unwrap_or('?'));
}
''',
   "normalise", Sig([("text", STR)], STR),
   {"en": """Write normalise(text) that cleans up a messy name:

  * trim both ends
  * collapse any run of inner whitespace to a single space
  * capitalise each word: first letter upper, the rest lower

  normalise("  aDA   LOVElace ") -> "Ada Lovelace"
  normalise("   ")               -> ""

split_whitespace() does the trimming and collapsing. For each word, take the
first char and the rest separately — remember there is no word[0].""",
    "de": """Schreib normalise(text), das einen unordentlichen Namen aufräumt:

  * an beiden Enden trimmen
  * jede Folge innerer Leerzeichen auf eine reduzieren
  * jedes Wort groß schreiben: erster Buchstabe groß, Rest klein

  normalise("  aDA   LOVElace ") -> "Ada Lovelace"
  normalise("   ")               -> ""

split_whitespace() erledigt Trimmen und Reduzieren. Nimm für jedes Wort das
erste Zeichen und den Rest getrennt — es gibt kein word[0]."""},
   [case("  aDA   LOVElace ", "Ada Lovelace"),
    case("guido van ROSSUM", "Guido Van Rossum"), case("   ", ""),
    case("a", "A", hidden=True),
    case("  linus     TORVALDS  ", "Linus Torvalds", hidden=True)],
   '''fn normalise(text: &str) -> String {
    text.split_whitespace()
        .map(|word| {
            let mut chars = word.chars();
            match chars.next() {
                Some(first) => first.to_uppercase().collect::<String>()
                    + &chars.as_str().to_lowercase(),
                None => String::new(),
            }
        })
        .collect::<Vec<String>>()
        .join(" ")
}
''',
   {"en": ["split_whitespace() trims and collapses in one call",
           "chars.next() takes the first char and leaves the rest in the iterator",
           "chars.as_str() gives you what is left, ready to lower-case"],
    "de": ["split_whitespace() trimmt und reduziert in einem Aufruf",
           "chars.next() nimmt das erste Zeichen, der Rest bleibt im Iterator",
           "chars.as_str() liefert den Rest, bereit zum Kleinschreiben"]})


# ===========================================================================
#  C++
# ===========================================================================
L_("syntax", "cpp", SEC_SYNTAX,
   {"en": "Types, auto and references", "de": "Typen, auto und Referenzen"},
   {"en": """C++ is statically typed, and `auto` asks the compiler to work the type out.

    long long count = 0;       use long long when anything multiplies
    double ratio = 7 / 2.0;
    bool ready = true;
    std::string name = "Ada";
    auto guessed = 42;         int

Integer division truncates, as everywhere in the C family:

    7 / 2    ->  3
    7 / 2.0  ->  3.5
    7 % 2    ->  1

The thing that has no Python equivalent is the REFERENCE. A plain parameter is
a COPY — for a big vector that is an expensive one — while `&` binds to the
caller's object:

    void f(std::vector<long long> v);          copies the whole thing
    void f(const std::vector<long long>& v);   no copy, read-only
    void f(std::vector<long long>& v);         no copy, can modify

`const T&` for anything bigger than a number is simply the default in modern
C++. The exercises here use it for exactly that reason.""",
    "de": """C++ ist statisch typisiert, und `auto` lässt den Compiler den Typ herleiten.

    long long count = 0;       nimm long long, sobald multipliziert wird
    double ratio = 7 / 2.0;
    bool ready = true;
    std::string name = "Ada";
    auto guessed = 42;         int

Ganzzahldivision schneidet ab, wie überall in der C-Familie:

    7 / 2    ->  3
    7 / 2.0  ->  3.5
    7 % 2    ->  1

Was es in Python nicht gibt, ist die REFERENZ. Ein einfacher Parameter ist eine
KOPIE — bei einem großen Vektor eine teure —, während `&` an das Objekt des
Aufrufers bindet:

    void f(std::vector<long long> v);          kopiert alles
    void f(const std::vector<long long>& v);   keine Kopie, nur lesen
    void f(std::vector<long long>& v);         keine Kopie, veränderbar

`const T&` für alles, was größer als eine Zahl ist, ist in modernem C++ schlicht
die Vorgabe. Genau deshalb nutzen die Übungen hier das."""},
   {"en": "A parameter without & is a copy. Use const T& for anything bigger than a number.",
    "de": "Ein Parameter ohne & ist eine Kopie. Nimm const T& für alles größer als eine Zahl."},
   '''#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

void grows(std::vector<long long> copied) { copied.push_back(99); }
void grows_ref(std::vector<long long>& shared) { shared.push_back(99); }

int main() {
    std::string name = "Ada";
    long long count = 7;

    std::cout << name << " has " << count << std::endl;
    std::cout << "7 / 2   = " << 7 / 2 << std::endl;
    std::cout << "7 / 2.0 = " << 7 / 2.0 << std::endl;
    std::cout << "7 % 2   = " << 7 % 2 << std::endl;

    std::vector<long long> nums{1, 2, 3};
    grows(nums);
    std::cout << "after by-value call, size is " << nums.size() << std::endl;
    grows_ref(nums);
    std::cout << "after by-reference call, size is " << nums.size() << std::endl;

    std::cout << std::setw(6) << count << "|" << std::endl;
    std::cout << std::fixed << std::setprecision(3) << 2.0 / 3 << std::endl;

    for (const auto& n : nums) std::cout << n << " ";
    std::cout << std::endl;
    return 0;
}
''',
   "clock", Sig([("seconds", INT)], STR),
   {"en": """Write clock(seconds) turning a number of seconds into "H:MM:SS".

  clock(3661) -> "1:01:01"
  clock(59)   -> "0:00:59"

Hours have no leading zero; minutes and seconds always have two digits.
An ostringstream with std::setw(2) and std::setfill('0') does the padding.""",
    "de": """Schreib clock(seconds), das Sekunden in "H:MM:SS" verwandelt.

  clock(3661) -> "1:01:01"
  clock(59)   -> "0:00:59"

Stunden ohne führende Null, Minuten und Sekunden immer zweistellig.
Ein ostringstream mit std::setw(2) und std::setfill('0') füllt auf."""},
   [case(3661, "1:01:01"), case(59, "0:00:59"), case(0, "0:00:00"),
    case(86399, "23:59:59", hidden=True), case(600, "0:10:00", hidden=True)],
   '''#include <iomanip>
#include <sstream>
#include <string>

std::string clock(long long seconds) {
    long long h = seconds / 3600;
    long long m = (seconds % 3600) / 60;
    long long s = seconds % 60;
    std::ostringstream out;
    out << h << ":" << std::setw(2) << std::setfill('0') << m
        << ":" << std::setw(2) << std::setfill('0') << s;
    return out.str();
}
''',
   {"en": ["seconds / 3600 truncates — those are the hours",
           "std::setw(2) applies to the NEXT item only, so repeat it",
           "out.str() turns the stream into a std::string"],
    "de": ["seconds / 3600 schneidet ab — das sind die Stunden",
           "std::setw(2) gilt nur für das NÄCHSTE Element, also wiederholen",
           "out.str() macht aus dem Stream einen std::string"]})

L_("containers", "cpp", SEC_DATA,
   {"en": "vector, map, set", "de": "vector, map, set"},
   {"en": """The standard library containers are the whole toolkit:

    std::vector<long long> nums{3, 1, 4};
    nums.push_back(5);   nums.size();   nums.empty();   nums[0];
    std::sort(nums.begin(), nums.end());          from <algorithm>
    std::reverse(nums.begin(), nums.end());

    std::map<char, int> counts;        sorted by key, O(log n)
    std::unordered_map<char, int> u;   hash table, O(1) average
    counts[c]++;                       a missing key is created as 0

    std::set<long long> unique;        sorted and unique
    std::unordered_set<long long> s;
    unique.insert(x);
    unique.count(x)                    0 or 1

Almost everything in <algorithm> takes a pair of iterators rather than a
container, which is why you keep writing v.begin(), v.end().

Note that counts[c] on a map INSERTS a default when the key is missing. Use
.count(k) or .find(k) when you only want to look.""",
    "de": """Die Container der Standardbibliothek sind der ganze Werkzeugkasten:

    std::vector<long long> nums{3, 1, 4};
    nums.push_back(5);   nums.size();   nums.empty();   nums[0];
    std::sort(nums.begin(), nums.end());          aus <algorithm>
    std::reverse(nums.begin(), nums.end());

    std::map<char, int> counts;        nach Schlüssel sortiert, O(log n)
    std::unordered_map<char, int> u;   Hashtabelle, im Mittel O(1)
    counts[c]++;                       ein fehlender Schlüssel entsteht als 0

    std::set<long long> unique;        sortiert und eindeutig
    std::unordered_set<long long> s;
    unique.insert(x);
    unique.count(x)                    0 oder 1

Fast alles in <algorithm> nimmt ein Iteratorpaar statt eines Containers —
deshalb schreibst du ständig v.begin(), v.end().

Beachte: counts[c] auf einer map FÜGT einen Vorgabewert ein, wenn der Schlüssel
fehlt. Nimm .count(k) oder .find(k), wenn du nur nachsehen willst."""},
   {"en": "map[k] inserts a default. Use .count(k) to look without inserting.",
    "de": "map[k] fügt einen Vorgabewert ein. Nimm .count(k) zum reinen Nachsehen."},
   '''#include <algorithm>
#include <iostream>
#include <map>
#include <set>
#include <string>
#include <vector>

int main() {
    std::vector<long long> nums{10, 9, 1, 4};
    nums.push_back(7);
    std::sort(nums.begin(), nums.end());
    for (const auto& n : nums) std::cout << n << " ";
    std::cout << std::endl;

    std::map<char, int> counts;
    for (char c : std::string("mississippi")) counts[c]++;
    for (const auto& pair : counts)
        std::cout << "  " << pair.first << " -> " << pair.second << std::endl;

    std::set<long long> unique(nums.begin(), nums.end());
    std::cout << "unique size: " << unique.size() << std::endl;
    std::cout << "contains 9? " << unique.count(9) << std::endl;

    std::cout << "map size before a lookup: " << counts.size() << std::endl;
    counts['z'];
    std::cout << "after counts['z'] it grew to: " << counts.size() << std::endl;

    auto biggest = std::max_element(nums.begin(), nums.end());
    std::cout << "max: " << *biggest << std::endl;
    return 0;
}
''',
   "second_largest", Sig([("nums", L(INT))], INT),
   {"en": """Write second_largest(nums) returning the second largest DISTINCT value.
Return -1 if there are fewer than two distinct values.

  second_largest([3, 1, 4, 4, 5]) -> 4
  second_largest([7, 7, 7])       -> -1

A std::set is sorted and unique already, so building one from the input does
most of the job.""",
    "de": """Schreib second_largest(nums), das den zweitgrößten VERSCHIEDENEN Wert liefert.
Gib -1 zurück, wenn es weniger als zwei verschiedene Werte gibt.

  second_largest([3, 1, 4, 4, 5]) -> 4
  second_largest([7, 7, 7])       -> -1

Ein std::set ist bereits sortiert und eindeutig — eines aus der Eingabe zu bauen
erledigt den Großteil."""},
   [case([3, 1, 4, 4, 5], 4), case([7, 7, 7], -1), case([2, 1], 1),
    case([], -1, hidden=True), case([-5, -2, -9, -2], -5, hidden=True)],
   '''#include <set>
#include <vector>

long long second_largest(const std::vector<long long>& nums) {
    std::set<long long> distinct(nums.begin(), nums.end());
    if (distinct.size() < 2) return -1;
    auto it = distinct.rbegin();
    ++it;
    return *it;
}
''',
   {"en": ["A std::set built from begin()/end() is sorted and deduplicated",
           "rbegin() is the largest; step it once for the second largest",
           "Check size() before stepping"],
    "de": ["Ein std::set aus begin()/end() ist sortiert und ohne Duplikate",
           "rbegin() ist das größte; einen Schritt weiter ist das zweitgrößte",
           "Prüf size(), bevor du weitergehst"]})

L_("algorithms", "cpp", SEC_CORE,
   {"en": "References and <algorithm>", "de": "Referenzen und <algorithm>"},
   {"en": """Two habits separate readable C++ from slow C++.

First, pass big things by reference. `const std::vector<T>&` costs nothing;
passing by value copies every element. In a loop, the same applies:

    for (auto n : nums)          copies each element
    for (const auto& n : nums)   does not
    for (auto& n : nums)         does not, and can modify

Second, reach for <algorithm> before writing a loop:

    std::sort(v.begin(), v.end());
    std::sort(v.begin(), v.end(), [](auto a, auto b) { return a > b; });
    std::reverse / std::count / std::find / std::accumulate  (<numeric>)
    std::max_element(v.begin(), v.end())    returns an ITERATOR — deref it
    std::unique(v.begin(), v.end())         needs a sorted range, and only
                                            moves duplicates to the back

Lambdas are the comparator syntax: [](long long a, long long b) { return a > b; }
The [] captures — [] captures nothing, [&] captures by reference.""",
    "de": """Zwei Gewohnheiten trennen lesbares von langsamem C++.

Erstens: übergib Großes per Referenz. `const std::vector<T>&` kostet nichts,
per Wert zu übergeben kopiert jedes Element. In Schleifen gilt dasselbe:

    for (auto n : nums)          kopiert jedes Element
    for (const auto& n : nums)   nicht
    for (auto& n : nums)         nicht, und kann verändern

Zweitens: greif zu <algorithm>, bevor du eine Schleife schreibst:

    std::sort(v.begin(), v.end());
    std::sort(v.begin(), v.end(), [](auto a, auto b) { return a > b; });
    std::reverse / std::count / std::find / std::accumulate  (<numeric>)
    std::max_element(v.begin(), v.end())    liefert einen ITERATOR — dereferenzieren
    std::unique(v.begin(), v.end())         braucht sortierte Daten und schiebt
                                            Duplikate nur nach hinten

Lambdas sind die Vergleichersyntax: [](long long a, long long b) { return a > b; }
Die [] fangen ein — [] gar nichts, [&] per Referenz."""},
   {"en": "const auto& in range loops. max_element returns an iterator — dereference it.",
    "de": "const auto& in Schleifen. max_element liefert einen Iterator — dereferenzieren."},
   '''#include <algorithm>
#include <iostream>
#include <numeric>
#include <vector>

int main() {
    std::vector<long long> nums{5, 3, 9, 3, 1};

    std::vector<long long> desc = nums;
    std::sort(desc.begin(), desc.end(),
              [](long long a, long long b) { return a > b; });
    for (const auto& n : desc) std::cout << n << " ";
    std::cout << std::endl;

    std::cout << "sum: "
              << std::accumulate(nums.begin(), nums.end(), 0LL) << std::endl;
    std::cout << "count of 3: "
              << std::count(nums.begin(), nums.end(), 3) << std::endl;
    std::cout << "max: "
              << *std::max_element(nums.begin(), nums.end()) << std::endl;

    std::vector<long long> doubled;
    for (auto& n : nums) n *= 2;            // & so the change sticks
    for (const auto& n : nums) std::cout << n << " ";
    std::cout << std::endl;

    auto found = std::find(nums.begin(), nums.end(), 18);
    std::cout << "found 18? " << (found != nums.end() ? "yes" : "no") << std::endl;
    return 0;
}
''',
   "col_sums", Sig([("grid", L(L(INT)))], L(INT)),
   {"en": """The grid is a rectangular list of rows. Return the sum of each COLUMN.

  col_sums([[1, 2], [3, 4], [5, 6]]) -> [9, 12]
  col_sums([])                       -> []

Take the grid by const reference and loop with const auto& — copying a grid you
only read from is exactly the habit this lesson is about.""",
    "de": """Das Gitter ist eine rechteckige Liste von Zeilen. Gib die Summe jeder SPALTE
zurück.

  col_sums([[1, 2], [3, 4], [5, 6]]) -> [9, 12]
  col_sums([])                       -> []

Nimm das Gitter per const-Referenz und lauf mit const auto& — ein Gitter zu
kopieren, aus dem du nur liest, ist genau die Gewohnheit, um die es hier geht."""},
   [case([[1, 2], [3, 4], [5, 6]], [9, 12]), case([], []),
    case([[1, 2, 3]], [1, 2, 3]),
    case([[0, 0], [0, 0]], [0, 0], hidden=True),
    case([[1], [2], [3], [4]], [10], hidden=True)],
   '''#include <vector>

std::vector<long long> col_sums(const std::vector<std::vector<long long>>& grid) {
    if (grid.empty()) return {};
    std::vector<long long> out(grid[0].size(), 0);
    for (const auto& row : grid) {
        for (size_t i = 0; i < row.size(); ++i) out[i] += row[i];
    }
    return out;
}
''',
   {"en": ["Size the result from the first row, then add every row into it",
           "const auto& in the loop avoids copying each row",
           "Return {} for an empty grid, before touching grid[0]"],
    "de": ["Dimensionier das Ergebnis nach der ersten Zeile und addier alle Zeilen hinein",
           "const auto& in der Schleife vermeidet das Kopieren jeder Zeile",
           "Gib bei leerem Gitter {} zurück, bevor du auf grid[0] zugreifst"]})

L_("strings", "cpp", SEC_STRINGS,
   {"en": "std::string", "de": "std::string"},
   {"en": """std::string is mutable, unlike almost every other language here.

    s.size()  s.length()   s.empty()
    s[0]                   indexing works
    s.substr(1, 3)         start and COUNT, like C#
    s.find("x")            returns std::string::npos when absent
    s += "more";           cheap; std::string grows
    std::reverse(s.begin(), s.end());

There is no split. The usual way is a stringstream, which also handles runs of
whitespace for you:

    std::istringstream stream(text);
    std::string word;
    while (stream >> word) { ... }      skips any amount of whitespace

For character tests include <cctype> and cast to unsigned char, because
std::tolower on a negative char is undefined behaviour:

    std::tolower(static_cast<unsigned char>(c))""",
    "de": """std::string ist veränderbar, anders als fast überall sonst hier.

    s.size()  s.length()   s.empty()
    s[0]                   Indizieren geht
    s.substr(1, 3)         Start und ANZAHL, wie in C#
    s.find("x")            liefert std::string::npos, wenn nicht gefunden
    s += "mehr";           günstig; std::string wächst
    std::reverse(s.begin(), s.end());

Ein split gibt es nicht. Üblich ist ein stringstream, der dir auch Folgen von
Leerraum abnimmt:

    std::istringstream stream(text);
    std::string word;
    while (stream >> word) { ... }      überspringt beliebig viel Leerraum

Für Zeichentests <cctype> einbinden und auf unsigned char casten, denn
std::tolower auf einem negativen char ist undefiniertes Verhalten:

    std::tolower(static_cast<unsigned char>(c))"""},
   {"en": "No split — use an istringstream. Cast to unsigned char before tolower.",
    "de": "Kein split — nimm einen istringstream. Vor tolower auf unsigned char casten."},
   '''#include <algorithm>
#include <cctype>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

int main() {
    std::string s = "  Hello, World  ";

    std::cout << "size: " << s.size() << ", first non-space: " << s[2] << std::endl;
    std::cout << "substr(2, 5): " << s.substr(2, 5) << std::endl;
    std::cout << "find World: " << s.find("World") << std::endl;
    std::cout << "not found gives: "
              << (s.find("zzz") == std::string::npos ? "npos" : "?") << std::endl;

    std::istringstream stream("  many   spaces here ");
    std::vector<std::string> words;
    std::string word;
    while (stream >> word) words.push_back(word);
    std::cout << words.size() << " words, first: " << words[0] << std::endl;

    std::string upper = "interview";
    for (auto& c : upper) c = std::toupper(static_cast<unsigned char>(c));
    std::cout << "upper: " << upper << std::endl;

    std::reverse(upper.begin(), upper.end());
    std::cout << "reversed: " << upper << std::endl;
    return 0;
}
''',
   "normalise", Sig([("text", STR)], STR),
   {"en": """Write normalise(text) that cleans up a messy name:

  * trim both ends
  * collapse any run of inner whitespace to a single space
  * capitalise each word: first letter upper, the rest lower

  normalise("  aDA   LOVElace ") -> "Ada Lovelace"
  normalise("   ")               -> ""

An istringstream with `while (stream >> word)` does the trimming and collapsing
in one step.""",
    "de": """Schreib normalise(text), das einen unordentlichen Namen aufräumt:

  * an beiden Enden trimmen
  * jede Folge innerer Leerzeichen auf eine reduzieren
  * jedes Wort groß schreiben: erster Buchstabe groß, Rest klein

  normalise("  aDA   LOVElace ") -> "Ada Lovelace"
  normalise("   ")               -> ""

Ein istringstream mit `while (stream >> word)` erledigt Trimmen und Reduzieren
in einem Schritt."""},
   [case("  aDA   LOVElace ", "Ada Lovelace"),
    case("guido van ROSSUM", "Guido Van Rossum"), case("   ", ""),
    case("a", "A", hidden=True),
    case("  linus     TORVALDS  ", "Linus Torvalds", hidden=True)],
   '''#include <cctype>
#include <sstream>
#include <string>

std::string normalise(const std::string& text) {
    std::istringstream stream(text);
    std::string word;
    std::string out;
    while (stream >> word) {
        if (!out.empty()) out += ' ';
        out += static_cast<char>(std::toupper(
            static_cast<unsigned char>(word[0])));
        for (size_t i = 1; i < word.size(); ++i) {
            out += static_cast<char>(std::tolower(
                static_cast<unsigned char>(word[i])));
        }
    }
    return out;
}
''',
   {"en": ["`while (stream >> word)` skips every run of whitespace for you",
           "Add a space only when the result is not empty yet",
           "Cast to unsigned char before toupper and tolower"],
    "de": ["`while (stream >> word)` überspringt jede Leerraumfolge für dich",
           "Füg nur dann ein Leerzeichen ein, wenn das Ergebnis nicht leer ist",
           "Vor toupper und tolower auf unsigned char casten"]})
