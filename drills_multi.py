"""Randomised drills that work in every language.

Same idea as drills.py, but the exercise is graded by a languages/ backend, so
the generator has to produce a reference solution per language with the random
parameter baked into each one.

That is the price of randomisation across seven languages: you cannot write the
solution once. What you get for it is a drill you can repeat forever in
whichever language you are preparing in.
"""
from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Callable

import i18n
import languages as LG
from languages import BOOL, INT, L, STR, Sig
from tasks import Task, make_cases

REGISTRY: list["MultiDrill"] = []


@dataclass
class MultiDrill:
    id: str
    topic: str
    difficulty: str
    build: Callable[[random.Random], Task]


def drill(did: str, topic: str, difficulty: str = "Easy"):
    def wrap(fn):
        REGISTRY.append(MultiDrill(did, topic, difficulty, fn))
        return fn
    return wrap


def _task(rng, did, topic, difficulty, func, sig, title, statement, ref,
          samples, solutions, hints) -> Task:
    """Assemble one randomised instance for the active language."""
    language = LG.CURRENT
    return Task(
        id=f"drill_{did}_{rng.randrange(10 ** 6)}",
        title=i18n.pick(title, did),
        func=func,
        statement=i18n.pick(statement, "").strip(),
        starter=LG.get(language).starter(func, sig),
        cases=make_cases(ref, samples, hidden_from=3),
        hints=list(i18n.pick(hints, []) or []),
        solution=solutions.get(language, ""),
        difficulty=difficulty,
        topic=topic,
        source="drill",
        sig=sig,
        language=language,
    )


def rand_list(rng, n=None, lo=-20, hi=40):
    n = n if n is not None else rng.randint(4, 9)
    return [rng.randint(lo, hi) for _ in range(n)]


# ===========================================================================
@drill("keep_divisible", "Lists")
def _keep_divisible(rng):
    k = rng.randint(2, 9)
    data = rand_list(rng, 8, 1, 60)

    def ref(nums):
        return [n for n in nums if n % k == 0]

    return _task(
        rng, "keep_divisible", "Lists", "Easy", "keep", Sig([("nums", L(INT))], L(INT)),
        {"en": f"Keep the multiples of {k}", "de": f"Vielfache von {k} behalten",
         "fr": f"Garder les multiples de {k}", "es": f"Quedarse con los múltiplos de {k}"},
        {"en": f"""Return only the values divisible by {k}, in their original order.

  keep({data}) -> {ref(data)}
  keep([]) -> []

Build a new list; do not modify the input.""",
         "de": f"""Gib nur die durch {k} teilbaren Werte zurück, in ursprünglicher Reihenfolge.

  keep({data}) -> {ref(data)}
  keep([]) -> []

Bau eine neue Liste; verändere die Eingabe nicht.""",
         "fr": f"""Renvoyez seulement les valeurs divisibles par {k}, dans leur ordre d'origine.

  keep({data}) -> {ref(data)}
  keep([]) -> []

Construisez une nouvelle liste ; ne modifiez pas l'entrée.""",
         "es": f"""Devuelve solo los valores divisibles por {k}, en su orden original.

  keep({data}) -> {ref(data)}
  keep([]) -> []

Construye una lista nueva; no modifiques la entrada."""},
        ref,
        [(data,), ([],), (rand_list(rng, 5, 1, 30),), (rand_list(rng, 12, 1, 90),),
         ([0, 0],), ([k, k * 2, k + 1],)],
        {
         "python": f"def keep(nums):\n    return [n for n in nums if n % {k} == 0]\n",
         "javascript": f"function keep(nums) {{\n  return nums.filter(n => n % {k} === 0);\n}}\n",
         "java": (f"import java.util.*;\n\nclass Solution {{\n"
                  f"    static long[] keep(long[] nums) {{\n"
                  f"        List<Long> out = new ArrayList<>();\n"
                  f"        for (long n : nums) if (n % {k} == 0) out.add(n);\n"
                  f"        long[] result = new long[out.size()];\n"
                  f"        for (int i = 0; i < out.size(); i++) result[i] = out.get(i);\n"
                  f"        return result;\n    }}\n}}\n"),
         "csharp": (f"using System.Linq;\n\npublic static class Solution\n{{\n"
                    f"    public static long[] keep(long[] nums)\n    {{\n"
                    f"        return nums.Where(n => n % {k} == 0).ToArray();\n"
                    f"    }}\n}}\n"),
         "go": (f"package main\n\nfunc keep(nums []int) []int {{\n\tout := []int{{}}\n"
                f"\tfor _, n := range nums {{\n\t\tif n%{k} == 0 {{\n"
                f"\t\t\tout = append(out, n)\n\t\t}}\n\t}}\n\treturn out\n}}\n"),
         "rust": (f"fn keep(nums: &[i64]) -> Vec<i64> {{\n"
                  f"    nums.iter().cloned().filter(|n| n % {k} == 0).collect()\n}}\n"),
         "cpp": (f"#include <vector>\n\n"
                 f"std::vector<long long> keep(const std::vector<long long>& nums) {{\n"
                 f"    std::vector<long long> out;\n"
                 f"    for (long long n : nums) if (n % {k} == 0) out.push_back(n);\n"
                 f"    return out;\n}}\n"),
        },
        {"en": [f"The test is n % {k} == 0",
                "Collect into a new container and return that"],
         "de": [f"Der Test lautet n % {k} == 0",
                "Sammle in einen neuen Behälter und gib den zurück"],
         "fr": [f"Le test est n % {k} == 0",
                "Rassemblez dans un nouveau conteneur et renvoyez-le"],
         "es": [f"La prueba es n % {k} == 0",
                "Recoge en un contenedor nuevo y devuélvelo"]})


