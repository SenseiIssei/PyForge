"""Interview problems that work in every supported language.

One statement, one set of test cases, one type signature — the starter code and
the test harness are generated per language, and a reference solution is stored
for each. Adding a language to a problem means writing one function; adding a
problem means writing the statement once and the solution seven times.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field

import i18n
import languages as LG
from languages import BOOL, FLOAT, INT, L, STR, Sig
from tasks import Task, case

BANK: list["MultiProblem"] = []


@dataclass
class MultiProblem:
    id: str
    func: str
    difficulty: str
    topic: str
    sig: Sig
    title: dict[str, str]
    statement: dict[str, str]
    cases: list[dict]
    solutions: dict[str, str]
    hints: dict[str, list[str]] = field(default_factory=dict)
    notes: dict[str, str] = field(default_factory=dict)
    complexity: str = ""

    # ------------------------------------------------------------ helpers
    def _pick(self, table: dict, fallback=""):
        return table.get(i18n.LANG) or table.get("en") or fallback

    @property
    def display_title(self) -> str:
        return self._pick(self.title, self.id)

    def supports(self, language_id: str) -> bool:
        return language_id in self.solutions

    def build(self, language_id: str | None = None,
              rng: random.Random | None = None) -> Task:
        language_id = language_id or LG.CURRENT
        backend = LG.get(language_id)
        return Task(
            id=self.id,
            title=self.display_title,
            func=self.func,
            statement=self._pick(self.statement).strip(),
            starter=backend.starter(self.func, self.sig),
            cases=list(self.cases),
            hints=list(self._pick(self.hints, []) or []),
            solution=self.solutions.get(language_id, ""),
            difficulty=self.difficulty,
            topic=self.topic,
            complexity=i18n.complexity(self.complexity),
            source="interview",
            notes=self._pick(self.notes),
            sig=self.sig,
            language=language_id,
        )


def P(pid, func, difficulty, topic, sig, title, statement, cases, solutions,
      hints=None, notes=None, complexity="") -> MultiProblem:
    problem = MultiProblem(
        id=pid, func=func, difficulty=difficulty, topic=topic, sig=sig,
        title=title, statement=statement, cases=cases, solutions=solutions,
        hints=hints or {}, notes=notes or {}, complexity=complexity)
    BANK.append(problem)
    return problem


# ===========================================================================
P("m_sum_range", "sum_range", "Easy", "Basics",
  Sig([("nums", L(INT))], INT),
  {"en": "Sum a list", "de": "Eine Liste summieren"},
  {"en": """Return the sum of every number in the list. An empty list sums to 0.

  sum_range([1, 2, 3]) -> 6
  sum_range([])        -> 0

This one exists so you can get a feel for the editor and the test runner in a
new language before the real problems start.""",
   "de": """Gib die Summe aller Zahlen der Liste zurück. Eine leere Liste ergibt 0.

  sum_range([1, 2, 3]) -> 6
  sum_range([])        -> 0

Diese Aufgabe gibt es, damit du dich in einer neuen Sprache erst mal an den
Editor und den Testlauf gewöhnen kannst, bevor es richtig losgeht."""},
  [case([1, 2, 3], 6), case([], 0), case([-5, 5], 0),
   case([7], 7, hidden=True), case(list(range(1, 101)), 5050, hidden=True)],
  {
   "python": "def sum_range(nums):\n    return sum(nums)\n",
   "javascript": "function sum_range(nums) {\n  return nums.reduce((a, b) => a + b, 0);\n}\n",
   "java": ("class Solution {\n    static long sum_range(long[] nums) {\n"
            "        long total = 0;\n        for (long n : nums) total += n;\n"
            "        return total;\n    }\n}\n"),
   "csharp": ("public static class Solution\n{\n    public static long sum_range(long[] nums)\n"
              "    {\n        long total = 0;\n        foreach (var n in nums) total += n;\n"
              "        return total;\n    }\n}\n"),
   "go": ("package main\n\nfunc sum_range(nums []int) int {\n\ttotal := 0\n"
          "\tfor _, n := range nums {\n\t\ttotal += n\n\t}\n\treturn total\n}\n"),
   "rust": "fn sum_range(nums: &[i64]) -> i64 {\n    nums.iter().sum()\n}\n",
   "cpp": ("#include <vector>\n\nlong long sum_range(const std::vector<long long>& nums) {\n"
           "    long long total = 0;\n    for (long long n : nums) total += n;\n"
           "    return total;\n}\n"),
  },
  {"en": ["Start an accumulator at 0 and add each element",
          "Most languages have a built-in for this — try both ways"],
   "de": ["Fang mit einem Zähler bei 0 an und addiere jedes Element",
          "Die meisten Sprachen haben dafür etwas Eingebautes — probier beides"]},
  complexity="O(n)")

# ---------------------------------------------------------------------------
P("m_contains_duplicate", "contains_duplicate", "Easy", "Sets",
  Sig([("nums", L(INT))], BOOL),
  {"en": "Contains Duplicate", "de": "Enthält Duplikate"},
  {"en": """Return true if any value appears at least twice, false if every value is
distinct.

  contains_duplicate([1, 2, 3, 1]) -> true
  contains_duplicate([1, 2, 3, 4]) -> false

The hidden tests include a large array, so a nested loop over every pair will be
too slow. Use a set (or sort first).""",
   "de": """Gib true zurück, wenn irgendein Wert mindestens zweimal vorkommt, sonst false.

  contains_duplicate([1, 2, 3, 1]) -> true
  contains_duplicate([1, 2, 3, 4]) -> false

Unter den versteckten Tests ist ein großes Array, eine verschachtelte Schleife
über alle Paare ist also zu langsam. Nimm ein Set (oder sortier zuerst)."""},
  [case([1, 2, 3, 1], True), case([1, 2, 3, 4], False), case([], False),
   case([7, 7], True, hidden=True),
   case(list(range(2000)), False, hidden=True, label="2000 distinct values"),
   case(list(range(2000)) + [42], True, hidden=True, label="2000 + one duplicate")],
  {
   "python": "def contains_duplicate(nums):\n    return len(set(nums)) != len(nums)\n",
   "javascript": ("function contains_duplicate(nums) {\n"
                  "  return new Set(nums).size !== nums.length;\n}\n"),
   "java": ("import java.util.HashSet;\nimport java.util.Set;\n\nclass Solution {\n"
            "    static boolean contains_duplicate(long[] nums) {\n"
            "        Set<Long> seen = new HashSet<>();\n"
            "        for (long n : nums) if (!seen.add(n)) return true;\n"
            "        return false;\n    }\n}\n"),
   "csharp": ("public static class Solution\n{\n"
              "    public static bool contains_duplicate(long[] nums)\n    {\n"
              "        var seen = new HashSet<long>();\n"
              "        foreach (var n in nums) if (!seen.Add(n)) return true;\n"
              "        return false;\n    }\n}\n"),
   "go": ("package main\n\nfunc contains_duplicate(nums []int) bool {\n"
          "\tseen := make(map[int]bool, len(nums))\n\tfor _, n := range nums {\n"
          "\t\tif seen[n] {\n\t\t\treturn true\n\t\t}\n\t\tseen[n] = true\n\t}\n"
          "\treturn false\n}\n"),
   "rust": ("use std::collections::HashSet;\n\nfn contains_duplicate(nums: &[i64]) -> bool {\n"
            "    let mut seen = HashSet::new();\n"
            "    for n in nums {\n        if !seen.insert(n) {\n            return true;\n"
            "        }\n    }\n    false\n}\n"),
   "cpp": ("#include <unordered_set>\n#include <vector>\n\n"
           "bool contains_duplicate(const std::vector<long long>& nums) {\n"
           "    std::unordered_set<long long> seen;\n"
           "    for (long long n : nums) {\n        if (!seen.insert(n).second) return true;\n"
           "    }\n    return false;\n}\n"),
  },
  {"en": ["Membership in a hash set is O(1); in a list it is O(n)",
          "Return as soon as you see a value for the second time",
          "Comparing the size of the set with the length works too"],
   "de": ["Enthaltensein ist bei einem Hash-Set O(1), bei einer Liste O(n)",
          "Gib zurück, sobald du einen Wert zum zweiten Mal siehst",
          "Die Größe des Sets mit der Länge zu vergleichen geht auch"]},
  {"en": "LeetCode 217. The first question where the naive answer times out.",
   "de": "LeetCode 217. Die erste Frage, bei der die naive Lösung ins Zeitlimit läuft."},
  complexity="O(n)")

# ---------------------------------------------------------------------------
P("m_max_subarray", "max_subarray", "Medium", "Dynamic programming",
  Sig([("nums", L(INT))], INT),
  {"en": "Maximum Subarray (Kadane)", "de": "Größte Teilarraysumme (Kadane)"},
  {"en": """Return the largest sum of any contiguous, non-empty run of numbers.

  max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]) -> 6      (the run 4, -1, 2, 1)
  max_subarray([-1])                            -> -1

Careful: the array can be entirely negative, so starting your best value at 0 is
wrong. This is Kadane's algorithm — one pass, O(n).""",
   "de": """Gib die größte Summe eines zusammenhängenden, nicht leeren Abschnitts zurück.

  max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]) -> 6      (der Abschnitt 4, -1, 2, 1)
  max_subarray([-1])                            -> -1

Achtung: Das Array kann komplett negativ sein — mit 0 als Startwert liegst du
also falsch. Das ist Kadanes Algorithmus: ein Durchlauf, O(n)."""},
  [case([-2, 1, -3, 4, -1, 2, 1, -5, 4], 6), case([-1], -1), case([5, 4, -1, 7, 8], 23),
   case([1], 1, hidden=True), case([-3, -1, -2], -1, hidden=True),
   case([2, -1, 2, -1, 2], 4, hidden=True)],
  {
   "python": ("def max_subarray(nums):\n    best = current = nums[0]\n"
              "    for value in nums[1:]:\n        current = max(value, current + value)\n"
              "        best = max(best, current)\n    return best\n"),
   "javascript": ("function max_subarray(nums) {\n  let best = nums[0], current = nums[0];\n"
                  "  for (let i = 1; i < nums.length; i++) {\n"
                  "    current = Math.max(nums[i], current + nums[i]);\n"
                  "    best = Math.max(best, current);\n  }\n  return best;\n}\n"),
   "java": ("class Solution {\n    static long max_subarray(long[] nums) {\n"
            "        long best = nums[0], current = nums[0];\n"
            "        for (int i = 1; i < nums.length; i++) {\n"
            "            current = Math.max(nums[i], current + nums[i]);\n"
            "            best = Math.max(best, current);\n        }\n        return best;\n"
            "    }\n}\n"),
   "csharp": ("public static class Solution\n{\n    public static long max_subarray(long[] nums)\n"
              "    {\n        long best = nums[0], current = nums[0];\n"
              "        for (int i = 1; i < nums.Length; i++)\n        {\n"
              "            current = Math.Max(nums[i], current + nums[i]);\n"
              "            best = Math.Max(best, current);\n        }\n        return best;\n"
              "    }\n}\n"),
   "go": ("package main\n\nfunc max_subarray(nums []int) int {\n"
          "\tbest, current := nums[0], nums[0]\n\tfor _, v := range nums[1:] {\n"
          "\t\tif v > current+v {\n\t\t\tcurrent = v\n\t\t} else {\n\t\t\tcurrent += v\n\t\t}\n"
          "\t\tif current > best {\n\t\t\tbest = current\n\t\t}\n\t}\n\treturn best\n}\n"),
   "rust": ("fn max_subarray(nums: &[i64]) -> i64 {\n    let mut best = nums[0];\n"
            "    let mut current = nums[0];\n    for &v in &nums[1..] {\n"
            "        current = v.max(current + v);\n        best = best.max(current);\n"
            "    }\n    best\n}\n"),
   "cpp": ("#include <algorithm>\n#include <vector>\n\n"
           "long long max_subarray(const std::vector<long long>& nums) {\n"
           "    long long best = nums[0], current = nums[0];\n"
           "    for (size_t i = 1; i < nums.size(); ++i) {\n"
           "        current = std::max(nums[i], current + nums[i]);\n"
           "        best = std::max(best, current);\n    }\n    return best;\n}\n"),
  },
  {"en": ["At each element decide: extend the current run, or start a new one here",
          "current = max(value, current + value)",
          "Initialise both best and current from the first element, not from 0"],
   "de": ["Entscheide bei jedem Element: den Abschnitt verlängern oder hier neu anfangen",
          "aktuell = max(wert, aktuell + wert)",
          "Initialisiere best und aktuell mit dem ersten Element, nicht mit 0"]},
  {"en": "LeetCode 53 and Codility's MaxSliceSum. Two lines you should know cold.",
   "de": "LeetCode 53 und Codilitys MaxSliceSum. Zwei Zeilen, die sitzen müssen."},
  complexity="O(n)")

# ---------------------------------------------------------------------------
P("m_two_sum", "two_sum", "Easy", "Hash map",
  Sig([("nums", L(INT)), ("target", INT)], L(INT)),
  {"en": "Two Sum", "de": "Zwei Summanden"},
  {"en": """Return the indices of the two numbers that add up to target, as a list
[i, j] with i < j. Exactly one solution exists and you may not use the same
element twice.

  two_sum([2, 7, 11, 15], 9) -> [0, 1]
  two_sum([3, 3], 6)         -> [0, 1]

The nested double loop is O(n^2). Do it in one pass with a map from value to
index — that is the answer the interviewer wants.""",
   "de": """Gib die Indizes der beiden Zahlen zurück, die zusammen target ergeben, als
Liste [i, j] mit i < j. Es gibt genau eine Lösung, und du darfst dasselbe
Element nicht zweimal verwenden.

  two_sum([2, 7, 11, 15], 9) -> [0, 1]
  two_sum([3, 3], 6)         -> [0, 1]

Die doppelte Schleife ist O(n^2). Mach es in einem Durchlauf mit einer Map von
Wert auf Index — das ist die Antwort, die im Interview erwartet wird."""},
  [case(([2, 7, 11, 15], 9), [0, 1]), case(([3, 3], 6), [0, 1]),
   case(([3, 2, 4], 6), [1, 2]),
   case(([-1, -2, -3, -4], -5), [1, 2], hidden=True),
   case(([0, 4, 3, 0], 0), [0, 3], hidden=True)],
  {
   "python": ("def two_sum(nums, target):\n    seen = {}\n"
              "    for i, value in enumerate(nums):\n"
              "        if target - value in seen:\n            return [seen[target - value], i]\n"
              "        seen[value] = i\n    return []\n"),
   "javascript": ("function two_sum(nums, target) {\n  const seen = new Map();\n"
                  "  for (let i = 0; i < nums.length; i++) {\n"
                  "    if (seen.has(target - nums[i])) return [seen.get(target - nums[i]), i];\n"
                  "    seen.set(nums[i], i);\n  }\n  return [];\n}\n"),
   "java": ("import java.util.HashMap;\nimport java.util.Map;\n\nclass Solution {\n"
            "    static long[] two_sum(long[] nums, long target) {\n"
            "        Map<Long, Integer> seen = new HashMap<>();\n"
            "        for (int i = 0; i < nums.length; i++) {\n"
            "            Integer j = seen.get(target - nums[i]);\n"
            "            if (j != null) return new long[]{j, i};\n"
            "            seen.put(nums[i], i);\n        }\n        return new long[]{};\n"
            "    }\n}\n"),
   "csharp": ("public static class Solution\n{\n"
              "    public static long[] two_sum(long[] nums, long target)\n    {\n"
              "        var seen = new Dictionary<long, int>();\n"
              "        for (int i = 0; i < nums.Length; i++)\n        {\n"
              "            if (seen.TryGetValue(target - nums[i], out int j))\n"
              "                return new long[]{j, i};\n"
              "            seen[nums[i]] = i;\n        }\n        return new long[]{};\n"
              "    }\n}\n"),
   "go": ("package main\n\nfunc two_sum(nums []int, target int) []int {\n"
          "\tseen := map[int]int{}\n\tfor i, v := range nums {\n"
          "\t\tif j, ok := seen[target-v]; ok {\n\t\t\treturn []int{j, i}\n\t\t}\n"
          "\t\tseen[v] = i\n\t}\n\treturn []int{}\n}\n"),
   "rust": ("use std::collections::HashMap;\n\nfn two_sum(nums: &[i64], target: i64) -> Vec<i64> {\n"
            "    let mut seen: HashMap<i64, usize> = HashMap::new();\n"
            "    for (i, &v) in nums.iter().enumerate() {\n"
            "        if let Some(&j) = seen.get(&(target - v)) {\n"
            "            return vec![j as i64, i as i64];\n        }\n"
            "        seen.insert(v, i);\n    }\n    Vec::new()\n}\n"),
   "cpp": ("#include <unordered_map>\n#include <vector>\n\n"
           "std::vector<long long> two_sum(const std::vector<long long>& nums, long long target) {\n"
           "    std::unordered_map<long long, long long> seen;\n"
           "    for (long long i = 0; i < (long long)nums.size(); ++i) {\n"
           "        auto it = seen.find(target - nums[i]);\n"
           "        if (it != seen.end()) return {it->second, i};\n"
           "        seen[nums[i]] = i;\n    }\n    return {};\n}\n"),
  },
  {"en": ["Store value -> index as you walk the array",
          "For each value ask whether target - value was already seen",
          "Insert AFTER the lookup, so an element cannot pair with itself"],
   "de": ["Speicher Wert -> Index, während du durch das Array läufst",
          "Frag für jeden Wert, ob target - Wert schon gesehen wurde",
          "Trag NACH der Abfrage ein, damit sich ein Element nicht mit sich selbst paart"]},
  {"en": "LeetCode 1 — the most asked interview question there is.",
   "de": "LeetCode 1 — die meistgestellte Interviewfrage überhaupt."},
  complexity="O(n)")

