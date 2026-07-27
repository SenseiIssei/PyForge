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