@drill("times_table", "Basics")
def _times_table(rng):
    limit = rng.choice([5, 8, 10, 12])
    example = rng.randint(3, 12)

    def ref(n):
        return [n * i for i in range(1, limit + 1)]

    return _task(
        rng, "times_table", "Basics", "Easy", "table", Sig([("n", INT)], L(INT)),
        {"en": f"Times table up to {limit}", "de": f"Einmaleins bis {limit}",
         "fr": f"Table de multiplication jusqu'à {limit}",
         "es": f"Tabla de multiplicar hasta {limit}"},
        {"en": f"""Return the first {limit} multiples of n.

  table({example}) -> {ref(example)}
  table(0) -> {ref(0)}

Start at 1 * n and end at {limit} * n.""",
         "de": f"""Gib die ersten {limit} Vielfachen von n zurück.

  table({example}) -> {ref(example)}
  table(0) -> {ref(0)}

Fang bei 1 * n an und hör bei {limit} * n auf.""",
         "fr": f"""Renvoyez les {limit} premiers multiples de n.

  table({example}) -> {ref(example)}
  table(0) -> {ref(0)}

Commencez à 1 * n et terminez à {limit} * n.""",
         "es": f"""Devuelve los primeros {limit} múltiplos de n.

  table({example}) -> {ref(example)}
  table(0) -> {ref(0)}

Empieza en 1 * n y termina en {limit} * n."""},
        ref,
        [(example,), (0,), (1,), (-3,), (rng.randint(20, 60),), (7,)],
        {
         "python": f"def table(n):\n    return [n * i for i in range(1, {limit + 1})]\n",
         "javascript": (f"function table(n) {{\n  const out = [];\n"
                        f"  for (let i = 1; i <= {limit}; i++) out.push(n * i);\n"
                        f"  return out;\n}}\n"),
         "java": (f"class Solution {{\n    static long[] table(long n) {{\n"
                  f"        long[] out = new long[{limit}];\n"
                  f"        for (int i = 1; i <= {limit}; i++) out[i - 1] = n * i;\n"
                  f"        return out;\n    }}\n}}\n"),
         "csharp": (f"public static class Solution\n{{\n"
                    f"    public static long[] table(long n)\n    {{\n"
                    f"        var outArr = new long[{limit}];\n"
                    f"        for (int i = 1; i <= {limit}; i++) outArr[i - 1] = n * i;\n"
                    f"        return outArr;\n    }}\n}}\n"),
         "go": (f"package main\n\nfunc table(n int) []int {{\n"
                f"\tout := []int{{}}\n\tfor i := 1; i <= {limit}; i++ {{\n"
                f"\t\tout = append(out, n*i)\n\t}}\n\treturn out\n}}\n"),
         "rust": (f"fn table(n: i64) -> Vec<i64> {{\n"
                  f"    (1..={limit}).map(|i| n * i).collect()\n}}\n"),
         "cpp": (f"#include <vector>\n\nstd::vector<long long> table(long long n) {{\n"
                 f"    std::vector<long long> out;\n"
                 f"    for (long long i = 1; i <= {limit}; ++i) out.push_back(n * i);\n"
                 f"    return out;\n}}\n"),
        },
        {"en": [f"Loop i from 1 to {limit} inclusive",
                "Careful with the upper bound — it is inclusive here"],
         "de": [f"Lauf i von 1 bis {limit} einschließlich",
                "Achte auf die obere Grenze — sie gehört dazu"],
         "fr": [f"Faites varier i de 1 à {limit} inclus",
                "Attention à la borne haute — elle est incluse"],
         "es": [f"Recorre i de 1 a {limit} inclusive",
                "Cuidado con el límite superior — está incluido"]})


