"""German translation of the interview problem bank (problems.py).

Keyed by problem id: title / statement / hints / notes. The reference solution
code itself stays as authored — it is Python, not prose.
"""

PROBLEMS_DE = {

# ============================================================ CODILITY
"binary_gap": {
 "title": "Binäre Lücke",
 "statement": """Eine binäre Lücke in einer positiven ganzen Zahl N ist eine möglichst lange
Folge aufeinanderfolgender NULLEN, die in der Binärdarstellung von N an beiden
Enden von einer Eins begrenzt wird.

  9  = 1001  -> eine Lücke der Länge 2    -> 2
  529 = 1000010001 -> Lücken 4 und 3      -> 4
  20 = 10100 -> eine Lücke der Länge 1    -> 1   (die letzte Null zählt nicht)
  15 = 1111  -> keine Lücke               -> 0
  32 = 100000 -> keine Lücke (nie geschlossen) -> 0

Schreib solution(n), das die Länge der längsten binären Lücke zurückgibt, oder
0, wenn es keine gibt. 1 <= n <= 2.147.483.647.""",
 "hints": ["bin(n)[2:] liefert die Binärziffern als String",
           "Fang erst NACH der ersten 1 an, Nullen zu zählen",
           "Eine Folge zählt nur, wenn sie von einer weiteren 1 GESCHLOSSEN wird — "
           "abschließende Nullen werden ignoriert"],
 "notes": "Codility Lektion 1. Die Falle ist die nicht abgeschlossene Nullfolge am Ende.",
},

"cyclic_rotation": {
 "title": "Zyklische Rotation",
 "statement": """Rotiere das Array `a` k-mal nach RECHTS. Jede Rotation schiebt das letzte
Element nach vorne.

  solution([3, 8, 9, 7, 6], 3) -> [9, 7, 6, 3, 8]
  solution([1, 2, 3, 4], 4)    -> [1, 2, 3, 4]
  solution([], 5)              -> []

k kann größer als len(a) sein. Gib eine NEUE Liste zurück.""",
 "hints": ["k % len(a) wirft die überflüssigen vollen Umdrehungen weg",
           "Eine Rechtsrotation um k ist a[-k:] + a[:-k]",
           "Fang die leere Liste ab (Division durch null!) und k == 0 "
           "(a[-0:] ist die GANZE Liste)"],
 "notes": "Codility Lektion 2. Dass a[-0:] alles zurückgibt, ist hier der klassische Bug.",
},

"odd_occurrences": {
 "title": "Ungerade Vorkommen im Array",
 "statement": """Das Array hat eine UNGERADE Anzahl Elemente. Jeder Wert kommt eine gerade
Anzahl von Malen vor — außer genau einem, der ungerade oft auftaucht.

Finde diesen Wert.

  solution([9, 3, 9, 3, 9, 7, 9]) -> 7

Erwartet werden O(n) Zeit und O(1) Speicher — also kein dict, kein set.""",
 "hints": ["XOR: x ^ x == 0 und x ^ 0 == x",
           "XOR ist kommutativ, die Paare heben sich also unabhängig von der Reihenfolge auf",
           "Falte das ganze Array mit ^ zusammen; was übrig bleibt, ist der einzelne Wert"],
 "notes": "Codility Lektion 2. XOR ist der O(1)-Speicher-Trick, auf den geprüft wird.",
},

"frog_jmp": {
 "title": "Froschsprung",
 "statement": """Ein kleiner Frosch sitzt an Position X und will mindestens Position Y erreichen.
Er springt jedes Mal eine feste Distanz D.

Schreib solution(x, y, d), das die MINIMALE Anzahl Sprünge zurückgibt.

  solution(10, 85, 30) -> 3
  solution(10, 10, 5)  -> 0

X <= Y, und die Zahlen gehen bis 1.000.000.000 — eine Schleife würde also ins
Zeitlimit laufen. Rechne es aus.""",
 "hints": ["distanz = y - x",
           "Du brauchst aufgerundet distanz / d Sprünge",
           "Ganzzahlige Aufrundung ohne floats: -(-a // b)"],
 "notes": "Codility Lektion 3. math.ceil auf floats verliert bei 1e9 an Genauigkeit — nimm -(-a // b).",
},

"perm_missing": {
 "title": "Fehlendes Element einer Permutation",
 "statement": """Das Array enthält N verschiedene ganze Zahlen aus dem Bereich 1..(N+1) — genau
ein Wert aus diesem Bereich fehlt.

Finde ihn.

  solution([2, 3, 1, 5]) -> 4
  solution([])           -> 1

Erwartet: O(n) Zeit, O(1) Speicher. NICHT sortieren.""",
 "hints": ["Der volle Bereich 1..N+1 summiert sich zu (N+1)(N+2)/2",
           "Zieh die tatsächliche Summe ab, und die fehlende Zahl fällt heraus",
           "Auch 1..N+1 gegen das Array zu XOR-en funktioniert"],
 "notes": "Codility Lektion 3. Die Gaußsche Summenformel, keine Schleife.",
},

"tape_equilibrium": {
 "title": "Bandgleichgewicht",
 "statement": """Teile das Array an Position P (1 <= P < N) in a[0..P-1] und a[P..N-1].
Der Unterschied ist |summe(links) - summe(rechts)|.

Gib den KLEINSTMÖGLICHEN Unterschied zurück.

  solution([3, 1, 2, 4, 3]) -> 1     (Teilung nach 3,1,2 -> |6 - 7| = 1)

N >= 2 und bis zu 100.000, beide Summen für jedes P neu zu berechnen (O(n^2))
läuft also ins Zeitlimit. Ein Durchlauf.""",
 "hints": ["gesamt = sum(a) einmal, vor der Schleife",
           "rechts = gesamt - links, damit summierst du nie neu",
           "P läuft von 1 bis N-1 — der Schleifenindex geht also bis len(a) - 2"],
 "notes": "Codility Lektion 3. Das kanonische 'die rechte Seite aus der Gesamtsumme ableiten'-Muster.",
},

"frog_river": {
 "title": "Frosch über den Fluss",
 "statement": """Ein Frosch will einen Fluss bis Position X überqueren. Blätter fallen: a[k] ist
die Position, an der zum Zeitpunkt k ein Blatt landet. Der Frosch kann hinüber,
sobald jede Position 1..X mindestens ein Blatt hat.

Gib den FRÜHESTEN Zeitpunkt (Index in a) zurück, an dem das der Fall ist, oder
-1, wenn es nie passiert.

  solution(5, [1, 3, 1, 4, 2, 3, 5, 4]) -> 6
  solution(1, [2, 2, 2])                -> -1""",
 "hints": ["Merk dir die abgedeckten Positionen in einem set",
           "Hör auf, sobald len(gesehen) == x ist — dieser Index ist die Antwort",
           "Positionen größer als x kannst du ignorieren"],
 "notes": "Codility Lektion 4. Zählen, wie viele verschiedene Ziele abgedeckt sind — nicht sortieren.",
},

"perm_check": {
 "title": "Permutationsprüfung",
 "statement": """Gib 1 zurück, wenn das Array eine Permutation von 1..N ist (jeder Wert genau
einmal), sonst 0.

  solution([4, 1, 3, 2]) -> 1
  solution([4, 1, 3])    -> 0""",
 "hints": ["Eine Permutation von 1..N hat genau N verschiedene Werte",
           "set(a) == set(range(1, len(a) + 1)) klärt das in einer Zeile",
           "Pass auf Duplikate UND auf Werte außerhalb des Bereichs auf"],
 "notes": "Codility Lektion 4.",
},

"missing_integer": {
 "title": "Fehlende positive Zahl",
 "statement": """Gib die KLEINSTE positive ganze Zahl (>= 1) zurück, die NICHT im Array vorkommt.

  solution([1, 3, 6, 4, 1, 2]) -> 5
  solution([1, 2, 3])          -> 4
  solution([-1, -3])           -> 1

Das Array darf negative Zahlen und Duplikate enthalten. O(n) erwartet.""",
 "hints": ["Pack erst alles in ein set, damit die Suche O(1) ist",
           "Dann geh 1, 2, 3, ... durch, bis du eine Lücke findest",
           "Die Antwort ist höchstens len(a) + 1, die Schleife ist also begrenzt"],
 "notes": "Codility Lektion 4. Die Antwort kann nie größer als N+1 sein — das begrenzt die Suche.",
},

"max_counters": {
 "title": "Maximale Zähler",
 "statement": """Du hast N Zähler, alle beginnen bei 0. Für jeden Wert K in der Operationsliste:

  * wenn 1 <= K <= N: erhöhe Zähler K um 1
  * wenn K == N + 1: setze ALLE Zähler auf das aktuelle Maximum

Gib die Zähler am Ende als Liste zurück.

  solution(5, [3, 4, 4, 6, 1, 4, 4]) -> [3, 2, 2, 4, 2]

N und len(a) gehen bis 100.000. Bei einer max_counter-Operation tatsächlich in
jeden Zähler zu schreiben, ist O(n*m) und läuft GARANTIERT ins Zeitlimit — genau
darum geht es bei dieser Aufgabe.""",
 "hints": ["Lauf bei einer max-Operation bloß NICHT über alle Zähler — das ist die Falle",
           "Führ einen faulen `boden`-Wert mit, auf den jeder Zähler implizit angehoben ist",
           "Wenn du einen Zähler anfasst, heb ihn erst an: max(zaehler, boden), dann +1",
           "Ganz am Ende alles anheben, was nie angefasst wurde"],
 "notes": "Codility Lektion 4. Faule Auswertung — die Codility-Aufgabe, an der die meisten scheitern.",
},

"count_div": {
 "title": "Teiler zählen",
 "statement": """Zähle die ganzen Zahlen im geschlossenen Bereich [a, b], die durch k teilbar sind.

  solution(6, 11, 2) -> 3      (6, 8, 10)
  solution(0, 0, 11) -> 1      (0 ist durch alles teilbar)

a und b gehen bis 2.000.000.000, eine Schleife ist also viel zu langsam.
O(1)-Arithmetik.""",
 "hints": ["Vielfache von k bis x: x // k",
           "Die Antwort ist also b//k - (a-1)//k",
           "a == 0 ist der Sonderfall: die Null selbst zählt, und (0-1)//k ist -1"],
 "notes": "Codility Lektion 5. Reine Zählarithmetik; der Sonderfall a == 0 ist die Falle.",
},

"passing_cars": {
 "title": "Sich begegnende Autos",
 "statement": """Ein Array aus 0en und 1en: 0 = ein Auto fährt nach OSTEN, 1 = nach WESTEN.
Ein Paar (P, Q) begegnet sich, wenn P < Q, a[P] == 0 und a[Q] == 1.

Gib die Anzahl der sich begegnenden Paare zurück, oder -1, wenn sie
1.000.000.000 übersteigt.

  solution([0, 1, 0, 1, 1]) -> 5

O(n) — Paare mit einer verschachtelten Schleife zu zählen ist O(n^2) und läuft
bei N = 100.000 ins Zeitlimit.""",
 "hints": ["Lauf von links nach rechts und zähl die bisher gesehenen 0en",
           "Jedes Mal, wenn eine 1 kommt, bildet sie mit ALL diesen 0en auf einen Schlag Paare",
           "Brich ab, sobald die laufende Summe 1e9 übersteigt"],
 "notes": "Codility Lektion 5. 'Zähl, wie viele von der anderen Sorte vorher kamen' — ein Kernmuster.",
},

"min_avg_slice": {
 "title": "Teilstück mit kleinstem Mittelwert",
 "statement": """Ein Teilstück ist ein zusammenhängender Abschnitt a[p..q] mit p < q. Gib den
START-Index des Teilstücks mit dem kleinsten Mittelwert zurück. Bei Gleichstand
den kleinsten Index.

  solution([4, 2, 2, 5, 1, 5, 8]) -> 1     (Teilstück [2,2], Mittelwert 2)

Die entscheidende Einsicht: du musst nie Teilstücke länger als 3 prüfen. Jedes
längere Teilstück lässt sich in 2er- und 3er-Stücke zerlegen, und mindestens
eines davon hat einen Mittelwert, der nicht schlechter ist als das Ganze. Alle
2er- und 3er-Stücke zu prüfen reicht also — O(n).""",
 "hints": ["Nur Teilstücke der Länge 2 und 3 können minimal sein — beweis es dir kurz, dann nutz es",
           "Ein Durchlauf, in dem du an jedem Index beide Fenster vergleichst",
           "Nimm ein striktes <, damit bei Gleichstand der frühere Index gewinnt"],
 "notes": "Codility Lektion 5. Das Lemma 'Länge 2 oder 3 genügt' IST die ganze Aufgabe.",
},

"distinct": {
 "title": "Verschiedene Werte",
 "statement": """Gib die Anzahl der VERSCHIEDENEN Werte im Array zurück.

  solution([2, 1, 1, 2, 3, 1]) -> 3
  solution([]) -> 0""",
 "hints": ["len(set(a)) ist schon die ganze Antwort",
           "Codilitys offizieller Weg sortiert und zählt die Wechsel — beides wird akzeptiert"],
 "notes": "Codility Lektion 6. Geschenkte Punkte — sag aber die Komplexität laut dazu.",
},

"triangle": {
 "title": "Dreieck",
 "statement": """Gib 1 zurück, wenn das Array ein Dreiecks-Tripel enthält (Indizes p < q < r mit
a[p] + a[q] > a[r], a[q] + a[r] > a[p], a[r] + a[p] > a[q]), sonst 0.

  solution([10, 2, 5, 1, 8, 20]) -> 1     (10, 8, 20)
  solution([10, 50, 5, 1])       -> 0

O(n log n): sortieren, danach können nur noch BENACHBARTE Tripel klappen.""",
 "hints": ["Sortier zuerst — dann sind zwei der drei Bedingungen automatisch erfüllt",
           "Nur aufeinanderfolgende Tripel zählen: größere Abstände machen die Summenbedingung nur schwerer",
           "Achte auf den Vergleich: a[i] + a[i+1] > a[i+2]"],
 "notes": "Codility Lektion 6. Sortieren macht aus drei Bedingungen eine.",
},

"max_product_three": {
 "title": "Größtes Produkt aus drei Werten",
 "statement": """Gib das größte Produkt dreier Werte aus dem Array zurück.

  solution([-3, 1, 2, -2, 5, 6]) -> 60     (2 * 5 * 6)
  solution([-5, -6, 1, 2, 3])    -> 90     (-5 * -6 * 3)

Die Falle sind die negativen Zahlen: zwei große negative Werte ergeben
multipliziert einen großen positiven.""",
 "hints": ["Sortieren, dann gibt es nur ZWEI Kandidaten",
           "Entweder die drei größten, oder die zwei kleinsten (am stärksten negativen) mal dem größten",
           "max() dieser beiden Kandidaten ist die Antwort"],
 "notes": "Codility Lektion 6. Auch eine sehr häufige Telefoninterview-Frage.",
},

"brackets": {
 "title": "Klammern",
 "statement": """Gib 1 zurück, wenn der Klammer-String korrekt verschachtelt ist, sonst 0.
Der String kann ( ) [ ] { } enthalten.

  solution("{[()()]}") -> 1
  solution("([)()]")   -> 0
  solution("")         -> 1""",
 "hints": ["Ein Stapel ist die Antwort — öffnende Klammern drauflegen, bei schließenden herunternehmen",
           "Passt die heruntergenommene öffnende Klammer nicht, sofort scheitern",
           "Am Ende muss der Stapel LEER sein, sonst wurde etwas nie geschlossen"],
 "notes": "Codility Lektion 7 == LeetCode 'Valid Parentheses'. Diese hier musst du im Schlaf können.",
},

"fish": {
 "title": "Fische",
 "statement": """N Fische treiben einen Fluss hinunter. a[i] ist die Größe von Fisch i, b[i]
seine Richtung: 0 = flussaufwärts (zu kleineren Indizes), 1 = flussabwärts.

Wenn ein abwärts treibender Fisch auf einen aufwärts treibenden trifft, frisst
der Größere den Kleineren. Alle Größen sind verschieden.

Gib zurück, wie viele Fische überleben.

  solution([4, 3, 2, 1, 5], [0, 1, 0, 0, 0]) -> 2""",
 "hints": ["Führ einen Stapel der abwärts treibenden Fische, die noch unterwegs sind",
           "Ein aufwärts treibender Fisch kämpft gegen die Spitze dieses Stapels, bis er gewinnt oder stirbt",
           "Leert sich der Stapel, überlebt der aufwärts treibende Fisch endgültig"],
 "notes": "Codility Lektion 7. Dasselbe Grundgerüst wie 'Asteroid Collision' auf LeetCode.",
},

"stone_wall": {
 "title": "Steinmauer",
 "statement": """Bau eine Mauer, deren Höhe an Position i genau h[i] sein muss. Jeder Stein ist
ein Rechteck beliebiger Breite mit konstanter Höhe. Gib die MINIMALE Anzahl
Steine zurück.

  solution([8, 8, 5, 7, 9, 8, 7, 4, 8]) -> 7""",
 "hints": ["Ein monoton steigender Stapel der gerade 'offenen' Höhen",
           "Nimm alles herunter, was höher als die aktuelle Höhe ist — diese Steine sind fertig",
           "Ist die Spitze gleich der aktuellen Höhe, benutz diesen Stein weiter (kein neuer Zähler)"],
 "notes": "Codility Lektion 7. Monotoner Stapel — dieselbe Idee wie 'Largest Rectangle in Histogram'.",
},

"dominator": {
 "title": "Dominator",
 "statement": """Der Dominator eines Arrays ist ein Wert, der an MEHR als der Hälfte der
Positionen vorkommt. Gib IRGENDEINEN Index zurück, an dem der Dominator steht,
oder -1, wenn es keinen gibt.

  solution([3, 4, 3, 2, 3, -1, 3, 3]) -> irgendein Index, an dem der Wert 3 steht
  solution([1, 2])                    -> -1

Erwartet: O(n) Zeit, O(1) Speicher -> Boyer-Moore-Wahlverfahren.""",
 "hints": ["Boyer-Moore: halt einen Kandidaten und einen Zähler; passende Stimmen +1, andere -1",
           "Fällt der Zähler auf 0, nimm den aktuellen Wert als neuen Kandidaten",
           "Du MUSST den Überlebenden am Ende überprüfen — die Wahl findet nur einen Kandidaten"],
 "notes": "Codility Lektion 8 == LeetCode 'Majority Element'. Der Überprüfungsschritt ist nicht optional.",
},

"max_profit": {
 "title": "Maximaler Gewinn",
 "statement": """a[i] ist ein Aktienkurs an Tag i. Kauf an einem Tag, verkauf an einem SPÄTEREN.
Gib den maximalen Gewinn zurück, oder 0, wenn es kein gewinnbringendes Geschäft
gibt.

  solution([23171, 21011, 21123, 21366, 21013, 21367]) -> 356
  solution([5, 4, 3])                                  -> 0

Ein Durchlauf, O(n).""",
 "hints": ["Merk dir den bisher günstigsten Kurs",
           "An jedem Tag ist der beste Verkauf heute: kurs - guenstigster",
           "Lass den Gewinn nie unter 0 fallen"],
 "notes": "Codility Lektion 9 == LeetCode 121 'Best Time to Buy and Sell Stock'.",
},

"max_slice_sum": {
 "title": "Größte Teilstücksumme (Kadane)",
 "statement": """Gib die größte Summe eines NICHT LEEREN zusammenhängenden Teilstücks zurück.

  solution([3, 2, -6, 4, 0]) -> 5
  solution([-5, -2, -8])     -> -2

Das ist Kadanes Algorithmus. Achtung: das Array kann komplett negativ sein, mit
`best = 0` anzufangen ist also falsch.""",
 "hints": ["Entscheide bei jedem Element: das aktuelle Teilstück verlängern oder hier neu anfangen",
           "aktuell = max(wert, aktuell + wert)",
           "Initialisiere BEIDE, best und aktuell, mit a[0] — nicht mit 0"],
 "notes": "Codility Lektion 9 == LeetCode 53 'Maximum Subarray'. Diese zwei Zeilen lernst du auswendig.",
},

"count_factors": {
 "title": "Teiler zählen",
 "statement": """Gib zurück, wie viele Teiler die positive ganze Zahl n hat.

  solution(24) -> 8      (1, 2, 3, 4, 6, 8, 12, 24)
  solution(1)  -> 1

n geht bis 2.147.483.647, Probedivision bis n ist also viel zu langsam.
Geh nur bis Wurzel(n) und zähl beide Partner jedes Paares.""",
 "hints": ["Teiler kommen paarweise: teilt i die Zahl n, dann auch n // i",
           "Lauf, solange i * i < n, und zähl bei jedem Treffer 2 dazu",
           "Eine Quadratzahl hat einen Teiler ohne Partner — behandle i * i == n extra"],
 "notes": "Codility Lektion 10. Nimm i*i < n statt i < sqrt(n) — dann gibt es keine Rundungsfehler.",
},

"min_perimeter": {
 "title": "Kleinster Rechteckumfang",
 "statement": """Finde den minimalen Umfang eines Rechtecks mit ganzzahligen Seiten, dessen
Fläche genau n ist.

  solution(30) -> 22     (5 x 6)
  solution(1)  -> 4

Umfang = 2 * (a + b) mit a * b == n. Das "quadratischste" Paar gewinnt, lauf
also von Wurzel(n) abwärts.""",
 "hints": ["Prüf nur Teiler bis Wurzel(n)",
           "Der LETZTE Teiler, den du unterhalb von Wurzel(n) findest, ist der quadratischste",
           "umfang = 2 * (i + n // i)"],
 "notes": "Codility Lektion 10.",
},

"chocolates": {
 "title": "Pralinen nach Zahlen",
 "statement": """N Pralinen liegen im Kreis, nummeriert 0..N-1. Du isst Praline 0 und springst
dann jedes Mal M weiter (mit Umlauf), bis du bei einer landest, die du schon
gegessen hast.

Gib zurück, wie viele du isst.

  solution(10, 4) -> 5

Die Zykluslänge ist n / ggT(n, m). Beweis es dir, dann ist es ein Einzeiler.
N und M gehen bis 1.000.000.000, den Rundgang zu simulieren ist also keine
Option.""",
 "hints": ["Simulieren ist O(n) — bei 1e9 zu langsam",
           "Du besuchst genau n // ggT(n, m) verschiedene Pralinen",
           "Implementier Euklids ggT mit der while-Schleife"],
 "notes": "Codility Lektion 12. Zahlentheorie, als Simulation getarnt.",
},

"genomic_range": {
 "title": "Genom-Bereichsabfrage",
 "statement": """Ein DNA-String aus A, C, G, T. Jeder Buchstabe hat einen Einflussfaktor:
A=1, C=2, G=3, T=4.

Gib für jede Abfrage (p[k], q[k]) — ein einschließender Abschnitt des Strings —
den KLEINSTEN Einflussfaktor darin zurück.

  solution("CAGCCTA", [2, 5, 0], [4, 5, 6]) -> [2, 4, 1]

Es kann 50.000 Abfragen über einen 100.000 Zeichen langen String geben; jeden
Abschnitt zu durchsuchen ist O(n*m) und läuft ins Zeitlimit. Bau stattdessen
vier Präfix-Zählarrays: dann ist jede Abfrage O(1).""",
 "hints": ["Bau ein Präfix-Zählarray pro Buchstabe: wie viele A stecken in s[0..i)",
           "Anzahl von Buchstabe k in [start, ende] = prefix[k][ende+1] - prefix[k][start]",
           "Prüf pro Abfrage erst A, dann C, dann G, dann T — der erste Treffer gewinnt"],
 "notes": "Codility Lektion 5 (schwer). Der 'Präfixzählung je Kategorie'-Trick lässt sich weit übertragen.",
},

"nesting": {
 "title": "Verschachtelung",
 "statement": """Gib 1 zurück, wenn der String, der nur aus ( und ) besteht, korrekt
verschachtelt ist, sonst 0.

  solution("(()(())())") -> 1
  solution("())")        -> 0
  solution("")           -> 1

O(1) Speicher: du brauchst nur einen Zähler, keinen Stapel.""",
 "hints": ["Ein einzelner Tiefenzähler genügt, wenn es nur eine Klammersorte gibt",
           "Wird die Tiefe je negativ, kam eine ) zu früh",
           "Am Ende muss sie genau 0 sein"],
 "notes": "Codility Lektion 7. Die Zähler-Variante ist die gewünschte Antwort.",
},

"number_of_disc": {
 "title": "Anzahl der Kreisüberschneidungen",
 "statement": """Kreis i hat den Mittelpunkt (i, 0) und den Radius a[i]. Zwei Kreise
überschneiden sich, wenn sie sich berühren oder überlappen.

Gib die Anzahl der sich überschneidenden PAARE zurück, oder -1, wenn sie
10.000.000 übersteigt.

  solution([1, 5, 2, 1, 4, 0]) -> 11

Der paarweise O(n^2)-Vergleich läuft bei N = 100.000 ins Zeitlimit. Sortier die
Intervallanfänge und -enden und überstreiche sie: bei jedem Anfang schneidet
jeder noch offene Kreis diesen.""",
 "hints": ["Mach aus jedem Kreis ein Intervall [i - r, i + r]",
           "Sortier Anfänge und Enden getrennt und überstreich sie mit zwei Zeigern",
           "Öffnet ein neuer Kreis, schneidet er jeden gerade offenen Kreis"],
 "notes": "Codility Lektion 6 (schwer). Das Sweep-Line-Muster taucht auch bei Kalender-/Meeting-Aufgaben auf.",
},

"equi_leader": {
 "title": "Gleichgewichts-Anführer",
 "statement": """Der Anführer eines Arrays ist ein Wert, der an mehr als der Hälfte der
Positionen vorkommt. Ein Gleichgewichts-Anführer ist ein Index S, bei dem
a[0..S] und a[S+1..n-1] DENSELBEN Anführer haben.

Gib zurück, wie viele solche Indizes es gibt.

  solution([4, 3, 4, 4, 4, 2]) -> 2""",
 "hints": ["Nur der Anführer des gesamten Arrays kann Anführer beider Hälften sein",
           "Find ihn mit Boyer-Moore und prüf dann, ob er wirklich Anführer ist",
           "Ein Durchlauf, der die Anzahl im linken Teil mitführt; die rechte ist gesamt - links"],
 "notes": "Codility Lektion 8. Verbindet Boyer-Moore mit einem Präfixdurchlauf.",
},

# ============================================================ LEETCODE
"two_sum": {
 "title": "Zwei Summanden",
 "statement": """Gib die INDIZES der beiden Zahlen zurück, die zusammen target ergeben, als Liste
[i, j] mit i < j. Es gibt genau eine Lösung, und du darfst kein Element zweimal
verwenden.

  two_sum([2, 7, 11, 15], 9) -> [0, 1]
  two_sum([3, 3], 6)         -> [0, 1]

O(n) mit einem dict von Wert -> Index. Die doppelte O(n^2)-Schleife ist die
Antwort, die durchfällt.""",
 "hints": ["Speicher Wert -> Index, während du durchläufst",
           "Frag für jeden Wert, ob target - wert schon gesehen wurde",
           "Trag NACH der Abfrage ein, damit sich ein Element nicht mit sich selbst paart"],
 "notes": "LeetCode 1. Die meistgestellte Frage überhaupt — die darf dir nie danebengehen.",
},

"valid_parens": {
 "title": "Gültige Klammern",
 "statement": """Gegeben ein String aus nur ()[]{}: entscheide, ob jede Klammer von derselben
Sorte und in der richtigen Reihenfolge geschlossen wird.

  is_valid("()[]{}") -> True
  is_valid("(]")     -> False
  is_valid("([)]")   -> False""",
 "hints": ["Leg öffnende Klammern auf einen Stapel",
           "Bei einer schließenden muss die heruntergenommene die passende öffnende sein",
           "Leerer Stapel am Ende = gültig"],
 "notes": "LeetCode 20.",
},

"max_subarray": {
 "title": "Größte Teilarraysumme",
 "statement": """Gib die größte Summe eines zusammenhängenden, nicht leeren Teilarrays zurück.

  max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]) -> 6      ([4, -1, 2, 1])
  max_subarray([-1])                            -> -1""",
 "hints": ["Kadanes Algorithmus",
           "aktuell = max(wert, aktuell + wert) — neu anfangen oder verlängern",
           "Eine komplett negative Eingabe bedeutet: du kannst nicht bei 0 starten"],
 "notes": "LeetCode 53.",
},

"product_except_self": {
 "title": "Produkt aller anderen Elemente",
 "statement": """Gib eine Liste zurück, in der out[i] das Produkt aller Elemente AUSSER nums[i]
ist.

  product_except_self([1, 2, 3, 4]) -> [24, 12, 8, 6]
  product_except_self([-1, 1, 0, -3, 3]) -> [0, 0, 9, 0, 0]

Du musst das OHNE Division schaffen, in O(n).""",
 "hints": ["out[i] = (Produkt links von i) * (Produkt rechts von i)",
           "Der erste Durchlauf von links nach rechts füllt die linken Produkte",
           "Der zweite von rechts nach links multipliziert die rechten dazu"],
 "notes": "LeetCode 238. Die Bedingung 'ohne Division' ist die eigentliche Übung.",
},

"longest_unique": {
 "title": "Längster Teilstring ohne Wiederholung",
 "statement": """Gib die Länge des längsten Teilstrings ohne wiederholtes Zeichen zurück.

  length_of_longest("abcabcbb") -> 3     ("abc")
  length_of_longest("bbbbb")    -> 1
  length_of_longest("pwwkew")   -> 3     ("wke")""",
 "hints": ["Schiebefenster mit einem dict von Zeichen -> letzter Index",
           "Triffst du INNERHALB des Fensters auf eine Wiederholung, spring mit links hinter deren alte Position",
           "Die Prüfung `>= links` ist wichtig — alte Vorkommen außerhalb des Fensters sind harmlos"],
 "notes": "LeetCode 3. Die Lehrbuchaufgabe zum Schiebefenster.",
},

"group_anagrams": {
 "title": "Anagramme gruppieren",
 "statement": """Gruppiere Wörter, die Anagramme voneinander sind.

Gib eine Liste von Gruppen zurück. Sortier jede Gruppe alphabetisch und die
Gruppen nach ihrem ersten Element, damit die Antwort eindeutig ist.

  group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
    -> [["ate", "eat", "tea"], ["bat"], ["nat", "tan"]]""",
 "hints": ['Die sortierten Buchstaben eines Worts sind sein Anagramm-Fingerabdruck: "eat" -> "aet"',
           "Sortier die Wörter in ein dict, das mit diesem Fingerabdruck indiziert ist",
           "Dann innerhalb jeder Gruppe sortieren und die Gruppen sortieren"],
 "notes": "LeetCode 49. 'Fingerabdruck in ein dict' ist ein Muster, das man im Interview benennen sollte.",
},

"merge_intervals": {
 "title": "Intervalle verschmelzen",
 "statement": """Verschmelze alle überlappenden Intervalle. Sich berührende Intervalle
verschmelzen auch: aus [1,4] und [4,5] wird [1,5].

Ein- und Ausgabe sind Listen aus Zweierlisten, nach Anfang sortiert.

  merge([[1, 3], [2, 6], [8, 10], [15, 18]]) -> [[1, 6], [8, 10], [15, 18]]
  merge([[1, 4], [4, 5]])                    -> [[1, 5]]""",
 "hints": ["Nach Anfang sortieren — danach genügt ein einziger Durchlauf",
           "Überlappungstest: der nächste Anfang ist <= dem aktuellen Ende",
           "Beim Verschmelzen das Maximum der Enden nehmen (ein Intervall kann ein anderes verschlucken)"],
 "notes": "LeetCode 56. Erst sortieren ist 90 % jeder Intervallaufgabe.",
},

"binary_search": {
 "title": "Binäre Suche",
 "statement": """`nums` ist aufsteigend sortiert. Gib den Index von target zurück, oder -1, wenn
er nicht vorkommt. Muss O(log n) sein.

  search([-1, 0, 3, 5, 9, 12], 9) -> 4
  search([-1, 0, 3, 5, 9, 12], 2) -> -1""",
 "hints": ["low, high = 0, len(nums) - 1 und Schleife, solange low <= high",
           "mid = (low + high) // 2",
           "Setz low auf mid + 1 oder high auf mid - 1 — niemals auf mid, sonst läufst du ewig"],
 "notes": "LeetCode 704. Schreib sie aus dem Kopf, bis die Fehler um eins aufhören.",
},

"search_rotated": {
 "title": "Suche im rotierten sortierten Array",
 "statement": """Ein sortiertes Array wurde an einer unbekannten Stelle rotiert (aus
[0,1,2,4,5,6,7] wird vielleicht [4,5,6,7,0,1,2]). Finde den Index von target,
oder -1. Weiterhin O(log n).

  search([4, 5, 6, 7, 0, 1, 2], 0) -> 4
  search([4, 5, 6, 7, 0, 1, 2], 3) -> -1""",
 "hints": ["In jedem Schritt ist mindestens EINE Hälfte richtig sortiert — finde heraus, welche",
           "nums[low] <= nums[mid] heißt: die linke Hälfte ist sortiert",
           "Prüf dann, ob das Ziel in dieser sortierten Hälfte liegt; wenn ja, geh dorthin"],
 "notes": "LeetCode 33. Beliebt, weil sie zeigt, ob du binäre Suche wirklich verstanden hast.",
},

"climb_stairs": {
 "title": "Treppensteigen",
 "statement": """Du steigst eine Treppe mit n Stufen und nimmst dabei 1 oder 2 Stufen auf einmal.
Wie viele verschiedene Wege gibt es nach oben?

  climb_stairs(2) -> 2      (1+1, 2)
  climb_stairs(3) -> 3      (1+1+1, 1+2, 2+1)

n kann 45 sein, einfache Rekursion ist also viel zu langsam — das ist Fibonacci
in Verkleidung.""",
 "hints": ["wege(n) = wege(n-1) + wege(n-2) — du kamst von einer oder zwei Stufen tiefer",
           "Iterier von unten nach oben mit zwei rollenden Variablen",
           "n = 0 und n = 1 haben beide genau einen Weg"],
 "notes": "LeetCode 70. Das Eingangstor zu jeder DP-Frage.",
},

"coin_change": {
 "title": "Münzwechsel",
 "statement": """Gib die KLEINSTE Anzahl Münzen zurück, mit der sich `amount` bilden lässt, oder
-1, wenn es unmöglich ist. Von jeder Münzsorte hast du unbegrenzt viele.

  coin_change([1, 2, 5], 11) -> 3      (5 + 5 + 1)
  coin_change([2], 3)        -> -1
  coin_change([1], 0)        -> 0

Gierig vorzugehen (immer die größte Münze nehmen) ist hier FALSCH — probier
Münzen [1, 3, 4] und Betrag 6. Du brauchst DP.""",
 "hints": ["dp[v] = kleinste Münzanzahl für genau v; dp[0] = 0",
           "dp[v] = Minimum über alle Münzen von dp[v - muenze] + 1",
           "Nimm unendlich für unerreichbare Beträge, dann funktioniert das Minimum von allein"],
 "notes": "LeetCode 322. Unbeschränktes Rucksackproblem — diese Form kommt ständig vor.",
},

"house_robber": {
 "title": "Der Einbrecher",
 "statement": """In jedem Haus liegt Geld. Du kannst nicht in zwei BENACHBARTE Häuser einbrechen.
Gib das Maximum zurück, das du mitnehmen kannst.

  rob([1, 2, 3, 1]) -> 4     (Häuser 0 und 2)
  rob([2, 7, 9, 3, 1]) -> 12 (Häuser 0, 2, 4)
  rob([]) -> 0""",
 "hints": ["Bei jedem Haus: entweder einbrechen (und das Beste von zwei Häusern zuvor dazuzählen) oder auslassen",
           "Zwei rollende Variablen genügen — kein Array nötig",
           "nehmen, auslassen = auslassen + wert, max(auslassen, nehmen)"],
 "notes": "LeetCode 198. Beachte die Umschreibung auf O(1) Speicher — danach wird gefragt.",
},

"longest_consecutive": {
 "title": "Längste Folge aufeinanderfolgender Zahlen",
 "statement": """Gib die Länge der längsten Folge AUFEINANDERFOLGENDER ganzer Zahlen zurück, die
im Array vorkommen (die Reihenfolge im Array spielt keine Rolle).

  longest_consecutive([100, 4, 200, 1, 3, 2]) -> 4      (1, 2, 3, 4)
  longest_consecutive([]) -> 0

Muss O(n) sein — Sortieren fällt streng genommen also weg.""",
 "hints": ["Pack alles in ein set, damit die Mitgliedschaft O(1) ist",
           "Fang nur bei Werten an zu zählen, die keinen Vorgänger im set haben",
           "Genau diese Bedingung hält es bei O(n) statt O(n^2)"],
 "notes": "LeetCode 128. Der Trick 'nur an Folgenanfängen starten' ist der Interview-Punkt.",
},

"three_sum": {
 "title": "3Sum",
 "statement": """Finde alle EINDEUTIGEN Tripel, die zusammen null ergeben. Gib sie sortiert
zurück: jedes Tripel aufsteigend, und die Liste der Tripel ebenfalls sortiert.

  three_sum([-1, 0, 1, 2, -1, -4]) -> [[-1, -1, 2], [-1, 0, 1]]
  three_sum([0, 0, 0, 0])          -> [[0, 0, 0]]

O(n^2): sortieren, ein Element festhalten, den Rest mit zwei Zeigern abgrasen.""",
 "hints": ["Erst sortieren, dann nums[i] festhalten und den Restbereich mit zwei Zeigern durchgehen",
           "Überspring doppelte Werte für i, sonst gibst du dasselbe Tripel mehrfach aus",
           "Nach einem Treffer auch am linken Zeiger die Duplikate überspringen"],
 "notes": "LeetCode 15. Am Überspringen der Duplikate scheitern die meisten.",
},

"container_water": {
 "title": "Behälter mit dem meisten Wasser",
 "statement": """Jedes heights[i] ist eine senkrechte Linie bei x = i. Wähl zwei Linien, die
zusammen mit der x-Achse das meiste Wasser fassen.

  max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]) -> 49
  max_area([1, 1]) -> 1

O(n) mit zwei Zeigern von den Enden her.""",
 "hints": ["Fang weit an: je ein Zeiger an jedem Ende",
           "Fläche = Breite * die KÜRZERE der beiden Linien",
           "Schieb immer die kürzere Linie nach innen — die höhere zu bewegen kann nie helfen"],
 "notes": "LeetCode 11. Sei bereit zu begründen, WARUM es sicher ist, die kürzere Seite zu bewegen.",
},

"move_zeroes": {
 "title": "Nullen nach hinten",
 "statement": """Schieb jede 0 ans Ende und behalte dabei die Reihenfolge der übrigen Werte.
Gib die entstandene Liste zurück.

  move_zeroes([0, 1, 0, 3, 12]) -> [1, 3, 12, 0, 0]
  move_zeroes([0]) -> [0]""",
 "hints": ["Sammel die Nicht-Nullen der Reihe nach ein",
           "Füll den Rest mit Nullen auf",
           "Die In-Place-Variante tauscht mit einem `schreib`-Zeiger — erwähn sie, wenn gefragt wird"],
 "notes": "LeetCode 283.",
},

"rotate_array": {
 "title": "Array rotieren",
 "statement": """Rotier die Liste um k Schritte nach rechts und gib sie zurück.

  rotate([1, 2, 3, 4, 5, 6, 7], 3) -> [5, 6, 7, 1, 2, 3, 4]
  rotate([-1, -100, 3, 99], 2)     -> [3, 99, -1, -100]

k darf größer als die Länge sein.""",
 "hints": ["Erst k %= len(nums)",
           "Slicing: nums[-k:] + nums[:-k]",
           "k == 0 braucht einen eigenen Zweig, denn nums[-0:] ist die ganze Liste"],
 "notes": "LeetCode 189.",
},

"majority_element": {
 "title": "Mehrheitselement",
 "statement": """Das Mehrheitselement kommt MEHR als n/2-mal vor. Hier existiert es immer.
Gib es zurück.

  majority([3, 2, 3])             -> 3
  majority([2, 2, 1, 1, 1, 2, 2]) -> 2

Zusatzziel: O(1) zusätzlicher Speicher (Boyer-Moore-Wahlverfahren).""",
 "hints": ["Ein Counter beantwortet es in O(n) Speicher — sag das, und verbesser es dann",
           "Boyer-Moore: halt einen Kandidaten und einen Stimmenzähler",
           "Setz den Kandidaten neu, sobald der Zähler auf null fällt"],
 "notes": "LeetCode 169.",
},

"single_number": {
 "title": "Die einzelne Zahl",
 "statement": """Jedes Element kommt zweimal vor, außer einem. Finde dieses eine.

  single_number([4, 1, 2, 1, 2]) -> 4

Lineare Zeit, konstanter zusätzlicher Speicher.""",
 "hints": ["x ^ x == 0, und x ^ 0 == x", "XOR das ganze Array zusammen"],
 "notes": "LeetCode 136.",
},

"top_k_frequent": {
 "title": "Die k häufigsten Elemente",
 "statement": """Gib die k häufigsten Werte zurück. Sortier die Antwort aufsteigend, damit sie
eindeutig ist.

  top_k_frequent([1, 1, 1, 2, 2, 3], 2) -> [1, 2]
  top_k_frequent([1], 1)                -> [1]""",
 "hints": ["In ein dict zählen, dann die Schlüssel nach -anzahl sortieren",
           "heapq.nlargest(k, counts, key=counts.get) ist die O(n log k)-Variante",
           "Bucket-Sort nach Häufigkeit liefert echtes O(n) — erwähnenswert"],
 "notes": "LeetCode 347.",
},

"valid_palindrome": {
 "title": "Gültiges Palindrom",
 "statement": """Ist der String ein Palindrom, wenn man Groß-/Kleinschreibung und alles ignoriert,
was kein Buchstabe und keine Ziffer ist?

  is_palindrome("A man, a plan, a canal: Panama") -> True
  is_palindrome("race a car")                     -> False
  is_palindrome(" ")                              -> True""",
 "hints": ["Filter mit ch.isalnum() und mach dabei klein",
           "Vergleich die bereinigte Liste mit ihrer Umkehrung",
           "Die O(1)-Speicher-Variante läuft mit zwei Zeigern nach innen — erwähn sie"],
 "notes": "LeetCode 125.",
},

"longest_common_prefix": {
 "title": "Längster gemeinsamer Präfix",
 "statement": """Gib den längsten String zurück, mit dem jedes Wort der Liste beginnt.
Gib "" zurück, wenn es keinen gibt.

  longest_common_prefix(["flower", "flow", "flight"]) -> "fl"
  longest_common_prefix(["dog", "racecar", "car"])    -> ""
  longest_common_prefix([])                           -> \"\"""",
 "hints": ["Die Antwort kann nie länger als das kürzeste Wort sein",
           "Geh das kürzeste Wort Zeichen für Zeichen durch und prüf jedes andere Wort",
           "Brich beim ersten Unterschied ab"],
 "notes": "LeetCode 14.",
},

"roman_to_int": {
 "title": "Römische Zahl zu Ganzzahl",
 "statement": """Wandle eine römische Zahl in eine ganze Zahl um. Symbole: I=1 V=5 X=10 L=50
C=100 D=500 M=1000. Ein kleinerer Wert VOR einem größeren wird abgezogen
(IV = 4, CM = 900).

  roman_to_int("III")     -> 3
  roman_to_int("LVIII")   -> 58
  roman_to_int("MCMXCIV") -> 1994""",
 "hints": ["Bild jedes Symbol in einem dict auf seinen Wert ab",
           "Ist ein Symbol kleiner als das NÄCHSTE, zieh es ab statt es zu addieren",
           "Ein Durchlauf, ohne IV / IX / XL einzeln zu behandeln"],
 "notes": "LeetCode 13.",
},

"spiral_matrix": {
 "title": "Spiralmatrix",
 "statement": """Gib alle Elemente der Matrix in Spiralreihenfolge zurück (rechts, runter, links,
hoch, nach innen).

  spiral_order([[1,2,3],[4,5,6],[7,8,9]]) -> [1,2,3,6,9,8,7,4,5]
  spiral_order([]) -> []

Die Matrix muss nicht quadratisch sein.""",
 "hints": ["Führ vier Grenzen mit: oben, unten, links, rechts",
           "Lauf eine Kante ab und zieh dann diese Grenze zusammen",
           "Prüf die Grenzen vor der unteren Zeile und der linken Spalte erneut, sonst besuchst du doppelt"],
 "notes": "LeetCode 54. Reine Grenzbuchführung — keine Cleverness, nur Sorgfalt.",
},

"num_islands": {
 "title": "Anzahl der Inseln",
 "statement": """Das Gitter enthält "1" (Land) und "0" (Wasser) als STRINGS. Eine Insel ist eine
Gruppe von 1en, die waagerecht oder senkrecht zusammenhängen. Zähl die Inseln.

  num_islands([["1","1","0"],
               ["1","0","0"],
               ["0","0","1"]]) -> 2

Flute jede Insel, sobald du sie das erste Mal berührst.""",
 "hints": ["Geh jedes Feld durch; findest du unbesuchtes Land, ist das eine NEUE Insel",
           "Flute sie mit einem eigenen Stapel (oder einer deque für BFS) und markier alles als gesehen",
           "Markier Felder beim HINEINLEGEN, nicht beim Herausnehmen — sonst gibt es Doppelte"],
 "notes": "LeetCode 200. Deine eine Gitter-Durchlauf-Vorlage — einmal lernen, für immer nutzen.",
},

"merge_sorted": {
 "title": "Zwei sortierte Listen verschmelzen",
 "statement": """Verschmelz zwei aufsteigende Listen zu einer aufsteigenden Liste.

  merge_sorted([1, 2, 4], [1, 3, 4]) -> [1, 1, 2, 3, 4, 4]
  merge_sorted([], [0])              -> [0]

Mach die echte Verschmelzung mit zwei Zeigern — sorted(a + b) funktioniert zwar,
verfehlt aber den Punkt.""",
 "hints": ["Zwei Indizes, einer pro Liste",
           "Nimm in jeder Runde den kleineren Kopf",
           "Ist eine Liste leer, häng den Rest der anderen an"],
 "notes": "LeetCode 21. Dieser Verschmelzungsschritt ist auch das Herz von Mergesort.",
},

"valid_anagram": {
 "title": "Gültiges Anagramm",
 "statement": """Gib True zurück, wenn t ein Anagramm von s ist.

  is_anagram("anagram", "nagaram") -> True
  is_anagram("rat", "car")         -> False""",
 "hints": ["Unterschiedliche Längen -> sofort False",
           "Zähl die Buchstaben von s und zieh beim Durchlaufen von t wieder ab",
           "sorted(s) == sorted(t) ist O(n log n) — in Ordnung, aber sag es dazu"],
 "notes": "LeetCode 242.",
},

"contains_duplicate": {
 "title": "Enthält Duplikate",
 "statement": """Gib True zurück, wenn irgendein Wert mindestens zweimal vorkommt.

  contains_duplicate([1, 2, 3, 1]) -> True
  contains_duplicate([1, 2, 3, 4]) -> False

Unter den versteckten Tests ist ein Array mit 200.000 Elementen, O(n^2) läuft
also ins Zeitlimit.""",
 "hints": ["len(set(nums)) != len(nums)",
           "Oder mit einem laufenden `gesehen`-Set früh abbrechen — besser, wenn das Duplikat früh kommt"],
 "notes": "LeetCode 217.",
},

"string_compress": {
 "title": "String-Kompression",
 "statement": """Komprimier Folgen wiederholter Zeichen: "aabcccccaaa" -> "a2b1c5a3".
Ist die komprimierte Form nicht KÜRZER als das Original, gib das Original zurück.

  compress("aabcccccaaa") -> "a2b1c5a3"
  compress("abc")         -> "abc"
  compress("")            -> \"\"""",
 "hints": ["Lauf mit einem Index, zähl die aktuelle Folge und schreib sie raus, wenn sie endet",
           "Jede Folge liefert Zeichen + Anzahl, auch eine Folge der Länge 1",
           "Vergleich ganz am Ende die Längen und gib die kürzere zurück"],
 "notes": "Cracking the Coding Interview 1.6 — ein sehr häufiges Aufwärmen.",
},

"set_matrix_zeroes": {
 "title": "Matrix-Nullen setzen",
 "statement": """Ist ein Feld 0, setz seine ganze ZEILE und SPALTE auf 0. Gib die geänderte
Matrix zurück.

  set_zeroes([[1,1,1],[1,0,1],[1,1,1]]) -> [[1,0,1],[0,0,0],[1,0,1]]

Die Falle: nullst du die Zeilen schon beim Durchlaufen, erzeugst du neue Nullen,
und es setzt sich fort. Sammel Zeilen und Spalten ZUERST, wende sie dann an.""",
 "hints": ["Zwei Durchläufe: erst die Nullen finden, dann die Nullen schreiben",
           "Merk dir die betroffenen Zeilen- und Spaltenindizes in Sets",
           "In einem Durchlauf setzt es sich fort und färbt die ganze Matrix schwarz"],
 "notes": "LeetCode 73.",
},

"min_window_len": {
 "title": "Kürzestes Teilarray mit Mindestsumme",
 "statement": """Gib die Länge des KÜRZESTEN zusammenhängenden Teilarrays zurück, dessen Summe
>= target ist. Gib 0 zurück, wenn es keines gibt. Alle Werte sind positiv.

  min_subarray_len(7, [2, 3, 1, 2, 4, 3]) -> 2      ([4, 3])
  min_subarray_len(11, [1, 1, 1])         -> 0

O(n) mit einem wachsenden und schrumpfenden Fenster.""",
 "hints": ["Lass das Fenster mit `rechts` wachsen und schrumpf es dann von `links`, solange es gültig bleibt",
           "Notier die Länge jedes Mal, wenn das Fenster gültig ist — vor dem Schrumpfen",
           "Jeder Index kommt einmal rein und einmal raus, trotz innerer while-Schleife ist es also O(n)"],
 "notes": "LeetCode 209. Die Vorlage für das Schiebefenster mit variabler Größe.",
},

"isomorphic": {
 "title": "Isomorphe Strings",
 "statement": """Zwei Strings sind isomorph, wenn sich die Zeichen von s konsistent ersetzen
lassen, sodass t herauskommt. Zwei verschiedene Zeichen dürfen NICHT auf
dasselbe abgebildet werden.

  is_isomorphic("egg", "add")     -> True
  is_isomorphic("foo", "bar")     -> False
  is_isomorphic("badc", "baba")   -> False""",
 "hints": ["Ein dict reicht nicht — du brauchst BEIDE Richtungen",
           "setdefault gibt die bestehende Zuordnung zurück, falls es eine gibt",
           "Der klassische Fehlerfall ist 'badc' / 'baba'"],
 "notes": "LeetCode 205. Die Prüfung in beide Richtungen ist die ganze Frage.",
},

"kth_largest": {
 "title": "Das k-größte Element",
 "statement": """Gib das k-größte Element zurück (k = 1 heißt das Maximum). Duplikate zählen als
eigene Positionen.

  find_kth_largest([3, 2, 1, 5, 6, 4], 2) -> 5
  find_kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) -> 4""",
 "hints": ["sorted(nums)[-k] ist die ehrliche O(n log n)-Ausgangslösung — nenn sie zuerst",
           "heapq.nlargest(k, nums)[-1] ist O(n log k)",
           "Quickselect schafft im Mittel O(n) — auch dann erwähnenswert, wenn du es nicht ausschreibst"],
 "notes": "LeetCode 215. Nenn alle drei Komplexitäten und entscheide dich für eine.",
},

"summary_ranges": {
 "title": "Bereiche zusammenfassen",
 "statement": """Gegeben eine SORTIERTE Liste verschiedener ganzer Zahlen: fass die
zusammenhängenden Läufe zusammen.

  summary_ranges([0, 1, 2, 4, 5, 7]) -> ["0->2", "4->5", "7"]
  summary_ranges([])                 -> []

Ein Lauf der Länge 1 wird nur als die Zahl geschrieben.""",
 "hints": ["Die äußere Schleife markiert den Anfang eines Laufs, die innere verlängert ihn",
           "Vergleich nums[i + 1] mit nums[i] + 1, um Aufeinanderfolge zu erkennen",
           "Einzelne Läufe werden ohne Pfeil ausgegeben"],
 "notes": "LeetCode 228. Schlicht, aber ein gutes Aufwärmen für Lauf-Erkennung.",
},

"sort_colors": {
 "title": "Farben sortieren (Niederländische Flagge)",
 "statement": """Die Liste enthält nur 0, 1 und 2. Sortier sie in EINEM Durchlauf, ohne sorted()
zu benutzen. Gib die Liste zurück.

  sort_colors([2, 0, 2, 1, 1, 0]) -> [0, 0, 1, 1, 2, 2]

Der Algorithmus der niederländischen Nationalflagge: drei Zeiger, ein Durchlauf.""",
 "hints": ["Drei Bereiche: alles unter low ist 0, alles über high ist 2",
           "Bei einer 0 tauschst du nach unten und erhöhst low UND i",
           "Bei einer 2 tauschst du nach oben und erhöhst i NICHT — du hast ja noch nicht gesehen, was angekommen ist"],
 "notes": "LeetCode 75. Das Detail 'nach dem Tausch einer 2 i nicht erhöhen' ist die Falle.",
},
}
