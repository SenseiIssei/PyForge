"""Interview problem bank: Codility-style tasks + the LeetCode patterns that
keep showing up in real screens.

Each problem stores its reference solution as SOURCE. The source is exec'd once
at import to produce the function that computes the expected answers, so the
"Show solution" button always shows code that provably passes the tests.

Every problem also gets fresh RANDOM test cases each time you open it, on top of
its fixed examples - so re-doing a problem is never just replaying a memorised
answer.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Callable

import i18n
import problems_de
from tasks import Task, make_cases, starter_for

BANK: list["Problem"] = []


@dataclass
class Problem:
    id: str
    title: str
    difficulty: str
    topic: str
    func: str
    params: str
    statement: str
    solution: str
    complexity: str = ""
    hints: list[str] = field(default_factory=list)
    fixed: list = field(default_factory=list)
    rand: Callable[[random.Random], tuple] | None = None
    n_random: int = 4
    notes: str = ""
    starter: str = ""
    checker_src: str = ""   # optional check(args, got) when several answers are valid
    ref: Callable = None    # filled in by P()

    @property
    def display_title(self) -> str:
        de = problems_de.PROBLEMS_DE.get(self.id, {})
        return de.get("title", self.title) if i18n.is_de() else self.title

    def build(self, rng: random.Random | None = None) -> Task:
        rng = rng or random.Random()
        samples = list(self.fixed)
        if self.rand:
            for _ in range(self.n_random):
                try:
                    samples.append(self.rand(rng))
                except Exception:       # a generator hiccup must never kill the UI
                    break
        task = Task(
            id=self.id, title=self.title, func=self.func,
            statement=self.statement.strip(),
            starter=self.starter or starter_for(self.func, self.params),
            cases=make_cases(self.ref, samples, hidden_from=min(3, len(self.fixed))),
            hints=self.hints, solution=self.solution.strip(),
            difficulty=self.difficulty, topic=self.topic,
            complexity=self.complexity, source="interview", notes=self.notes,
            checker_src=self.checker_src,
        )
        return i18n.localize_task(task, problems_de.PROBLEMS_DE.get(self.id))


def P(pid, title, difficulty, topic, func, params, statement, solution,
      complexity="", hints=(), fixed=(), rand=None, n_random=4, notes="",
      starter="") -> Problem:
    ns: dict = {}
    exec(solution, ns)
    prob = Problem(id=pid, title=title, difficulty=difficulty, topic=topic,
                   func=func, params=params, statement=statement.strip(),
                   solution=solution.strip(), complexity=complexity,
                   hints=list(hints), fixed=list(fixed), rand=rand,
                   n_random=n_random, notes=notes, starter=starter,
                   ref=ns[func])
    BANK.append(prob)
    return prob


def rl(rng, n=None, lo=-50, hi=50):
    n = n if n is not None else rng.randint(1, 12)
    return [rng.randint(lo, hi) for _ in range(n)]


def rgrid(rng, choices, min_side=1, max_side=4):
    """A RECTANGULAR random grid (same width on every row)."""
    rows = rng.randint(min_side, max_side)
    cols = rng.randint(min_side, max_side)
    return [[rng.choice(choices) for _ in range(cols)] for _ in range(rows)]


# ============================================================================
#  CODILITY — the official lesson tasks people actually get asked
# ============================================================================

P("binary_gap", "Binary Gap", "Easy", "Bit tricks", "solution", "n", """
A binary gap in a positive integer N is a maximal run of consecutive ZEROS that
is surrounded by ones at both ends in N's binary representation.

  9  = 1001  -> one gap of length 2      -> 2
  529 = 1000010001 -> gaps of 4 and 3    -> 4
  20 = 10100 -> one gap of length 1      -> 1   (the trailing zero doesn't count)
  15 = 1111  -> no gap                   -> 0
  32 = 100000 -> no gap (never closed)   -> 0

Write solution(n) returning the length of the longest binary gap, or 0 if there
is none. 1 <= n <= 2,147,483,647.
""", '''def solution(n):
    bits = bin(n)[2:]
    best = current = 0
    counting = False
    for bit in bits:
        if bit == "1":
            if counting:
                best = max(best, current)
            counting = True
            current = 0
        elif counting:
            current += 1
    return best
''', "O(log n)",
  ["bin(n)[2:] gives the binary digits as a string",
   "Only start counting zeros AFTER you have seen a 1",
   "A run only counts when it is CLOSED by another 1 — trailing zeros are ignored"],
  fixed=[(9,), (529,), (20,), (15,), (32,), (1041,), (1,)],
  rand=lambda rng: (rng.randint(1, 2 ** 30),),
  notes="Codility Lesson 1. The trap is the unterminated trailing run of zeros.")

P("cyclic_rotation", "Cyclic Rotation", "Easy", "Arrays", "solution", "a, k", """
Rotate the array `a` to the RIGHT `k` times. Each rotation moves the last
element to the front.

  solution([3, 8, 9, 7, 6], 3) -> [9, 7, 6, 3, 8]
  solution([1, 2, 3, 4], 4)    -> [1, 2, 3, 4]
  solution([], 5)              -> []

k can be larger than len(a). Return a NEW list.
""", '''def solution(a, k):
    if not a:
        return []
    k %= len(a)
    return a[-k:] + a[:-k] if k else a[:]
''', "O(n)",
  ["k % len(a) collapses the redundant full turns",
   "A right rotation by k is a[-k:] + a[:-k]",
   "Guard the empty list (modulo by zero!) and k == 0 (a[-0:] is the WHOLE list)"],
  fixed=[([3, 8, 9, 7, 6], 3), ([1, 2, 3, 4], 4), ([], 5), ([1], 7), ([0, 0, 0], 1)],
  rand=lambda rng: (rl(rng, rng.randint(0, 10), -20, 20), rng.randint(0, 15)),
  notes="Codility Lesson 2. a[-0:] returning everything is the classic bug here.")

P("odd_occurrences", "Odd Occurrences In Array", "Easy", "Bit tricks", "solution", "a", """
The array has an ODD number of elements. Every value occurs an even number of
times except exactly one, which occurs an odd number of times.

Find that unpaired value.

  solution([9, 3, 9, 3, 9, 7, 9]) -> 7

O(n) time and O(1) space is expected — so no dict, no set.
""", '''def solution(a):
    result = 0
    for value in a:
        result ^= value
    return result
''', "O(n) time, O(1) space",
  ["XOR: x ^ x == 0 and x ^ 0 == x",
   "XOR is commutative, so the pairs cancel no matter the order",
   "Fold the whole array with ^ and whatever survives is the odd one"],
  fixed=[([9, 3, 9, 3, 9, 7, 9],), ([42],), ([1, 1, 2, 2, 5],)],
  rand=lambda rng: (_odd_array(rng),),
  notes="Codility Lesson 2. XOR is the O(1)-space trick they are testing for.")


def _odd_array(rng):
    pairs = [rng.randint(1, 100) for _ in range(rng.randint(1, 6))]
    lonely = rng.randint(101, 200)
    arr = pairs + pairs + [lonely]
    rng.shuffle(arr)
    return arr


P("frog_jmp", "Frog Jump", "Easy", "Math", "solution", "x, y, d", """
A small frog is at position X and wants to reach at least position Y. It jumps
a fixed distance D each time.

Write solution(x, y, d) returning the MINIMUM number of jumps needed.

  solution(10, 85, 30) -> 3
  solution(10, 10, 5)  -> 0

X <= Y, and the numbers go up to 1,000,000,000 — so a loop would time out.
Compute it with arithmetic.
""", '''def solution(x, y, d):
    gap = y - x
    return -(-gap // d)
''', "O(1)",
  ["distance = y - x",
   "You need ceil(distance / d) jumps",
   "Integer ceiling division without floats: -(-a // b)"],
  fixed=[(10, 85, 30), (10, 10, 5), (1, 1000000000, 1), (0, 7, 3)],
  rand=lambda rng: (lambda x, d: (x, x + rng.randint(0, 10 ** 6), d))(
      rng.randint(1, 1000), rng.randint(1, 1000)),
  notes="Codility Lesson 3. math.ceil on floats loses precision at 1e9 — use -(-a // b).")

P("perm_missing", "Permutation Missing Element", "Easy", "Math", "solution", "a", """
The array contains N distinct integers from the range 1..(N+1) — exactly one
value from that range is missing.

Find it.

  solution([2, 3, 1, 5]) -> 4
  solution([])           -> 1

Expected: O(n) time, O(1) space. Do NOT sort.
""", '''def solution(a):
    n = len(a)
    return (n + 1) * (n + 2) // 2 - sum(a)
''', "O(n) time, O(1) space",
  ["The full range 1..N+1 sums to (N+1)(N+2)/2",
   "Subtract the actual sum and the missing number falls out",
   "XOR-ing 1..N+1 against the array works too"],
  fixed=[([2, 3, 1, 5],), ([],), ([1],), ([2],)],
  rand=lambda rng: (_perm_missing(rng),),
  notes="Codility Lesson 3. Gauss' sum formula, not a loop over a `seen` array.")


def _perm_missing(rng):
    n = rng.randint(0, 12)
    full = list(range(1, n + 2))
    full.pop(rng.randrange(len(full)))
    rng.shuffle(full)
    return full


P("tape_equilibrium", "Tape Equilibrium", "Easy", "Prefix sums", "solution", "a", """
Split the array at position P (1 <= P < N) into a[0..P-1] and a[P..N-1].
The difference is |sum(left) - sum(right)|.

Return the MINIMAL difference achievable.

  solution([3, 1, 2, 4, 3]) -> 1     (split after 3,1,2 -> |6 - 7| = 1)

N >= 2 and up to 100,000, so recomputing both sums for every P (O(n^2)) times
out. One pass.
""", '''def solution(a):
    total = sum(a)
    left = 0
    best = None
    for i in range(len(a) - 1):
        left += a[i]
        diff = abs(left - (total - left))
        best = diff if best is None else min(best, diff)
    return best
''', "O(n)",
  ["total = sum(a) once, before the loop",
   "right = total - left, so you never re-sum",
   "P runs from 1 to N-1 — the loop index goes to len(a) - 2"],
  fixed=[([3, 1, 2, 4, 3],), ([1, 1],), ([-1000, 1000],), ([1, 2],)],
  rand=lambda rng: (rl(rng, rng.randint(2, 15), -100, 100),),
  notes="Codility Lesson 3. The canonical 'derive the right side from the total' pattern.")

P("frog_river", "Frog River One", "Easy", "Hash map", "solution", "x, a", """
A frog wants to cross a river to position X. Leaves fall: a[k] is the position
where a leaf falls at time k. The frog can cross once every position 1..X has
at least one leaf.

Return the EARLIEST time (index into a) when that happens, or -1 if it never does.

  solution(5, [1, 3, 1, 4, 2, 3, 5, 4]) -> 6
  solution(1, [2, 2, 2])                -> -1
""", '''def solution(x, a):
    seen = set()
    for time, position in enumerate(a):
        if position <= x and position not in seen:
            seen.add(position)
            if len(seen) == x:
                return time
    return -1
''', "O(n)",
  ["Track covered positions in a set",
   "Stop the moment len(seen) == x — that index is the answer",
   "Ignore positions greater than x"],
  fixed=[(5, [1, 3, 1, 4, 2, 3, 5, 4]), (1, [2, 2, 2]), (1, [1]), (3, [1, 2])],
  rand=lambda rng: (lambda x: (x, [rng.randint(1, x + 1) for _ in range(rng.randint(1, 20))]))(
      rng.randint(1, 6)),
  notes="Codility Lesson 4. Counting how many distinct targets are covered, not sorting.")

P("perm_check", "Permutation Check", "Easy", "Hash map", "solution", "a", """
Return 1 if the array is a permutation of 1..N (each value exactly once),
otherwise 0.

  solution([4, 1, 3, 2]) -> 1
  solution([4, 1, 3])    -> 0
""", '''def solution(a):
    n = len(a)
    return 1 if set(a) == set(range(1, n + 1)) else 0
''', "O(n)",
  ["A permutation of 1..N has exactly N distinct values",
   "set(a) == set(range(1, len(a) + 1)) settles it in one line",
   "Watch out for duplicates AND out-of-range values"],
  fixed=[([4, 1, 3, 2],), ([4, 1, 3],), ([1],), ([2],), ([1, 1],)],
  rand=lambda rng: (_perm_check_case(rng),),
  notes="Codility Lesson 4.")


def _perm_check_case(rng):
    n = rng.randint(1, 10)
    arr = list(range(1, n + 1))
    rng.shuffle(arr)
    if rng.random() < 0.5:
        arr[rng.randrange(n)] = rng.randint(1, n + 3)
    return arr


P("missing_integer", "Missing Integer", "Medium", "Hash map", "solution", "a", """
Return the SMALLEST positive integer (>= 1) that does NOT occur in the array.

  solution([1, 3, 6, 4, 1, 2]) -> 5
  solution([1, 2, 3])          -> 4
  solution([-1, -3])           -> 1

The array may contain negatives and duplicates. O(n) expected.
""", '''def solution(a):
    present = set(a)
    candidate = 1
    while candidate in present:
        candidate += 1
    return candidate
''', "O(n)",
  ["Put everything in a set first so lookups are O(1)",
   "Then walk 1, 2, 3, ... until you find a gap",
   "The answer is at most len(a) + 1, so the loop is bounded"],
  fixed=[([1, 3, 6, 4, 1, 2],), ([1, 2, 3],), ([-1, -3],), ([],), ([2],)],
  rand=lambda rng: (rl(rng, rng.randint(1, 15), -5, 15),),
  notes="Codility Lesson 4. The answer can never exceed N+1 — that bounds the scan.")

P("max_counters", "Max Counters", "Medium", "Arrays", "solution", "n, a", """
You have N counters, all starting at 0. For each value K in the operations list:

  * if 1 <= K <= N: increase counter K by 1
  * if K == N + 1: set ALL counters to the current maximum

Return the final counters as a list.

  solution(5, [3, 4, 4, 6, 1, 4, 4]) -> [3, 2, 2, 4, 2]

N and len(a) go up to 100,000. Actually writing to every counter on a max_counter
operation is O(n*m) and WILL time out — that is the whole point of this task.
""", '''def solution(n, a):
    counters = [0] * n
    floor = 0          # every counter is at least this
    current_max = 0
    for op in a:
        if op == n + 1:
            floor = current_max
        else:
            i = op - 1
            counters[i] = max(counters[i], floor) + 1
            current_max = max(current_max, counters[i])
    return [max(value, floor) for value in counters]
''', "O(n + m)",
  ["Do NOT loop over all counters on a max-op — that is the trap",
   "Keep a lazy `floor` value that every counter is implicitly raised to",
   "When you touch a counter, first lift it: max(counter, floor), then +1",
   "At the very end, lift everything that was never touched"],
  fixed=[(5, [3, 4, 4, 6, 1, 4, 4]), (1, [1, 2, 1]), (3, [4, 4, 4]), (2, [])],
  rand=lambda rng: (lambda n: (n, [rng.randint(1, n + 1) for _ in range(rng.randint(0, 20))]))(
      rng.randint(1, 8)),
  notes="Codility Lesson 4. Lazy propagation — the single most-failed Codility task.")

P("count_div", "Count Div", "Easy", "Math", "solution", "a, b, k", """
Count the integers in the inclusive range [a, b] that are divisible by k.

  solution(6, 11, 2) -> 3      (6, 8, 10)
  solution(0, 0, 11) -> 1      (0 is divisible by everything)

a and b go up to 2,000,000,000 so a loop is far too slow. O(1) arithmetic.
""", '''def solution(a, b, k):
    return b // k - (a - 1) // k if a > 0 else b // k + 1
''', "O(1)",
  ["Multiples of k up to x: x // k",
   "So the answer is b//k - (a-1)//k",
   "a == 0 is the special case: zero itself counts, and (0-1)//k is -1"],
  fixed=[(6, 11, 2), (0, 0, 11), (0, 10, 3), (1, 1, 1), (11, 345, 17)],
  rand=lambda rng: (lambda a: (a, a + rng.randint(0, 10 ** 6), rng.randint(1, 1000)))(
      rng.randint(0, 10 ** 6)),
  notes="Codility Lesson 5. Pure counting arithmetic; the a == 0 edge case is the trap.")

P("passing_cars", "Passing Cars", "Easy", "Prefix sums", "solution", "a", """
An array of 0s and 1s: 0 = a car driving EAST, 1 = a car driving WEST.
A pair (P, Q) passes each other when P < Q, a[P] == 0 and a[Q] == 1.

Return the number of passing pairs, or -1 if it exceeds 1,000,000,000.

  solution([0, 1, 0, 1, 1]) -> 5

O(n) — counting pairs with a nested loop is O(n^2) and times out at N = 100,000.
""", '''def solution(a):
    east = 0
    pairs = 0
    for value in a:
        if value == 0:
            east += 1
        else:
            pairs += east
            if pairs > 1000000000:
                return -1
    return pairs
''', "O(n)",
  ["Sweep left to right counting the 0s seen so far",
   "Every time you meet a 1, it pairs with ALL of those 0s at once",
   "Bail out as soon as the running total exceeds 1e9"],
  fixed=[([0, 1, 0, 1, 1],), ([],), ([1, 1, 1],), ([0, 0, 0],), ([0, 1],)],
  rand=lambda rng: ([rng.randint(0, 1) for _ in range(rng.randint(0, 20))],),
  notes="Codility Lesson 5. 'Count how many of the other kind came before' — a core pattern.")

P("min_avg_slice", "Min Avg Two Slice", "Medium", "Prefix sums", "solution", "a", """
A slice is a contiguous chunk a[p..q] with p < q. Return the STARTING index of
the slice with the smallest average. If several tie, return the smallest index.

  solution([4, 2, 2, 5, 1, 5, 8]) -> 1     (slice [2,2], average 2)

Key insight: you never need to check slices longer than 3. Any longer slice can
be split into 2- and 3-slices, and at least one of them has an average no worse
than the whole. So checking every 2-slice and 3-slice is enough — O(n).
""", '''def solution(a):
    n = len(a)
    best_index = 0
    best_avg = (a[0] + a[1]) / 2
    for i in range(n - 1):
        avg2 = (a[i] + a[i + 1]) / 2
        if avg2 < best_avg:
            best_avg, best_index = avg2, i
        if i < n - 2:
            avg3 = (a[i] + a[i + 1] + a[i + 2]) / 3
            if avg3 < best_avg:
                best_avg, best_index = avg3, i
    return best_index
''', "O(n)",
  ["Only slices of length 2 and 3 can be minimal — prove it to yourself, then use it",
   "One pass, comparing both windows at each index",
   "Use strict < so ties keep the earliest index"],
  fixed=[([4, 2, 2, 5, 1, 5, 8],), ([1, 1],), ([-3, -5, -8, -4, -10],), ([5, 1, 1, 5],)],
  rand=lambda rng: (rl(rng, rng.randint(2, 12), -20, 20),),
  notes="Codility Lesson 5. The 'length 2 or 3 is enough' lemma is the entire task.")

P("distinct", "Distinct", "Easy", "Sorting", "solution", "a", """
Return the number of DISTINCT values in the array.

  solution([2, 1, 1, 2, 3, 1]) -> 3
  solution([]) -> 0
""", '''def solution(a):
    return len(set(a))
''', "O(n) with a set / O(n log n) sorted",
  ["len(set(a)) is the whole answer",
   "Codility's official approach sorts and counts changes — both are accepted"],
  fixed=[([2, 1, 1, 2, 3, 1],), ([],), ([7],), ([1, 1, 1],)],
  rand=lambda rng: (rl(rng, rng.randint(0, 20), -5, 5),),
  notes="Codility Lesson 6. Free points — but say the complexity out loud.")

P("triangle", "Triangle", "Easy", "Sorting", "solution", "a", """
Return 1 if the array contains a triangular triplet (indices p < q < r with
a[p] + a[q] > a[r], a[q] + a[r] > a[p], a[r] + a[p] > a[q]), otherwise 0.

  solution([10, 2, 5, 1, 8, 20]) -> 1     (10, 8, 20)
  solution([10, 50, 5, 1])       -> 0

O(n log n): sort, then only ADJACENT triples can possibly work.
""", '''def solution(a):
    ordered = sorted(a)
    for i in range(len(ordered) - 2):
        if ordered[i] + ordered[i + 1] > ordered[i + 2]:
            return 1
    return 0
''', "O(n log n)",
  ["Sort first — then two of the three conditions are automatically true",
   "Only consecutive triples matter: a wider gap only makes the sum condition harder",
   "Watch out for overflow-free comparison: a[i] + a[i+1] > a[i+2]"],
  fixed=[([10, 2, 5, 1, 8, 20],), ([10, 50, 5, 1],), ([],), ([1, 1, 1],), ([1, 2, 3],)],
  rand=lambda rng: (rl(rng, rng.randint(0, 10), 1, 40),),
  notes="Codility Lesson 6. Sorting turns three conditions into one.")

P("max_product_three", "Max Product Of Three", "Medium", "Sorting", "solution", "a", """
Return the maximum product of any three values in the array.

  solution([-3, 1, 2, -2, 5, 6]) -> 60     (2 * 5 * 6)
  solution([-5, -6, 1, 2, 3])    -> 90     (-5 * -6 * 3)

The trap is negatives: two big negatives multiply into a big positive.
""", '''def solution(a):
    ordered = sorted(a)
    return max(ordered[-1] * ordered[-2] * ordered[-3],
               ordered[0] * ordered[1] * ordered[-1])
''', "O(n log n)",
  ["Sort, then there are only TWO candidates",
   "Either the three largest, or the two smallest (most negative) times the largest",
   "max() of those two candidates is the answer"],
  fixed=[([-3, 1, 2, -2, 5, 6],), ([-5, -6, 1, 2, 3],), ([1, 2, 3],),
         ([-1, -2, -3],), ([0, 0, 0, 5],)],
  rand=lambda rng: (rl(rng, rng.randint(3, 12), -30, 30),),
  notes="Codility Lesson 6. Also a very common phone-screen question.")

P("brackets", "Brackets", "Medium", "Stack", "solution", "s", """
Return 1 if the string of brackets is properly nested, otherwise 0.
The string can contain ( ) [ ] { }.

  solution("{[()()]}") -> 1
  solution("([)()]")   -> 0
  solution("")         -> 1
""", '''def solution(s):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in s:
        if ch in "([{":
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return 0
    return 1 if not stack else 0
''', "O(n)",
  ["A stack is the answer — push openers, pop on closers",
   "If the popped opener does not match the closer, fail immediately",
   "At the end the stack must be EMPTY, otherwise something never closed"],
  fixed=[("{[()()]}",), ("([)()]",), ("",), ("(",), (")(",), ("{{{{",)],
  rand=lambda rng: ("".join(rng.choice("()[]{}") for _ in range(rng.randint(0, 10))),),
  notes="Codility Lesson 7 == LeetCode 'Valid Parentheses'. Learn this one cold.")

P("fish", "Fish", "Medium", "Stack", "solution", "a, b", """
N fish flow down a river. a[i] is the size of fish i, b[i] its direction:
0 = upstream (flowing toward smaller indices), 1 = downstream.

When a downstream fish meets an upstream fish, the bigger one eats the smaller.
All sizes are distinct.

Return how many fish stay alive.

  solution([4, 3, 2, 1, 5], [0, 1, 0, 0, 0]) -> 2
""", '''def solution(a, b):
    downstream = []
    alive = 0
    for size, direction in zip(a, b):
        if direction == 1:
            downstream.append(size)
        else:
            while downstream and downstream[-1] < size:
                downstream.pop()
            if not downstream:
                alive += 1
    return alive + len(downstream)
''', "O(n)",
  ["Keep a stack of the downstream fish that are still swimming",
   "An upstream fish fights the top of that stack until it wins or dies",
   "If the stack empties, the upstream fish survives for good"],
  fixed=[([4, 3, 2, 1, 5], [0, 1, 0, 0, 0]), ([1], [0]), ([1, 2], [1, 0]),
         ([5, 1], [1, 0]), ([], [])],
  rand=lambda rng: (lambda n: (rng.sample(range(1, 100), n),
                               [rng.randint(0, 1) for _ in range(n)]))(rng.randint(0, 8)),
  notes="Codility Lesson 7. Same skeleton as 'Asteroid Collision' on LeetCode.")

P("stone_wall", "Stone Wall", "Medium", "Stack", "solution", "h", """
Build a wall whose height at position i must be exactly h[i]. Each stone is a
rectangle of any width but constant height. Return the MINIMUM number of stones.

  solution([8, 8, 5, 7, 9, 8, 7, 4, 8]) -> 7
""", '''def solution(h):
    stack = []
    stones = 0
    for height in h:
        while stack and stack[-1] > height:
            stack.pop()
        if not stack or stack[-1] < height:
            stack.append(height)
            stones += 1
    return stones
''', "O(n)",
  ["A monotonically increasing stack of the heights currently 'open'",
   "Pop everything taller than the current height — those stones are finished",
   "If the top equals the current height, reuse that stone (no new count)"],
  fixed=[([8, 8, 5, 7, 9, 8, 7, 4, 8],), ([],), ([1],), ([1, 1, 1],), ([1, 2, 3, 2, 1],)],
  rand=lambda rng: (rl(rng, rng.randint(0, 12), 1, 10),),
  notes="Codility Lesson 7. Monotonic stack — the same idea as 'Largest Rectangle in Histogram'.")

P("dominator", "Dominator", "Medium", "Counting", "solution", "a", """
The dominator of an array is a value occurring in MORE than half the positions.
Return ANY index holding the dominator, or -1 if there is none.

  solution([3, 4, 3, 2, 3, -1, 3, 3]) -> any index where the value is 3
  solution([1, 2])                    -> -1

Expected O(n) time, O(1) space -> Boyer-Moore voting.
""", '''def solution(a):
    candidate = None
    count = 0
    for value in a:
        if count == 0:
            candidate, count = value, 1
        elif value == candidate:
            count += 1
        else:
            count -= 1
    if candidate is None:
        return -1
    occurrences = a.count(candidate)
    if occurrences * 2 <= len(a):
        return -1
    return a.index(candidate)
''', "O(n) time, O(1) space",
  ["Boyer-Moore: hold one candidate and a counter; matching votes +1, others -1",
   "When the counter hits 0, adopt the current value as the new candidate",
   "You MUST verify the survivor at the end — the vote only finds a candidate"],
  fixed=[([3, 4, 3, 2, 3, -1, 3, 3],), ([1, 2],), ([],), ([7],), ([1, 1, 2],)],
  rand=lambda rng: (_dominator_case(rng),),
  notes="Codility Lesson 8 == LeetCode 'Majority Element'. The verification step is not optional.",
  # any index of the dominator is accepted
  )
_DOMINATOR_CHECK = '''
def check(args, got):
    a = args[0]
    if not a:
        return got == -1
    counts = {}
    for v in a:
        counts[v] = counts.get(v, 0) + 1
    best = max(counts, key=lambda k: counts[k])
    if counts[best] * 2 <= len(a):
        return got == -1
    return isinstance(got, int) and 0 <= got < len(a) and a[got] == best
'''
BANK[-1].checker_src = _DOMINATOR_CHECK  # type: ignore[attr-defined]


def _dominator_case(rng):
    n = rng.randint(1, 12)
    if rng.random() < 0.6:
        dom = rng.randint(1, 5)
        arr = [dom] * (n // 2 + 1) + [rng.randint(6, 9) for _ in range(n - n // 2 - 1)]
    else:
        arr = [rng.randint(1, 9) for _ in range(n)]
    rng.shuffle(arr)
    return arr


P("max_profit", "Max Profit", "Easy", "Greedy", "solution", "a", """
a[i] is a share price on day i. Buy on one day, sell on a LATER day.
Return the maximum profit, or 0 if no profitable trade exists.

  solution([23171, 21011, 21123, 21366, 21013, 21367]) -> 356
  solution([5, 4, 3])                                  -> 0

One pass, O(n).
""", '''def solution(a):
    best = 0
    cheapest = None
    for price in a:
        if cheapest is None or price < cheapest:
            cheapest = price
        else:
            best = max(best, price - cheapest)
    return best
''', "O(n)",
  ["Track the cheapest price seen so far",
   "At every day, the best sale today is price - cheapest",
   "Never let the profit go below 0"],
  fixed=[([23171, 21011, 21123, 21366, 21013, 21367],), ([5, 4, 3],), ([],), ([1],),
         ([1, 2, 3, 4],)],
  rand=lambda rng: (rl(rng, rng.randint(0, 15), 1, 200),),
  notes="Codility Lesson 9 == LeetCode 121 'Best Time to Buy and Sell Stock'.")

P("max_slice_sum", "Max Slice Sum (Kadane)", "Medium", "Dynamic programming",
  "solution", "a", """
Return the maximum sum of any NON-EMPTY contiguous slice.

  solution([3, 2, -6, 4, 0]) -> 5
  solution([-5, -2, -8])     -> -2

This is Kadane's algorithm. Note the array can be all-negative, so starting
`best = 0` is wrong.
""", '''def solution(a):
    best = current = a[0]
    for value in a[1:]:
        current = max(value, current + value)
        best = max(best, current)
    return best
''', "O(n)",
  ["At each element decide: extend the current slice, or start fresh here",
   "current = max(value, current + value)",
   "Initialise BOTH best and current from a[0], not from 0"],
  fixed=[([3, 2, -6, 4, 0],), ([-5, -2, -8],), ([1],), ([-1],), ([2, -1, 2, -1, 2],)],
  rand=lambda rng: (rl(rng, rng.randint(1, 15), -20, 20),),
  notes="Codility Lesson 9 == LeetCode 53 'Maximum Subarray'. Memorise the two lines.")

P("count_factors", "Count Factors", "Medium", "Math", "solution", "n", """
Return how many factors (divisors) the positive integer n has.

  solution(24) -> 8      (1, 2, 3, 4, 6, 8, 12, 24)
  solution(1)  -> 1

n goes up to 2,147,483,647, so trial division up to n is far too slow.
Only go up to sqrt(n) and count both members of each pair.
""", '''def solution(n):
    count = 0
    i = 1
    while i * i < n:
        if n % i == 0:
            count += 2
        i += 1
    if i * i == n:
        count += 1
    return count
''', "O(sqrt n)",
  ["Divisors come in pairs: if i divides n, so does n // i",
   "Loop while i * i < n and add 2 for each hit",
   "A perfect square has one unpaired divisor — handle i * i == n separately"],
  fixed=[(24,), (1,), (36,), (2147483647,), (97,)],
  rand=lambda rng: (rng.randint(1, 10 ** 6),),
  notes="Codility Lesson 10. Use i*i < n, not i < sqrt(n) — no float rounding bugs.")

P("min_perimeter", "Min Perimeter Rectangle", "Medium", "Math", "solution", "n", """
Find the minimal perimeter of a rectangle with integer sides whose area is
exactly n.

  solution(30) -> 22     (5 x 6)
  solution(1)  -> 4

Perimeter = 2 * (a + b) where a * b == n. The most "square" pair wins, so walk
down from sqrt(n).
""", '''def solution(n):
    i = 1
    best = None
    while i * i <= n:
        if n % i == 0:
            best = 2 * (i + n // i)
        i += 1
    return best
''', "O(sqrt n)",
  ["Only check divisors up to sqrt(n)",
   "The LAST divisor you find below sqrt(n) is the most square one",
   "perimeter = 2 * (i + n // i)"],
  fixed=[(30,), (1,), (36,), (101,), (1000000,)],
  rand=lambda rng: (rng.randint(1, 10 ** 6),),
  notes="Codility Lesson 10.")

P("chocolates", "Chocolates By Numbers", "Medium", "Math", "solution", "n, m", """
There are N chocolates in a circle, numbered 0..N-1. You eat chocolate 0, then
jump M forward each time (wrapping around), until you reach one you already ate.

Return how many you eat.

  solution(10, 4) -> 5

The cycle length is n / gcd(n, m). Prove it, then it is a one-liner.
N and M go up to 1,000,000,000, so simulating the walk is not an option.
""", '''def solution(n, m):
    x, y = n, m
    while y:
        x, y = y, x % y
    return n // x
''', "O(log n)",
  ["Simulating is O(n) — too slow at 1e9",
   "You visit exactly n // gcd(n, m) distinct chocolates",
   "Implement Euclid's gcd with the while loop"],
  fixed=[(10, 4), (1, 1), (947853, 4453), (10, 10), (13, 5)],
  rand=lambda rng: (rng.randint(1, 10 ** 6), rng.randint(1, 10 ** 6)),
  notes="Codility Lesson 12. Number theory disguised as a simulation.")

P("genomic_range", "Genomic Range Query", "Hard", "Prefix sums", "solution", "s, p, q", """
A DNA string of A, C, G, T. Each letter has an impact factor: A=1, C=2, G=3, T=4.

For each query (p[k], q[k]) — an inclusive slice of the string — return the
MINIMAL impact factor inside it.

  solution("CAGCCTA", [2, 5, 0], [4, 5, 6]) -> [2, 4, 1]

There can be 50,000 queries over a 100,000-character string, so scanning each
slice is O(n*m) and times out. Build four prefix-count arrays instead: then each
query is O(1).
""", '''def solution(s, p, q):
    n = len(s)
    letters = "ACGT"
    prefix = [[0] * (n + 1) for _ in range(4)]
    for i, ch in enumerate(s):
        for k in range(4):
            prefix[k][i + 1] = prefix[k][i] + (1 if ch == letters[k] else 0)
    out = []
    for start, end in zip(p, q):
        for k in range(4):
            if prefix[k][end + 1] - prefix[k][start] > 0:
                out.append(k + 1)
                break
    return out
''', "O(n + m)",
  ["Build one prefix-count array per letter: how many A's in s[0..i)",
   "Count of letter k inside [start, end] = prefix[k][end+1] - prefix[k][start]",
   "For each query, check A first, then C, then G, then T — the first non-zero wins"],
  fixed=[("CAGCCTA", [2, 5, 0], [4, 5, 6]), ("A", [0], [0]), ("TTTT", [0, 1], [3, 2])],
  rand=lambda rng: _genomic_case(rng),
  notes="Codility Lesson 5 (hard). The 'prefix count per category' trick generalises a lot.")


def _genomic_case(rng):
    s = "".join(rng.choice("ACGT") for _ in range(rng.randint(1, 20)))
    n = len(s)
    p, q = [], []
    for _ in range(rng.randint(1, 5)):
        a = rng.randrange(n)
        b = rng.randrange(a, n)
        p.append(a)
        q.append(b)
    return (s, p, q)


P("nesting", "Nesting", "Easy", "Stack", "solution", "s", """
Return 1 if the string of only ( and ) is properly nested, else 0.

  solution("(()(())())") -> 1
  solution("())")        -> 0
  solution("")           -> 1

O(1) space: you only need a counter, not a stack.
""", '''def solution(s):
    depth = 0
    for ch in s:
        depth += 1 if ch == "(" else -1
        if depth < 0:
            return 0
    return 1 if depth == 0 else 0
''', "O(n) time, O(1) space",
  ["A single depth counter is enough when there is only one bracket type",
   "If the depth ever goes negative, a ) came too early",
   "It must end at exactly 0"],
  fixed=[("(()(())())",), ("())",), ("",), ("(",), ("()()",)],
  rand=lambda rng: ("".join(rng.choice("()") for _ in range(rng.randint(0, 12))),),
  notes="Codility Lesson 7. The counter version is the answer they want.")

P("number_of_disc", "Number Of Disc Intersections", "Hard", "Sorting", "solution", "a", """
Disc i is centred at (i, 0) with radius a[i]. Two discs intersect if they touch
or overlap.

Return the number of intersecting PAIRS, or -1 if it exceeds 10,000,000.

  solution([1, 5, 2, 1, 4, 0]) -> 11

The O(n^2) pairwise check times out at N = 100,000. Sort the interval starts and
ends, then sweep: at each start, every disc still open intersects it.
""", '''def solution(a):
    starts = sorted(i - r for i, r in enumerate(a))
    ends = sorted(i + r for i, r in enumerate(a))
    pairs = 0
    open_discs = 0
    j = 0
    for start in starts:
        while j < len(ends) and ends[j] < start:
            open_discs -= 1
            j += 1
        pairs += open_discs
        open_discs += 1
        if pairs > 10000000:
            return -1
    return pairs
''', "O(n log n)",
  ["Turn each disc into an interval [i - r, i + r]",
   "Sort starts and ends separately, then sweep with two pointers",
   "When a new disc opens, it intersects every disc still open"],
  fixed=[([1, 5, 2, 1, 4, 0],), ([],), ([0, 0],), ([1, 1],), ([0],)],
  rand=lambda rng: (rl(rng, rng.randint(0, 12), 0, 10),),
  notes="Codility Lesson 6 (hard). The sweep-line pattern shows up in calendar/meeting problems too.")

P("equi_leader", "Equi Leader", "Medium", "Counting", "solution", "a", """
A leader of an array is a value occurring in more than half its positions.
An equi leader is an index S such that a[0..S] and a[S+1..n-1] have the SAME
leader.

Return how many equi leaders exist.

  solution([4, 3, 4, 4, 4, 2]) -> 2
""", '''def solution(a):
    n = len(a)
    candidate, count = None, 0
    for value in a:
        if count == 0:
            candidate, count = value, 1
        elif value == candidate:
            count += 1
        else:
            count -= 1
    if candidate is None:
        return 0
    total = a.count(candidate)
    if total * 2 <= n:
        return 0
    equi = 0
    left = 0
    for i in range(n - 1):
        if a[i] == candidate:
            left += 1
        if left * 2 > i + 1 and (total - left) * 2 > n - i - 1:
            equi += 1
    return equi
''', "O(n)",
  ["Only the array's own leader can be the leader of both halves",
   "Find it with Boyer-Moore, then verify it really is a leader",
   "Sweep once keeping the count in the left part; the right count is total - left"],
  fixed=[([4, 3, 4, 4, 4, 2],), ([],), ([1, 1],), ([1, 2],), ([2, 2, 2, 2],)],
  rand=lambda rng: (_dominator_case(rng),),
  notes="Codility Lesson 8. Combines Boyer-Moore with a prefix sweep.")

# ============================================================================
#  LEETCODE PATTERNS
# ============================================================================

P("two_sum", "Two Sum", "Easy", "Hash map", "two_sum", "nums, target", """
Return the INDICES of the two numbers that add up to target, as a list
[i, j] with i < j. Exactly one solution exists and you may not reuse an element.

  two_sum([2, 7, 11, 15], 9) -> [0, 1]
  two_sum([3, 3], 6)         -> [0, 1]

O(n) with a dict of value -> index. The O(n^2) double loop is the "no" answer.
""", '''def two_sum(nums, target):
    seen = {}
    for i, value in enumerate(nums):
        if target - value in seen:
            return [seen[target - value], i]
        seen[value] = i
    return []
''', "O(n)",
  ["Store value -> index as you go",
   "For each value ask whether target - value was already seen",
   "Insert AFTER the lookup so an element cannot pair with itself"],
  fixed=[([2, 7, 11, 15], 9), ([3, 3], 6), ([3, 2, 4], 6), ([-1, -2, -3], -5)],
  rand=lambda rng: _two_sum_case(rng),
  notes="LeetCode 1. The most-asked question in existence — never miss it.")


def _two_sum_case(rng):
    nums = rng.sample(range(-40, 60), rng.randint(2, 10))
    i, j = sorted(rng.sample(range(len(nums)), 2))
    return (nums, nums[i] + nums[j])


P("valid_parens", "Valid Parentheses", "Easy", "Stack", "is_valid", "s", """
Given a string of just ()[]{}, decide whether every bracket is closed by the
same type, in the right order.

  is_valid("()[]{}") -> True
  is_valid("(]")     -> False
  is_valid("([)]")   -> False
""", '''def is_valid(s):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in s:
        if ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
        else:
            stack.append(ch)
    return not stack
''', "O(n)",
  ["Push openers onto a stack",
   "On a closer, the popped item must be its matching opener",
   "Empty stack at the end = valid"],
  fixed=[("()[]{}",), ("(]",), ("([)]",), ("",), ("{[]}",)],
  rand=lambda rng: ("".join(rng.choice("()[]{}") for _ in range(rng.randint(0, 10))),),
  notes="LeetCode 20.")

P("max_subarray", "Maximum Subarray", "Medium", "Dynamic programming",
  "max_subarray", "nums", """
Return the largest sum of a contiguous non-empty subarray.

  max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]) -> 6      ([4, -1, 2, 1])
  max_subarray([-1])                            -> -1