@drill("count_above", "Lists")
def _count_above(rng):
    threshold = rng.randint(5, 40)
    data = rand_list(rng, 9, -10, 60)

    def ref(nums):
        return sum(1 for n in nums if n > threshold)

    return _task(
        rng, "count_above", "Lists", "Easy", "count_above",
        Sig([("nums", L(INT))], INT),
        {"en": f"Count values above {threshold}",
         "de": f"Werte über {threshold} zählen",
         "fr": f"Compter les valeurs au-dessus de {threshold}",
         "es": f"Contar valores por encima de {threshold}"},
        {"en": f"""Count how many values are strictly greater than {threshold}.

  count_above({data}) -> {ref(data)}
  count_above([]) -> 0""",
         "de": f"""Zähl, wie viele Werte echt größer als {threshold} sind.

  count_above({data}) -> {ref(data)}
  count_above([]) -> 0""",
         "fr": f"""Comptez combien de valeurs sont strictement supérieures à {threshold}.

  count_above({data}) -> {ref(data)}
  count_above([]) -> 0""",
         "es": f"""Cuenta cuántos valores son estrictamente mayores que {threshold}.

  count_above({data}) -> {ref(data)}
  count_above([]) -> 0"""},
        ref,
        [(data,), ([],), ([threshold, threshold + 1],),
         (rand_list(rng, 6, 0, 50),), (rand_list(rng, 14, -20, 80),), ([0],)],
        {
         "python": (f"def count_above(nums):\n"
                    f"    return sum(1 for n in nums if n > {threshold})\n"),
         "javascript": (f"function count_above(nums) {{\n"
                        f"  return nums.filter(n => n > {threshold}).length;\n}}\n"),
         "java": (f"class Solution {{\n    static long count_above(long[] nums) {{\n"
                  f"        long total = 0;\n"
                  f"        for (long n : nums) if (n > {threshold}) total++;\n"
                  f"        return total;\n    }}\n}}\n"),
         "csharp": (f"using System.Linq;\n\npublic static class Solution\n{{\n"
                    f"    public static long count_above(long[] nums)\n    {{\n"
                    f"        return nums.Count(n => n > {threshold});\n    }}\n}}\n"),
         "go": (f"package main\n\nfunc count_above(nums []int) int {{\n\ttotal := 0\n"
                f"\tfor _, n := range nums {{\n\t\tif n > {threshold} {{\n"
                f"\t\t\ttotal++\n\t\t}}\n\t}}\n\treturn total\n}}\n"),
         "rust": (f"fn count_above(nums: &[i64]) -> i64 {{\n"
                  f"    nums.iter().filter(|n| **n > {threshold}).count() as i64\n}}\n"),
         "cpp": (f"#include <vector>\n\n"
                 f"long long count_above(const std::vector<long long>& nums) {{\n"
                 f"    long long total = 0;\n"
                 f"    for (long long n : nums) if (n > {threshold}) total++;\n"
                 f"    return total;\n}}\n"),
        },
        {"en": [f"Strictly greater: {threshold} itself does not count",
                "One counter, one pass"],
         "de": [f"Echt größer: {threshold} selbst zählt nicht",
                "Ein Zähler, ein Durchlauf"],
         "fr": [f"Strictement supérieur : {threshold} lui-même ne compte pas",
                "Un compteur, un seul passage"],
         "es": [f"Estrictamente mayor: {threshold} no cuenta",
                "Un contador, una pasada"]})


