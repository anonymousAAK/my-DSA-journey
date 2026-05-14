"""
WEEK 5 - PYTHON FUNCTIONS & RECURSION
Topic: Common Recursion Patterns
File: 6.recursion_patterns.py

CONCEPT:
Mastering a handful of recursion patterns covers ~90% of DSA recursion
problems:
  1. Linear recursion -- one recursive call per invocation (factorial, sum, reverse)
  2. Binary recursion -- two recursive calls (Fibonacci, binary search, merge sort)
  3. Tail recursion -- the recursive call is the LAST operation
  4. Mutual recursion -- function A calls B; B calls A (e.g., isEven/isOdd)
  5. Helper / accumulator -- carry state in extra parameters
  6. Subset / backtracking -- explore each choice (include / exclude)

KEY POINTS:
 - Python doesn't optimise tail calls -- depth still costs stack frames.
 - Closures + mutable captures replace Java's "static counter" idioms.
 - For SUBSETS / PERMUTATIONS, recursion is the standard technique.
"""


# Pattern 1: Linear recursion -- reverse a string
def reverse_str(s: str) -> str:
    if not s:
        return ""
    return reverse_str(s[1:]) + s[0]


# Pattern 3: Tail recursion with accumulator -- factorial
def fact_tail(n: int, acc: int = 1) -> int:
    if n <= 1:
        return acc
    return fact_tail(n - 1, n * acc)


# Pattern 4: Mutual recursion
def is_even(n: int) -> bool:
    if n == 0:
        return True
    return is_odd(n - 1)


def is_odd(n: int) -> bool:
    if n == 0:
        return False
    return is_even(n - 1)


# Pattern 5: Sum of digits via recursion
def digit_sum(n: int) -> int:
    if n == 0:
        return 0
    return (n % 10) + digit_sum(n // 10)


# Pattern 6: Generate all subsets of a list (2^n total)
def subsets(arr: list[int], idx: int = 0, current: list[int] | None = None) -> None:
    if current is None:
        current = []
    if idx == len(arr):
        print("{" + ",".join(str(x) for x in current) + "}")
        return
    # Choice 1: exclude arr[idx]
    subsets(arr, idx + 1, current)
    # Choice 2: include arr[idx]
    subsets(arr, idx + 1, current + [arr[idx]])


# Bonus: palindrome check via recursion
def is_palindrome(s: str, left: int = 0, right: int | None = None) -> bool:
    if right is None:
        right = len(s) - 1
    if left >= right:
        return True
    if s[left] != s[right]:
        return False
    return is_palindrome(s, left + 1, right - 1)


def main() -> None:
    print("reverse('hello') =", reverse_str("hello"))
    print("fact_tail(5)    =", fact_tail(5))
    print("fact_tail(10)   =", fact_tail(10))

    print("is_even(4) =", is_even(4))
    print("is_odd(7)  =", is_odd(7))

    print("digit_sum(1234) =", digit_sum(1234))

    print("\nAll subsets of [1, 2, 3]:")
    subsets([1, 2, 3])

    print("\nis_palindrome('racecar') =", is_palindrome("racecar"))
    print("is_palindrome('hello')   =", is_palindrome("hello"))


if __name__ == "__main__":
    main()


# NOTES:
# - Python list slicing (s[1:]) is O(n) and allocates -- watch the cost in deep recursion.
# - For tail recursion, prefer iterative form because Python doesn't optimise TCO.
# - Subsets via recursion is the foundation of BACKTRACKING (Week 14+ material).
# - Use itertools.combinations / permutations for ready-made enumerations.