""", '''def max_subarray(nums):
    best = current = nums[0]
    for value in nums[1:]:
        current = max(value, current + value)
        best = max(best, current)
    return best
''', "O(n)",
  ["Kadane's algorithm",
   "current = max(value, current + value) — restart or extend",
   "All-negative input means you cannot start at 0"],
  fixed=[([-2, 1, -3, 4, -1, 2, 1, -5, 4],), ([-1],), ([5, 4, -1, 7, 8],), ([1],)],
  rand=lambda rng: (rl(rng, rng.randint(1, 15), -15, 15),),
  notes="LeetCode 53.")

P("product_except_self", "Product of Array Except Self", "Medium", "Prefix sums",
  "product_except_self", "nums", """
Return a list where out[i] is the product of every element EXCEPT nums[i].

  product_except_self([1, 2, 3, 4]) -> [24, 12, 8, 6]
  product_except_self([-1, 1, 0, -3, 3]) -> [0, 0, 9, 0, 0]

You must do it WITHOUT division, in O(n).
""", '''def product_except_self(nums):
    n = len(nums)
    out = [1] * n
    running = 1
    for i in range(n):
        out[i] = running
        running *= nums[i]
    running = 1
    for i in range(n - 1, -1, -1):
        out[i] *= running
        running *= nums[i]
    return out
''', "O(n) time, O(1) extra space",
  ["out[i] = (product of everything left of i) * (product of everything right of i)",
   "First pass left-to-right fills in the left products",
   "Second pass right-to-left multiplies in the right products"],
  fixed=[([1, 2, 3, 4],), ([-1, 1, 0, -3, 3],), ([1, 1],), ([0, 0],), ([5],)],
  rand=lambda rng: (rl(rng, rng.randint(1, 8), -5, 5),),
  notes="LeetCode 238. The no-division constraint is the whole exercise.")

P("longest_unique", "Longest Substring Without Repeating Characters", "Medium",
  "Sliding window", "length_of_longest", "s", """