@drill("window_sum", "Two pointers", "Medium")
def _window_sum(rng):
    k = rng.randint(2, 4)
    data = rand_list(rng, rng.randint(7, 11), -8, 25)

    def ref(nums):
        if len(nums) < k:
            return 0
        window = sum(nums[:k])
        best = window
        for i in range(k, len(nums)):
            window += nums[i] - nums[i - k]
            best = max(best, window)
        return best

    return _task(
        rng, "window_sum", "Two pointers", "Medium", "best_window",
        Sig([("nums", L(INT))], INT),
        {"en": f"Best window of {k}", "de": f"Bestes Fenster der Größe {k}",
         "fr": f"Meilleure fenêtre de {k}", "es": f"Mejor ventana de {k}"},
        {"en": f"""Return the largest sum of {k} CONSECUTIVE values. Return 0 if the list is
shorter than {k}.

  best_window({data}) -> {ref(data)}

Slide the window: add the value entering and subtract the one leaving. Summing
each window from scratch is O(n*{k}).""",
         "de": f"""Gib die größte Summe von {k} AUFEINANDERFOLGENDEN Werten zurück. Gib 0 zurück,
wenn die Liste kürzer als {k} ist.

  best_window({data}) -> {ref(data)}

Schieb das Fenster: addier den eintretenden Wert und zieh den austretenden ab.
Jedes Fenster neu zu summieren ist O(n*{k}).""",
         "fr": f"""Renvoyez la plus grande somme de {k} valeurs CONSÉCUTIVES. Renvoyez 0 si la
liste est plus courte que {k}.

  best_window({data}) -> {ref(data)}

Faites glisser la fenêtre : ajoutez la valeur qui entre, retirez celle qui sort.
Resommer chaque fenêtre coûte O(n*{k}).""",
         "es": f"""Devuelve la mayor suma de {k} valores CONSECUTIVOS. Devuelve 0 si la lista es
más corta que {k}.

  best_window({data}) -> {ref(data)}

Desliza la ventana: suma el valor que entra y resta el que sale. Sumar cada
ventana de cero cuesta O(n*{k})."""},
        ref,
        [(data,), ([1],), (list(range(k)),), (rand_list(rng, 6, 1, 9),),
         ([-4] * (k + 2),), (rand_list(rng, 15, -30, 30),)],
        {
         "python": (f"def best_window(nums):\n    if len(nums) < {k}:\n        return 0\n"
                    f"    window = sum(nums[:{k}])\n    best = window\n"
                    f"    for i in range({k}, len(nums)):\n"
                    f"        window += nums[i] - nums[i - {k}]\n"
                    f"        best = max(best, window)\n    return best\n"),
         "javascript": (f"function best_window(nums) {{\n"
                        f"  if (nums.length < {k}) return 0;\n  let window = 0;\n"
                        f"  for (let i = 0; i < {k}; i++) window += nums[i];\n"
                        f"  let best = window;\n"
                        f"  for (let i = {k}; i < nums.length; i++) {{\n"
                        f"    window += nums[i] - nums[i - {k}];\n"
                        f"    best = Math.max(best, window);\n  }}\n  return best;\n}}\n"),
         "java": (f"class Solution {{\n    static long best_window(long[] nums) {{\n"
                  f"        if (nums.length < {k}) return 0;\n        long window = 0;\n"
                  f"        for (int i = 0; i < {k}; i++) window += nums[i];\n"
                  f"        long best = window;\n"
                  f"        for (int i = {k}; i < nums.length; i++) {{\n"
                  f"            window += nums[i] - nums[i - {k}];\n"
                  f"            best = Math.max(best, window);\n        }}\n"
                  f"        return best;\n    }}\n}}\n"),
         "csharp": (f"using System;\n\npublic static class Solution\n{{\n"
                    f"    public static long best_window(long[] nums)\n    {{\n"
                    f"        if (nums.Length < {k}) return 0;\n        long window = 0;\n"
                    f"        for (int i = 0; i < {k}; i++) window += nums[i];\n"
                    f"        long best = window;\n"
                    f"        for (int i = {k}; i < nums.Length; i++)\n        {{\n"
                    f"            window += nums[i] - nums[i - {k}];\n"
                    f"            best = Math.Max(best, window);\n        }}\n"
                    f"        return best;\n    }}\n}}\n"),
         "go": (f"package main\n\nfunc best_window(nums []int) int {{\n"
                f"\tif len(nums) < {k} {{\n\t\treturn 0\n\t}}\n\twindow := 0\n"
                f"\tfor i := 0; i < {k}; i++ {{\n\t\twindow += nums[i]\n\t}}\n"
                f"\tbest := window\n\tfor i := {k}; i < len(nums); i++ {{\n"
                f"\t\twindow += nums[i] - nums[i-{k}]\n\t\tif window > best {{\n"
                f"\t\t\tbest = window\n\t\t}}\n\t}}\n\treturn best\n}}\n"),
         "rust": (f"fn best_window(nums: &[i64]) -> i64 {{\n"
                  f"    if nums.len() < {k} {{ return 0; }}\n"
                  f"    let mut window: i64 = nums[..{k}].iter().sum();\n"
                  f"    let mut best = window;\n"
                  f"    for i in {k}..nums.len() {{\n"
                  f"        window += nums[i] - nums[i - {k}];\n"
                  f"        best = best.max(window);\n    }}\n    best\n}}\n"),
         "cpp": (f"#include <algorithm>\n#include <vector>\n\n"
                 f"long long best_window(const std::vector<long long>& nums) {{\n"
                 f"    if (nums.size() < {k}) return 0;\n    long long window = 0;\n"
                 f"    for (size_t i = 0; i < {k}; ++i) window += nums[i];\n"
                 f"    long long best = window;\n"
                 f"    for (size_t i = {k}; i < nums.size(); ++i) {{\n"
                 f"        window += nums[i] - nums[i - {k}];\n"
                 f"        best = std::max(best, window);\n    }}\n    return best;\n}}\n"),
        },
        {"en": [f"The first window is the sum of the first {k} values",
                f"Sliding: window += nums[i] - nums[i - {k}]",
                "Guard the too-short list before you start"],
         "de": [f"Das erste Fenster ist die Summe der ersten {k} Werte",
                f"Schieben: window += nums[i] - nums[i - {k}]",
                "Fang die zu kurze Liste vorher ab"],
         "fr": [f"La première fenêtre est la somme des {k} premières valeurs",
                f"Glissement : window += nums[i] - nums[i - {k}]",
                "Traitez la liste trop courte avant de commencer"],
         "es": [f"La primera ventana es la suma de los primeros {k} valores",
                f"Deslizamiento: window += nums[i] - nums[i - {k}]",
                "Controla la lista demasiado corta antes de empezar"]})