# ---------------------------------------------------------------------------
P("m_valid_palindrome", "is_palindrome", "Easy", "Two pointers",
  Sig([("text", STR)], BOOL),
  {"en": "Valid Palindrome", "de": "Gültiges Palindrom"},
  {"en": """Ignoring case and every character that is not a letter or a digit, does the
text read the same forwards and backwards?

  is_palindrome("A man, a plan, a canal: Panama") -> true
  is_palindrome("race a car")                     -> false
  is_palindrome(" ")                              -> true

The empty string counts as a palindrome.""",
   "de": """Liest sich der Text vorwärts und rückwärts gleich, wenn man Groß- und
Kleinschreibung sowie alle Zeichen ignoriert, die weder Buchstabe noch Ziffer
sind?

  is_palindrome("A man, a plan, a canal: Panama") -> true
  is_palindrome("race a car")                     -> false
  is_palindrome(" ")                              -> true

Der leere String gilt als Palindrom."""},
  [case("A man, a plan, a canal: Panama", True), case("race a car", False),
   case(" ", True), case("", True, hidden=True), case("0P", False, hidden=True),
   case("Was it a car or a cat I saw?", True, hidden=True)],
  {
   "python": ("def is_palindrome(text):\n"
              "    cleaned = [c.lower() for c in text if c.isalnum()]\n"
              "    return cleaned == cleaned[::-1]\n"),
   "javascript": ("function is_palindrome(text) {\n"
                  "  const cleaned = text.toLowerCase().replace(/[^a-z0-9]/g, \"\");\n"
                  "  return cleaned === [...cleaned].reverse().join(\"\");\n}\n"),
   "java": ("class Solution {\n    static boolean is_palindrome(String text) {\n"
            "        int i = 0, j = text.length() - 1;\n        while (i < j) {\n"
            "            while (i < j && !Character.isLetterOrDigit(text.charAt(i))) i++;\n"
            "            while (i < j && !Character.isLetterOrDigit(text.charAt(j))) j--;\n"
            "            if (Character.toLowerCase(text.charAt(i))\n"
            "                != Character.toLowerCase(text.charAt(j))) return false;\n"
            "            i++; j--;\n        }\n        return true;\n    }\n}\n"),
   "csharp": ("public static class Solution\n{\n"
              "    public static bool is_palindrome(string text)\n    {\n"
              "        int i = 0, j = text.Length - 1;\n        while (i < j)\n        {\n"
              "            while (i < j && !char.IsLetterOrDigit(text[i])) i++;\n"
              "            while (i < j && !char.IsLetterOrDigit(text[j])) j--;\n"
              "            if (char.ToLowerInvariant(text[i]) != char.ToLowerInvariant(text[j]))\n"
              "                return false;\n            i++; j--;\n        }\n"
              "        return true;\n    }\n}\n"),
   "go": ("package main\n\nimport \"unicode\"\n\nfunc is_palindrome(text string) bool {\n"
          "\tvar cleaned []rune\n\tfor _, r := range text {\n"
          "\t\tif unicode.IsLetter(r) || unicode.IsDigit(r) {\n"
          "\t\t\tcleaned = append(cleaned, unicode.ToLower(r))\n\t\t}\n\t}\n"
          "\tfor i, j := 0, len(cleaned)-1; i < j; i, j = i+1, j-1 {\n"
          "\t\tif cleaned[i] != cleaned[j] {\n\t\t\treturn false\n\t\t}\n\t}\n"
          "\treturn true\n}\n"),
   "rust": ("fn is_palindrome(text: &str) -> bool {\n"
            "    let cleaned: Vec<char> = text.chars()\n"
            "        .filter(|c| c.is_alphanumeric())\n"
            "        .map(|c| c.to_ascii_lowercase())\n        .collect();\n"
            "    let reversed: Vec<char> = cleaned.iter().rev().cloned().collect();\n"
            "    cleaned == reversed\n}\n"),
   "cpp": ("#include <cctype>\n#include <string>\n\n"
           "bool is_palindrome(const std::string& text) {\n"
           "    int i = 0, j = (int)text.size() - 1;\n    while (i < j) {\n"
           "        while (i < j && !std::isalnum((unsigned char)text[i])) i++;\n"
           "        while (i < j && !std::isalnum((unsigned char)text[j])) j--;\n"
           "        if (std::tolower((unsigned char)text[i])\n"
           "            != std::tolower((unsigned char)text[j])) return false;\n"
           "        i++; j--;\n    }\n    return true;\n}\n"),
  },
  {"en": ["Either clean the string first, or walk two pointers inward and skip junk",
          "Compare lower-cased characters",
          "The two-pointer version needs no extra memory"],
   "de": ["Entweder den String erst säubern, oder mit zwei Zeigern nach innen laufen",
          "Vergleiche kleingeschriebene Zeichen",
          "Die Zwei-Zeiger-Variante braucht keinen Zusatzspeicher"]},
  {"en": "LeetCode 125.", "de": "LeetCode 125."},
  complexity="O(n)")

# ---------------------------------------------------------------------------
P("m_fizzbuzz", "fizzbuzz", "Easy", "Basics",
  Sig([("n", INT)], L(STR)),
  {"en": "FizzBuzz", "de": "FizzBuzz"},
  {"en": """Return a list of strings for the numbers 1..n:

  * multiples of 3 and 5 -> "FizzBuzz"
  * multiples of 3       -> "Fizz"
  * multiples of 5       -> "Buzz"
  * everything else      -> the number itself, as text

  fizzbuzz(5) -> ["1", "2", "Fizz", "4", "Buzz"]
  fizzbuzz(0) -> []

Check the 15 case first, or it can never happen.""",
   "de": """Gib eine Liste von Strings für die Zahlen 1..n zurück:

  * Vielfache von 3 und 5 -> "FizzBuzz"
  * Vielfache von 3       -> "Fizz"
  * Vielfache von 5       -> "Buzz"
  * alles andere          -> die Zahl selbst, als Text

  fizzbuzz(5) -> ["1", "2", "Fizz", "4", "Buzz"]
  fizzbuzz(0) -> []

Prüf den 15er-Fall zuerst, sonst kann er nie eintreten."""},
  [case(5, ["1", "2", "Fizz", "4", "Buzz"]), case(0, []),
   case(15, ["1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8", "Fizz", "Buzz",
             "11", "Fizz", "13", "14", "FizzBuzz"]),
   case(1, ["1"], hidden=True),
   case(3, ["1", "2", "Fizz"], hidden=True)],
  {
   "python": ("def fizzbuzz(n):\n    out = []\n    for i in range(1, n + 1):\n"
              "        if i % 15 == 0:\n            out.append('FizzBuzz')\n"
              "        elif i % 3 == 0:\n            out.append('Fizz')\n"
              "        elif i % 5 == 0:\n            out.append('Buzz')\n"
              "        else:\n            out.append(str(i))\n    return out\n"),
   "javascript": ("function fizzbuzz(n) {\n  const out = [];\n"
                  "  for (let i = 1; i <= n; i++) {\n"
                  "    if (i % 15 === 0) out.push('FizzBuzz');\n"
                  "    else if (i % 3 === 0) out.push('Fizz');\n"
                  "    else if (i % 5 === 0) out.push('Buzz');\n"
                  "    else out.push(String(i));\n  }\n  return out;\n}\n"),
   "java": ("class Solution {\n    static String[] fizzbuzz(long n) {\n"
            "        String[] out = new String[(int) Math.max(0, n)];\n"
            "        for (int i = 1; i <= n; i++) {\n"
            "            if (i % 15 == 0) out[i - 1] = \"FizzBuzz\";\n"
            "            else if (i % 3 == 0) out[i - 1] = \"Fizz\";\n"
            "            else if (i % 5 == 0) out[i - 1] = \"Buzz\";\n"
            "            else out[i - 1] = String.valueOf(i);\n        }\n"
            "        return out;\n    }\n}\n"),
   "csharp": ("public static class Solution\n{\n    public static string[] fizzbuzz(long n)\n"
              "    {\n        var out_ = new string[(int)Math.Max(0, n)];\n"
              "        for (int i = 1; i <= n; i++)\n        {\n"
              "            if (i % 15 == 0) out_[i - 1] = \"FizzBuzz\";\n"
              "            else if (i % 3 == 0) out_[i - 1] = \"Fizz\";\n"
              "            else if (i % 5 == 0) out_[i - 1] = \"Buzz\";\n"
              "            else out_[i - 1] = i.ToString();\n        }\n"
              "        return out_;\n    }\n}\n"),
   "go": ("package main\n\nimport \"strconv\"\n\nfunc fizzbuzz(n int) []string {\n"
          "\tout := []string{}\n\tfor i := 1; i <= n; i++ {\n"
          "\t\tswitch {\n\t\tcase i%15 == 0:\n\t\t\tout = append(out, \"FizzBuzz\")\n"
          "\t\tcase i%3 == 0:\n\t\t\tout = append(out, \"Fizz\")\n"
          "\t\tcase i%5 == 0:\n\t\t\tout = append(out, \"Buzz\")\n"
          "\t\tdefault:\n\t\t\tout = append(out, strconv.Itoa(i))\n\t\t}\n\t}\n"
          "\treturn out\n}\n"),
   "rust": ("fn fizzbuzz(n: i64) -> Vec<String> {\n    let mut out = Vec::new();\n"
            "    for i in 1..=n {\n        out.push(match (i % 3, i % 5) {\n"
            "            (0, 0) => \"FizzBuzz\".to_string(),\n"
            "            (0, _) => \"Fizz\".to_string(),\n"
            "            (_, 0) => \"Buzz\".to_string(),\n"
            "            _ => i.to_string(),\n        });\n    }\n    out\n}\n"),
   "cpp": ("#include <string>\n#include <vector>\n\n"
           "std::vector<std::string> fizzbuzz(long long n) {\n"
           "    std::vector<std::string> out;\n    for (long long i = 1; i <= n; ++i) {\n"
           "        if (i % 15 == 0) out.push_back(\"FizzBuzz\");\n"
           "        else if (i % 3 == 0) out.push_back(\"Fizz\");\n"
           "        else if (i % 5 == 0) out.push_back(\"Buzz\");\n"
           "        else out.push_back(std::to_string(i));\n    }\n    return out;\n}\n"),
  },
  {"en": ["i % 15 == 0 covers both conditions at once",
          "Every entry is a string, including the plain numbers",
          "n = 0 must give an empty list, not a crash"],
   "de": ["i % 15 == 0 deckt beide Bedingungen auf einmal ab",
          "Jeder Eintrag ist ein String, auch die reinen Zahlen",
          "n = 0 muss eine leere Liste liefern, keinen Absturz"]},
  complexity="O(n)")

# ---------------------------------------------------------------------------
P("m_binary_search", "binary_search", "Easy", "Binary search",
  Sig([("nums", L(INT)), ("target", INT)], INT),
  {"en": "Binary Search", "de": "Binäre Suche"},
  {"en": """`nums` is sorted ascending. Return the index of target, or -1 if it is not
there. Must run in O(log n).

  binary_search([-1, 0, 3, 5, 9, 12], 9) -> 4
  binary_search([-1, 0, 3, 5, 9, 12], 2) -> -1
  binary_search([], 1)                   -> -1

Write it from memory until the off-by-one errors stop happening.""",
   "de": """`nums` ist aufsteigend sortiert. Gib den Index von target zurück, oder -1, wenn
er nicht vorkommt. Muss in O(log n) laufen.

  binary_search([-1, 0, 3, 5, 9, 12], 9) -> 4
  binary_search([-1, 0, 3, 5, 9, 12], 2) -> -1
  binary_search([], 1)                   -> -1

Schreib sie aus dem Kopf, bis die Fehler um eins aufhören."""},
  [case(([-1, 0, 3, 5, 9, 12], 9), 4), case(([-1, 0, 3, 5, 9, 12], 2), -1),
   case(([], 1), -1), case(([5], 5), 0, hidden=True),
   case((list(range(0, 2000, 2)), 1998), 999, hidden=True)],
  {
   "python": ("def binary_search(nums, target):\n    low, high = 0, len(nums) - 1\n"
              "    while low <= high:\n        mid = (low + high) // 2\n"
              "        if nums[mid] == target:\n            return mid\n"
              "        if nums[mid] < target:\n            low = mid + 1\n"
              "        else:\n            high = mid - 1\n    return -1\n"),
   "javascript": ("function binary_search(nums, target) {\n"
                  "  let low = 0, high = nums.length - 1;\n  while (low <= high) {\n"
                  "    const mid = (low + high) >> 1;\n"
                  "    if (nums[mid] === target) return mid;\n"
                  "    if (nums[mid] < target) low = mid + 1; else high = mid - 1;\n"
                  "  }\n  return -1;\n}\n"),
   "java": ("class Solution {\n    static long binary_search(long[] nums, long target) {\n"
            "        int low = 0, high = nums.length - 1;\n        while (low <= high) {\n"
            "            int mid = low + (high - low) / 2;\n"
            "            if (nums[mid] == target) return mid;\n"
            "            if (nums[mid] < target) low = mid + 1; else high = mid - 1;\n"
            "        }\n        return -1;\n    }\n}\n"),
   "csharp": ("public static class Solution\n{\n"
              "    public static long binary_search(long[] nums, long target)\n    {\n"
              "        int low = 0, high = nums.Length - 1;\n        while (low <= high)\n"
              "        {\n            int mid = low + (high - low) / 2;\n"
              "            if (nums[mid] == target) return mid;\n"
              "            if (nums[mid] < target) low = mid + 1; else high = mid - 1;\n"
              "        }\n        return -1;\n    }\n}\n"),
   "go": ("package main\n\nfunc binary_search(nums []int, target int) int {\n"
          "\tlow, high := 0, len(nums)-1\n\tfor low <= high {\n\t\tmid := (low + high) / 2\n"
          "\t\tif nums[mid] == target {\n\t\t\treturn mid\n\t\t}\n"
          "\t\tif nums[mid] < target {\n\t\t\tlow = mid + 1\n\t\t} else {\n"
          "\t\t\thigh = mid - 1\n\t\t}\n\t}\n\treturn -1\n}\n"),
   "rust": ("fn binary_search(nums: &[i64], target: i64) -> i64 {\n"
            "    if nums.is_empty() { return -1; }\n"
            "    let (mut low, mut high) = (0i64, nums.len() as i64 - 1);\n"
            "    while low <= high {\n        let mid = low + (high - low) / 2;\n"
            "        let value = nums[mid as usize];\n"
            "        if value == target { return mid; }\n"
            "        if value < target { low = mid + 1; } else { high = mid - 1; }\n"
            "    }\n    -1\n}\n"),
   "cpp": ("#include <vector>\n\n"
           "long long binary_search(const std::vector<long long>& nums, long long target) {\n"
           "    long long low = 0, high = (long long)nums.size() - 1;\n"
           "    while (low <= high) {\n        long long mid = low + (high - low) / 2;\n"
           "        if (nums[mid] == target) return mid;\n"
           "        if (nums[mid] < target) low = mid + 1; else high = mid - 1;\n"
           "    }\n    return -1;\n}\n"),
  },
  {"en": ["low, high = 0, len - 1 and loop while low <= high",
          "mid = low + (high - low) / 2 avoids overflow in fixed-width languages",
          "Move to mid + 1 or mid - 1, never to mid, or you loop forever"],
   "de": ["low, high = 0, len - 1 und Schleife, solange low <= high",
          "mid = low + (high - low) / 2 vermeidet Überlauf in Sprachen mit festen Breiten",
          "Geh auf mid + 1 oder mid - 1, nie auf mid, sonst läufst du ewig"]},
  {"en": "LeetCode 704.", "de": "LeetCode 704."},
  complexity="O(log n)")