Return the length of the longest substring with no repeated character.

  length_of_longest("abcabcbb") -> 3     ("abc")
  length_of_longest("bbbbb")    -> 1
  length_of_longest("pwwkew")   -> 3     ("wke")
""", '''def length_of_longest(s):
    last_seen = {}
    left = 0
    best = 0
    for right, ch in enumerate(s):
        if ch in last_seen and last_seen[ch] >= left:
            left = last_seen[ch] + 1
        last_seen[ch] = right
        best = max(best, right - left + 1)
    return best
''', "O(n)",
  ["Sliding window with a dict of char -> last index",
   "When you hit a repeat INSIDE the window, jump left past its previous position",
   "The `>= left` check matters — old occurrences outside the window are harmless"],
  fixed=[("abcabcbb",), ("bbbbb",), ("pwwkew",), ("",), ("dvdf",)],
  rand=lambda rng: ("".join(rng.choice("abcde") for _ in range(rng.randint(0, 15))),),
  notes="LeetCode 3. The textbook sliding-window problem.")

P("group_anagrams", "Group Anagrams", "Medium", "Hash map", "group_anagrams", "words", """
Group words that are anagrams of each other.

Return a list of groups. Sort each group alphabetically, and sort the groups by
their first element, so the answer is unique.

  group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
    -> [["ate", "eat", "tea"], ["bat"], ["nat", "tan"]]