@drill("count_letter", "Strings")
def _count_letter(rng):
    letter = rng.choice("aeiostrn")
    words = ["banana", "mississippi", "interview", "raccoon", "silverware",
             "kernel", "tomorrow", "assessment"]
    sample = rng.choice(words)

    def ref(text):
        return text.lower().count(letter)

    return _task(
        rng, "count_letter", "Strings", "Easy", "count_it",
        Sig([("text", STR)], INT),
        {"en": f"Count the letter '{letter}'", "de": f"Den Buchstaben '{letter}' zählen",
         "fr": f"Compter la lettre « {letter} »",
         "es": f"Contar la letra «{letter}»"},
        {"en": f"""Count how many times the letter '{letter}' appears. Upper and lower case both
count.

  count_it("{sample}") -> {ref(sample)}
  count_it("") -> 0""",
         "de": f"""Zähl, wie oft der Buchstabe '{letter}' vorkommt. Groß- und Kleinschreibung
zählen beide.

  count_it("{sample}") -> {ref(sample)}
  count_it("") -> 0""",
         "fr": f"""Comptez combien de fois la lettre « {letter} » apparaît. Majuscules et
minuscules comptent toutes les deux.

  count_it("{sample}") -> {ref(sample)}
  count_it("") -> 0""",
         "es": f"""Cuenta cuántas veces aparece la letra «{letter}». Mayúsculas y minúsculas
cuentan igual.

  count_it("{sample}") -> {ref(sample)}
  count_it("") -> 0"""},
        ref,
        [(sample,), ("",), (letter * 4,), (rng.choice(words),),
         (rng.choice(words).upper(),), ("XYZ",)],
        {
         "python": (f"def count_it(text):\n    return text.lower().count('{letter}')\n"),
         "javascript": (f"function count_it(text) {{\n"
                        f"  return (text.match(/{letter}/gi) || []).length;\n}}\n"),
         "java": (f"class Solution {{\n    static long count_it(String text) {{\n"
                  f"        long total = 0;\n"
                  f"        for (char c : text.toLowerCase().toCharArray())\n"
                  f"            if (c == '{letter}') total++;\n"
                  f"        return total;\n    }}\n}}\n"),
         "csharp": (f"public static class Solution\n{{\n"
                    f"    public static long count_it(string text)\n    {{\n"
                    f"        long total = 0;\n"
                    f"        foreach (var c in text.ToLowerInvariant())\n"
                    f"            if (c == '{letter}') total++;\n"
                    f"        return total;\n    }}\n}}\n"),
         "go": (f"package main\n\nimport \"strings\"\n\n"
                f"func count_it(text string) int {{\n"
                f"\treturn strings.Count(strings.ToLower(text), \"{letter}\")\n}}\n"),
         "rust": (f"fn count_it(text: &str) -> i64 {{\n"
                  f"    text.to_lowercase().matches('{letter}').count() as i64\n}}\n"),
         "cpp": (f"#include <cctype>\n#include <string>\n\n"
                 f"long long count_it(const std::string& text) {{\n"
                 f"    long long total = 0;\n    for (char c : text)\n"
                 f"        if (std::tolower(static_cast<unsigned char>(c)) == '{letter}')\n"
                 f"            total++;\n    return total;\n}}\n"),
        },
        {"en": ["Lower-case the text first so both cases match",
                "Then it is a single count over the characters"],
         "de": ["Mach den Text erst klein, damit beide Schreibweisen passen",
                "Dann ist es ein einfaches Zählen über die Zeichen"],
         "fr": ["Mettez d'abord le texte en minuscules pour couvrir les deux casses",
                "Ensuite c'est un simple comptage sur les caractères"],
         "es": ["Pasa primero el texto a minúsculas para cubrir ambos casos",
                "Después es un simple conteo sobre los caracteres"]})