# ---------------------------------------------------------------------------
P("m_reverse_words", "reverse_words", "Easy", "Strings",
  Sig([("text", STR)], STR),
  {"en": "Reverse the Words", "de": "Wörter umdrehen"},
  {"en": """Reverse the ORDER of the words in a sentence. Words are separated by spaces;
collapse any run of spaces to a single one and trim the ends.

  reverse_words("the sky  is blue") -> "blue is sky the"
  reverse_words("  hello world  ")   -> "world hello"
  reverse_words("")                  -> ""

Each word itself stays as it is — only their order changes.""",
   "de": """Dreh die REIHENFOLGE der Wörter eines Satzes um. Wörter sind durch Leerzeichen
getrennt; mehrfache Leerzeichen werden zu einem, Anfang und Ende werden
abgeschnitten.

  reverse_words("the sky  is blue") -> "blue is sky the"
  reverse_words("  hello world  ")   -> "world hello"
  reverse_words("")                  -> ""

Jedes Wort selbst bleibt, wie es ist — nur die Reihenfolge ändert sich."""},
  [case("the sky  is blue", "blue is sky the"), case("  hello world  ", "world hello"),
   case("", ""), case("single", "single", hidden=True),
   case("a b c d", "d c b a", hidden=True)],
  {
   "python": ("def reverse_words(text):\n    return ' '.join(reversed(text.split()))\n"),
   "javascript": ("function reverse_words(text) {\n"
                  "  return text.split(/\\s+/).filter(Boolean).reverse().join(' ');\n}\n"),
   "java": ("class Solution {\n    static String reverse_words(String text) {\n"
            "        String[] parts = text.trim().split(\"\\\\s+\");\n"
            "        StringBuilder sb = new StringBuilder();\n"
            "        for (int i = parts.length - 1; i >= 0; i--) {\n"
            "            if (parts[i].isEmpty()) continue;\n"
            "            if (sb.length() > 0) sb.append(' ');\n"
            "            sb.append(parts[i]);\n        }\n        return sb.toString();\n"
            "    }\n}\n"),
   "csharp": ("public static class Solution\n{\n"
              "    public static string reverse_words(string text)\n    {\n"
              "        var parts = text.Split((char[])null,\n"
              "            StringSplitOptions.RemoveEmptyEntries);\n"
              "        Array.Reverse(parts);\n        return string.Join(\" \", parts);\n"
              "    }\n}\n"),
   "go": ("package main\n\nimport \"strings\"\n\nfunc reverse_words(text string) string {\n"
          "\tparts := strings.Fields(text)\n"
          "\tfor i, j := 0, len(parts)-1; i < j; i, j = i+1, j-1 {\n"
          "\t\tparts[i], parts[j] = parts[j], parts[i]\n\t}\n"
          "\treturn strings.Join(parts, \" \")\n}\n"),
   "rust": ("fn reverse_words(text: &str) -> String {\n"
            "    text.split_whitespace().rev().collect::<Vec<&str>>().join(\" \")\n}\n"),
   "cpp": ("#include <sstream>\n#include <string>\n#include <vector>\n\n"
           "std::string reverse_words(const std::string& text) {\n"
           "    std::istringstream stream(text);\n    std::vector<std::string> parts;\n"
           "    std::string word;\n    while (stream >> word) parts.push_back(word);\n"
           "    std::string out;\n"
           "    for (size_t i = parts.size(); i-- > 0; ) {\n"
           "        if (!out.empty()) out += ' ';\n        out += parts[i];\n    }\n"
           "    return out;\n}\n"),
  },
  {"en": ["Splitting on whitespace usually drops the empty pieces for you",
          "Reverse the list of words, then join with a single space",
          "Watch the leading and trailing spaces"],
   "de": ["Das Trennen an Leerraum wirft die leeren Teile meist schon weg",
          "Dreh die Wortliste um und füge sie mit einem Leerzeichen zusammen",
          "Achte auf Leerzeichen am Anfang und Ende"]},
  complexity="O(n)")

# ---------------------------------------------------------------------------
P("m_move_zeroes", "move_zeroes", "Easy", "Two pointers",
  Sig([("nums", L(INT))], L(INT)),
  {"en": "Move Zeroes", "de": "Nullen nach hinten"},
  {"en": """Move every 0 to the end of the list while keeping the order of the non-zero
values. Return the resulting list.

  move_zeroes([0, 1, 0, 3, 12]) -> [1, 3, 12, 0, 0]
  move_zeroes([0])              -> [0]
  move_zeroes([])               -> []""",
   "de": """Schieb jede 0 ans Ende der Liste und behalte dabei die Reihenfolge der
Werte ungleich null. Gib die entstandene Liste zurück.

  move_zeroes([0, 1, 0, 3, 12]) -> [1, 3, 12, 0, 0]
  move_zeroes([0])              -> [0]
  move_zeroes([])               -> []"""},
  [case([0, 1, 0, 3, 12], [1, 3, 12, 0, 0]), case([0], [0]), case([], []),
   case([1, 2, 3], [1, 2, 3], hidden=True),
   case([0, 0, 1], [1, 0, 0], hidden=True)],
  {
   "python": ("def move_zeroes(nums):\n    kept = [n for n in nums if n != 0]\n"
              "    return kept + [0] * (len(nums) - len(kept))\n"),
   "javascript": ("function move_zeroes(nums) {\n  const kept = nums.filter(n => n !== 0);\n"
                  "  while (kept.length < nums.length) kept.push(0);\n  return kept;\n}\n"),
   "java": ("class Solution {\n    static long[] move_zeroes(long[] nums) {\n"
            "        long[] out = new long[nums.length];\n        int w = 0;\n"
            "        for (long n : nums) if (n != 0) out[w++] = n;\n"
            "        return out;\n    }\n}\n"),
   "csharp": ("public static class Solution\n{\n"
              "    public static long[] move_zeroes(long[] nums)\n    {\n"
              "        var outArr = new long[nums.Length];\n        int w = 0;\n"
              "        foreach (var n in nums) if (n != 0) outArr[w++] = n;\n"
              "        return outArr;\n    }\n}\n"),
   "go": ("package main\n\nfunc move_zeroes(nums []int) []int {\n"
          "\tout := make([]int, len(nums))\n\tw := 0\n\tfor _, n := range nums {\n"
          "\t\tif n != 0 {\n\t\t\tout[w] = n\n\t\t\tw++\n\t\t}\n\t}\n\treturn out\n}\n"),
   "rust": ("fn move_zeroes(nums: &[i64]) -> Vec<i64> {\n"
            "    let mut out: Vec<i64> = nums.iter().cloned().filter(|&n| n != 0).collect();\n"
            "    out.resize(nums.len(), 0);\n    out\n}\n"),
   "cpp": ("#include <vector>\n\n"
           "std::vector<long long> move_zeroes(const std::vector<long long>& nums) {\n"
           "    std::vector<long long> out;\n"
           "    for (long long n : nums) if (n != 0) out.push_back(n);\n"
           "    out.resize(nums.size(), 0);\n    return out;\n}\n"),
  },
  {"en": ["Collect the non-zero values in order",
          "Pad the rest of the result with zeros",
          "In languages with fixed-size arrays a write pointer does both at once"],
   "de": ["Sammel die Werte ungleich null der Reihe nach ein",
          "Füll den Rest des Ergebnisses mit Nullen auf",
          "In Sprachen mit festen Arrays erledigt ein Schreibzeiger beides auf einmal"]},
  {"en": "LeetCode 283.", "de": "LeetCode 283."},
  complexity="O(n)")

# ---------------------------------------------------------------------------
P("m_max_profit", "max_profit", "Easy", "Greedy",
  Sig([("prices", L(INT))], INT),
  {"en": "Best Time to Buy and Sell", "de": "Bester Kauf- und Verkaufszeitpunkt"},
  {"en": """prices[i] is a share price on day i. Buy on one day and sell on a LATER day.
Return the biggest profit possible, or 0 if no trade makes money.

  max_profit([7, 1, 5, 3, 6, 4]) -> 5      (buy at 1, sell at 6)
  max_profit([7, 6, 4, 3, 1])    -> 0
  max_profit([])                 -> 0

One pass: remember the cheapest price seen so far.""",
   "de": """prices[i] ist ein Aktienkurs an Tag i. Kauf an einem Tag und verkauf an einem
SPÄTEREN. Gib den größtmöglichen Gewinn zurück, oder 0, wenn sich kein Handel
lohnt.

  max_profit([7, 1, 5, 3, 6, 4]) -> 5      (bei 1 kaufen, bei 6 verkaufen)
  max_profit([7, 6, 4, 3, 1])    -> 0
  max_profit([])                 -> 0

Ein Durchlauf: merk dir den bisher günstigsten Kurs."""},
  [case([7, 1, 5, 3, 6, 4], 5), case([7, 6, 4, 3, 1], 0), case([], 0),
   case([1], 0, hidden=True), case([1, 2, 3, 4, 5], 4, hidden=True),
   case([2, 4, 1, 7], 6, hidden=True)],
  {
   "python": ("def max_profit(prices):\n    best = 0\n    cheapest = None\n"
              "    for price in prices:\n"
              "        if cheapest is None or price < cheapest:\n            cheapest = price\n"
              "        elif price - cheapest > best:\n            best = price - cheapest\n"
              "    return best\n"),
   "javascript": ("function max_profit(prices) {\n  let best = 0, cheapest = Infinity;\n"
                  "  for (const price of prices) {\n"
                  "    if (price < cheapest) cheapest = price;\n"
                  "    else if (price - cheapest > best) best = price - cheapest;\n"
                  "  }\n  return best;\n}\n"),
   "java": ("class Solution {\n    static long max_profit(long[] prices) {\n"
            "        long best = 0, cheapest = Long.MAX_VALUE;\n"
            "        for (long price : prices) {\n"
            "            if (price < cheapest) cheapest = price;\n"
            "            else if (price - cheapest > best) best = price - cheapest;\n"
            "        }\n        return best;\n    }\n}\n"),
   "csharp": ("public static class Solution\n{\n"
              "    public static long max_profit(long[] prices)\n    {\n"
              "        long best = 0, cheapest = long.MaxValue;\n"
              "        foreach (var price in prices)\n        {\n"
              "            if (price < cheapest) cheapest = price;\n"
              "            else if (price - cheapest > best) best = price - cheapest;\n"
              "        }\n        return best;\n    }\n}\n"),
   "go": ("package main\n\nimport \"math\"\n\nfunc max_profit(prices []int) int {\n"
          "\tbest := 0\n\tcheapest := math.MaxInt\n\tfor _, price := range prices {\n"
          "\t\tif price < cheapest {\n\t\t\tcheapest = price\n"
          "\t\t} else if price-cheapest > best {\n\t\t\tbest = price - cheapest\n\t\t}\n\t}\n"
          "\treturn best\n}\n"),
   "rust": ("fn max_profit(prices: &[i64]) -> i64 {\n    let mut best = 0i64;\n"
            "    let mut cheapest = i64::MAX;\n    for &price in prices {\n"
            "        if price < cheapest { cheapest = price; }\n"
            "        else if price - cheapest > best { best = price - cheapest; }\n"
            "    }\n    best\n}\n"),
   "cpp": ("#include <climits>\n#include <vector>\n\n"
           "long long max_profit(const std::vector<long long>& prices) {\n"
           "    long long best = 0, cheapest = LLONG_MAX;\n"
           "    for (long long price : prices) {\n"
           "        if (price < cheapest) cheapest = price;\n"
           "        else if (price - cheapest > best) best = price - cheapest;\n"
           "    }\n    return best;\n}\n"),
  },
  {"en": ["Track the minimum price seen so far",
          "At each day the best sale today is price - cheapest",
          "Never let the profit drop below 0"],
   "de": ["Merk dir den bisher kleinsten Kurs",
          "An jedem Tag ist der beste Verkauf heute: Kurs - günstigster",
          "Lass den Gewinn nie unter 0 fallen"]},
  {"en": "LeetCode 121 and Codility's MaxProfit.",
   "de": "LeetCode 121 und Codilitys MaxProfit."},
  complexity="O(n)")

# ---------------------------------------------------------------------------
P("m_row_sums", "row_sums", "Easy", "Matrix",
  Sig([("grid", L(L(INT)))], L(INT)),
  {"en": "Row Sums", "de": "Zeilensummen"},
  {"en": """The input is a grid — a list of rows, each row a list of numbers. Return the
sum of each row.

  row_sums([[1, 2], [3, 4], [5, 6]]) -> [3, 7, 11]
  row_sums([])                       -> []

This is the warm-up for every two-dimensional problem: getting comfortable with
nested indexing in a new language.""",
   "de": """Die Eingabe ist ein Gitter — eine Liste von Zeilen, jede Zeile eine Liste von
Zahlen. Gib die Summe jeder Zeile zurück.

  row_sums([[1, 2], [3, 4], [5, 6]]) -> [3, 7, 11]
  row_sums([])                       -> []

Das ist das Aufwärmen für jede zweidimensionale Aufgabe: sich in einer neuen
Sprache an verschachtelte Indizes gewöhnen."""},
  [case([[1, 2], [3, 4], [5, 6]], [3, 7, 11]), case([], []),
   case([[5]], [5]), case([[0, 0], [1, -1]], [0, 0], hidden=True),
   case([[1, 2, 3, 4]], [10], hidden=True)],
  {
   "python": "def row_sums(grid):\n    return [sum(row) for row in grid]\n",
   "javascript": ("function row_sums(grid) {\n"
                  "  return grid.map(row => row.reduce((a, b) => a + b, 0));\n}\n"),
   "java": ("class Solution {\n    static long[] row_sums(long[][] grid) {\n"
            "        long[] out = new long[grid.length];\n"
            "        for (int i = 0; i < grid.length; i++) {\n"
            "            long total = 0;\n            for (long v : grid[i]) total += v;\n"
            "            out[i] = total;\n        }\n        return out;\n    }\n}\n"),
   "csharp": ("public static class Solution\n{\n"
              "    public static long[] row_sums(long[][] grid)\n    {\n"
              "        var outArr = new long[grid.Length];\n"
              "        for (int i = 0; i < grid.Length; i++)\n        {\n"
              "            long total = 0;\n            foreach (var v in grid[i]) total += v;\n"
              "            outArr[i] = total;\n        }\n        return outArr;\n    }\n}\n"),
   "go": ("package main\n\nfunc row_sums(grid [][]int) []int {\n"
          "\tout := make([]int, len(grid))\n\tfor i, row := range grid {\n"
          "\t\ttotal := 0\n\t\tfor _, v := range row {\n\t\t\ttotal += v\n\t\t}\n"
          "\t\tout[i] = total\n\t}\n\treturn out\n}\n"),
   "rust": ("fn row_sums(grid: &[Vec<i64>]) -> Vec<i64> {\n"
            "    grid.iter().map(|row| row.iter().sum()).collect()\n}\n"),
   "cpp": ("#include <vector>\n\n"
           "std::vector<long long> row_sums(const std::vector<std::vector<long long>>& grid) {\n"
           "    std::vector<long long> out;\n    for (const auto& row : grid) {\n"
           "        long long total = 0;\n        for (long long v : row) total += v;\n"
           "        out.push_back(total);\n    }\n    return out;\n}\n"),
  },
  {"en": ["Loop over the rows, and inside that over the values",
          "The result has one entry per row",
          "An empty grid gives an empty result"],
   "de": ["Lauf über die Zeilen und darin über die Werte",
          "Das Ergebnis hat einen Eintrag pro Zeile",
          "Ein leeres Gitter ergibt ein leeres Ergebnis"]},
  complexity="O(rows * cols)")