""", '''def group_anagrams(words):
    buckets = {}
    for word in words:
        key = "".join(sorted(word))
        buckets.setdefault(key, []).append(word)
    return sorted((sorted(group) for group in buckets.values()),
                  key=lambda group: group[0])
''', "O(n * k log k)",
  ['The sorted letters of a word are its anagram fingerprint: "eat" -> "aet"',
   "Bucket the words into a dict keyed by that fingerprint",
   "Then sort inside each group and sort the groups"],
  fixed=[(["eat", "tea", "tan", "ate", "nat", "bat"],), ([],), (["a"],),
         (["ab", "ba", "abc"],)],
  rand=lambda rng: ([_scramble(rng, rng.choice(["cat", "dog", "star", "loop"]))
                     for _ in range(rng.randint(1, 8))],),
  notes="LeetCode 49. 'Fingerprint into a dict' is a pattern worth naming out loud.")


def _scramble(rng, word):
    letters = list(word)
    rng.shuffle(letters)
    return "".join(letters)


P("merge_intervals", "Merge Intervals", "Medium", "Sorting", "merge", "intervals", """
Merge all overlapping intervals. Intervals touch-merge too: [1,4] and [4,5]
become [1,5].

Input and output are lists of two-element lists, sorted by start.

  merge([[1, 3], [2, 6], [8, 10], [15, 18]]) -> [[1, 6], [8, 10], [15, 18]]
  merge([[1, 4], [4, 5]])                    -> [[1, 5]]