@drill("nth_smallest", "Sorting", "Medium")
def _nth_smallest(rng):
    k = rng.randint(1, 3)
    data = rand_list(rng, rng.randint(6, 10), 1, 50)

    def ref(nums):
        distinct = sorted(set(nums))
        return distinct[k - 1] if len(distinct) >= k else -1

    return _task(
        rng, "nth_smallest", "Sorting", "Medium", "nth_smallest",
        Sig([("nums", L(INT))], INT),
        {"en": f"{k}. smallest distinct value", "de": f"{k}.-kleinster verschiedener Wert",
         "fr": f"{k}e plus petite valeur distincte",
         "es": f"{k}.º valor distinto más pequeño"},
        {"en": f"""Return the {k}. smallest DISTINCT value. Return -1 if there are fewer than
{k} distinct values.

  nth_smallest({data}) -> {ref(data)}
  nth_smallest([]) -> -1

Remove the duplicates first, then sort.""",
         "de": f"""Gib den {k}.-kleinsten VERSCHIEDENEN Wert zurück. Gib -1 zurück, wenn es
weniger als {k} verschiedene Werte gibt.

  nth_smallest({data}) -> {ref(data)}
  nth_smallest([]) -> -1

Entferne zuerst die Duplikate, dann sortiere.""",
         "fr": f"""Renvoyez la {k}e plus petite valeur DISTINCTE. Renvoyez -1 s'il y a moins de
{k} valeurs distinctes.

  nth_smallest({data}) -> {ref(data)}
  nth_smallest([]) -> -1

Supprimez d'abord les doublons, puis triez.""",
         "es": f"""Devuelve el {k}.º valor DISTINTO más pequeño. Devuelve -1 si hay menos de
{k} valores distintos.

  nth_smallest({data}) -> {ref(data)}
  nth_smallest([]) -> -1

Elimina primero los duplicados y luego ordena."""},
        ref,
        [(data,), ([],), ([5, 5, 5],), (rand_list(rng, 5, 1, 10),),
         (list(range(k)),), (rand_list(rng, 12, 1, 8),)],
        {
         "python": (f"def nth_smallest(nums):\n    distinct = sorted(set(nums))\n"
                    f"    return distinct[{k - 1}] if len(distinct) >= {k} else -1\n"),
         "javascript": (f"function nth_smallest(nums) {{\n"
                        f"  const d = [...new Set(nums)].sort((a, b) => a - b);\n"
                        f"  return d.length >= {k} ? d[{k - 1}] : -1;\n}}\n"),
         "java": (f"import java.util.TreeSet;\n\nclass Solution {{\n"
                  f"    static long nth_smallest(long[] nums) {{\n"
                  f"        TreeSet<Long> d = new TreeSet<>();\n"
                  f"        for (long n : nums) d.add(n);\n"
                  f"        if (d.size() < {k}) return -1;\n"
                  f"        int i = 0;\n        for (long v : d) {{\n"
                  f"            if (i == {k - 1}) return v;\n            i++;\n        }}\n"
                  f"        return -1;\n    }}\n}}\n"),
         "csharp": (f"using System.Linq;\n\npublic static class Solution\n{{\n"
                    f"    public static long nth_smallest(long[] nums)\n    {{\n"
                    f"        var d = nums.Distinct().OrderBy(n => n).ToArray();\n"
                    f"        return d.Length >= {k} ? d[{k - 1}] : -1;\n    }}\n}}\n"),
         "go": (f"package main\n\nimport \"sort\"\n\n"
                f"func nth_smallest(nums []int) int {{\n\tseen := map[int]bool{{}}\n"
                f"\td := []int{{}}\n\tfor _, n := range nums {{\n"
                f"\t\tif !seen[n] {{\n\t\t\tseen[n] = true\n\t\t\td = append(d, n)\n"
                f"\t\t}}\n\t}}\n\tif len(d) < {k} {{\n\t\treturn -1\n\t}}\n"
                f"\tsort.Ints(d)\n\treturn d[{k - 1}]\n}}\n"),
         "rust": (f"fn nth_smallest(nums: &[i64]) -> i64 {{\n"
                  f"    let mut d = nums.to_vec();\n    d.sort();\n    d.dedup();\n"
                  f"    if d.len() < {k} {{ return -1; }}\n    d[{k - 1}]\n}}\n"),
         "cpp": (f"#include <set>\n#include <vector>\n\n"
                 f"long long nth_smallest(const std::vector<long long>& nums) {{\n"
                 f"    std::set<long long> d(nums.begin(), nums.end());\n"
                 f"    if (d.size() < {k}) return -1;\n"
                 f"    auto it = d.begin();\n    std::advance(it, {k - 1});\n"
                 f"    return *it;\n}}\n"),
        },
        {"en": ["A set removes the duplicates",
                f"After sorting, the answer is at index {k - 1}",
                "Check the size before you index"],
         "de": ["Ein Set entfernt die Duplikate",
                f"Nach dem Sortieren steht die Antwort an Index {k - 1}",
                "Prüf die Größe, bevor du indizierst"],
         "fr": ["Un ensemble supprime les doublons",
                f"Après le tri, la réponse est à l'indice {k - 1}",
                "Vérifiez la taille avant d'indexer"],
         "es": ["Un conjunto elimina los duplicados",
                f"Tras ordenar, la respuesta está en el índice {k - 1}",
                "Comprueba el tamaño antes de indexar"]})


TOPICS: list[str] = sorted({d.topic for d in REGISTRY})


def generate(topic: str | None = None, difficulty: str | None = None,
             rng: random.Random | None = None) -> Task:
    rng = rng or random.Random()
    pool = REGISTRY
    if topic and topic != "All topics":
        pool = [d for d in pool if d.topic == topic] or REGISTRY
    if difficulty and difficulty != "Any":
        pool = [d for d in pool if d.difficulty == difficulty] or pool
    return rng.choice(pool).build(rng)