# ---------------------------------------------------------------------------
P("m_count_vowels", "count_vowels", "Easy", "Strings",
  Sig([("text", STR)], INT),
  {"en": "Count the Vowels", "de": "Vokale zählen"},
  {"en": """Count how many vowels (a, e, i, o, u) the text contains. Upper and lower
case both count; everything else is ignored.

  count_vowels("Hello World") -> 3
  count_vowels("xyz")         -> 0
  count_vowels("")            -> 0""",
   "de": """Zähl, wie viele Vokale (a, e, i, o, u) der Text enthält. Groß- und
Kleinschreibung zählen beide, alles andere wird ignoriert.

  count_vowels("Hello World") -> 3
  count_vowels("xyz")         -> 0
  count_vowels("")            -> 0"""},
  [case("Hello World", 3), case("xyz", 0), case("", 0),
   case("AEIOUaeiou", 10, hidden=True), case("Programming", 3, hidden=True)],
  {
   "python": ("def count_vowels(text):\n"
              "    return sum(1 for c in text.lower() if c in 'aeiou')\n"),
   "javascript": ("function count_vowels(text) {\n"
                  "  return (text.match(/[aeiou]/gi) || []).length;\n}\n"),
   "java": ("class Solution {\n    static long count_vowels(String text) {\n"
            "        long total = 0;\n"
            "        for (char c : text.toLowerCase().toCharArray())\n"
            "            if (\"aeiou\".indexOf(c) >= 0) total++;\n"
            "        return total;\n    }\n}\n"),
   "csharp": ("public static class Solution\n{\n"
              "    public static long count_vowels(string text)\n    {\n"
              "        long total = 0;\n"
              "        foreach (var c in text.ToLowerInvariant())\n"
              "            if (\"aeiou\".IndexOf(c) >= 0) total++;\n"
              "        return total;\n    }\n}\n"),
   "go": ("package main\n\nimport \"strings\"\n\nfunc count_vowels(text string) int {\n"
          "\ttotal := 0\n\tfor _, r := range strings.ToLower(text) {\n"
          "\t\tif strings.ContainsRune(\"aeiou\", r) {\n\t\t\ttotal++\n\t\t}\n\t}\n"
          "\treturn total\n}\n"),
   "rust": ("fn count_vowels(text: &str) -> i64 {\n"
            "    text.chars()\n"
            "        .filter(|c| \"aeiou\".contains(c.to_ascii_lowercase()))\n"
            "        .count() as i64\n}\n"),
   "cpp": ("#include <cctype>\n#include <string>\n\n"
           "long long count_vowels(const std::string& text) {\n"
           "    long long total = 0;\n    for (char c : text) {\n"
           "        char lower = (char)std::tolower((unsigned char)c);\n"
           "        if (lower=='a'||lower=='e'||lower=='i'||lower=='o'||lower=='u')\n"
           "            total++;\n    }\n    return total;\n}\n"),
  },
  {"en": ["Lower-case the character before checking it",
          "Checking membership in the string \"aeiou\" is the shortest test"],
   "de": ["Mach das Zeichen klein, bevor du es prüfst",
          "Auf Enthaltensein in \"aeiou\" zu prüfen ist der kürzeste Test"]},
  complexity="O(n)")

# ---------------------------------------------------------------------------
P("m_reverse_list", "reverse_list", "Easy", "Arrays",
  Sig([("nums", L(INT))], L(INT)),
  {"en": "Reverse a List", "de": "Eine Liste umdrehen"},
  {"en": """Return the list in reverse order, as a new list.

  reverse_list([1, 2, 3]) -> [3, 2, 1]
  reverse_list([])        -> []

Most languages have this built in, but write the index loop at least once —
walking from both ends is a pattern you will reuse constantly.""",
   "de": """Gib die Liste in umgekehrter Reihenfolge zurück, als neue Liste.

  reverse_list([1, 2, 3]) -> [3, 2, 1]
  reverse_list([])        -> []

Die meisten Sprachen haben das eingebaut, aber schreib die Indexschleife
wenigstens einmal selbst — von beiden Enden zu laufen brauchst du ständig wieder."""},
  [case([1, 2, 3], [3, 2, 1]), case([], []), case([7], [7]),
   case([1, 2, 3, 4], [4, 3, 2, 1], hidden=True),
   case([-1, 0, 1], [1, 0, -1], hidden=True)],
  {
   "python": "def reverse_list(nums):\n    return nums[::-1]\n",
   "javascript": "function reverse_list(nums) {\n  return [...nums].reverse();\n}\n",
   "java": ("class Solution {\n    static long[] reverse_list(long[] nums) {\n"
            "        long[] out = new long[nums.length];\n"
            "        for (int i = 0; i < nums.length; i++)\n"
            "            out[i] = nums[nums.length - 1 - i];\n"
            "        return out;\n    }\n}\n"),
   "csharp": ("public static class Solution\n{\n"
              "    public static long[] reverse_list(long[] nums)\n    {\n"
              "        var outArr = new long[nums.Length];\n"
              "        for (int i = 0; i < nums.Length; i++)\n"
              "            outArr[i] = nums[nums.Length - 1 - i];\n"
              "        return outArr;\n    }\n}\n"),
   "go": ("package main\n\nfunc reverse_list(nums []int) []int {\n"
          "\tout := make([]int, len(nums))\n\tfor i, v := range nums {\n"
          "\t\tout[len(nums)-1-i] = v\n\t}\n\treturn out\n}\n"),
   "rust": ("fn reverse_list(nums: &[i64]) -> Vec<i64> {\n"
            "    nums.iter().rev().cloned().collect()\n}\n"),
   "cpp": ("#include <vector>\n\n"
           "std::vector<long long> reverse_list(const std::vector<long long>& nums) {\n"
           "    return std::vector<long long>(nums.rbegin(), nums.rend());\n}\n"),
  },
  {"en": ["Walk the input backwards, or write the output backwards",
          "out[i] = nums[len - 1 - i]"],
   "de": ["Lauf die Eingabe rückwärts durch, oder schreib die Ausgabe rückwärts",
          "out[i] = nums[len - 1 - i]"]},
  complexity="O(n)")

# ---------------------------------------------------------------------------
P("m_single_number", "single_number", "Easy", "Bit tricks",
  Sig([("nums", L(INT))], INT),
  {"en": "The Single Number", "de": "Die einzelne Zahl"},
  {"en": """Every value in the list appears exactly twice, except one that appears once.
Find that one.

  single_number([4, 1, 2, 1, 2]) -> 4
  single_number([7])             -> 7

A set solves it in O(n) memory. The expected answer uses O(1): XOR every value
together. x ^ x is 0 and x ^ 0 is x, so all the pairs cancel out no matter what
order they arrive in.""",
   "de": """Jeder Wert der Liste kommt genau zweimal vor — außer einem, der einmal
vorkommt. Finde ihn.

  single_number([4, 1, 2, 1, 2]) -> 4
  single_number([7])             -> 7

Ein Set löst das mit O(n) Speicher. Die erwartete Antwort braucht O(1): XOR alle
Werte zusammen. x ^ x ist 0 und x ^ 0 ist x, die Paare heben sich also auf, egal
in welcher Reihenfolge sie kommen."""},
  [case([4, 1, 2, 1, 2], 4), case([7], 7), case([2, 2, 1], 1),
   case([1, 1, 3, 3, 99], 99, hidden=True),
   case([5, 4, 5, 4, 8], 8, hidden=True)],
  {
   "python": ("def single_number(nums):\n    result = 0\n    for value in nums:\n"
              "        result ^= value\n    return result\n"),
   "javascript": ("function single_number(nums) {\n  let result = 0;\n"
                  "  for (const value of nums) result ^= value;\n  return result;\n}\n"),
   "java": ("class Solution {\n    static long single_number(long[] nums) {\n"
            "        long result = 0;\n        for (long v : nums) result ^= v;\n"
            "        return result;\n    }\n}\n"),
   "csharp": ("public static class Solution\n{\n"
              "    public static long single_number(long[] nums)\n    {\n"
              "        long result = 0;\n        foreach (var v in nums) result ^= v;\n"
              "        return result;\n    }\n}\n"),
   "go": ("package main\n\nfunc single_number(nums []int) int {\n\tresult := 0\n"
          "\tfor _, v := range nums {\n\t\tresult ^= v\n\t}\n\treturn result\n}\n"),
   "rust": ("fn single_number(nums: &[i64]) -> i64 {\n"
            "    nums.iter().fold(0, |acc, v| acc ^ v)\n}\n"),
   "cpp": ("#include <vector>\n\n"
           "long long single_number(const std::vector<long long>& nums) {\n"
           "    long long result = 0;\n    for (long long v : nums) result ^= v;\n"
           "    return result;\n}\n"),
  },
  {"en": ["The XOR operator is ^ in every language here",
          "Start the accumulator at 0 and fold the whole list into it",
          "Order does not matter — XOR is commutative"],
   "de": ["Der XOR-Operator ist in allen Sprachen hier ^",
          "Fang bei 0 an und falte die ganze Liste hinein",
          "Die Reihenfolge ist egal — XOR ist kommutativ"]},
  {"en": "LeetCode 136 and Codility's OddOccurrencesInArray.",
   "de": "LeetCode 136 und Codilitys OddOccurrencesInArray."},
  complexity="O(n) time, O(1) space")

# ---------------------------------------------------------------------------
P("m_majority_element", "majority_element", "Easy", "Counting",
  Sig([("nums", L(INT))], INT),
  {"en": "Majority Element", "de": "Mehrheitselement"},
  {"en": """One value appears MORE than half the time. Return it. The list is never empty
and such a value always exists.

  majority_element([3, 2, 3])             -> 3
  majority_element([2, 2, 1, 1, 1, 2, 2]) -> 2

Counting into a map is O(n) memory. Boyer-Moore voting does it in O(1): hold a
candidate and a counter, +1 when the value matches, -1 when it does not, and
adopt a new candidate whenever the counter hits zero.""",
   "de": """Ein Wert kommt in MEHR als der Hälfte der Fälle vor. Gib ihn zurück. Die Liste
ist nie leer, und so ein Wert existiert immer.

  majority_element([3, 2, 3])             -> 3
  majority_element([2, 2, 1, 1, 1, 2, 2]) -> 2

In eine Map zu zählen kostet O(n) Speicher. Das Boyer-Moore-Wahlverfahren
schafft es mit O(1): halt einen Kandidaten und einen Zähler, +1 bei
Übereinstimmung, -1 sonst, und nimm einen neuen Kandidaten, sobald der Zähler
auf null fällt."""},
  [case([3, 2, 3], 3), case([2, 2, 1, 1, 1, 2, 2], 2), case([1], 1),
   case([6, 5, 5], 5, hidden=True), case([4, 4, 4, 9, 9], 4, hidden=True)],
  {
   "python": ("def majority_element(nums):\n    candidate, count = None, 0\n"
              "    for value in nums:\n        if count == 0:\n            candidate = value\n"
              "        count += 1 if value == candidate else -1\n    return candidate\n"),
   "javascript": ("function majority_element(nums) {\n  let candidate = 0, count = 0;\n"
                  "  for (const value of nums) {\n"
                  "    if (count === 0) candidate = value;\n"
                  "    count += value === candidate ? 1 : -1;\n  }\n  return candidate;\n}\n"),
   "java": ("class Solution {\n    static long majority_element(long[] nums) {\n"
            "        long candidate = 0;\n        int count = 0;\n"
            "        for (long v : nums) {\n            if (count == 0) candidate = v;\n"
            "            count += (v == candidate) ? 1 : -1;\n        }\n"
            "        return candidate;\n    }\n}\n"),
   "csharp": ("public static class Solution\n{\n"
              "    public static long majority_element(long[] nums)\n    {\n"
              "        long candidate = 0;\n        int count = 0;\n"
              "        foreach (var v in nums)\n        {\n"
              "            if (count == 0) candidate = v;\n"
              "            count += (v == candidate) ? 1 : -1;\n        }\n"
              "        return candidate;\n    }\n}\n"),
   "go": ("package main\n\nfunc majority_element(nums []int) int {\n"
          "\tcandidate, count := 0, 0\n\tfor _, v := range nums {\n"
          "\t\tif count == 0 {\n\t\t\tcandidate = v\n\t\t}\n"
          "\t\tif v == candidate {\n\t\t\tcount++\n\t\t} else {\n\t\t\tcount--\n\t\t}\n\t}\n"
          "\treturn candidate\n}\n"),
   "rust": ("fn majority_element(nums: &[i64]) -> i64 {\n"
            "    let mut candidate = 0i64;\n    let mut count = 0i64;\n"
            "    for &v in nums {\n        if count == 0 { candidate = v; }\n"
            "        count += if v == candidate { 1 } else { -1 };\n    }\n    candidate\n}\n"),
   "cpp": ("#include <vector>\n\n"
           "long long majority_element(const std::vector<long long>& nums) {\n"
           "    long long candidate = 0;\n    long long count = 0;\n"
           "    for (long long v : nums) {\n        if (count == 0) candidate = v;\n"
           "        count += (v == candidate) ? 1 : -1;\n    }\n    return candidate;\n}\n"),
  },
  {"en": ["Say the O(n)-memory counting version out loud first, then improve it",
          "Keep a candidate and a vote counter",
          "Reset the candidate whenever the counter reaches zero"],
   "de": ["Nenn zuerst die Zählvariante mit O(n) Speicher, dann verbesser sie",
          "Halt einen Kandidaten und einen Stimmenzähler",
          "Setz den Kandidaten neu, sobald der Zähler null erreicht"]},
  {"en": "LeetCode 169 and Codility's Dominator.",
   "de": "LeetCode 169 und Codilitys Dominator."},
  complexity="O(n) time, O(1) space")