""", '''def merge(intervals):
    if not intervals:
        return []
    ordered = sorted(intervals, key=lambda pair: pair[0])
    out = [list(ordered[0])]
    for start, end in ordered[1:]:
        if start <= out[-1][1]:
            out[-1][1] = max(out[-1][1], end)
        else:
            out.append([start, end])
    return out
''', "O(n log n)",
  ["Sort by start — after that a single pass is enough",
   "Overlap test: the next start is <= the current end",
   "When merging, take max of the ends (one interval can swallow another)"],
  fixed=[([[1, 3], [2, 6], [8, 10], [15, 18]],), ([[1, 4], [4, 5]],), ([],),
         ([[1, 4], [2, 3]],)],
  rand=lambda rng: ([sorted((rng.randint(0, 20), rng.randint(0, 20)))
                     for _ in range(rng.randint(0, 6))],),
  notes="LeetCode 56. Sorting first is 90% of every interval problem.")

P("binary_search", "Binary Search", "Easy", "Binary search", "search", "nums, target", """
`nums` is sorted ascending. Return the index of target, or -1 if absent.
Must be O(log n).

  search([-1, 0, 3, 5, 9, 12], 9) -> 4
  search([-1, 0, 3, 5, 9, 12], 2) -> -1
""", '''def search(nums, target):
    low, high = 0, len(nums) - 1
    while low <= high:
        mid = (low + high) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1
''', "O(log n)",
  ["low, high = 0, len(nums) - 1 and loop while low <= high",
   "mid = (low + high) // 2",
   "Move low to mid + 1 or high to mid - 1 — never to mid, or you loop forever"],
  fixed=[([-1, 0, 3, 5, 9, 12], 9), ([-1, 0, 3, 5, 9, 12], 2), ([], 1), ([5], 5)],
  rand=lambda rng: (lambda nums: (nums, rng.choice(nums + [999]) if nums else 1))(
      sorted(rng.sample(range(-50, 50), rng.randint(0, 12)))),
  notes="LeetCode 704. Write it from memory until the off-by-ones stop happening.")

P("search_rotated", "Search in Rotated Sorted Array", "Medium", "Binary search",
  "search", "nums, target", """
A sorted array was rotated at an unknown pivot ([0,1,2,4,5,6,7] might become
[4,5,6,7,0,1,2]). Find target's index, or -1. Still O(log n).

  search([4, 5, 6, 7, 0, 1, 2], 0) -> 4
  search([4, 5, 6, 7, 0, 1, 2], 3) -> -1
""", '''def search(nums, target):
    low, high = 0, len(nums) - 1
    while low <= high:
        mid = (low + high) // 2
        if nums[mid] == target:
            return mid
        if nums[low] <= nums[mid]:              # left half is sorted
            if nums[low] <= target < nums[mid]:
                high = mid - 1
            else:
                low = mid + 1
        else:                                    # right half is sorted
            if nums[mid] < target <= nums[high]:
                low = mid + 1
            else:
                high = mid - 1
    return -1
''', "O(log n)",
  ["At every step at least ONE half is properly sorted — figure out which",
   "nums[low] <= nums[mid] means the left half is sorted",
   "Then check whether the target lies inside that sorted half; if yes go there"],
  fixed=[([4, 5, 6, 7, 0, 1, 2], 0), ([4, 5, 6, 7, 0, 1, 2], 3), ([1], 1), ([], 5)],
  rand=lambda rng: _rotated_case(rng),
  notes="LeetCode 33. A favourite because it tests whether you really understand binary search.")


def _rotated_case(rng):
    base = sorted(rng.sample(range(-30, 30), rng.randint(1, 10)))
    k = rng.randrange(len(base))
    rotated = base[k:] + base[:k]
    target = rng.choice(base + [999])
    return (rotated, target)


P("climb_stairs", "Climbing Stairs", "Easy", "Dynamic programming", "climb_stairs", "n", """
You climb a staircase of n steps, taking 1 or 2 steps at a time.
How many distinct ways are there to reach the top?

  climb_stairs(2) -> 2      (1+1, 2)
  climb_stairs(3) -> 3      (1+1+1, 1+2, 2+1)

n can be 45, so plain recursion is far too slow — this is Fibonacci in disguise.
""", '''def climb_stairs(n):
    if n <= 2:
        return max(n, 1)
    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b
''', "O(n) time, O(1) space",
  ["ways(n) = ways(n-1) + ways(n-2) — you arrived from one step below or two",
   "Iterate bottom-up with two rolling variables",
   "n = 0 and n = 1 both have exactly 1 way"],
  fixed=[(2,), (3,), (1,), (0,), (10,), (45,)],
  rand=lambda rng: (rng.randint(0, 40),),
  notes="LeetCode 70. The gateway to every DP question.")

P("coin_change", "Coin Change", "Medium", "Dynamic programming", "coin_change",
  "coins, amount", """
