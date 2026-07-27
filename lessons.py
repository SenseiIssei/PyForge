"""The 'Learn' curriculum: 22 lessons, each = theory + runnable example + exercise."""
from __future__ import annotations

import copy
from dataclasses import dataclass, field

import i18n
import lessons_de
from tasks import Task, case


@dataclass
class Lesson:
    id: str
    title: str
    section: str
    theory: str
    example: str
    task: Task
    takeaway: str = ""


def _t(lid, title, func, statement, starter, cases, hints, solution, topic,
       checker_src: str = "") -> Task:
    return Task(id=f"lesson_{lid}", title=title, func=func, statement=statement,
                starter=starter, cases=cases, hints=hints, solution=solution,
                difficulty="Easy", topic=topic, source="lesson",
                checker_src=checker_src)


STACK_CHECKER = '''
def check(args, got):
    items = list(args[0])
    if got is None:
        return False
    for name in ("push", "pop", "peek", "size"):
        if not callable(getattr(got, name, None)):
            return False
    if got.size() != len(items):
        return False
    if items:
        if got.peek() != items[-1]:
            return False
        if got.size() != len(items):      # peek must not remove anything
            return False
        if got.pop() != items[-1]:
            return False
        if got.size() != len(items) - 1:
            return False
    else:
        if got.peek() is not None or got.pop() is not None:
            return False
    got.push("sentinel")
    return got.peek() == "sentinel" and got.size() == max(0, len(items) - 1) + 1
'''