# ---------------------------------------------------------------------------
P("m_gcd", "gcd", "Easy", "Math",
  Sig([("a", INT), ("b", INT)], INT),
  {"en": "Greatest Common Divisor", "de": "Größter gemeinsamer Teiler"},
  {"en": """Return the greatest common divisor of two non-negative integers.

  gcd(84, 36) -> 12
  gcd(7, 13)  -> 1
  gcd(5, 0)   -> 5

Use Euclid's algorithm: replace (a, b) with (b, a % b) until b is zero, and
whatever is left in a is the answer. Do not loop from 1 upwards — the inputs go
into the billions.""",
   "de": """Gib den größten gemeinsamen Teiler zweier nicht negativer ganzer Zahlen zurück.

  gcd(84, 36) -> 12
  gcd(7, 13)  -> 1
  gcd(5, 0)   -> 5

Nimm Euklids Algorithmus: ersetz (a, b) durch (b, a % b), bis b null ist — was
dann in a steht, ist die Antwort. Zähl nicht von 1 aufwärts, die Eingaben gehen
in die Milliarden."""},
  [case((84, 36), 12), case((7, 13), 1), case((5, 0), 5),
   case((0, 9), 9, hidden=True), case((1000000000, 6), 2, hidden=True),
   case((270, 192), 6, hidden=True)],
  {
   "python": "def gcd(a, b):\n    while b:\n        a, b = b, a % b\n    return a\n",
   "javascript": ("function gcd(a, b) {\n  while (b !== 0) {\n    const t = a % b;\n"
                  "    a = b;\n    b = t;\n  }\n  return a;\n}\n"),
   "java": ("class Solution {\n    static long gcd(long a, long b) {\n"
            "        while (b != 0) {\n            long t = a % b;\n"
            "            a = b;\n            b = t;\n        }\n        return a;\n    }\n}\n"),
   "csharp": ("public static class Solution\n{\n"
              "    public static long gcd(long a, long b)\n    {\n"
              "        while (b != 0)\n        {\n            long t = a % b;\n"
              "            a = b;\n            b = t;\n        }\n        return a;\n    }\n}\n"),
   "go": ("package main\n\nfunc gcd(a int, b int) int {\n\tfor b != 0 {\n"
          "\t\ta, b = b, a%b\n\t}\n\treturn a\n}\n"),
   "rust": ("fn gcd(a: i64, b: i64) -> i64 {\n    let (mut a, mut b) = (a, b);\n"
            "    while b != 0 {\n        let t = a % b;\n        a = b;\n        b = t;\n"
            "    }\n    a\n}\n"),
   "cpp": ("long long gcd(long long a, long long b) {\n    while (b != 0) {\n"
           "        long long t = a % b;\n        a = b;\n        b = t;\n    }\n"
           "    return a;\n}\n"),
  },
  {"en": ["while b != 0: (a, b) becomes (b, a % b)",
          "When the loop ends, a holds the answer",
          "gcd(x, 0) is x, which the loop already handles"],
   "de": ["while b != 0: aus (a, b) wird (b, a % b)",
          "Wenn die Schleife endet, steht die Antwort in a",
          "ggT(x, 0) ist x — das erledigt die Schleife schon"]},
  {"en": "The core of Codility's ChocolatesByNumbers, among many others.",
   "de": "Der Kern von Codilitys ChocolatesByNumbers und vieler anderer Aufgaben."},
  complexity="O(log n)")

# ---------------------------------------------------------------------------
P("m_is_anagram", "is_anagram", "Easy", "Counting",
  Sig([("a", STR), ("b", STR)], BOOL),
  {"en": "Valid Anagram", "de": "Gültiges Anagramm"},
  {"en": """Return true if the two strings use exactly the same letters, the same number
of times.

  is_anagram("anagram", "nagaram") -> true
  is_anagram("rat", "car")         -> false
  is_anagram("", "")               -> true

Different lengths mean false immediately. Sorting both is O(n log n) and
perfectly acceptable; counting characters is O(n) and better.""",
   "de": """Gib true zurück, wenn beide Strings genau dieselben Buchstaben gleich oft
verwenden.

  is_anagram("anagram", "nagaram") -> true
  is_anagram("rat", "car")         -> false
  is_anagram("", "")               -> true

Unterschiedliche Längen bedeuten sofort false. Beide zu sortieren ist
O(n log n) und völlig in Ordnung, Zeichen zu zählen ist O(n) und besser."""},
  [case(("anagram", "nagaram"), True), case(("rat", "car"), False),
   case(("", ""), True), case(("a", "ab"), False, hidden=True),
   case(("aabb", "bbaa"), True, hidden=True),
   case(("abc", "abd"), False, hidden=True)],
  {
   "python": "def is_anagram(a, b):\n    return sorted(a) == sorted(b)\n",
   "javascript": ("function is_anagram(a, b) {\n  if (a.length !== b.length) return false;\n"
                  "  const counts = new Map();\n"
                  "  for (const c of a) counts.set(c, (counts.get(c) || 0) + 1);\n"
                  "  for (const c of b) {\n    const n = counts.get(c) || 0;\n"
                  "    if (n === 0) return false;\n    counts.set(c, n - 1);\n  }\n"
                  "  return true;\n}\n"),
   "java": ("import java.util.Arrays;\n\nclass Solution {\n"
            "    static boolean is_anagram(String a, String b) {\n"
            "        if (a.length() != b.length()) return false;\n"
            "        char[] x = a.toCharArray(), y = b.toCharArray();\n"
            "        Arrays.sort(x);\n        Arrays.sort(y);\n"
            "        return Arrays.equals(x, y);\n    }\n}\n"),
   "csharp": ("public static class Solution\n{\n"
              "    public static bool is_anagram(string a, string b)\n    {\n"
              "        if (a.Length != b.Length) return false;\n"
              "        var x = a.ToCharArray();\n        var y = b.ToCharArray();\n"
              "        Array.Sort(x);\n        Array.Sort(y);\n"
              "        return new string(x) == new string(y);\n    }\n}\n"),
   "go": ("package main\n\nfunc is_anagram(a string, b string) bool {\n"
          "\tif len(a) != len(b) {\n\t\treturn false\n\t}\n"
          "\tcounts := map[rune]int{}\n\tfor _, r := range a {\n\t\tcounts[r]++\n\t}\n"
          "\tfor _, r := range b {\n\t\tcounts[r]--\n\t\tif counts[r] < 0 {\n"
          "\t\t\treturn false\n\t\t}\n\t}\n\treturn true\n}\n"),
   "rust": ("fn is_anagram(a: &str, b: &str) -> bool {\n"
            "    let mut x: Vec<char> = a.chars().collect();\n"
            "    let mut y: Vec<char> = b.chars().collect();\n"
            "    x.sort();\n    y.sort();\n    x == y\n}\n"),
   "cpp": ("#include <algorithm>\n#include <string>\n\n"
           "bool is_anagram(const std::string& a, const std::string& b) {\n"
           "    if (a.size() != b.size()) return false;\n"
           "    std::string x = a, y = b;\n    std::sort(x.begin(), x.end());\n"
           "    std::sort(y.begin(), y.end());\n    return x == y;\n}\n"),
  },
  {"en": ["Compare the lengths first and bail out early",
          "Sorting both and comparing is the two-line version",
          "Counting up for one string and down for the other is the O(n) version"],
   "de": ["Vergleich zuerst die Längen und brich früh ab",
          "Beide sortieren und vergleichen ist die Zwei-Zeilen-Variante",
          "Für den einen String hoch- und für den anderen runterzählen ist O(n)"]},
  {"en": "LeetCode 242.", "de": "LeetCode 242."},
  complexity="O(n log n)")

# ---------------------------------------------------------------------------
P("m_merge_sorted", "merge_sorted", "Easy", "Two pointers",
  Sig([("a", L(INT)), ("b", L(INT))], L(INT)),
  {"en": "Merge Two Sorted Lists", "de": "Zwei sortierte Listen verschmelzen"},
  {"en": """Both lists are already sorted ascending. Merge them into one sorted list.

  merge_sorted([1, 2, 4], [1, 3, 4]) -> [1, 1, 2, 3, 4, 4]
  merge_sorted([], [0])              -> [0]
  merge_sorted([], [])               -> []

Concatenating and sorting works, but throws away the fact that both are already
sorted. Do the real merge with two indices — O(n + m), and it is the step at the
heart of merge sort.""",
   "de": """Beide Listen sind bereits aufsteigend sortiert. Verschmelz sie zu einer
sortierten Liste.

  merge_sorted([1, 2, 4], [1, 3, 4]) -> [1, 1, 2, 3, 4, 4]
  merge_sorted([], [0])              -> [0]
  merge_sorted([], [])               -> []

Aneinanderhängen und sortieren funktioniert, wirft aber weg, dass beide schon
sortiert sind. Mach die echte Verschmelzung mit zwei Indizes — O(n + m), und das
ist der Kernschritt von Mergesort."""},
  [case(([1, 2, 4], [1, 3, 4]), [1, 1, 2, 3, 4, 4]), case(([], [0]), [0]),
   case(([], []), []), case(([5], [1]), [1, 5], hidden=True),
   case(([1, 3, 5], [2, 4, 6]), [1, 2, 3, 4, 5, 6], hidden=True)],
  {
   "python": ("def merge_sorted(a, b):\n    out = []\n    i = j = 0\n"
              "    while i < len(a) and j < len(b):\n"
              "        if a[i] <= b[j]:\n            out.append(a[i])\n            i += 1\n"
              "        else:\n            out.append(b[j])\n            j += 1\n"
              "    out.extend(a[i:])\n    out.extend(b[j:])\n    return out\n"),
   "javascript": ("function merge_sorted(a, b) {\n  const out = [];\n  let i = 0, j = 0;\n"
                  "  while (i < a.length && j < b.length) {\n"
                  "    if (a[i] <= b[j]) out.push(a[i++]);\n    else out.push(b[j++]);\n  }\n"
                  "  while (i < a.length) out.push(a[i++]);\n"
                  "  while (j < b.length) out.push(b[j++]);\n  return out;\n}\n"),
   "java": ("class Solution {\n    static long[] merge_sorted(long[] a, long[] b) {\n"
            "        long[] out = new long[a.length + b.length];\n"
            "        int i = 0, j = 0, w = 0;\n"
            "        while (i < a.length && j < b.length)\n"
            "            out[w++] = (a[i] <= b[j]) ? a[i++] : b[j++];\n"
            "        while (i < a.length) out[w++] = a[i++];\n"
            "        while (j < b.length) out[w++] = b[j++];\n"
            "        return out;\n    }\n}\n"),
   "csharp": ("public static class Solution\n{\n"
              "    public static long[] merge_sorted(long[] a, long[] b)\n    {\n"
              "        var outArr = new long[a.Length + b.Length];\n"
              "        int i = 0, j = 0, w = 0;\n"
              "        while (i < a.Length && j < b.Length)\n"
              "            outArr[w++] = (a[i] <= b[j]) ? a[i++] : b[j++];\n"
              "        while (i < a.Length) outArr[w++] = a[i++];\n"
              "        while (j < b.Length) outArr[w++] = b[j++];\n"
              "        return outArr;\n    }\n}\n"),
   "go": ("package main\n\nfunc merge_sorted(a []int, b []int) []int {\n"
          "\tout := make([]int, 0, len(a)+len(b))\n\ti, j := 0, 0\n"
          "\tfor i < len(a) && j < len(b) {\n\t\tif a[i] <= b[j] {\n"
          "\t\t\tout = append(out, a[i])\n\t\t\ti++\n\t\t} else {\n"
          "\t\t\tout = append(out, b[j])\n\t\t\tj++\n\t\t}\n\t}\n"
          "\tout = append(out, a[i:]...)\n\tout = append(out, b[j:]...)\n\treturn out\n}\n"),
   "rust": ("fn merge_sorted(a: &[i64], b: &[i64]) -> Vec<i64> {\n"
            "    let mut out = Vec::with_capacity(a.len() + b.len());\n"
            "    let (mut i, mut j) = (0usize, 0usize);\n"
            "    while i < a.len() && j < b.len() {\n"
            "        if a[i] <= b[j] { out.push(a[i]); i += 1; }\n"
            "        else { out.push(b[j]); j += 1; }\n    }\n"
            "    out.extend_from_slice(&a[i..]);\n    out.extend_from_slice(&b[j..]);\n"
            "    out\n}\n"),
   "cpp": ("#include <vector>\n\nstd::vector<long long> merge_sorted(\n"
           "        const std::vector<long long>& a, const std::vector<long long>& b) {\n"
           "    std::vector<long long> out;\n    out.reserve(a.size() + b.size());\n"
           "    size_t i = 0, j = 0;\n    while (i < a.size() && j < b.size()) {\n"
           "        if (a[i] <= b[j]) out.push_back(a[i++]);\n"
           "        else out.push_back(b[j++]);\n    }\n"
           "    while (i < a.size()) out.push_back(a[i++]);\n"
           "    while (j < b.size()) out.push_back(b[j++]);\n    return out;\n}\n"),
  },
  {"en": ["One index per list, both starting at 0",
          "Take the smaller head each round and advance only that index",
          "When one list runs out, append the whole remainder of the other"],
   "de": ["Ein Index pro Liste, beide bei 0",
          "Nimm in jeder Runde den kleineren Kopf und erhöh nur diesen Index",
          "Ist eine Liste leer, häng den ganzen Rest der anderen an"]},
  {"en": "LeetCode 21.", "de": "LeetCode 21."},
  complexity="O(n + m)")

# ---------------------------------------------------------------------------
P("m_climb_stairs", "climb_stairs", "Easy", "Dynamic programming",
  Sig([("n", INT)], INT),
  {"en": "Climbing Stairs", "de": "Treppensteigen"},
  {"en": """You climb a staircase of n steps, taking 1 or 2 steps at a time. How many
distinct ways are there to reach the top?

  climb_stairs(2)  -> 2      (1+1, 2)
  climb_stairs(3)  -> 3      (1+1+1, 1+2, 2+1)
  climb_stairs(0)  -> 1      (one way: do nothing)

n goes up to 45, so plain recursion is far too slow. Notice that
ways(n) = ways(n-1) + ways(n-2) — this is Fibonacci wearing a hat. Two rolling
variables are enough; no array needed.""",
   "de": """Du steigst eine Treppe mit n Stufen und nimmst 1 oder 2 Stufen auf einmal. Wie
viele verschiedene Wege gibt es nach oben?

  climb_stairs(2)  -> 2      (1+1, 2)
  climb_stairs(3)  -> 3      (1+1+1, 1+2, 2+1)
  climb_stairs(0)  -> 1      (ein Weg: nichts tun)

n geht bis 45, einfache Rekursion ist also viel zu langsam. Beachte:
wege(n) = wege(n-1) + wege(n-2) — das ist Fibonacci mit Hut. Zwei rollende
Variablen genügen, ein Array brauchst du nicht."""},
  [case(2, 2), case(3, 3), case(0, 1),
   case(1, 1, hidden=True), case(10, 89, hidden=True),
   case(45, 1836311903, hidden=True)],
  {
   "python": ("def climb_stairs(n):\n    a, b = 1, 1\n    for _ in range(n):\n"
              "        a, b = b, a + b\n    return a\n"),
   "javascript": ("function climb_stairs(n) {\n  let a = 1, b = 1;\n"
                  "  for (let i = 0; i < n; i++) {\n    const next = a + b;\n"
                  "    a = b;\n    b = next;\n  }\n  return a;\n}\n"),
   "java": ("class Solution {\n    static long climb_stairs(long n) {\n"
            "        long a = 1, b = 1;\n        for (long i = 0; i < n; i++) {\n"
            "            long next = a + b;\n            a = b;\n            b = next;\n"
            "        }\n        return a;\n    }\n}\n"),
   "csharp": ("public static class Solution\n{\n"
              "    public static long climb_stairs(long n)\n    {\n"
              "        long a = 1, b = 1;\n        for (long i = 0; i < n; i++)\n"
              "        {\n            long next = a + b;\n            a = b;\n"
              "            b = next;\n        }\n        return a;\n    }\n}\n"),
   "go": ("package main\n\nfunc climb_stairs(n int) int {\n\ta, b := 1, 1\n"
          "\tfor i := 0; i < n; i++ {\n\t\ta, b = b, a+b\n\t}\n\treturn a\n}\n"),
   "rust": ("fn climb_stairs(n: i64) -> i64 {\n    let (mut a, mut b) = (1i64, 1i64);\n"
            "    for _ in 0..n {\n        let next = a + b;\n        a = b;\n"
            "        b = next;\n    }\n    a\n}\n"),
   "cpp": ("long long climb_stairs(long long n) {\n    long long a = 1, b = 1;\n"
           "    for (long long i = 0; i < n; ++i) {\n        long long next = a + b;\n"
           "        a = b;\n        b = next;\n    }\n    return a;\n}\n"),
  },
  {"en": ["ways(n) = ways(n-1) + ways(n-2) — you arrived from one or two steps below",
          "Iterate upwards with two rolling variables",
          "n = 0 and n = 1 both have exactly one way"],
   "de": ["wege(n) = wege(n-1) + wege(n-2) — du kamst von einer oder zwei Stufen tiefer",
          "Iterier nach oben mit zwei rollenden Variablen",
          "n = 0 und n = 1 haben beide genau einen Weg"]},
  {"en": "LeetCode 70 — the gateway to every dynamic programming question.",
   "de": "LeetCode 70 — das Eingangstor zu jeder DP-Frage."},
  complexity="O(n) time, O(1) space")