Return the FEWEST coins needed to make `amount`, or -1 if impossible.
You have an unlimited supply of each coin.

  coin_change([1, 2, 5], 11) -> 3      (5 + 5 + 1)
  coin_change([2], 3)        -> -1
  coin_change([1], 0)        -> 0

Greedy (always take the biggest coin) is WRONG here — try coins [1, 3, 4],
amount 6. You need DP.
""", '''def coin_change(coins, amount):
    INF = float("inf")
    dp = [0] + [INF] * amount
    for value in range(1, amount + 1):
        for coin in coins:
            if coin <= value and dp[value - coin] + 1 < dp[value]:
                dp[value] = dp[value - coin] + 1
    return -1 if dp[amount] == INF else dp[amount]
''', "O(amount * len(coins))",
  ["dp[v] = fewest coins to make exactly v; dp[0] = 0",
   "dp[v] = min over coins of dp[v - coin] + 1",
   "Use infinity for unreachable amounts so the min works naturally"],
  fixed=[([1, 2, 5], 11), ([2], 3), ([1], 0), ([1, 3, 4], 6), ([5], 5)],
  rand=lambda rng: (sorted(rng.sample(range(1, 12), rng.randint(1, 4))),
                    rng.randint(0, 40)),
  notes="LeetCode 322. Unbounded knapsack — the shape shows up constantly.")

P("house_robber", "House Robber", "Medium", "Dynamic programming", "rob", "nums", """
Each house holds some money. You cannot rob two ADJACENT houses.
Return the maximum you can take.

  rob([1, 2, 3, 1]) -> 4     (houses 0 and 2)
  rob([2, 7, 9, 3, 1]) -> 12 (houses 0, 2, 4)
  rob([]) -> 0
""", '''def rob(nums):
    take, skip = 0, 0
    for value in nums:
        take, skip = skip + value, max(skip, take)
    return max(take, skip)
''', "O(n) time, O(1) space",
  ["At each house: either rob it (and add the best from two back) or skip it",
   "Two rolling variables are enough — no array needed",
   "take, skip = skip + value, max(skip, take)"],
  fixed=[([1, 2, 3, 1],), ([2, 7, 9, 3, 1],), ([],), ([5],), ([2, 1, 1, 2],)],
  rand=lambda rng: (rl(rng, rng.randint(0, 12), 0, 40),),
  notes="LeetCode 198. Notice the O(1)-space rewrite — interviewers ask for it.")

P("longest_consecutive", "Longest Consecutive Sequence", "Medium", "Hash map",
  "longest_consecutive", "nums", """
Return the length of the longest run of CONSECUTIVE integers present in the
array (order in the array does not matter).

  longest_consecutive([100, 4, 200, 1, 3, 2]) -> 4      (1, 2, 3, 4)
  longest_consecutive([]) -> 0

Must be O(n) — so sorting is technically off the table.
""", '''def longest_consecutive(nums):
    values = set(nums)
    best = 0
    for value in values:
        if value - 1 in values:
            continue                # not the start of a run
        length = 1
        while value + length in values:
            length += 1
        best = max(best, length)
    return best
''', "O(n)",
  ["Put everything in a set for O(1) membership",
   "Only start counting from values that have no predecessor in the set",
   "That guard is what keeps it O(n) instead of O(n^2)"],
  fixed=[([100, 4, 200, 1, 3, 2],), ([],), ([1, 1, 1],), ([0, -1, 1],)],
  rand=lambda rng: (rl(rng, rng.randint(0, 15), -10, 15),),
  notes="LeetCode 128. The 'only start at run beginnings' trick is the interview point.")

P("three_sum", "3Sum", "Medium", "Two pointers", "three_sum", "nums", """
Find all UNIQUE triplets that sum to zero. Return them sorted: each triplet
ascending, and the list of triplets sorted too.

  three_sum([-1, 0, 1, 2, -1, -4]) -> [[-1, -1, 2], [-1, 0, 1]]
  three_sum([0, 0, 0, 0])          -> [[0, 0, 0]]

O(n^2): sort, fix one element, two-pointer the rest.
""", '''def three_sum(nums):
    ordered = sorted(nums)
    n = len(ordered)
    out = []
    for i in range(n - 2):
        if i > 0 and ordered[i] == ordered[i - 1]:
            continue
        left, right = i + 1, n - 1
        while left < right:
            total = ordered[i] + ordered[left] + ordered[right]
            if total < 0:
                left += 1
            elif total > 0:
                right -= 1
            else:
                out.append([ordered[i], ordered[left], ordered[right]])
                left += 1
                while left < right and ordered[left] == ordered[left - 1]:
                    left += 1
                right -= 1
    return out
''', "O(n^2)",
  ["Sort first, then fix nums[i] and two-pointer the remaining subarray",
   "Skip duplicate values for i, otherwise you emit the same triplet twice",
   "After recording a hit, skip duplicates on the left pointer as well"],
  fixed=[([-1, 0, 1, 2, -1, -4],), ([0, 0, 0, 0],), ([],), ([1, 2, 3],)],
  rand=lambda rng: (rl(rng, rng.randint(0, 10), -6, 6),),
  notes="LeetCode 15. The duplicate-skipping is where most people lose the offer.")

P("container_water", "Container With Most Water", "Medium", "Two pointers",
  "max_area", "heights", """
Each heights[i] is a vertical line at x = i. Pick two lines that, with the
x-axis, hold the most water.

  max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]) -> 49
  max_area([1, 1]) -> 1

O(n) with two pointers from the ends.
""", '''def max_area(heights):
    left, right = 0, len(heights) - 1
    best = 0
    while left < right:
        best = max(best, (right - left) * min(heights[left], heights[right]))
        if heights[left] < heights[right]:
            left += 1
        else:
            right -= 1
    return best
''', "O(n)",
  ["Start wide: one pointer at each end",
   "Area = width * the SHORTER of the two lines",
   "Always move the shorter line inward — moving the taller one can never help"],
  fixed=[([1, 8, 6, 2, 5, 4, 8, 3, 7],), ([1, 1],), ([],), ([4, 3, 2, 1, 4],)],
  rand=lambda rng: (rl(rng, rng.randint(0, 12), 0, 20),),
  notes="LeetCode 11. Be ready to justify WHY moving the shorter side is safe.")

P("move_zeroes", "Move Zeroes", "Easy", "Two pointers", "move_zeroes", "nums", """
Move every 0 to the end while keeping the order of the non-zero values.
Return the resulting list.

  move_zeroes([0, 1, 0, 3, 12]) -> [1, 3, 12, 0, 0]
  move_zeroes([0]) -> [0]
""", '''def move_zeroes(nums):
    out = [value for value in nums if value != 0]
    return out + [0] * (len(nums) - len(out))
''', "O(n)",
  ["Collect the non-zeros in order",
   "Pad the rest with zeros",
   "The in-place version swaps with a `write` pointer — mention it if asked"],
  fixed=[([0, 1, 0, 3, 12],), ([0],), ([],), ([1, 2, 3],), ([0, 0, 1],)],
  rand=lambda rng: ([rng.choice([0, 0, rng.randint(1, 9)]) for _ in range(rng.randint(0, 12))],),
  notes="LeetCode 283.")

P("rotate_array", "Rotate Array", "Medium", "Arrays", "rotate", "nums, k", """
Rotate the list right by k steps and return it.

  rotate([1, 2, 3, 4, 5, 6, 7], 3) -> [5, 6, 7, 1, 2, 3, 4]
  rotate([-1, -100, 3, 99], 2)     -> [3, 99, -1, -100]

k may exceed the length.
""", '''def rotate(nums, k):
    if not nums:
        return []
    k %= len(nums)
    return nums[-k:] + nums[:-k] if k else nums[:]
''', "O(n)",
  ["k %= len(nums) first", "Slice: nums[-k:] + nums[:-k]",
   "k == 0 needs its own branch, because nums[-0:] is the whole list"],
  fixed=[([1, 2, 3, 4, 5, 6, 7], 3), ([-1, -100, 3, 99], 2), ([], 3), ([1], 0)],
  rand=lambda rng: (rl(rng, rng.randint(0, 10), -20, 20), rng.randint(0, 15)),
  notes="LeetCode 189.")

P("majority_element", "Majority Element", "Easy", "Counting", "majority", "nums", """
The majority element appears MORE than n/2 times. It always exists here.
Return it.

  majority([3, 2, 3])          -> 3
  majority([2, 2, 1, 1, 1, 2, 2]) -> 2

Bonus goal: O(1) extra space (Boyer-Moore voting).
""", '''def majority(nums):
    candidate, count = None, 0
    for value in nums:
        if count == 0:
            candidate = value
        count += 1 if value == candidate else -1
    return candidate
''', "O(n) time, O(1) space",
  ["A Counter answers it in O(n) space — say that, then improve it",
   "Boyer-Moore: keep a candidate and a vote counter",
   "Reset the candidate whenever the counter hits zero"],
  fixed=[([3, 2, 3],), ([2, 2, 1, 1, 1, 2, 2],), ([1],), ([6, 5, 5],)],
  rand=lambda rng: (_majority_case(rng),),
  notes="LeetCode 169.")


def _majority_case(rng):
    n = rng.randint(1, 11)
    dom = rng.randint(1, 5)
    arr = [dom] * (n // 2 + 1) + [rng.randint(6, 9) for _ in range(n - n // 2 - 1)]
    rng.shuffle(arr)
    return arr


P("single_number", "Single Number", "Easy", "Bit tricks", "single_number", "nums", """
Every element appears twice except one. Find that one.

  single_number([4, 1, 2, 1, 2]) -> 4

Linear time, constant extra space.
""", '''def single_number(nums):
    result = 0
    for value in nums:
        result ^= value
    return result
''', "O(n) time, O(1) space",
  ["x ^ x == 0, and x ^ 0 == x", "XOR the whole array together"],
  fixed=[([4, 1, 2, 1, 2],), ([1],), ([0, 1, 0],)],
  rand=lambda rng: (_odd_array(rng),),
  notes="LeetCode 136.")

P("top_k_frequent", "Top K Frequent Elements", "Medium", "Hash map",
  "top_k_frequent", "nums, k", """