LESSONS: list[Lesson] = [

# ============================================================ 1. FOUNDATIONS
Lesson(
    id="vars", section="Foundations", title="Variables & types",
    theory="""Python has no type declarations. A variable is just a name pointing at an object,
and the object knows its own type.

    age = 30            # int
    price = 4.99        # float
    name = "Ada"        # str
    is_ready = True     # bool  (capital T / F!)
    nothing = None      # the "no value" object

Useful things you will use constantly:
  * type(x)      -> the type of x
  * int("42")    -> convert text to a number
  * str(42)      -> convert a number to text
  * f-strings    -> f"{name} is {age}" builds text with values inside

Integer division and remainder come up in every interview:
  7 / 2  -> 3.5     (true division, always a float)
  7 // 2 -> 3       (floor division)
  7 %  2 -> 1       (remainder — the key to even/odd and cyclic problems)
  2 ** 10 -> 1024   (power)

Names are snake_case, constants are SHOUTING_CASE. Python cares about that
socially, not technically.""",
    example='''name = "Ada"
age = 36
height = 1.68
likes_python = True

print(f"{name} is {age} years old and {height} m tall.")
print("type of age:", type(age))
print("age as text:", str(age) + " years")

print("7 / 2  =", 7 / 2)
print("7 // 2 =", 7 // 2)
print("7 % 2  =", 7 % 2)
print("2 ** 10 =", 2 ** 10)

# multiple assignment / swapping without a temp variable
a, b = 1, 2
a, b = b, a
print("swapped:", a, b)
''',
    takeaway="A variable is a label on an object. % and // are your interview workhorses.",
    task=_t("vars", "Seconds to clock", "to_clock",
            """Write to_clock(seconds) that turns a number of seconds into a "H:MM:SS" string.

Rules:
  * hours have no leading zero, minutes and seconds always have two digits
  * to_clock(3661) -> "1:01:01"
  * to_clock(59)   -> "0:00:59"

Hint: // gives you whole units, % gives you the leftovers.""",
            'def to_clock(seconds):\n    # your code here\n    pass\n',
            [case(3661, "1:01:01"), case(59, "0:00:59"), case(0, "0:00:00"),
             case(86399, "23:59:59", hidden=True), case(600, "0:10:00", hidden=True),
             case(45296, "12:34:56", hidden=True)],
            ["hours = seconds // 3600", "minutes = (seconds % 3600) // 60",
             'f-strings can pad: f"{m:02d}" gives "07" for 7'],
            'def to_clock(seconds):\n    hours = seconds // 3600\n    minutes = (seconds % 3600) // 60\n'
            '    secs = seconds % 60\n    return f"{hours}:{minutes:02d}:{secs:02d}"\n',
            "Basics"),
),

Lesson(
    id="strings", section="Foundations", title="Strings",
    theory="""Strings are immutable sequences of characters. Every "modifying" method returns a
NEW string.

    s = "  Hello, World  "
    s.strip()          -> "Hello, World"
    s.lower()          -> "  hello, world  "
    s.replace("l","L") -> new string
    s.split(",")       -> ['  Hello', ' World  ']
    ",".join(parts)    -> glue a list back together
    s.startswith("H"), s.endswith("d"), "World" in s

Indexing and slicing (this is the single most useful Python skill):

    s[0]      first character
    s[-1]     last character
    s[2:5]    characters 2,3,4      (start included, stop excluded)
    s[:3]     first three
    s[3:]     everything from 3 on
    s[::-1]   the whole thing reversed

Building a string in a loop with += is O(n^2). Collect pieces in a list and
"".join(them) instead — interviewers notice.""",
    example='''s = "  Hello, Python World  "

print(repr(s.strip()))
print(s.strip().lower())
print(s.strip().split())
print("-".join(["a", "b", "c"]))

word = "interview"
print("first:", word[0], "| last:", word[-1])
print("slice 2:5 ->", word[2:5])
print("reversed ->", word[::-1])
print("every 2nd ->", word[::2])

print("is 'view' inside?", "view" in word)
print("count of 'e':", word.count("e"))

# efficient string building
parts = []
for i in range(5):
    parts.append(str(i * i))
print(", ".join(parts))
''',
    takeaway="Strings are immutable. Slice with [start:stop:step]. Join, don't +=.",
    task=_t("strings", "Normalise a name", "normalise",
            """Write normalise(text) that cleans up a messy full name:

  * strip whitespace at both ends
  * collapse multiple inner spaces into one
  * capitalise every word (first letter upper, rest lower)

normalise("  aDA   LOVElace ") -> "Ada Lovelace"

Hint: text.split() with no argument already splits on any run of whitespace.""",
            'def normalise(text):\n    # your code here\n    pass\n',
            [case("  aDA   LOVElace ", "Ada Lovelace"),
             case("guido van ROSSUM", "Guido Van Rossum"),
             case("   ", ""),
             case("gRaCe   hopper", "Grace Hopper", hidden=True),
             case("a", "A", hidden=True),
             case("  linus     TORVALDS  ", "Linus Torvalds", hidden=True)],
            ["words = text.split() removes all the extra whitespace for you",
             "word.capitalize() upper-cases the first letter and lowers the rest",
             'return " ".join(...)'],
            'def normalise(text):\n    words = text.split()\n'
            '    return " ".join(word.capitalize() for word in words)\n',
            "Strings"),
),

Lesson(
    id="lists", section="Foundations", title="Lists",
    theory="""A list is an ordered, mutable sequence. It is the default container in Python.

    nums = [3, 1, 4, 1, 5]
    nums.append(9)        add to the end                 O(1)
    nums.pop()            remove & return the last       O(1)
    nums.pop(0)           remove & return the first      O(n)  <- careful!
    nums.insert(0, 7)     insert at front                O(n)
    nums.remove(1)        remove the FIRST value 1       O(n)
    len(nums), sum(nums), min(nums), max(nums)
    nums.sort()           sorts in place, returns None
    sorted(nums)          returns a NEW sorted list
    nums[::-1]            reversed copy

The classic beginner trap:

    a = [1, 2, 3]
    b = a          # b is the SAME list, not a copy
    b.append(4)    # a is now [1, 2, 3, 4] too!
    c = a[:]       # this IS a copy (or a.copy() / list(a))

Sorting with a key is interview bread and butter:

    people.sort(key=lambda p: p[1])            by second element
    words.sort(key=len, reverse=True)          longest first
    items.sort(key=lambda x: (-x.score, x.name))  score desc, then name asc""",
    example='''nums = [3, 1, 4, 1, 5, 9, 2, 6]

print("length:", len(nums), "| sum:", sum(nums), "| max:", max(nums))
nums.append(5)
print("after append:", nums)
print("popped:", nums.pop(), "->", nums)

print("sorted copy:", sorted(nums))
print("original still:", nums)
nums.sort()
print("sorted in place:", nums)

words = ["pear", "fig", "banana", "kiwi"]
words.sort(key=len)
print("by length:", words)
words.sort(key=lambda w: (-len(w), w))
print("long->short, then a-z:", words)

# aliasing vs copying
a = [1, 2, 3]
alias, copy = a, a[:]
alias.append(99)
print("a:", a, "| copy:", copy)
''',
    takeaway="Lists are mutable and shared by reference. sort() mutates, sorted() copies.",
    task=_t("lists", "Second largest", "second_largest",
            """Write second_largest(nums) that returns the second largest DISTINCT value in a list.

  second_largest([3, 1, 4, 4, 5]) -> 4
  second_largest([7, 7, 7])       -> None   (there is no second distinct value)

Return None if the list has fewer than two distinct values.""",
            'def second_largest(nums):\n    # your code here\n    pass\n',
            [case([3, 1, 4, 4, 5], 4), case([7, 7, 7], None), case([2, 1], 1),
             case([10], None, hidden=True), case([], None, hidden=True),
             case([-5, -2, -9, -2], -5, hidden=True),
             case([1, 2, 3, 4, 5, 6], 5, hidden=True)],
            ["set(nums) throws away the duplicates",
             "sorted(...) then take index -2",
             "Guard the short case first: if len(distinct) < 2: return None"],
            'def second_largest(nums):\n    distinct = sorted(set(nums))\n'
            '    if len(distinct) < 2:\n        return None\n    return distinct[-2]\n',
            "Lists"),
),

Lesson(
    id="control", section="Foundations", title="if / else & loops",
    theory="""Indentation IS the block. Four spaces, always.

    if score >= 90:
        grade = "A"
    elif score >= 80:
        grade = "B"
    else:
        grade = "C"

Loop over the ITEMS, not the indices, whenever you can:

    for word in words:            # good
    for i in range(len(words)):   # only when you truly need i
    for i, word in enumerate(words):        # index AND item
    for name, score in zip(names, scores):  # two lists in lockstep

while loops run until a condition flips:

    while low <= high:            # binary search shape
        ...

Loop control:
    break      leave the loop right now
    continue   skip to the next iteration
    for...else the else runs only if the loop was NOT broken out of

range(start, stop, step) — stop is exclusive:
    range(5)        0 1 2 3 4
    range(2, 8, 2)  2 4 6
    range(5, 0, -1) 5 4 3 2 1""",
    example='''scores = [92, 78, 85, 61, 99]
names = ["Ada", "Linus", "Grace", "Guido", "Hedy"]

for name, score in zip(names, scores):
    if score >= 90:
        grade = "A"
    elif score >= 80:
        grade = "B"
    else:
        grade = "C"
    print(f"{name:<6} {score:>3}  {grade}")

print("---")
for i, name in enumerate(names, start=1):
    print(i, name)

print("--- first score above 95")
for score in scores:
    if score > 95:
        print("found", score)
        break
else:
    print("none found")

n, steps = 27, 0
while n != 1:                 # Collatz
    n = n // 2 if n % 2 == 0 else 3 * n + 1
    steps += 1
print("collatz steps for 27:", steps)
''',
    takeaway="Iterate over items; reach for enumerate/zip before range(len(x)).",
    task=_t("control", "FizzBuzz, returned not printed", "fizzbuzz",
            """The classic — but return a LIST instead of printing.

fizzbuzz(n) returns a list for the numbers 1..n where:
  * multiples of 3 and 5 -> "FizzBuzz"
  * multiples of 3       -> "Fizz"
  * multiples of 5       -> "Buzz"
  * everything else      -> the number itself, as an int

fizzbuzz(5) -> [1, 2, "Fizz", 4, "Buzz"]

Check the 15-case FIRST, or it can never happen.""",
            'def fizzbuzz(n):\n    # your code here\n    pass\n',
            [case(5, [1, 2, "Fizz", 4, "Buzz"]),
             case(3, [1, 2, "Fizz"]),
             case(15, [1, 2, "Fizz", 4, "Buzz", "Fizz", 7, 8, "Fizz", "Buzz",
                       11, "Fizz", 13, 14, "FizzBuzz"]),
             case(0, [], hidden=True),
             case(1, [1], hidden=True),
             case(16, [1, 2, "Fizz", 4, "Buzz", "Fizz", 7, 8, "Fizz", "Buzz",
                       11, "Fizz", 13, 14, "FizzBuzz", 16], hidden=True)],
            ["Build a result list and append to it",
             "range(1, n + 1) gives you 1..n inclusive",
             "if i % 15 == 0 handles both at once"],
            'def fizzbuzz(n):\n    out = []\n    for i in range(1, n + 1):\n'
            '        if i % 15 == 0:\n            out.append("FizzBuzz")\n'
            '        elif i % 3 == 0:\n            out.append("Fizz")\n'
            '        elif i % 5 == 0:\n            out.append("Buzz")\n'
            '        else:\n            out.append(i)\n    return out\n',
            "Basics"),
),

# ============================================================ 2. STRUCTURES
Lesson(
    id="dicts", section="Data structures", title="Dictionaries",
    theory="""A dict maps keys to values with O(1) average lookup. It is THE tool for turning
an O(n^2) loop into an O(n) one, which is most of what coding interviews reward.

    ages = {"Ada": 36, "Linus": 54}
    ages["Grace"] = 85          insert / overwrite
    ages["Ada"]                 KeyError if missing
    ages.get("Nobody")          -> None  (no crash)
    ages.get("Nobody", 0)       -> 0     (default)
    "Ada" in ages               membership test, O(1)
    del ages["Ada"]
    ages.keys() / .values() / .items()

Counting idioms, best to worst-known:

    counts[c] = counts.get(c, 0) + 1        works everywhere
    from collections import Counter
    counts = Counter(text)                  batteries included
    counts.most_common(3)

Grouping:

    from collections import defaultdict
    groups = defaultdict(list)
    for word in words:
        groups[len(word)].append(word)

Since Python 3.7 dicts keep insertion order.""",
    example='''from collections import Counter, defaultdict

text = "mississippi"

counts = {}
for ch in text:
    counts[ch] = counts.get(ch, 0) + 1
print("manual:", counts)

print("Counter:", Counter(text))
print("top 2:", Counter(text).most_common(2))

words = ["fig", "pear", "kiwi", "plum", "apple"]
by_length = defaultdict(list)
for word in words:
    by_length[len(word)].append(word)
print("grouped:", dict(by_length))

stock = {"apple": 3, "pear": 0, "fig": 7}
for name, qty in stock.items():
    print(f"{name:<6} {qty}")
print("in stock:", [n for n, q in stock.items() if q > 0])
print("missing key safely:", stock.get("banana", 0))
''',
    takeaway="Dict lookup is O(1). Counter and defaultdict save you real time.",
    task=_t("dicts", "First non-repeating character", "first_unique",
            """Write first_unique(text) that returns the first character appearing exactly once.
Return None if every character repeats.

  first_unique("swiss")    -> "w"
  first_unique("aabbcc")   -> None

Do it in two passes: count first, then scan in order. That is O(n) — an O(n^2)
nested loop is the answer they do NOT want.""",
            'def first_unique(text):\n    # your code here\n    pass\n',
            [case("swiss", "w"), case("aabbcc", None), case("aabbc", "c"),
             case("", None, hidden=True), case("x", "x", hidden=True),
             case("leetcode", "l", hidden=True),
             case("loveleetcode", "v", hidden=True)],
            ["First loop: build counts[ch] = counts.get(ch, 0) + 1",
             "Second loop: over text again, return the first ch with counts[ch] == 1",
             "Scan the TEXT in the second pass, not the dict — order matters"],
            'def first_unique(text):\n    counts = {}\n    for ch in text:\n'
            '        counts[ch] = counts.get(ch, 0) + 1\n    for ch in text:\n'
            '        if counts[ch] == 1:\n            return ch\n    return None\n',
            "Hash map"),
),

Lesson(
    id="sets", section="Data structures", title="Sets & tuples",
    theory="""A set is an unordered collection of unique items with O(1) membership.

    seen = set()
    seen.add(3)
    3 in seen            O(1)  <- vs O(n) for a list!
    seen.discard(3)      no error if absent
    a | b   union        a & b  intersection
    a - b   difference   a ^ b  symmetric difference

Turning `if x in big_list` into `if x in big_set` is the single most common
"make it faster" fix in coding tests.

A tuple is an immutable list: (3, 4). Because it is immutable it is hashable,
so tuples can be dict keys and set members — lists cannot.

    point = (3, 4)
    x, y = point                 unpacking
    grid[(row, col)] = value     tuple as a dict key
    seen.add((row, col))         visited-cells pattern

Careful: {} is an empty DICT. An empty set is set().""",
    example='''nums = [3, 1, 4, 1, 5, 9, 2, 6, 5]

print("unique:", set(nums))
print("has 4?", 4 in set(nums))
print("dupes removed, order kept:", list(dict.fromkeys(nums)))

a, b = {1, 2, 3, 4}, {3, 4, 5}
print("union:", a | b, "| intersection:", a & b)
print("only in a:", a - b, "| in exactly one:", a ^ b)

# the "have I seen this before" pattern
seen, duplicates = set(), []
for n in nums:
    if n in seen:
        duplicates.append(n)
    seen.add(n)
print("duplicates:", duplicates)

# tuples: immutable, hashable, unpackable
point = (3, 4)
x, y = point
print("x =", x, "y =", y)
visited = {(0, 0), (1, 2)}
print("visited (1,2)?", (1, 2) in visited)
''',
    takeaway="`in` on a set is O(1), on a list O(n). Tuples are hashable, lists are not.",
    task=_t("sets", "Do two lists share anything?", "common_items",
            """Write common_items(a, b) that returns the values present in BOTH lists,
sorted ascending, with no duplicates.

  common_items([1, 2, 2, 3], [3, 4, 2]) -> [2, 3]
  common_items([1], [2])                -> []

Aim for O(n + m), not a nested loop.""",
            'def common_items(a, b):\n    # your code here\n    pass\n',
            [case(([1, 2, 2, 3], [3, 4, 2]), [2, 3]),
             case(([1], [2]), []),
             case(([5, 5], [5]), [5]),
             case(([], [1, 2]), [], hidden=True),
             case(([9, 8, 7], [7, 8, 9]), [7, 8, 9], hidden=True),
             case(([-1, 0], [0, -1, 3]), [-1, 0], hidden=True)],
            ["set(a) & set(b) gives the shared values",
             "sorted(...) turns the set into an ordered list"],
            'def common_items(a, b):\n    return sorted(set(a) & set(b))\n',
            "Sets"),
),

Lesson(
    id="comprehensions", section="Data structures", title="Comprehensions",
    theory="""A comprehension is a loop that builds a container, written as one expression.

    squares  = [n * n for n in range(10)]
    evens    = [n for n in nums if n % 2 == 0]
    labels   = [f"#{i}" for i in ids]
    lookup   = {word: len(word) for word in words}      dict comprehension
    unique   = {w.lower() for w in words}               set comprehension
    total    = sum(n * n for n in nums)                 generator, no list built

Shape to remember:

    [ WHAT_TO_KEEP   for ITEM in ITERABLE   if CONDITION ]

Nested (read it top-to-bottom, left-to-right, exactly like nested for loops):

    flat = [x for row in matrix for x in row]

Conditional VALUE (this if/else goes in front, it is not a filter):

    parity = ["even" if n % 2 == 0 else "odd" for n in nums]

Rule of thumb: if it does not fit comfortably on one line, use a real loop.""",
    example='''nums = [1, 2, 3, 4, 5, 6, 7, 8]

print([n * n for n in nums])
print([n for n in nums if n % 2 == 0])
print(["even" if n % 2 == 0 else "odd" for n in nums])

words = ["fig", "banana", "kiwi"]
print({w: len(w) for w in words})
print({w[0] for w in words})

matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print("flattened:", [x for row in matrix for x in row])
print("diagonal:", [matrix[i][i] for i in range(len(matrix))])
print("transposed:", [list(col) for col in zip(*matrix)])

# generator expression: no intermediate list in memory
print("sum of squares:", sum(n * n for n in range(1000)))
print("any negative?", any(n < 0 for n in nums))
print("all positive?", all(n > 0 for n in nums))
''',
    takeaway="[expr for item in it if cond]. Use a generator inside sum/any/all.",
    task=_t("comprehensions", "Matrix column sums", "col_sums",
            """Write col_sums(matrix) that returns the sum of each COLUMN of a rectangular
list-of-lists.

  col_sums([[1, 2], [3, 4], [5, 6]]) -> [9, 12]
  col_sums([])                       -> []

zip(*matrix) transposes a matrix — that plus a comprehension is a one-liner.""",
            'def col_sums(matrix):\n    # your code here\n    pass\n',
            [case([[1, 2], [3, 4], [5, 6]], [9, 12]),
             case([[1, 2, 3]], [1, 2, 3]),
             case([], []),
             case([[0, 0], [0, 0]], [0, 0], hidden=True),
             case([[-1, 5], [1, -5]], [0, 0], hidden=True),
             case([[1], [2], [3], [4]], [10], hidden=True)],
            ["zip(*matrix) yields one tuple per column",
             "[sum(col) for col in zip(*matrix)]",
             "zip(*[]) is empty, so the empty case already works"],
            'def col_sums(matrix):\n    return [sum(col) for col in zip(*matrix)]\n',
            "Lists"),
),

# ============================================================ 3. FUNCTIONS
Lesson(
    id="functions", section="Functions & structure", title="Functions",
    theory="""    def greet(name, greeting="Hello", *, loud=False):
        text = f"{greeting}, {name}!"
        return text.upper() if loud else text

  * `greeting="Hello"` is a default — optional at the call site
  * everything after `*` must be passed by keyword: greet("Ada", loud=True)
  * a function with no `return` returns None
  * `return a, b` returns a tuple; the caller can unpack it

THE classic Python trap — never use a mutable default:

    def bad(item, bucket=[]):     # the SAME list is reused across all calls!
        bucket.append(item)
        return bucket

    def good(item, bucket=None):
        if bucket is None:
            bucket = []
        bucket.append(item)
        return bucket

Scope: a name assigned inside a function is local to it. Reading an outer
variable is fine; rebinding it needs `global` (which you almost never want —
pass it in and return it out instead).

Type hints are optional and never enforced, but they document intent:

    def total(prices: list[float]) -> float: ...""",
    example='''def greet(name, greeting="Hello", *, loud=False):
    text = f"{greeting}, {name}!"
    return text.upper() if loud else text

print(greet("Ada"))
print(greet("Linus", "Hi"))
print(greet("Grace", loud=True))

def min_max(nums):
    return min(nums), max(nums)

low, high = min_max([4, 9, 1, 7])
print("low:", low, "high:", high)

def bad(item, bucket=[]):
    bucket.append(item)
    return bucket

print("bad call 1:", bad(1))
print("bad call 2:", bad(2), "  <- the list survived!")

def good(item, bucket=None):
    bucket = [] if bucket is None else bucket
    bucket.append(item)
    return bucket

print("good call 1:", good(1))
print("good call 2:", good(2))

def apply_twice(fn, value):
    return fn(fn(value))
print("apply_twice:", apply_twice(lambda x: x * 3, 2))
''',
    takeaway="Default arguments are evaluated once. Never default to [] or {}.",
    task=_t("functions", "Flexible average", "average",
            """Write average(nums, ndigits=2) that returns the mean of a list of numbers,
rounded to `ndigits` decimal places. Return 0.0 for an empty list.

  average([1, 2, 3, 4])       -> 2.5
  average([1, 2], ndigits=0)  -> 2.0   (round() returns a float here since we ask for a float)

Use round(value, ndigits). Guard the empty list before dividing!""",
            'def average(nums, ndigits=2):\n    # your code here\n    pass\n',
            [case([1, 2, 3, 4], 2.5), case([], 0.0), case(([1, 2, 4], 1), 2.3),
             case([10], 10.0, hidden=True),
             case(([1, 1, 1, 2], 3), 1.25, hidden=True),
             case(([-2, 2], 2), 0.0, hidden=True)],
            ["if not nums: return 0.0",
             "mean = sum(nums) / len(nums)",
             "return round(mean, ndigits)"],
            'def average(nums, ndigits=2):\n    if not nums:\n        return 0.0\n'
            '    return round(sum(nums) / len(nums), ndigits)\n',
            "Functions"),
),

Lesson(
    id="errors", section="Functions & structure", title="Errors & exceptions",
    theory="""    try:
        value = int(text)
    except ValueError:
        value = 0
    else:
        print("worked:", value)     # only if no exception
    finally:
        print("always runs")        # cleanup

Catch the SPECIFIC exception. A bare `except:` swallows typos, Ctrl-C and real
bugs alike.

Common ones you will meet:
    ValueError        int("abc")
    TypeError         "a" + 1
    KeyError          d["missing"]
    IndexError        lst[99]
    ZeroDivisionError 1 / 0
    AttributeError    None.strip()

Raise your own when an argument makes no sense:

    if n < 0:
        raise ValueError(f"n must be >= 0, got {n}")

Python style is EAFP — "easier to ask forgiveness than permission". Trying and
catching is idiomatic; checking every precondition first is not.

    try:                        # EAFP, pythonic
        return d[key]
    except KeyError:
        return default""",
    example='''def safe_int(text, default=0):
    try:
        return int(text)
    except (ValueError, TypeError):
        return default

print(safe_int("42"), safe_int("nope"), safe_int(None, -1))

def divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("  -> cannot divide by zero")
        return None
    else:
        return result
    finally:
        print("  (divide finished)")

print("10/2 =", divide(10, 2))
print("10/0 =", divide(10, 0))

def sqrt_of(n):
    if n < 0:
        raise ValueError(f"n must be >= 0, got {n}")
    return n ** 0.5

try:
    sqrt_of(-4)
except ValueError as exc:
    print("caught:", exc)
''',
    takeaway="Catch specific exceptions. Raise ValueError for bad input.",
    task=_t("errors", "Parse a list of numbers", "parse_numbers",
            """Write parse_numbers(items) that converts a list of strings to ints and returns
(numbers, bad_count):

  * numbers   — the list of successfully converted ints, in order
  * bad_count — how many items could not be converted

parse_numbers(["1", "x", "3"]) -> ([1, 3], 1)

Return a real tuple. Do not let a bad item crash the function.""",
            'def parse_numbers(items):\n    # your code here\n    pass\n',
            [case(["1", "x", "3"], ([1, 3], 1)),
             case(["10", "20"], ([10, 20], 0)),
             case([], ([], 0)),
             case(["a", "b"], ([], 2), hidden=True),
             case(["-5", "3.5", "7"], ([-5, 7], 1), hidden=True),
             case([" 8 ", "nope"], ([8], 1), hidden=True)],
            ["Loop, and wrap int(item) in try/except ValueError",
             'int("3.5") raises ValueError — that is intended here',
             "return numbers, bad  builds the tuple automatically"],
            'def parse_numbers(items):\n    numbers, bad = [], 0\n    for item in items:\n'
            '        try:\n            numbers.append(int(item))\n'
            '        except (ValueError, TypeError):\n            bad += 1\n'
            '    return numbers, bad\n',
            "Errors"),
),

Lesson(
    id="oop", section="Functions & structure", title="Classes & objects",
    theory="""A class bundles data with the functions that work on it.

    class Account:
        def __init__(self, owner, balance=0):   # runs on Account("Ada")
            self.owner = owner                  # instance attributes
            self.balance = balance

        def deposit(self, amount):              # self = this object
            if amount <= 0:
                raise ValueError("amount must be positive")
            self.balance += amount
            return self.balance

        def __repr__(self):                     # how it prints
            return f"Account({self.owner!r}, {self.balance})"

`self` is the first parameter of every instance method and Python passes it for
you: acc.deposit(50) calls deposit(acc, 50).

Dunder methods hook into the language:
    __init__  construction     __repr__  developer-facing text
    __str__   user-facing text __len__   len(obj)
    __eq__    ==               __lt__    < , which makes sort() work

Inheritance:

    class Savings(Account):
        def __init__(self, owner, balance=0, rate=0.02):
            super().__init__(owner, balance)
            self.rate = rate

For plain data bundles, reach for a dataclass — it writes __init__ and
__repr__ for you:

    from dataclasses import dataclass
    @dataclass
    class Point:
        x: int
        y: int""",
    example='''from dataclasses import dataclass

class Account:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("amount must be positive")
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("insufficient funds")
        self.balance -= amount
        return self.balance

    def __repr__(self):
        return f"Account({self.owner!r}, {self.balance})"

acc = Account("Ada", 100)
acc.deposit(50)
print(acc, "| balance:", acc.balance)
try:
    acc.withdraw(1000)
except ValueError as exc:
    print("caught:", exc)

class Savings(Account):
    def __init__(self, owner, balance=0, rate=0.02):
        super().__init__(owner, balance)
        self.rate = rate

    def add_interest(self):
        return self.deposit(self.balance * self.rate)

s = Savings("Grace", 1000)
s.add_interest()
print(s, "| rate:", s.rate)

@dataclass
class Point:
    x: int
    y: int
    def dist(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

p = Point(3, 4)
print(p, "| distance:", p.dist())
''',
    takeaway="__init__ builds it, self is the object, super() reaches the parent.",
    task=_t("oop", "A tiny Stack class", "make_stack",
            """Build a Stack class and a factory function make_stack(items) that returns a
Stack already filled with `items` (pushed left to right).

Your Stack needs:
  * push(x)   add on top
  * pop()     remove and return the top, or None if empty
  * peek()    return the top without removing it, or None if empty
  * size()    number of items

make_stack([1, 2, 3]).pop() -> 3

The tests call make_stack(...) and then poke at the object it returns.""",
            'class Stack:\n    def __init__(self):\n        self.items = []\n\n'
            '    # add push / pop / peek / size here\n\n\n'
            'def make_stack(items):\n    # your code here\n    pass\n',
            [case([1, 2, 3], None, label="push 1,2,3 then peek/pop/size"),
             case([], None, label="an empty stack must not crash"),
             case([5], None, label="a single item"),
             case([1, 2, 3, 4], None, hidden=True),
             case(["a", "b"], None, hidden=True)],
            ["push -> self.items.append(x)",
             "pop -> if not self.items: return None, else self.items.pop()",
             "make_stack: build a Stack, loop over items, push each, return it"],
            'class Stack:\n    def __init__(self):\n        self.items = []\n\n'
            '    def push(self, x):\n        self.items.append(x)\n\n'
            '    def pop(self):\n        return self.items.pop() if self.items else None\n\n'
            '    def peek(self):\n        return self.items[-1] if self.items else None\n\n'
            '    def size(self):\n        return len(self.items)\n\n\n'
            'def make_stack(items):\n    stack = Stack()\n    for item in items:\n'
            '        stack.push(item)\n    return stack\n',
            "OOP", checker_src=STACK_CHECKER),
),

Lesson(
    id="modules", section="Functions & structure", title="Modules & the standard library",
    theory="""    import math                      math.sqrt(16)
    from math import sqrt, pi        sqrt(16)
    import statistics as stats       stats.mean(nums)

The batteries you actually reach for in a coding test:

  collections   Counter, defaultdict, deque, namedtuple
  itertools     accumulate, combinations, permutations, groupby, product
  math          gcd, sqrt, ceil, floor, inf, comb, isclose
  heapq         heappush/heappop — a priority queue (top-K problems)
  bisect        binary search into a sorted list
  functools     lru_cache (memoisation!), reduce
  re            regular expressions

deque is the one people forget: popping from the FRONT of a list is O(n), from
a deque it is O(1). That is the difference between passing and timing out on a
BFS / sliding-window problem.

    from collections import deque
    q = deque([1, 2, 3])
    q.append(4); q.appendleft(0)
    q.popleft()      # O(1)

Every file you write is itself a module. `if __name__ == "__main__":` guards
code that should only run when the file is executed directly.""",
    example='''import math
from collections import deque, Counter
from itertools import accumulate, combinations
from functools import lru_cache
import bisect, heapq

print("gcd(84, 36):", math.gcd(84, 36))
print("ceil(2.1):", math.ceil(2.1), "| floor(2.9):", math.floor(2.9))
print("comb(5, 2):", math.comb(5, 2))

q = deque([1, 2, 3])
q.appendleft(0)
print("deque:", q, "| popleft ->", q.popleft(), q)

print("running totals:", list(accumulate([1, 2, 3, 4])))
print("pairs:", list(combinations("abc", 2)))
print("counter:", Counter("banana").most_common())

nums = [1, 3, 5, 7, 9]
print("insert 6 at index:", bisect.bisect_left(nums, 6))
print("3 largest:", heapq.nlargest(3, [5, 1, 9, 3, 7]))

@lru_cache(maxsize=None)
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)
print("fib(60) instantly:", fib(60))

if __name__ == "__main__":
    print("this file was run directly")
''',
    takeaway="deque for O(1) front ops, lru_cache for free memoisation, Counter for tallies.",
    task=_t("modules", "Top K frequent words", "top_k",
            """Write top_k(words, k) returning the k most frequent words, most frequent first.
Ties are broken alphabetically.

  top_k(["a", "b", "a", "c", "b", "a"], 2) -> ["a", "b"]

collections.Counter does the counting; the tie-break needs a sort key of
(-count, word).""",
            'from collections import Counter\n\n\n'
            'def top_k(words, k):\n    # your code here\n    pass\n',
            [case((["a", "b", "a", "c", "b", "a"], 2), ["a", "b"]),
             case((["x"], 1), ["x"]),
             case((["b", "a"], 2), ["a", "b"]),
             case(([], 3), [], hidden=True),
             case((["p", "q", "q", "p", "r"], 3), ["p", "q", "r"], hidden=True),
             case((["z", "z", "y"], 1), ["z"], hidden=True)],
            ["counts = Counter(words)",
             "ordered = sorted(counts, key=lambda w: (-counts[w], w))",
             "return ordered[:k]"],
            'from collections import Counter\n\n\n'
            'def top_k(words, k):\n    counts = Counter(words)\n'
            '    ordered = sorted(counts, key=lambda w: (-counts[w], w))\n'
            '    return ordered[:k]\n',
            "Sorting"),
),

# ============================================= 4. INTERVIEW-SHAPED TECHNIQUES
Lesson(
    id="complexity", section="Interview technique", title="Big-O in practice",
    theory="""Codility and friends do not just check that your answer is right — they check
that it is fast enough. Learn to read your own code's cost.

  O(1)        a fixed number of steps       d[key], lst[i], arithmetic
  O(log n)    halving each step             binary search
  O(n)        one pass                      sum(lst), a single for loop
  O(n log n)  sort                          sorted(lst), lst.sort()
  O(n^2)      loop inside a loop            two nested for loops over n
  O(2^n)      naive recursion over subsets  the "too slow" cliff

Hidden costs people miss:
    x in list        O(n)      but  x in set / dict  is O(1)
    list.pop(0)      O(n)      but  deque.popleft()  is O(1)
    list.insert(0,x) O(n)
    s += "x" in loop O(n^2)    build a list and "".join it
    sorting          O(n log n) — often the intended answer, not a failure

Rule of thumb for a 1-second limit: about 10^7-10^8 simple operations. So for
n = 100000, an O(n^2) solution (10^10 steps) will time out; O(n log n) is fine.

The interview move: state the complexity out loud, then say what would improve
it. "This is O(n^2); a hash set makes it O(n)." That sentence is worth points.""",
    example='''import time

n = 20000
data = list(range(n))
as_set = set(data)

start = time.perf_counter()
hits = sum(1 for x in range(0, n, 200) if x in data)      # O(n) per lookup
list_time = time.perf_counter() - start

start = time.perf_counter()
hits = sum(1 for x in range(0, n, 200) if x in as_set)    # O(1) per lookup
set_time = time.perf_counter() - start

print(f"list lookups: {list_time * 1000:8.2f} ms")
print(f"set  lookups: {set_time * 1000:8.2f} ms")
print(f"speedup: {list_time / max(set_time, 1e-9):.0f}x")

# string building
start = time.perf_counter()
s = ""
for i in range(20000):
    s += "x"
concat = time.perf_counter() - start

start = time.perf_counter()
s = "".join("x" for _ in range(20000))
joined = time.perf_counter() - start
print(f"\\n+= concat: {concat * 1000:6.2f} ms | join: {joined * 1000:6.2f} ms")
''',
    takeaway="n^2 dies above ~10k items. Sets, sorting and one clean pass are the fixes.",
    task=_t("complexity", "Has a duplicate? (must be O(n))", "has_duplicate",
            """Write has_duplicate(nums) -> True if any value appears more than once.

  has_duplicate([1, 2, 3, 1]) -> True
  has_duplicate([1, 2, 3])    -> False

One of the hidden tests feeds you 200 000 numbers with a 1-second-ish budget,
so a nested loop will fail. Use a set (or compare len(set(nums)) to len(nums)).""",
            'def has_duplicate(nums):\n    # your code here\n    pass\n',
            [case([1, 2, 3, 1], True), case([1, 2, 3], False), case([], False),
             case([7, 7], True, hidden=True),
             case(list(range(200000)), False, hidden=True, label="200k distinct — speed test"),
             case(list(range(200000)) + [17], True, hidden=True, label="200k + one dupe")],
            ["len(set(nums)) != len(nums) is the one-liner",
             "Or: keep a `seen` set and return True the moment you re-see a value",
             "Never write `for i ... for j ...` here"],
            'def has_duplicate(nums):\n    seen = set()\n    for n in nums:\n'
            '        if n in seen:\n            return True\n        seen.add(n)\n'
            '    return False\n',
            "Sets"),
),

Lesson(
    id="twopointer", section="Interview technique", title="Two pointers & sliding window",
    theory="""Two indices walking through one array replace a nested loop, turning O(n^2) into
O(n). Two shapes cover most problems.

1) Opposite ends (needs a SORTED array):

    left, right = 0, len(nums) - 1
    while left < right:
        total = nums[left] + nums[right]
        if total == target: return (left, right)
        if total < target:  left += 1      # need more
        else:               right -= 1     # need less

2) Sliding window (contiguous subarray/substring):

    left = 0
    for right, value in enumerate(nums):
        window_sum += value
        while window_sum > limit:          # shrink until valid again
            window_sum -= nums[left]
            left += 1
        best = max(best, right - left + 1)

Each index only ever moves forward, so the whole thing is O(n) even though
there are two loops.

Signals that a problem wants this: "contiguous", "subarray", "substring",
"pair that sums to", "longest/shortest window such that", "sorted array".""",
    example='''def two_sum_sorted(nums, target):
    left, right = 0, len(nums) - 1
    while left < right:
        total = nums[left] + nums[right]
        if total == target:
            return (left, right)
        if total < target:
            left += 1
        else:
            right -= 1
    return None

print(two_sum_sorted([1, 3, 4, 7, 11], 10))

def longest_unique(text):
    """Longest substring with no repeated character."""
    last_seen, left, best = {}, 0, 0
    for right, ch in enumerate(text):
        if ch in last_seen and last_seen[ch] >= left:
            left = last_seen[ch] + 1
        last_seen[ch] = right
        best = max(best, right - left + 1)
    return best

print("longest unique in 'abcabcbb':", longest_unique("abcabcbb"))

def max_window_sum(nums, k):
    """Biggest sum of any k consecutive values — fixed-size window."""
    window = sum(nums[:k])
    best = window
    for i in range(k, len(nums)):
        window += nums[i] - nums[i - k]
        best = max(best, window)
    return best

print("max sum of 3 in a row:", max_window_sum([2, 1, 5, 1, 3, 2], 3))
''',
    takeaway="'contiguous' or 'sorted pair' => two pointers. Both indices only move forward.",
    task=_t("twopointer", "Longest run of equal values", "longest_run",
            """Write longest_run(nums) that returns the length of the longest streak of
IDENTICAL consecutive values.

  longest_run([1, 1, 2, 2, 2, 3]) -> 3
  longest_run([])                 -> 0

One pass, one counter. No nested loops.""",
            'def longest_run(nums):\n    # your code here\n    pass\n',
            [case([1, 1, 2, 2, 2, 3], 3), case([], 0), case([5], 1),
             case([1, 2, 3], 1, hidden=True),
             case([4, 4, 4, 4], 4, hidden=True),
             case([1, 1, 2, 1, 1, 1], 3, hidden=True)],
            ["Track `current` (streak so far) and `best`",
             "If nums[i] == nums[i-1]: current += 1 else current = 1",
             "best = max(best, current) every step"],
            'def longest_run(nums):\n    if not nums:\n        return 0\n'
            '    best = current = 1\n    for i in range(1, len(nums)):\n'
            '        current = current + 1 if nums[i] == nums[i - 1] else 1\n'
            '        best = max(best, current)\n    return best\n',
            "Two pointers"),
),

Lesson(
    id="prefix", section="Interview technique", title="Prefix sums & counting tricks",
    theory="""Precompute once, then answer every query in O(1). This is the trick behind a
large share of Codility's "Prefix Sums" and "Counting Elements" tasks.

Prefix sums:

    prefix = [0] * (len(nums) + 1)
    for i, value in enumerate(nums):
        prefix[i + 1] = prefix[i] + value

    # sum of nums[a..b] inclusive, in O(1):
    total = prefix[b + 1] - prefix[a]

Or just: from itertools import accumulate.

Counting sort / bucket counting — when values are small integers, count them
into a fixed array instead of sorting:

    counts = [0] * (max_value + 1)
    for value in nums:
        counts[value] += 1

The "split the array" pattern (Codility's TapeEquilibrium, and half the
"find the pivot" family): sweep left-to-right keeping a running left sum, and
derive the right sum as total - left. One pass, O(n).

    total = sum(nums)
    left = 0
    for i in range(len(nums) - 1):
        left += nums[i]
        right = total - left
        best = min(best, abs(left - right))""",
    example='''from itertools import accumulate

nums = [3, 1, 4, 1, 5, 9, 2, 6]

prefix = [0]
for value in nums:
    prefix.append(prefix[-1] + value)
print("prefix:", prefix)

def range_sum(a, b):
    return prefix[b + 1] - prefix[a]

print("sum nums[2..5] =", range_sum(2, 5), "(check:", sum(nums[2:6]), ")")
print("accumulate:", list(accumulate(nums)))

# minimal difference when splitting the array in two
total, left, best = sum(nums), 0, float("inf")
for i in range(len(nums) - 1):
    left += nums[i]
    best = min(best, abs(left - (total - left)))
print("best split difference:", best)

# counting instead of sorting, when values are small
values = [3, 1, 2, 3, 3, 1]
counts = [0] * (max(values) + 1)
for v in values:
    counts[v] += 1
print("counts by value:", counts)
print("most common value:", counts.index(max(counts)))
''',
    takeaway="Build prefix sums once, answer range queries in O(1). total - left = right.",
    task=_t("prefix", "Equilibrium index", "equilibrium",
            """An equilibrium index is a position where the sum of everything to its LEFT
equals the sum of everything to its RIGHT (the element itself counts for neither).

Write equilibrium(nums) returning the SMALLEST such index, or -1 if none exists.

  equilibrium([-1, 3, -4, 5, 1, -6, 2, 1]) -> 1
  equilibrium([1, 2, 3])                   -> -1

Must be O(n): keep a running left sum and derive the right side from the total.""",
            'def equilibrium(nums):\n    # your code here\n    pass\n',
            [case([-1, 3, -4, 5, 1, -6, 2, 1], 1),
             case([1, 2, 3], -1),
             case([0], 0),
             case([1, -1, 0], 2, hidden=True),
             case([], -1, hidden=True),
             case([2, 0, 2], 1, hidden=True),
             case(list(range(100000)), -1, hidden=True, label="100k — speed test")],
            ["total = sum(nums); left = 0",
             "At index i: right = total - left - nums[i]",
             "Compare, then do left += nums[i] AFTER the check"],
            'def equilibrium(nums):\n    total = sum(nums)\n    left = 0\n'
            '    for i, value in enumerate(nums):\n'
            '        if left == total - left - value:\n            return i\n'
            '        left += value\n    return -1\n',
            "Prefix sums"),
),

Lesson(
    id="recursion", section="Interview technique", title="Recursion & memoisation",
    theory="""A recursive function calls itself on a smaller version of the problem. Two parts,
always:

    def factorial(n):
        if n <= 1:          # 1. BASE CASE — stops the recursion
            return 1
        return n * factorial(n - 1)   # 2. RECURSIVE STEP — moves toward the base

Naive recursion can explode. fib(35) makes ~30 million calls because it
recomputes the same values over and over. Memoisation fixes it for free:

    from functools import lru_cache

    @lru_cache(maxsize=None)
    def fib(n):
        return n if n < 2 else fib(n - 1) + fib(n - 2)

That one decorator turns O(2^n) into O(n). It is the cheapest dynamic
programming you will ever write.

Python's recursion limit is ~1000 frames, so deep recursion over a big list
will hit RecursionError — rewrite those iteratively with an explicit stack.

Bottom-up DP is the same idea without the call stack:

    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]""",
    example='''from functools import lru_cache
import time

def fib_slow(n):
    return n if n < 2 else fib_slow(n - 1) + fib_slow(n - 2)

@lru_cache(maxsize=None)
def fib_fast(n):
    return n if n < 2 else fib_fast(n - 1) + fib_fast(n - 2)

start = time.perf_counter()
fib_slow(28)
slow = time.perf_counter() - start
start = time.perf_counter()
fib_fast(28)
fast = time.perf_counter() - start
print(f"fib(28) naive: {slow*1000:.1f} ms | memoised: {fast*1000:.4f} ms")
print("fib(200) memoised:", fib_fast(200))

def flatten(nested):
    out = []
    for item in nested:
        if isinstance(item, list):
            out.extend(flatten(item))
        else:
            out.append(item)
    return out

print("flatten:", flatten([1, [2, [3, [4, 5]], 6], 7]))

# bottom-up: how many ways to climb n stairs taking 1 or 2 steps
def climb(n):
    dp = [0] * (n + 1)
    dp[0] = 1
    for i in range(1, n + 1):
        dp[i] = dp[i - 1] + (dp[i - 2] if i >= 2 else 0)
    return dp[n]

print("ways to climb 10 stairs:", climb(10))
''',
    takeaway="Base case first. @lru_cache turns exponential recursion into linear.",
    task=_t("recursion", "Sum a deeply nested list", "deep_sum",
            """Write deep_sum(nested) that adds up every number inside an arbitrarily nested
list of numbers and lists.

  deep_sum([1, [2, [3, [4]]], 5]) -> 15
  deep_sum([])                    -> 0

Use isinstance(item, list) to decide whether to recurse.""",
            'def deep_sum(nested):\n    # your code here\n    pass\n',
            [case([1, [2, [3, [4]]], 5], 15),
             case([], 0),
             case([[[[7]]]], 7),
             case([1, 2, 3], 6, hidden=True),
             case([[], [[]], [[[1]]]], 1, hidden=True),
             case([-1, [1], [-2, [2]]], 0, hidden=True)],
            ["total = 0, then loop over the items",
             "if isinstance(item, list): total += deep_sum(item)",
             "else: total += item"],
            'def deep_sum(nested):\n    total = 0\n    for item in nested:\n'
            '        if isinstance(item, list):\n            total += deep_sum(item)\n'
            '        else:\n            total += item\n    return total\n',
            "Recursion"),
),

Lesson(
    id="io", section="Interview technique", title="Reading input & printing output",
    theory="""Some judges hand you a function to fill in (Codility does this). Others feed you
stdin and read your stdout. Know both.

Reading stdin:

    line = input()                       one line, as a string
    n = int(input())                     one number
    nums = list(map(int, input().split()))   "3 1 4" -> [3, 1, 4]

    import sys
    data = sys.stdin.read().split()      everything at once — much faster
    for line in sys.stdin:               line by line

Printing:

    print(a, b)              -> "a b"
    print(*nums)             -> unpacks the list: "1 2 3"
    print(", ".join(map(str, nums)))
    print(f"{value:.2f}")    two decimals
    print(x, end="")         no newline

Formatting cheatsheet:
    f"{n:5d}"     right-aligned in 5 columns
    f"{n:<5}"     left-aligned
    f"{n:05d}"    zero padded  -> 00042
    f"{x:.3f}"    3 decimals
    f"{x:,}"      thousands separators -> 1,234,567
    f"{p:.1%}"    percent -> 42.0%

In this app: the Playground tab has an stdin box, so you can practise the
read-from-stdin style exactly as a judge would run it.""",
    example='''# This example uses a fake input so it runs without you typing anything.
raw = """3
5 3 8
Ada
"""
lines = raw.strip().split("\\n")

n = int(lines[0])
nums = list(map(int, lines[1].split()))
name = lines[2]

print("n =", n)
print("nums =", nums, "sum =", sum(nums))
print("name =", name)

print("unpacked:", *nums)
print("joined:", ", ".join(map(str, nums)))

print()
print(f"{'item':<10}{'qty':>5}{'price':>10}")
for item, qty, price in [("apple", 3, 1.5), ("watermelon", 12, 4.25)]:
    print(f"{item:<10}{qty:>5}{price:>10.2f}")

print()
print(f"padded: {42:05d} | percent: {0.4237:.1%} | big: {1234567:,}")
''',
    takeaway="list(map(int, input().split())) parses a line of numbers. f-strings format it back.",
    task=_t("io", "Format a receipt line", "receipt_line",
            """Write receipt_line(name, qty, price) that returns one formatted row:

  * name left-aligned in 12 columns
  * qty right-aligned in 4 columns
  * the line total (qty * price) right-aligned in 10 columns with 2 decimals

receipt_line("apple", 3, 1.5) -> "apple          3      4.50"

(that is 12 + 4 + 10 = 26 characters)""",
            'def receipt_line(name, qty, price):\n    # your code here\n    pass\n',
            [case(("apple", 3, 1.5), "apple          3      4.50"),
             case(("watermelon", 12, 4.25), "watermelon    12     51.00"),
             case(("fig", 1, 0.5), "fig            1      0.50"),
             case(("a", 100, 10), "a            100   1000.00", hidden=True),
             case(("bread", 0, 2.2), "bread          0      0.00", hidden=True)],
            ['f"{name:<12}" left-aligns in 12 columns',
             'f"{qty:>4}" right-aligns in 4',
             'f"{qty * price:>10.2f}" for the total'],
            'def receipt_line(name, qty, price):\n'
            '    return f"{name:<12}{qty:>4}{qty * price:>10.2f}"\n',
            "Strings"),
),

Lesson(
    id="debug", section="Interview technique", title="Reading a traceback",
    theory="""A traceback is read BOTTOM-UP. The last line is what went wrong; the line above
it is where.

    Traceback (most recent call last):
      File "your_code.py", line 7, in <module>
        print(total(prices))
      File "your_code.py", line 4, in total
        return sum(p["cost"] for p in prices)
    KeyError: 'cost'

Read it as: "KeyError 'cost'" happened inside total() on line 4.

The frequent ones and their usual cause:

  IndexError: list index out of range   -> off-by-one, or an empty list
  KeyError: 'x'                         -> missing dict key; use .get()
  TypeError: 'NoneType' object is not subscriptable
                                        -> a function returned None (forgot `return`!)
  TypeError: unsupported operand type(s) for +: 'int' and 'str'
                                        -> mixing a number with text
  ValueError: invalid literal for int() -> int("12a")
  UnboundLocalError                     -> using a variable before assigning it
  IndentationError / SyntaxError        -> the caret ^ points at the spot

Debugging without a debugger: print the SHAPE of your data, not just the value.

    print(f"{i=} {left=} {right=} {window=}")     # 3.8+ self-documenting

That `=` inside an f-string prints "i=3 left=0" — the fastest debug tool in the
language.""",
    example='''def total(prices):
    return sum(p["cost"] for p in prices)

items = [{"name": "fig", "cost": 2}, {"name": "pear", "price": 3}]

try:
    print(total(items))
except KeyError as exc:
    print("KeyError on key:", exc, "-> one dict uses 'price', not 'cost'")

def safe_total(prices):
    return sum(p.get("cost", p.get("price", 0)) for p in prices)
print("fixed total:", safe_total(items))

# the "forgot to return" bug
def double_broken(n):
    n * 2          # no return -> None

result = double_broken(5)
print("result is", result, "of type", type(result).__name__)

# self-documenting f-strings
left, right, window = 0, 4, [1, 2, 3]
print(f"{left=} {right=} {window=} {len(window)=}")

nums = [1, 2, 3]
for i in range(len(nums)):
    print(f"index {i} -> {nums[i]}")
print("the classic off-by-one would be range(len(nums) + 1)")
''',
    takeaway="Read tracebacks bottom-up. `TypeError: NoneType` almost always means a missing return.",
    task=_t("debug", "Fix the broken function", "average_score",
            """The function below is MEANT to return the average score of a list of student
dicts, rounded to 1 decimal, and 0.0 for an empty list. It has three bugs.

Fix it so it works:

    def average_score(students):
        total = 0
        for s in students:
            total += s["score"]
        return round(total / len(students), 1)

Bugs to find: it crashes on an empty list, it crashes when a student has no
"score" key (treat a missing score as 0), and it must return a float even when
the average is a whole number.""",
            'def average_score(students):\n    total = 0\n    for s in students:\n'
            '        total += s["score"]\n    return round(total / len(students), 1)\n',
            [case([{"score": 90}, {"score": 80}], 85.0),
             case([], 0.0),
             case([{"score": 70}, {"name": "x"}], 35.0),
             case([{"score": 100}], 100.0, hidden=True),
             case([{"a": 1}, {"b": 2}], 0.0, hidden=True),
             case([{"score": 1}, {"score": 2}, {"score": 2}], 1.7, hidden=True)],
            ["if not students: return 0.0  — before the division",
             's.get("score", 0) instead of s["score"]',
             "round(x, 1) already returns a float when x is a float — divide with /"],
            'def average_score(students):\n    if not students:\n        return 0.0\n'
            '    total = 0\n    for s in students:\n        total += s.get("score", 0)\n'
            '    return round(total / len(students), 1)\n',
            "Debugging"),
),
]

SECTIONS: list[str] = []
for _lesson in LESSONS:
    if _lesson.section not in SECTIONS:
        SECTIONS.append(_lesson.section)


def by_id(lesson_id: str) -> Lesson | None:
    for lesson in LESSONS:
        if lesson.id == lesson_id:
            return lesson
    return None


# ---------------------------------------------------------------- localisation
def _de(lesson: Lesson) -> dict:
    return lessons_de.LESSONS_DE.get(lesson.id, {}) if i18n.is_de() else {}


def field_of(lesson: Lesson, name: str) -> str:
    """theory / takeaway / example / title / section in the active language."""
    return _de(lesson).get(name) or getattr(lesson, name)


def section_of(lesson: Lesson) -> str:
    if i18n.is_de():
        return lessons_de.SECTIONS_DE.get(lesson.section, lesson.section)
    return lesson.section


def sections() -> list[str]:
    out = []
    for lesson in LESSONS:
        name = section_of(lesson)
        if name not in out:
            out.append(name)
    return out


def task_of(lesson: Lesson) -> Task:
    """A fresh copy of the lesson's exercise in the active language."""
    task = copy.deepcopy(lesson.task)
    return i18n.localize_task(task, _de(lesson).get("task"))