# ---------------------------------------------------------------------------
P("m_longest_common_prefix", "longest_common_prefix", "Easy", "Strings",
  Sig([("words", L(STR))], STR),
  {"en": "Longest Common Prefix", "de": "Längster gemeinsamer Präfix"},
  {"en": """Return the longest string that every word in the list starts with. Return an
empty string if there is none, or if the list is empty.

  longest_common_prefix(["flower", "flow", "flight"]) -> "fl"
  longest_common_prefix(["dog", "racecar", "car"])    -> ""
  longest_common_prefix([])                           -> ""

The answer can never be longer than the shortest word, which bounds the search.""",
   "de": """Gib den längsten String zurück, mit dem jedes Wort der Liste beginnt. Gib einen
leeren String zurück, wenn es keinen gibt oder die Liste leer ist.

  longest_common_prefix(["flower", "flow", "flight"]) -> "fl"
  longest_common_prefix(["dog", "racecar", "car"])    -> ""
  longest_common_prefix([])                           -> ""

Die Antwort kann nie länger als das kürzeste Wort sein — das begrenzt die Suche."""},
  [case(["flower", "flow", "flight"], "fl"),
   case(["dog", "racecar", "car"], ""),
   case([], ""),
   case(["a"], "a", hidden=True),
   case(["", "abc"], "", hidden=True),
   case(["interview", "internal", "internet"], "inter", hidden=True)],
  {
   "python": ("def longest_common_prefix(words):\n    if not words:\n        return ''\n"
              "    prefix = words[0]\n    for word in words:\n        i = 0\n"
              "        while i < len(prefix) and i < len(word) and prefix[i] == word[i]:\n"
              "            i += 1\n        prefix = prefix[:i]\n"
              "        if not prefix:\n            return ''\n    return prefix\n"),
   "javascript": ("function longest_common_prefix(words) {\n"
                  "  if (words.length === 0) return \"\";\n  let prefix = words[0];\n"
                  "  for (const word of words) {\n    let i = 0;\n"
                  "    while (i < prefix.length && i < word.length && prefix[i] === word[i]) i++;\n"
                  "    prefix = prefix.slice(0, i);\n    if (prefix === \"\") return \"\";\n"
                  "  }\n  return prefix;\n}\n"),
   "java": ("class Solution {\n    static String longest_common_prefix(String[] words) {\n"
            "        if (words.length == 0) return \"\";\n"
            "        String prefix = words[0];\n        for (String word : words) {\n"
            "            int i = 0;\n"
            "            while (i < prefix.length() && i < word.length()\n"
            "                   && prefix.charAt(i) == word.charAt(i)) i++;\n"
            "            prefix = prefix.substring(0, i);\n"
            "            if (prefix.isEmpty()) return \"\";\n        }\n"
            "        return prefix;\n    }\n}\n"),
   "csharp": ("public static class Solution\n{\n"
              "    public static string longest_common_prefix(string[] words)\n    {\n"
              "        if (words.Length == 0) return \"\";\n"
              "        string prefix = words[0];\n        foreach (var word in words)\n"
              "        {\n            int i = 0;\n"
              "            while (i < prefix.Length && i < word.Length\n"
              "                   && prefix[i] == word[i]) i++;\n"
              "            prefix = prefix.Substring(0, i);\n"
              "            if (prefix.Length == 0) return \"\";\n        }\n"
              "        return prefix;\n    }\n}\n"),
   "go": ("package main\n\nfunc longest_common_prefix(words []string) string {\n"
          "\tif len(words) == 0 {\n\t\treturn \"\"\n\t}\n\tprefix := words[0]\n"
          "\tfor _, word := range words {\n\t\ti := 0\n"
          "\t\tfor i < len(prefix) && i < len(word) && prefix[i] == word[i] {\n"
          "\t\t\ti++\n\t\t}\n\t\tprefix = prefix[:i]\n\t\tif prefix == \"\" {\n"
          "\t\t\treturn \"\"\n\t\t}\n\t}\n\treturn prefix\n}\n"),
   "rust": ("fn longest_common_prefix(words: &[String]) -> String {\n"
            "    if words.is_empty() { return String::new(); }\n"
            "    let mut prefix: Vec<char> = words[0].chars().collect();\n"
            "    for word in words {\n"
            "        let other: Vec<char> = word.chars().collect();\n"
            "        let mut i = 0;\n"
            "        while i < prefix.len() && i < other.len() && prefix[i] == other[i] {\n"
            "            i += 1;\n        }\n        prefix.truncate(i);\n"
            "        if prefix.is_empty() { return String::new(); }\n    }\n"
            "    prefix.into_iter().collect()\n}\n"),
   "cpp": ("#include <string>\n#include <vector>\n\n"
           "std::string longest_common_prefix(const std::vector<std::string>& words) {\n"
           "    if (words.empty()) return \"\";\n    std::string prefix = words[0];\n"
           "    for (const auto& word : words) {\n        size_t i = 0;\n"
           "        while (i < prefix.size() && i < word.size() && prefix[i] == word[i]) ++i;\n"
           "        prefix = prefix.substr(0, i);\n        if (prefix.empty()) return \"\";\n"
           "    }\n    return prefix;\n}\n"),
  },
  {"en": ["Start with the first word as the candidate prefix",
          "Shrink it against every other word until they all agree",
          "An empty list and an empty word both give an empty answer"],
   "de": ["Fang mit dem ersten Wort als Kandidaten an",
          "Kürz ihn an jedem weiteren Wort, bis alle übereinstimmen",
          "Eine leere Liste und ein leeres Wort ergeben beide eine leere Antwort"]},
  {"en": "LeetCode 14.", "de": "LeetCode 14."},
  complexity="O(total characters)")


# ---------------------------------------------------------------------------
P("m_rotate_array", "rotate_array", "Medium", "Arrays",
  Sig([("nums", L(INT)), ("k", INT)], L(INT)),
  {"en": "Rotate an Array", "de": "Ein Array rotieren"},
  {"en": """Rotate the list k steps to the RIGHT and return the result.

  rotate_array([1, 2, 3, 4, 5, 6, 7], 3) -> [5, 6, 7, 1, 2, 3, 4]
  rotate_array([], 3)                    -> []

k may be larger than the list. Take k modulo the length first — and watch the
empty list, because that modulo would divide by zero.""",
   "de": """Rotier die Liste k Schritte nach RECHTS und gib das Ergebnis zurück.

  rotate_array([1, 2, 3, 4, 5, 6, 7], 3) -> [5, 6, 7, 1, 2, 3, 4]
  rotate_array([], 3)                    -> []

k darf größer als die Liste sein. Nimm k modulo der Länge — und pass bei der
leeren Liste auf, dieses Modulo würde durch null teilen."""},
  [case(([1, 2, 3, 4, 5, 6, 7], 3), [5, 6, 7, 1, 2, 3, 4]),
   case(([], 3), []), case(([1], 0), [1]),
   case(([-1, -100, 3, 99], 2), [3, 99, -1, -100], hidden=True),
   case(([1, 2], 5), [2, 1], hidden=True)],
  {
   "python": ("def rotate_array(nums, k):\n    n = len(nums)\n"
              "    if n == 0:\n        return []\n    k %= n\n"
              "    out = [0] * n\n    for i, value in enumerate(nums):\n"
              "        out[(i + k) % n] = value\n    return out\n"),
   "javascript": ("function rotate_array(nums, k) {\n  const n = nums.length;\n"
                  "  if (n === 0) return [];\n  k = ((k % n) + n) % n;\n"
                  "  const out = new Array(n);\n"
                  "  for (let i = 0; i < n; i++) out[(i + k) % n] = nums[i];\n"
                  "  return out;\n}\n"),
   "java": ("class Solution {\n    static long[] rotate_array(long[] nums, long k) {\n"
            "        int n = nums.length;\n        if (n == 0) return new long[]{};\n"
            "        int shift = (int) (((k % n) + n) % n);\n"
            "        long[] out = new long[n];\n"
            "        for (int i = 0; i < n; i++) out[(i + shift) % n] = nums[i];\n"
            "        return out;\n    }\n}\n"),
   "csharp": ("public static class Solution\n{\n"
              "    public static long[] rotate_array(long[] nums, long k)\n    {\n"
              "        int n = nums.Length;\n        if (n == 0) return new long[]{};\n"
              "        int shift = (int)(((k % n) + n) % n);\n"
              "        var outArr = new long[n];\n"
              "        for (int i = 0; i < n; i++) outArr[(i + shift) % n] = nums[i];\n"
              "        return outArr;\n    }\n}\n"),
   "go": ("package main\n\nfunc rotate_array(nums []int, k int) []int {\n"
          "\tn := len(nums)\n\tif n == 0 {\n\t\treturn []int{}\n\t}\n"
          "\tshift := ((k % n) + n) % n\n\tout := make([]int, n)\n"
          "\tfor i, v := range nums {\n\t\tout[(i+shift)%n] = v\n\t}\n\treturn out\n}\n"),
   "rust": ("fn rotate_array(nums: &[i64], k: i64) -> Vec<i64> {\n"
            "    let n = nums.len();\n    if n == 0 { return Vec::new(); }\n"
            "    let shift = (((k % n as i64) + n as i64) % n as i64) as usize;\n"
            "    let mut out = vec![0i64; n];\n"
            "    for (i, &v) in nums.iter().enumerate() {\n"
            "        out[(i + shift) % n] = v;\n    }\n    out\n}\n"),
   "cpp": ("#include <vector>\n\nstd::vector<long long> rotate_array(\n"
           "        const std::vector<long long>& nums, long long k) {\n"
           "    long long n = (long long)nums.size();\n    if (n == 0) return {};\n"
           "    long long shift = ((k % n) + n) % n;\n"
           "    std::vector<long long> out(nums.size());\n"
           "    for (long long i = 0; i < n; ++i) out[(i + shift) % n] = nums[i];\n"
           "    return out;\n}\n"),
  },
  {"en": ["k %= length collapses the redundant full turns",
          "The value at index i ends up at index (i + k) % length",
          "Handle the empty list before the modulo"],
   "de": ["k %= Länge wirft die überflüssigen vollen Umdrehungen weg",
          "Der Wert an Index i landet an Index (i + k) % Länge",
          "Behandle die leere Liste vor dem Modulo"]},
  {"en": "LeetCode 189 and Codility's CyclicRotation.",
   "de": "LeetCode 189 und Codilitys CyclicRotation."},
  complexity="O(n)")

# ---------------------------------------------------------------------------
P("m_longest_run", "longest_run", "Easy", "Two pointers",
  Sig([("nums", L(INT))], INT),
  {"en": "Longest Run of Equal Values", "de": "Längste Serie gleicher Werte"},
  {"en": """Return the length of the longest streak of IDENTICAL consecutive values.

  longest_run([1, 1, 2, 2, 2, 3]) -> 3
  longest_run([1, 2, 3])          -> 1
  longest_run([])                 -> 0

One pass, one counter, no nested loops.""",
   "de": """Gib die Länge der längsten Serie IDENTISCHER aufeinanderfolgender Werte zurück.

  longest_run([1, 1, 2, 2, 2, 3]) -> 3
  longest_run([1, 2, 3])          -> 1
  longest_run([])                 -> 0

Ein Durchlauf, ein Zähler, keine verschachtelten Schleifen."""},
  [case([1, 1, 2, 2, 2, 3], 3), case([1, 2, 3], 1), case([], 0),
   case([5], 1, hidden=True), case([4, 4, 4, 4], 4, hidden=True),
   case([1, 1, 2, 1, 1, 1], 3, hidden=True)],
  {
   "python": ("def longest_run(nums):\n    if not nums:\n        return 0\n"
              "    best = current = 1\n    for i in range(1, len(nums)):\n"
              "        current = current + 1 if nums[i] == nums[i - 1] else 1\n"
              "        best = max(best, current)\n    return best\n"),
   "javascript": ("function longest_run(nums) {\n  if (nums.length === 0) return 0;\n"
                  "  let best = 1, current = 1;\n"
                  "  for (let i = 1; i < nums.length; i++) {\n"
                  "    current = nums[i] === nums[i - 1] ? current + 1 : 1;\n"
                  "    best = Math.max(best, current);\n  }\n  return best;\n}\n"),
   "java": ("class Solution {\n    static long longest_run(long[] nums) {\n"
            "        if (nums.length == 0) return 0;\n"
            "        long best = 1, current = 1;\n"
            "        for (int i = 1; i < nums.length; i++) {\n"
            "            current = (nums[i] == nums[i - 1]) ? current + 1 : 1;\n"
            "            best = Math.max(best, current);\n        }\n"
            "        return best;\n    }\n}\n"),
   "csharp": ("public static class Solution\n{\n"
              "    public static long longest_run(long[] nums)\n    {\n"
              "        if (nums.Length == 0) return 0;\n"
              "        long best = 1, current = 1;\n"
              "        for (int i = 1; i < nums.Length; i++)\n        {\n"
              "            current = (nums[i] == nums[i - 1]) ? current + 1 : 1;\n"
              "            best = Math.Max(best, current);\n        }\n"
              "        return best;\n    }\n}\n"),
   "go": ("package main\n\nfunc longest_run(nums []int) int {\n"
          "\tif len(nums) == 0 {\n\t\treturn 0\n\t}\n\tbest, current := 1, 1\n"
          "\tfor i := 1; i < len(nums); i++ {\n\t\tif nums[i] == nums[i-1] {\n"
          "\t\t\tcurrent++\n\t\t} else {\n\t\t\tcurrent = 1\n\t\t}\n"
          "\t\tif current > best {\n\t\t\tbest = current\n\t\t}\n\t}\n\treturn best\n}\n"),
   "rust": ("fn longest_run(nums: &[i64]) -> i64 {\n"
            "    if nums.is_empty() { return 0; }\n"
            "    let (mut best, mut current) = (1i64, 1i64);\n"
            "    for i in 1..nums.len() {\n"
            "        current = if nums[i] == nums[i - 1] { current + 1 } else { 1 };\n"
            "        best = best.max(current);\n    }\n    best\n}\n"),
   "cpp": ("#include <algorithm>\n#include <vector>\n\n"
           "long long longest_run(const std::vector<long long>& nums) {\n"
           "    if (nums.empty()) return 0;\n"
           "    long long best = 1, current = 1;\n"
           "    for (size_t i = 1; i < nums.size(); ++i) {\n"
           "        current = (nums[i] == nums[i - 1]) ? current + 1 : 1;\n"
           "        best = std::max(best, current);\n    }\n    return best;\n}\n"),
  },
  {"en": ["Track the current streak and the best streak",
          "If this value equals the previous one, extend; otherwise reset to 1",
          "Update the best on every step"],
   "de": ["Führ die aktuelle Serie und die beste Serie mit",
          "Ist der Wert gleich dem vorherigen, verlängern — sonst auf 1 zurück",
          "Aktualisier das Beste in jedem Schritt"]},
  complexity="O(n)")