Return the k most frequent values. Sort the answer ascending so it is unique.

  top_k_frequent([1, 1, 1, 2, 2, 3], 2) -> [1, 2]
  top_k_frequent([1], 1)                -> [1]
""", '''def top_k_frequent(nums, k):
    counts = {}
    for value in nums:
        counts[value] = counts.get(value, 0) + 1
    ordered = sorted(counts, key=lambda value: (-counts[value], value))
    return sorted(ordered[:k])
''', "O(n log n) — O(n) with bucket sort",
  ["Count into a dict, then sort the keys by -count",
   "heapq.nlargest(k, counts, key=counts.get) is the O(n log k) version",
   "Bucket sort by frequency gets you a true O(n) — worth mentioning"],
  fixed=[([1, 1, 1, 2, 2, 3], 2), ([1], 1), ([1, 2], 2)],
  rand=lambda rng: (lambda nums: (nums, rng.randint(1, max(1, len(set(nums))))))(
      [rng.randint(1, 5) for _ in range(rng.randint(1, 15))]),
  notes="LeetCode 347.")

P("valid_palindrome", "Valid Palindrome", "Easy", "Two pointers", "is_palindrome", "s", """
Ignoring case and everything that is not a letter or digit, is the string a
palindrome?

  is_palindrome("A man, a plan, a canal: Panama") -> True
  is_palindrome("race a car")                     -> False
  is_palindrome(" ")                              -> True
""", '''def is_palindrome(s):
    cleaned = [ch.lower() for ch in s if ch.isalnum()]
    return cleaned == cleaned[::-1]
''', "O(n)",
  ["Filter with ch.isalnum(), lower-case as you go",
   "Compare the cleaned list with its reverse",
   "The O(1)-space version walks two pointers inward — mention it"],
  fixed=[("A man, a plan, a canal: Panama",), ("race a car",), (" ",), ("",), ("0P",)],
  rand=lambda rng: ("".join(rng.choice("aabb ,.") for _ in range(rng.randint(0, 12))),),
  notes="LeetCode 125.")

P("longest_common_prefix", "Longest Common Prefix", "Easy", "Strings",
  "longest_common_prefix", "words", """
Return the longest string that starts every word in the list.
Return "" if there is none.

  longest_common_prefix(["flower", "flow", "flight"]) -> "fl"
  longest_common_prefix(["dog", "racecar", "car"])    -> ""
  longest_common_prefix([])                           -> ""
""", '''def longest_common_prefix(words):
    if not words:
        return ""
    shortest = min(words, key=len)
    for i, ch in enumerate(shortest):
        for word in words:
            if word[i] != ch:
                return shortest[:i]
    return shortest
''', "O(total characters)",
  ["The answer can never be longer than the shortest word",
   "Walk the shortest word character by character and check every other word",
   "Bail out at the first mismatch"],
  fixed=[(["flower", "flow", "flight"],), (["dog", "racecar", "car"],), ([],),
         (["a"],), (["", "abc"],)],
  rand=lambda rng: ([rng.choice(["pre", "prefix", "press", "zebra"]) + "x" * rng.randint(0, 3)
                     for _ in range(rng.randint(1, 5))],),
  notes="LeetCode 14.")

P("roman_to_int", "Roman to Integer", "Easy", "Strings", "roman_to_int", "s", """
Convert a Roman numeral to an integer. Symbols: I=1 V=5 X=10 L=50 C=100 D=500
M=1000. A smaller value BEFORE a larger one is subtracted (IV = 4, CM = 900).

  roman_to_int("III")     -> 3
  roman_to_int("LVIII")   -> 58
  roman_to_int("MCMXCIV") -> 1994
""", '''def roman_to_int(s):
    values = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    total = 0
    for i, ch in enumerate(s):
        if i + 1 < len(s) and values[ch] < values[s[i + 1]]:
            total -= values[ch]
        else:
            total += values[ch]
    return total
''', "O(n)",
  ["Map each symbol to its value in a dict",
   "If a symbol is smaller than the NEXT one, subtract it instead of adding",
   "One pass, no special-casing IV / IX / XL individually"],
  fixed=[("III",), ("LVIII",), ("MCMXCIV",), ("IV",), ("MMMCMXCIX",)],
  rand=lambda rng: (rng.choice(["XII", "XL", "XCIX", "CDXLIV", "MMXXVI", "IX", "DCCC"]),),
  notes="LeetCode 13.")

P("spiral_matrix", "Spiral Matrix", "Medium", "Matrix", "spiral_order", "matrix", """
Return all elements of the matrix in spiral order (right, down, left, up,
inward).

  spiral_order([[1,2,3],[4,5,6],[7,8,9]]) -> [1,2,3,6,9,8,7,4,5]
  spiral_order([]) -> []

The matrix can be non-square.
""", '''def spiral_order(matrix):
    if not matrix or not matrix[0]:
        return []
    out = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    while top <= bottom and left <= right:
        for col in range(left, right + 1):
            out.append(matrix[top][col])
        top += 1
        for row in range(top, bottom + 1):
            out.append(matrix[row][right])
        right -= 1
        if top <= bottom:
            for col in range(right, left - 1, -1):
                out.append(matrix[bottom][col])
            bottom -= 1
        if left <= right:
            for row in range(bottom, top - 1, -1):
                out.append(matrix[row][left])
            left += 1
    return out
''', "O(rows * cols)",
  ["Keep four boundaries: top, bottom, left, right",
   "Walk one edge, then shrink that boundary",
   "Re-check the bounds before the bottom row and left column, or you double-visit"],
  fixed=[([[1, 2, 3], [4, 5, 6], [7, 8, 9]],), ([],), ([[1]],),
         ([[1, 2], [3, 4], [5, 6]],)],
  rand=lambda rng: (rgrid(rng, list(range(10))),),
  notes="LeetCode 54. Pure boundary bookkeeping — no cleverness, just care.")

P("num_islands", "Number of Islands", "Medium", "Graphs", "num_islands", "grid", """
The grid holds "1" (land) and "0" (water) as STRINGS. An island is a group of
1s connected horizontally or vertically. Count the islands.

  num_islands([["1","1","0"],
               ["1","0","0"],
               ["0","0","1"]]) -> 2

Flood-fill each island the first time you touch it.
""", '''def num_islands(grid):
    if not grid or not grid[0]:
        return 0
    rows, cols = len(grid), len(grid[0])
    seen = set()
    islands = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != "1" or (r, c) in seen:
                continue
            islands += 1
            stack = [(r, c)]
            seen.add((r, c))
            while stack:
                cr, cc = stack.pop()
                for nr, nc in ((cr + 1, cc), (cr - 1, cc), (cr, cc + 1), (cr, cc - 1)):
                    if (0 <= nr < rows and 0 <= nc < cols
                            and grid[nr][nc] == "1" and (nr, nc) not in seen):
                        seen.add((nr, nc))
                        stack.append((nr, nc))
    return islands
''', "O(rows * cols)",
  ["Scan every cell; when you find unvisited land, that is a NEW island",
   "Flood-fill it with an explicit stack (or a deque for BFS) and mark everything seen",
   "Mark cells as seen when you PUSH them, not when you pop — otherwise duplicates"],
  fixed=[([["1", "1", "0"], ["1", "0", "0"], ["0", "0", "1"]],), ([],),
         ([["0"]],), ([["1", "0", "1"]],)],
  rand=lambda rng: (rgrid(rng, ["0", "1"]),),
  notes="LeetCode 200. Your one grid-traversal template — learn it once, reuse forever.")

P("merge_sorted", "Merge Two Sorted Lists", "Easy", "Two pointers", "merge_sorted",
  "a, b", """
Merge two ascending lists into one ascending list.

  merge_sorted([1, 2, 4], [1, 3, 4]) -> [1, 1, 2, 3, 4, 4]
  merge_sorted([], [0])              -> [0]

Do the real merge with two pointers — sorted(a + b) works but misses the point.
""", '''def merge_sorted(a, b):
    out = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            out.append(a[i])
            i += 1
        else:
            out.append(b[j])
            j += 1
    out.extend(a[i:])
    out.extend(b[j:])
    return out
''', "O(n + m)",
  ["Two indices, one per list",
   "Take the smaller head each round",
   "When one list runs out, extend with the remainder of the other"],
  fixed=[([1, 2, 4], [1, 3, 4]), ([], [0]), ([], []), ([5], [1])],
  rand=lambda rng: (sorted(rl(rng, rng.randint(0, 8), -20, 20)),
                    sorted(rl(rng, rng.randint(0, 8), -20, 20))),
  notes="LeetCode 21. This merge step is also the heart of merge sort.")

P("valid_anagram", "Valid Anagram", "Easy", "Counting", "is_anagram", "s, t", """
Return True if t is an anagram of s.

  is_anagram("anagram", "nagaram") -> True
  is_anagram("rat", "car")         -> False
""", '''def is_anagram(s, t):
    if len(s) != len(t):
        return False
    counts = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1
    for ch in t:
        if counts.get(ch, 0) == 0:
            return False
        counts[ch] -= 1
    return True
''', "O(n)",
  ["Different lengths -> immediate False",
   "Count the letters of s, then decrement while walking t",
   "sorted(s) == sorted(t) is O(n log n) — fine, but say so"],
  fixed=[("anagram", "nagaram"), ("rat", "car"), ("", ""), ("a", "ab")],
  rand=lambda rng: (lambda w: (w, _scramble(rng, w) if rng.random() < 0.5 else w + "z"))(
      "".join(rng.choice("abcde") for _ in range(rng.randint(1, 8)))),
  notes="LeetCode 242.")

P("contains_duplicate", "Contains Duplicate", "Easy", "Sets", "contains_duplicate",
  "nums", """
Return True if any value appears at least twice.

  contains_duplicate([1, 2, 3, 1]) -> True
  contains_duplicate([1, 2, 3, 4]) -> False