# ---------------------------------------------------------------------------
P("m_equilibrium_index", "equilibrium_index", "Medium", "Prefix sums",
  Sig([("nums", L(INT))], INT),
  {"en": "Equilibrium Index", "de": "Gleichgewichtsindex"},
  {"en": """An equilibrium index is a position where everything to its LEFT sums to the
same value as everything to its RIGHT. The element itself counts for neither
side.

Return the SMALLEST such index, or -1 if there is none.

  equilibrium_index([-1, 3, -4, 5, 1, -6, 2, 1]) -> 1
  equilibrium_index([1, 2, 3])                   -> -1
  equilibrium_index([])                          -> -1

Must be O(n): compute the total once, keep a running left sum, and derive the
right side as total - left - current.""",
   "de": """Ein Gleichgewichtsindex ist eine Position, an der alles LINKS davon dieselbe
Summe hat wie alles RECHTS davon. Das Element selbst zählt zu keiner Seite.

Gib den KLEINSTEN solchen Index zurück, oder -1, wenn es keinen gibt.

  equilibrium_index([-1, 3, -4, 5, 1, -6, 2, 1]) -> 1
  equilibrium_index([1, 2, 3])                   -> -1
  equilibrium_index([])                          -> -1

Muss O(n) sein: die Gesamtsumme einmal berechnen, eine laufende linke Summe
mitführen und die rechte Seite als gesamt - links - aktuell ableiten."""},
  [case([-1, 3, -4, 5, 1, -6, 2, 1], 1), case([1, 2, 3], -1), case([], -1),
   case([0], 0, hidden=True), case([1, -1, 0], 2, hidden=True),
   case([2, 0, 2], 1, hidden=True)],
  {
   "python": ("def equilibrium_index(nums):\n    total = sum(nums)\n    left = 0\n"
              "    for i, value in enumerate(nums):\n"
              "        if left == total - left - value:\n            return i\n"
              "        left += value\n    return -1\n"),
   "javascript": ("function equilibrium_index(nums) {\n"
                  "  let total = nums.reduce((a, b) => a + b, 0);\n  let left = 0;\n"
                  "  for (let i = 0; i < nums.length; i++) {\n"
                  "    if (left === total - left - nums[i]) return i;\n"
                  "    left += nums[i];\n  }\n  return -1;\n}\n"),
   "java": ("class Solution {\n    static long equilibrium_index(long[] nums) {\n"
            "        long total = 0;\n        for (long v : nums) total += v;\n"
            "        long left = 0;\n"
            "        for (int i = 0; i < nums.length; i++) {\n"
            "            if (left == total - left - nums[i]) return i;\n"
            "            left += nums[i];\n        }\n        return -1;\n    }\n}\n"),
   "csharp": ("public static class Solution\n{\n"
              "    public static long equilibrium_index(long[] nums)\n    {\n"
              "        long total = 0;\n        foreach (var v in nums) total += v;\n"
              "        long left = 0;\n"
              "        for (int i = 0; i < nums.Length; i++)\n        {\n"
              "            if (left == total - left - nums[i]) return i;\n"
              "            left += nums[i];\n        }\n        return -1;\n    }\n}\n"),
   "go": ("package main\n\nfunc equilibrium_index(nums []int) int {\n\ttotal := 0\n"
          "\tfor _, v := range nums {\n\t\ttotal += v\n\t}\n\tleft := 0\n"
          "\tfor i, v := range nums {\n\t\tif left == total-left-v {\n\t\t\treturn i\n\t\t}\n"
          "\t\tleft += v\n\t}\n\treturn -1\n}\n"),
   "rust": ("fn equilibrium_index(nums: &[i64]) -> i64 {\n"
            "    let total: i64 = nums.iter().sum();\n    let mut left = 0i64;\n"
            "    for (i, &v) in nums.iter().enumerate() {\n"
            "        if left == total - left - v { return i as i64; }\n"
            "        left += v;\n    }\n    -1\n}\n"),
   "cpp": ("#include <vector>\n\n"
           "long long equilibrium_index(const std::vector<long long>& nums) {\n"
           "    long long total = 0;\n    for (long long v : nums) total += v;\n"
           "    long long left = 0;\n"
           "    for (size_t i = 0; i < nums.size(); ++i) {\n"
           "        if (left == total - left - nums[i]) return (long long)i;\n"
           "        left += nums[i];\n    }\n    return -1;\n}\n"),
  },
  {"en": ["total = sum(nums), computed once before the loop",
          "At index i the right side is total - left - nums[i]",
          "Compare first, then add nums[i] to left — in that order"],
   "de": ["gesamt = sum(nums), einmal vor der Schleife berechnet",
          "An Index i ist die rechte Seite gesamt - links - nums[i]",
          "Erst vergleichen, dann nums[i] zu links addieren — in dieser Reihenfolge"]},
  {"en": "Codility's TapeEquilibrium wearing a different hat.",
   "de": "Codilitys TapeEquilibrium mit anderem Hut."},
  complexity="O(n)")

# ---------------------------------------------------------------------------
P("m_binary_gap", "binary_gap", "Medium", "Bit tricks",
  Sig([("n", INT)], INT),
  {"en": "Binary Gap", "de": "Binäre Lücke"},
  {"en": """A binary gap is a run of consecutive ZEROS that is surrounded by a one on BOTH
sides in the binary representation of n.

  binary_gap(9)    -> 2      9 is 1001
  binary_gap(529)  -> 4      529 is 1000010001, gaps of 4 and 3
  binary_gap(20)   -> 1      20 is 10100 — the trailing zero does not count
  binary_gap(15)   -> 0      1111 has no gap
  binary_gap(32)   -> 0      100000 — never closed by another one

Return the length of the longest gap, or 0 if there is none. The trap is the
run of zeros at the end: it is not surrounded, so it does not count.""",
   "de": """Eine binäre Lücke ist eine Folge aufeinanderfolgender NULLEN, die in der
Binärdarstellung von n auf BEIDEN Seiten von einer Eins begrenzt wird.

  binary_gap(9)    -> 2      9 ist 1001
  binary_gap(529)  -> 4      529 ist 1000010001, Lücken von 4 und 3
  binary_gap(20)   -> 1      20 ist 10100 — die letzte Null zählt nicht
  binary_gap(15)   -> 0      1111 hat keine Lücke
  binary_gap(32)   -> 0      100000 — nie von einer weiteren Eins geschlossen

Gib die Länge der längsten Lücke zurück, oder 0. Die Falle ist die Nullfolge am
Ende: sie ist nicht umschlossen und zählt deshalb nicht."""},
  [case(9, 2), case(529, 4), case(20, 1),
   case(15, 0, hidden=True), case(32, 0, hidden=True),
   case(1041, 5, hidden=True), case(1, 0, hidden=True)],
  {
   "python": ("def binary_gap(n):\n    best = current = 0\n    counting = False\n"
              "    while n > 0:\n        bit = n & 1\n        n >>= 1\n"
              "        if bit == 1:\n"
              "            if counting:\n                best = max(best, current)\n"
              "            counting = True\n            current = 0\n"
              "        elif counting:\n            current += 1\n    return best\n"),
   "javascript": ("function binary_gap(n) {\n  let best = 0, current = 0, counting = false;\n"
                  "  while (n > 0) {\n    const bit = n % 2;\n    n = Math.floor(n / 2);\n"
                  "    if (bit === 1) {\n      if (counting) best = Math.max(best, current);\n"
                  "      counting = true;\n      current = 0;\n"
                  "    } else if (counting) current++;\n  }\n  return best;\n}\n"),
   "java": ("class Solution {\n    static long binary_gap(long n) {\n"
            "        long best = 0, current = 0;\n        boolean counting = false;\n"
            "        while (n > 0) {\n            long bit = n & 1L;\n            n >>= 1;\n"
            "            if (bit == 1) {\n"
            "                if (counting) best = Math.max(best, current);\n"
            "                counting = true;\n                current = 0;\n"
            "            } else if (counting) current++;\n        }\n"
            "        return best;\n    }\n}\n"),
   "csharp": ("public static class Solution\n{\n"
              "    public static long binary_gap(long n)\n    {\n"
              "        long best = 0, current = 0;\n        bool counting = false;\n"
              "        while (n > 0)\n        {\n            long bit = n & 1L;\n"
              "            n >>= 1;\n            if (bit == 1)\n            {\n"
              "                if (counting) best = Math.Max(best, current);\n"
              "                counting = true;\n                current = 0;\n"
              "            }\n            else if (counting) current++;\n        }\n"
              "        return best;\n    }\n}\n"),
   "go": ("package main\n\nfunc binary_gap(n int) int {\n\tbest, current := 0, 0\n"
          "\tcounting := false\n\tfor n > 0 {\n\t\tbit := n & 1\n\t\tn >>= 1\n"
          "\t\tif bit == 1 {\n\t\t\tif counting && current > best {\n"
          "\t\t\t\tbest = current\n\t\t\t}\n\t\t\tcounting = true\n\t\t\tcurrent = 0\n"
          "\t\t} else if counting {\n\t\t\tcurrent++\n\t\t}\n\t}\n\treturn best\n}\n"),
   "rust": ("fn binary_gap(n: i64) -> i64 {\n    let mut n = n;\n"
            "    let (mut best, mut current) = (0i64, 0i64);\n    let mut counting = false;\n"
            "    while n > 0 {\n        let bit = n & 1;\n        n >>= 1;\n"
            "        if bit == 1 {\n            if counting { best = best.max(current); }\n"
            "            counting = true;\n            current = 0;\n"
            "        } else if counting {\n            current += 1;\n        }\n    }\n"
            "    best\n}\n"),
   "cpp": ("#include <algorithm>\n\nlong long binary_gap(long long n) {\n"
           "    long long best = 0, current = 0;\n    bool counting = false;\n"
           "    while (n > 0) {\n        long long bit = n & 1LL;\n        n >>= 1;\n"
           "        if (bit == 1) {\n            if (counting) best = std::max(best, current);\n"
           "            counting = true;\n            current = 0;\n"
           "        } else if (counting) {\n            current++;\n        }\n    }\n"
           "    return best;\n}\n"),
  },
  {"en": ["Walk the bits with n & 1 and n >>= 1",
          "Only start counting zeros AFTER you have seen your first one",
          "A run only counts when another one closes it"],
   "de": ["Lauf über die Bits mit n & 1 und n >>= 1",
          "Fang erst NACH der ersten Eins an, Nullen zu zählen",
          "Eine Folge zählt nur, wenn eine weitere Eins sie schließt"]},
  {"en": "Codility Lesson 1 — the first task most people meet there.",
   "de": "Codility Lektion 1 — die erste Aufgabe, der man dort begegnet."},
  complexity="O(log n)")

# ---------------------------------------------------------------------------
P("m_passing_cars", "passing_cars", "Medium", "Prefix sums",
  Sig([("a", L(INT))], INT),
  {"en": "Passing Cars", "de": "Sich begegnende Autos"},
  {"en": """The list holds only 0s and 1s: 0 is a car driving EAST, 1 is a car driving
WEST. A pair (P, Q) passes each other when P < Q, a[P] is 0 and a[Q] is 1.

Return how many such pairs there are.

  passing_cars([0, 1, 0, 1, 1]) -> 5
  passing_cars([1, 1, 1])       -> 0
  passing_cars([])              -> 0

Counting every pair is O(n^2). Sweep once instead: keep a running count of the
0s seen so far, and every time you meet a 1 it pairs with all of them at once.""",
   "de": """Die Liste enthält nur 0 und 1: 0 ist ein Auto Richtung OSTEN, 1 eines Richtung
WESTEN. Ein Paar (P, Q) begegnet sich, wenn P < Q, a[P] gleich 0 und a[Q]
gleich 1 ist.

Gib zurück, wie viele solche Paare es gibt.

  passing_cars([0, 1, 0, 1, 1]) -> 5
  passing_cars([1, 1, 1])       -> 0
  passing_cars([])              -> 0

Jedes Paar zu zählen ist O(n^2). Lauf stattdessen einmal durch: zähl die bisher
gesehenen 0en mit, und jede 1 bildet auf einen Schlag mit allen davon ein Paar."""},
  [case([0, 1, 0, 1, 1], 5), case([1, 1, 1], 0), case([], 0),
   case([0, 0, 0], 0, hidden=True), case([0, 1], 1, hidden=True),
   case([0, 0, 1, 1], 4, hidden=True)],
  {
   "python": ("def passing_cars(a):\n    east = 0\n    pairs = 0\n    for value in a:\n"
              "        if value == 0:\n            east += 1\n"
              "        else:\n            pairs += east\n    return pairs\n"),
   "javascript": ("function passing_cars(a) {\n  let east = 0, pairs = 0;\n"
                  "  for (const value of a) {\n    if (value === 0) east++;\n"
                  "    else pairs += east;\n  }\n  return pairs;\n}\n"),
   "java": ("class Solution {\n    static long passing_cars(long[] a) {\n"
            "        long east = 0, pairs = 0;\n        for (long v : a) {\n"
            "            if (v == 0) east++;\n            else pairs += east;\n        }\n"
            "        return pairs;\n    }\n}\n"),
   "csharp": ("public static class Solution\n{\n"
              "    public static long passing_cars(long[] a)\n    {\n"
              "        long east = 0, pairs = 0;\n        foreach (var v in a)\n"
              "        {\n            if (v == 0) east++;\n            else pairs += east;\n"
              "        }\n        return pairs;\n    }\n}\n"),
   "go": ("package main\n\nfunc passing_cars(a []int) int {\n\teast, pairs := 0, 0\n"
          "\tfor _, v := range a {\n\t\tif v == 0 {\n\t\t\teast++\n\t\t} else {\n"
          "\t\t\tpairs += east\n\t\t}\n\t}\n\treturn pairs\n}\n"),
   "rust": ("fn passing_cars(a: &[i64]) -> i64 {\n"
            "    let (mut east, mut pairs) = (0i64, 0i64);\n    for &v in a {\n"
            "        if v == 0 { east += 1; } else { pairs += east; }\n    }\n    pairs\n}\n"),
   "cpp": ("#include <vector>\n\nlong long passing_cars(const std::vector<long long>& a) {\n"
           "    long long east = 0, pairs = 0;\n    for (long long v : a) {\n"
           "        if (v == 0) east++;\n        else pairs += east;\n    }\n"
           "    return pairs;\n}\n"),
  },
  {"en": ["Sweep left to right counting the 0s you have passed",
          "Every 1 pairs with all of those 0s at once",
          "This 'how many of the other kind came before' shape is worth remembering"],
   "de": ["Lauf von links nach rechts und zähl die passierten 0en",
          "Jede 1 bildet mit all diesen 0en auf einmal ein Paar",
          "Dieses Muster 'wie viele der anderen Sorte kamen davor' lohnt sich zu merken"]},
  {"en": "Codility Lesson 5.", "de": "Codility Lektion 5."},
  complexity="O(n)")