The hidden tests include a 200,000-element array, so O(n^2) will time out.
""", '''def contains_duplicate(nums):
    return len(set(nums)) != len(nums)
''', "O(n)",
  ["len(set(nums)) != len(nums)",
   "Or short-circuit with a running `seen` set — better when a duplicate is early"],
  fixed=[([1, 2, 3, 1],), ([1, 2, 3, 4],), ([],),
         (list(range(200000)),), (list(range(200000)) + [5],)],
  rand=lambda rng: (rl(rng, rng.randint(0, 15), 1, 10),),
  notes="LeetCode 217.")

P("string_compress", "String Compression", "Medium", "Strings", "compress", "s", """
Compress runs of repeated characters: "aabcccccaaa" -> "a2b1c5a3".
If the compressed form is not SHORTER than the original, return the original.

  compress("aabcccccaaa") -> "a2b1c5a3"
  compress("abc")         -> "abc"
  compress("")            -> ""
""", '''def compress(s):
    if not s:
        return ""
    parts = []
    count = 1
    for i in range(1, len(s) + 1):
        if i < len(s) and s[i] == s[i - 1]:
            count += 1
        else:
            parts.append(s[i - 1] + str(count))
            count = 1
    compressed = "".join(parts)
    return compressed if len(compressed) < len(s) else s
''', "O(n)",
  ["Walk with an index, count the current run, flush when it ends",
   "Every run emits char + count, even a run of 1",
   "Compare lengths at the very end and return whichever is shorter"],
  fixed=[("aabcccccaaa",), ("abc",), ("",), ("aa",), ("aabb",)],
  rand=lambda rng: ("".join(rng.choice("aabbc") for _ in range(rng.randint(0, 14))),),
  notes="Cracking the Coding Interview 1.6 — a very common warm-up.")

P("set_matrix_zeroes", "Set Matrix Zeroes", "Medium", "Matrix", "set_zeroes", "matrix", """
If a cell is 0, set its entire ROW and COLUMN to 0. Return the modified matrix.

  set_zeroes([[1,1,1],[1,0,1],[1,1,1]]) -> [[1,0,1],[0,0,0],[1,0,1]]

The trap: if you zero rows as you scan, you create new zeros and cascade.
Collect the rows and columns FIRST, then apply.
""", '''def set_zeroes(matrix):
    if not matrix or not matrix[0]:
        return matrix
    zero_rows = set()
    zero_cols = set()
    for r, row in enumerate(matrix):
        for c, value in enumerate(row):
            if value == 0:
                zero_rows.add(r)
                zero_cols.add(c)
    for r, row in enumerate(matrix):
        for c in range(len(row)):
            if r in zero_rows or c in zero_cols:
                row[c] = 0
    return matrix
''', "O(rows * cols)",
  ["Two passes: find the zeros, then write the zeros",
   "Store the affected row and column indices in sets",
   "Doing it in one pass cascades and blanks the whole matrix"],
  fixed=[([[1, 1, 1], [1, 0, 1], [1, 1, 1]],),
         ([[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]],), ([],), ([[1]],)],
  rand=lambda rng: (rgrid(rng, [0, 1, 1, 2]),),
  notes="LeetCode 73.")

P("min_window_len", "Minimum Size Subarray Sum", "Medium", "Sliding window",
  "min_subarray_len", "target, nums", """
Return the length of the SHORTEST contiguous subarray whose sum is >= target.
Return 0 if none exists. All values are positive.

  min_subarray_len(7, [2, 3, 1, 2, 4, 3]) -> 2      ([4, 3])
  min_subarray_len(11, [1, 1, 1])         -> 0

O(n) with a growing/shrinking window.
""", '''def min_subarray_len(target, nums):
    left = 0
    total = 0
    best = None
    for right, value in enumerate(nums):
        total += value
        while total >= target:
            length = right - left + 1
            best = length if best is None else min(best, length)
            total -= nums[left]
            left += 1
    return best or 0
''', "O(n)",
  ["Grow the window with `right`, then shrink from `left` while it is still valid",
   "Record the length every time the window is valid, before shrinking",
   "Each index enters and leaves once, so it is O(n) despite the inner while"],
  fixed=[(7, [2, 3, 1, 2, 4, 3]), (11, [1, 1, 1]), (4, [1, 4, 4]), (1, [])],
  rand=lambda rng: (rng.randint(1, 30), rl(rng, rng.randint(0, 12), 1, 12)),
  notes="LeetCode 209. The variable-size sliding window template.")

P("isomorphic", "Isomorphic Strings", "Easy", "Hash map", "is_isomorphic", "s, t", """
Two strings are isomorphic if the characters of s can be consistently replaced
to get t. Two different characters may NOT map to the same one.

  is_isomorphic("egg", "add")     -> True
  is_isomorphic("foo", "bar")     -> False
  is_isomorphic("badc", "baba")   -> False
""", '''def is_isomorphic(s, t):
    if len(s) != len(t):
        return False
    forward = {}
    backward = {}
    for a, b in zip(s, t):
        if forward.setdefault(a, b) != b:
            return False
        if backward.setdefault(b, a) != a:
            return False
    return True
''', "O(n)",
  ["One dict is not enough — you need BOTH directions",
   "setdefault returns the existing mapping if there is one",
   "The classic failing case is 'badc' / 'baba'"],
  fixed=[("egg", "add"), ("foo", "bar"), ("badc", "baba"), ("", ""), ("ab", "aa")],
  rand=lambda rng: ("".join(rng.choice("abc") for _ in range(rng.randint(1, 6))),
                    "".join(rng.choice("xyz") for _ in range(rng.randint(1, 6)))),
  notes="LeetCode 205. The bidirectional check is the whole question.")

P("kth_largest", "Kth Largest Element", "Medium", "Sorting", "find_kth_largest",
  "nums, k", """
Return the k-th largest element (k = 1 means the maximum). Duplicates count as
separate positions.

  find_kth_largest([3, 2, 1, 5, 6, 4], 2) -> 5
  find_kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) -> 4
""", '''def find_kth_largest(nums, k):
    import heapq
    return heapq.nlargest(k, nums)[-1]
''', "O(n log k) with a heap",
  ["sorted(nums)[-k] is the honest O(n log n) baseline — say it first",
   "heapq.nlargest(k, nums)[-1] is O(n log k)",
   "Quickselect gets O(n) average — worth naming even if you do not write it"],
  fixed=[([3, 2, 1, 5, 6, 4], 2), ([3, 2, 3, 1, 2, 4, 5, 5, 6], 4), ([1], 1)],
  rand=lambda rng: (lambda nums: (nums, rng.randint(1, len(nums))))(
      rl(rng, rng.randint(1, 12), -20, 20)),
  notes="LeetCode 215. Say all three complexities and pick one.")

P("summary_ranges", "Summary Ranges", "Easy", "Arrays", "summary_ranges", "nums", """
Given a SORTED list of distinct integers, summarise the consecutive runs.

  summary_ranges([0, 1, 2, 4, 5, 7]) -> ["0->2", "4->5", "7"]
  summary_ranges([])                 -> []

A run of length 1 is written as just the number.
""", '''def summary_ranges(nums):
    out = []
    i = 0
    n = len(nums)
    while i < n:
        start = i
        while i + 1 < n and nums[i + 1] == nums[i] + 1:
            i += 1
        if start == i:
            out.append(str(nums[start]))
        else:
            out.append(f"{nums[start]}->{nums[i]}")
        i += 1
    return out
''', "O(n)",
  ["Outer loop marks the start of a run, inner loop extends it",
   "Compare nums[i + 1] with nums[i] + 1 to detect consecutiveness",
   "Single-element runs print without the arrow"],
  fixed=[([0, 1, 2, 4, 5, 7],), ([],), ([1],), ([0, 2, 3, 4, 6, 8, 9],)],
  rand=lambda rng: (sorted(rng.sample(range(-20, 20), rng.randint(0, 10))),),
  notes="LeetCode 228. Straightforward, but a great warm-up for run-detection.")

P("sort_colors", "Sort Colors (Dutch flag)", "Medium", "Two pointers", "sort_colors",
  "nums", """
The list contains only 0, 1 and 2. Sort it in ONE pass without using sorted().
Return the list.

  sort_colors([2, 0, 2, 1, 1, 0]) -> [0, 0, 1, 1, 2, 2]

The Dutch national flag algorithm: three pointers, one sweep.
""", '''def sort_colors(nums):
    low, i, high = 0, 0, len(nums) - 1
    while i <= high:
        if nums[i] == 0:
            nums[low], nums[i] = nums[i], nums[low]
            low += 1
            i += 1
        elif nums[i] == 2:
            nums[high], nums[i] = nums[i], nums[high]
            high -= 1
        else:
            i += 1
    return nums
''', "O(n) time, O(1) space, one pass",
  ["Three regions: everything < low is 0, everything > high is 2",
   "On a 0, swap it down and advance both low and i",
   "On a 2, swap it up and DO NOT advance i — you have not looked at what arrived"],
  fixed=[([2, 0, 2, 1, 1, 0],), ([],), ([1],), ([2, 0],), ([0, 0, 1, 1, 2, 2],)],
  rand=lambda rng: ([rng.randint(0, 2) for _ in range(rng.randint(0, 12))],),
  notes="LeetCode 75. The 'do not advance i after swapping a 2' detail is the trap.")


# ---------------------------------------------------------------------------
TOPICS: list[str] = sorted({p.topic for p in BANK})
DIFFICULTIES = ["Easy", "Medium", "Hard"]


def by_id(pid: str) -> Problem | None:
    for problem in BANK:
        if problem.id == pid:
            return problem
    return None


def filtered(topic: str = "All topics", difficulty: str = "Any",
             query: str = "") -> list[Problem]:
    out = BANK
    if topic and topic != "All topics":
        out = [p for p in out if p.topic == topic]
    if difficulty and difficulty != "Any":
        out = [p for p in out if p.difficulty == difficulty]
    if query:
        q = query.lower()

        def matches(p: Problem) -> bool:
            haystack = [p.title, p.topic, p.statement, p.display_title,
                        i18n.topic(p.topic)]
            de = problems_de.PROBLEMS_DE.get(p.id, {})
            haystack += [de.get("title", ""), de.get("statement", "")]
            return any(q in part.lower() for part in haystack if part)

        out = [p for p in out if matches(p)]
    return out


def random_problem(rng: random.Random | None = None, **kw) -> Problem:
    rng = rng or random.Random()
    pool = filtered(**kw) or BANK
    return rng.choice(pool)