# ---------------------------------------------------------------------------
P("m_min_subarray_len", "min_subarray_len", "Medium", "Sliding window",
  Sig([("target", INT), ("nums", L(INT))], INT),
  {"en": "Minimum Size Subarray Sum", "de": "Kürzestes Teilarray mit Mindestsumme"},
  {"en": """Return the length of the SHORTEST contiguous subarray whose sum is at least
target. Return 0 if no such subarray exists. All values are positive.

  min_subarray_len(7, [2, 3, 1, 2, 4, 3]) -> 2      ([4, 3])
  min_subarray_len(11, [1, 1, 1])         -> 0
  min_subarray_len(4, [1, 4, 4])          -> 1

Grow a window to the right while the sum is too small, then shrink it from the
left while it is still valid. Every index enters and leaves once, so despite the
inner loop the whole thing is O(n).""",
   "de": """Gib die Länge des KÜRZESTEN zusammenhängenden Teilarrays zurück, dessen Summe
mindestens target beträgt. Gib 0 zurück, wenn es keines gibt. Alle Werte sind
positiv.

  min_subarray_len(7, [2, 3, 1, 2, 4, 3]) -> 2      ([4, 3])
  min_subarray_len(11, [1, 1, 1])         -> 0
  min_subarray_len(4, [1, 4, 4])          -> 1

Lass ein Fenster nach rechts wachsen, solange die Summe zu klein ist, und
schrumpf es dann von links, solange es noch gültig bleibt. Jeder Index kommt
einmal rein und einmal raus — trotz innerer Schleife ist das Ganze O(n)."""},
  [case((7, [2, 3, 1, 2, 4, 3]), 2), case((11, [1, 1, 1]), 0),
   case((4, [1, 4, 4]), 1),
   case((1, []), 0, hidden=True),
   case((11, [1, 2, 3, 4, 5]), 3, hidden=True),
   case((15, [1, 2, 3, 4, 5]), 5, hidden=True)],
  {
   "python": ("def min_subarray_len(target, nums):\n    left = 0\n    total = 0\n"
              "    best = 0\n    for right, value in enumerate(nums):\n"
              "        total += value\n        while total >= target:\n"
              "            length = right - left + 1\n"
              "            if best == 0 or length < best:\n                best = length\n"
              "            total -= nums[left]\n            left += 1\n    return best\n"),
   "javascript": ("function min_subarray_len(target, nums) {\n"
                  "  let left = 0, total = 0, best = 0;\n"
                  "  for (let right = 0; right < nums.length; right++) {\n"
                  "    total += nums[right];\n    while (total >= target) {\n"
                  "      const length = right - left + 1;\n"
                  "      if (best === 0 || length < best) best = length;\n"
                  "      total -= nums[left++];\n    }\n  }\n  return best;\n}\n"),
   "java": ("class Solution {\n    static long min_subarray_len(long target, long[] nums) {\n"
            "        int left = 0;\n        long total = 0, best = 0;\n"
            "        for (int right = 0; right < nums.length; right++) {\n"
            "            total += nums[right];\n            while (total >= target) {\n"
            "                long length = right - left + 1;\n"
            "                if (best == 0 || length < best) best = length;\n"
            "                total -= nums[left++];\n            }\n        }\n"
            "        return best;\n    }\n}\n"),
   "csharp": ("public static class Solution\n{\n"
              "    public static long min_subarray_len(long target, long[] nums)\n    {\n"
              "        int left = 0;\n        long total = 0, best = 0;\n"
              "        for (int right = 0; right < nums.Length; right++)\n        {\n"
              "            total += nums[right];\n            while (total >= target)\n"
              "            {\n                long length = right - left + 1;\n"
              "                if (best == 0 || length < best) best = length;\n"
              "                total -= nums[left++];\n            }\n        }\n"
              "        return best;\n    }\n}\n"),
   "go": ("package main\n\nfunc min_subarray_len(target int, nums []int) int {\n"
          "\tleft, total, best := 0, 0, 0\n\tfor right, v := range nums {\n"
          "\t\ttotal += v\n\t\tfor total >= target {\n\t\t\tlength := right - left + 1\n"
          "\t\t\tif best == 0 || length < best {\n\t\t\t\tbest = length\n\t\t\t}\n"
          "\t\t\ttotal -= nums[left]\n\t\t\tleft++\n\t\t}\n\t}\n\treturn best\n}\n"),
   "rust": ("fn min_subarray_len(target: i64, nums: &[i64]) -> i64 {\n"
            "    let mut left = 0usize;\n    let mut total = 0i64;\n    let mut best = 0i64;\n"
            "    for right in 0..nums.len() {\n        total += nums[right];\n"
            "        while total >= target {\n"
            "            let length = (right - left + 1) as i64;\n"
            "            if best == 0 || length < best { best = length; }\n"
            "            total -= nums[left];\n            left += 1;\n        }\n    }\n"
            "    best\n}\n"),
   "cpp": ("#include <vector>\n\n"
           "long long min_subarray_len(long long target, const std::vector<long long>& nums) {\n"
           "    size_t left = 0;\n    long long total = 0, best = 0;\n"
           "    for (size_t right = 0; right < nums.size(); ++right) {\n"
           "        total += nums[right];\n        while (total >= target) {\n"
           "            long long length = (long long)(right - left + 1);\n"
           "            if (best == 0 || length < best) best = length;\n"
           "            total -= nums[left++];\n        }\n    }\n    return best;\n}\n"),
  },
  {"en": ["Grow with the right index, shrink with the left one",
          "Record the length while the window is still valid, before shrinking",
          "best stays 0 if the window is never large enough"],
   "de": ["Wachsen mit dem rechten Index, schrumpfen mit dem linken",
          "Notier die Länge, solange das Fenster gültig ist — vor dem Schrumpfen",
          "best bleibt 0, wenn das Fenster nie groß genug wird"]},
  {"en": "LeetCode 209 — the variable-size sliding window template.",
   "de": "LeetCode 209 — die Vorlage für das Schiebefenster mit variabler Größe."},
  complexity="O(n)")

# ---------------------------------------------------------------------------
P("m_count_primes", "count_primes", "Medium", "Math",
  Sig([("n", INT)], INT),
  {"en": "Count the Primes", "de": "Primzahlen zählen"},
  {"en": """Count how many prime numbers are strictly LESS than n.

  count_primes(10)  -> 4      (2, 3, 5, 7)
  count_primes(2)   -> 0
  count_primes(0)   -> 0

Testing each number for primality on its own is too slow. Use the Sieve of
Eratosthenes: mark every multiple of each prime as composite, and only start
crossing out at p*p because everything below that is already crossed.""",
   "de": """Zähl, wie viele Primzahlen echt KLEINER als n sind.

  count_primes(10)  -> 4      (2, 3, 5, 7)
  count_primes(2)   -> 0
  count_primes(0)   -> 0

Jede Zahl einzeln auf Primalität zu prüfen ist zu langsam. Nimm das Sieb des
Eratosthenes: streich jedes Vielfache einer Primzahl als zusammengesetzt an, und
fang erst bei p*p an zu streichen — alles darunter ist schon gestrichen."""},
  [case(10, 4), case(2, 0), case(0, 0),
   case(3, 1, hidden=True), case(100, 25, hidden=True),
   case(1000, 168, hidden=True)],
  {
   "python": ("def count_primes(n):\n    if n < 3:\n        return 0\n"
              "    sieve = [True] * n\n    sieve[0] = sieve[1] = False\n"
              "    p = 2\n    while p * p < n:\n"
              "        if sieve[p]:\n"
              "            for multiple in range(p * p, n, p):\n"
              "                sieve[multiple] = False\n        p += 1\n"
              "    return sum(1 for value in sieve if value)\n"),
   "javascript": ("function count_primes(n) {\n  if (n < 3) return 0;\n"
                  "  const sieve = new Array(n).fill(true);\n"
                  "  sieve[0] = false; sieve[1] = false;\n"
                  "  for (let p = 2; p * p < n; p++) {\n    if (!sieve[p]) continue;\n"
                  "    for (let m = p * p; m < n; m += p) sieve[m] = false;\n  }\n"
                  "  return sieve.filter(Boolean).length;\n}\n"),
   "java": ("class Solution {\n    static long count_primes(long n) {\n"
            "        if (n < 3) return 0;\n        int size = (int) n;\n"
            "        boolean[] composite = new boolean[size];\n"
            "        long count = 0;\n"
            "        for (int p = 2; p < size; p++) {\n"
            "            if (composite[p]) continue;\n            count++;\n"
            "            if ((long) p * p >= size) continue;\n"
            "            for (int m = p * p; m < size; m += p) composite[m] = true;\n"
            "        }\n        return count;\n    }\n}\n"),
   "csharp": ("public static class Solution\n{\n"
              "    public static long count_primes(long n)\n    {\n"
              "        if (n < 3) return 0;\n        int size = (int)n;\n"
              "        var composite = new bool[size];\n        long count = 0;\n"
              "        for (int p = 2; p < size; p++)\n        {\n"
              "            if (composite[p]) continue;\n            count++;\n"
              "            if ((long)p * p >= size) continue;\n"
              "            for (int m = p * p; m < size; m += p) composite[m] = true;\n"
              "        }\n        return count;\n    }\n}\n"),
   "go": ("package main\n\nfunc count_primes(n int) int {\n\tif n < 3 {\n\t\treturn 0\n\t}\n"
          "\tcomposite := make([]bool, n)\n\tcount := 0\n"
          "\tfor p := 2; p < n; p++ {\n\t\tif composite[p] {\n\t\t\tcontinue\n\t\t}\n"
          "\t\tcount++\n\t\tif p*p >= n {\n\t\t\tcontinue\n\t\t}\n"
          "\t\tfor m := p * p; m < n; m += p {\n\t\t\tcomposite[m] = true\n\t\t}\n\t}\n"
          "\treturn count\n}\n"),
   "rust": ("fn count_primes(n: i64) -> i64 {\n    if n < 3 { return 0; }\n"
            "    let size = n as usize;\n    let mut composite = vec![false; size];\n"
            "    let mut count = 0i64;\n    for p in 2..size {\n"
            "        if composite[p] { continue; }\n        count += 1;\n"
            "        if p * p >= size { continue; }\n"
            "        let mut m = p * p;\n        while m < size {\n"
            "            composite[m] = true;\n            m += p;\n        }\n    }\n"
            "    count\n}\n"),
   "cpp": ("#include <vector>\n\nlong long count_primes(long long n) {\n"
           "    if (n < 3) return 0;\n    size_t size = (size_t)n;\n"
           "    std::vector<bool> composite(size, false);\n    long long count = 0;\n"
           "    for (size_t p = 2; p < size; ++p) {\n"
           "        if (composite[p]) continue;\n        count++;\n"
           "        if (p * p >= size) continue;\n"
           "        for (size_t m = p * p; m < size; m += p) composite[m] = true;\n"
           "    }\n    return count;\n}\n"),
  },
  {"en": ["Allocate a boolean array of size n and cross out the composites",
          "Start crossing out at p*p, not at 2*p",
          "Anything still unmarked when you reach it is prime"],
   "de": ["Leg ein Boolean-Array der Größe n an und streich die zusammengesetzten",
          "Fang bei p*p an zu streichen, nicht bei 2*p",
          "Was beim Erreichen noch unmarkiert ist, ist prim"]},
  {"en": "LeetCode 204. The sieve is worth knowing by heart.",
   "de": "LeetCode 204. Das Sieb sollte man auswendig können."},
  complexity="O(n log log n)")

# ---------------------------------------------------------------------------
P("m_transpose", "transpose", "Medium", "Matrix",
  Sig([("grid", L(L(INT)))], L(L(INT))),
  {"en": "Transpose a Matrix", "de": "Eine Matrix transponieren"},
  {"en": """Return the transposed grid: rows become columns and columns become rows.

  transpose([[1, 2, 3], [4, 5, 6]]) -> [[1, 4], [2, 5], [3, 6]]
  transpose([[1]])                  -> [[1]]
  transpose([])                     -> []

The input is rectangular. The result has one row per input column, so watch the
dimensions: an r-by-c grid becomes c-by-r.""",
   "de": """Gib das transponierte Gitter zurück: Zeilen werden zu Spalten und Spalten zu
Zeilen.

  transpose([[1, 2, 3], [4, 5, 6]]) -> [[1, 4], [2, 5], [3, 6]]
  transpose([[1]])                  -> [[1]]
  transpose([])                     -> []

Die Eingabe ist rechteckig. Das Ergebnis hat eine Zeile pro Eingabespalte — pass
also auf die Maße auf: aus r-mal-c wird c-mal-r."""},
  [case([[1, 2, 3], [4, 5, 6]], [[1, 4], [2, 5], [3, 6]]),
   case([[1]], [[1]]), case([], []),
   case([[1, 2], [3, 4]], [[1, 3], [2, 4]], hidden=True),
   case([[7], [8], [9]], [[7, 8, 9]], hidden=True)],
  {
   "python": ("def transpose(grid):\n    return [list(column) for column in zip(*grid)]\n"),
   "javascript": ("function transpose(grid) {\n  if (grid.length === 0) return [];\n"
                  "  return grid[0].map((_, c) => grid.map(row => row[c]));\n}\n"),
   "java": ("class Solution {\n    static long[][] transpose(long[][] grid) {\n"
            "        if (grid.length == 0) return new long[][]{};\n"
            "        int rows = grid.length, cols = grid[0].length;\n"
            "        long[][] out = new long[cols][rows];\n"
            "        for (int r = 0; r < rows; r++)\n"
            "            for (int c = 0; c < cols; c++)\n"
            "                out[c][r] = grid[r][c];\n        return out;\n    }\n}\n"),
   "csharp": ("public static class Solution\n{\n"
              "    public static long[][] transpose(long[][] grid)\n    {\n"
              "        if (grid.Length == 0) return new long[][]{};\n"
              "        int rows = grid.Length, cols = grid[0].Length;\n"
              "        var outArr = new long[cols][];\n"
              "        for (int c = 0; c < cols; c++)\n        {\n"
              "            outArr[c] = new long[rows];\n"
              "            for (int r = 0; r < rows; r++) outArr[c][r] = grid[r][c];\n"
              "        }\n        return outArr;\n    }\n}\n"),
   "go": ("package main\n\nfunc transpose(grid [][]int) [][]int {\n"
          "\tif len(grid) == 0 {\n\t\treturn [][]int{}\n\t}\n"
          "\trows, cols := len(grid), len(grid[0])\n\tout := make([][]int, cols)\n"
          "\tfor c := 0; c < cols; c++ {\n\t\tout[c] = make([]int, rows)\n"
          "\t\tfor r := 0; r < rows; r++ {\n\t\t\tout[c][r] = grid[r][c]\n\t\t}\n\t}\n"
          "\treturn out\n}\n"),
   "rust": ("fn transpose(grid: &[Vec<i64>]) -> Vec<Vec<i64>> {\n"
            "    if grid.is_empty() { return Vec::new(); }\n"
            "    let (rows, cols) = (grid.len(), grid[0].len());\n"
            "    let mut out = vec![vec![0i64; rows]; cols];\n"
            "    for r in 0..rows {\n        for c in 0..cols {\n"
            "            out[c][r] = grid[r][c];\n        }\n    }\n    out\n}\n"),
   "cpp": ("#include <vector>\n\nstd::vector<std::vector<long long>> transpose(\n"
           "        const std::vector<std::vector<long long>>& grid) {\n"
           "    if (grid.empty()) return {};\n"
           "    size_t rows = grid.size(), cols = grid[0].size();\n"
           "    std::vector<std::vector<long long>> out(cols,\n"
           "        std::vector<long long>(rows));\n"
           "    for (size_t r = 0; r < rows; ++r)\n"
           "        for (size_t c = 0; c < cols; ++c)\n"
           "            out[c][r] = grid[r][c];\n    return out;\n}\n"),
  },
  {"en": ["out[c][r] = grid[r][c] — that single line is the whole operation",
          "Allocate the result with the swapped dimensions first",
          "An empty grid gives an empty result, before you touch grid[0]"],
   "de": ["out[c][r] = grid[r][c] — diese eine Zeile ist die ganze Operation",
          "Leg das Ergebnis zuerst mit vertauschten Maßen an",
          "Ein leeres Gitter ergibt ein leeres Ergebnis — noch vor dem Zugriff auf grid[0]"]},
  {"en": "LeetCode 867.", "de": "LeetCode 867."},
  complexity="O(rows * cols)")


# ---------------------------------------------------------------------------
TOPICS: list[str] = sorted({p.topic for p in BANK})
DIFFICULTIES = ["Easy", "Medium", "Hard"]


def by_id(pid: str) -> MultiProblem | None:
    for problem in BANK:
        if problem.id == pid:
            return problem
    return None


def for_language(language_id: str) -> list[MultiProblem]:
    return [p for p in BANK if p.supports(language_id)]


def filtered(language_id: str, topic: str = "All topics", difficulty: str = "Any",
             query: str = "") -> list[MultiProblem]:
    out = for_language(language_id)
    if topic and topic != "All topics":
        out = [p for p in out if p.topic == topic]
    if difficulty and difficulty != "Any":
        out = [p for p in out if p.difficulty == difficulty]
    if query:
        needle = query.lower()

        def matches(problem: MultiProblem) -> bool:
            parts = list(problem.title.values()) + list(problem.statement.values())
            parts += [problem.topic, i18n.topic(problem.topic)]
            return any(needle in part.lower() for part in parts if part)

        out = [p for p in out if matches(p)]
    return out
