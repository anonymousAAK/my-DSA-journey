"""
WEEK 3 - PYTHON LOOPS & NUMBER THEORY
Topic: For Loop Basics
File: 1.for_loop.py

CONCEPT:
Python's `for` loop is FUNDAMENTALLY DIFFERENT from Java's. It iterates
over the items of any ITERABLE (list, tuple, str, range, generator, ...).
There is NO `for (init; cond; update)` C-style header.

To imitate Java's `for (int i = 0; i < n; i++)`, use `for i in range(n):`.

KEY POINTS:
 - `range(stop)`            -> 0, 1, ..., stop-1
 - `range(start, stop)`     -> start, ..., stop-1
 - `range(start, stop, step)` -> with custom step (negative for descending)
 - `range` is lazy: it generates values on demand (no list created).
 - `for-else`: the `else:` clause runs after a NORMAL exit (not after break).
 - `enumerate(iterable, start=0)` yields (index, value) pairs.
 - `zip(a, b)` pairs items from two iterables.

SYNTAX:
 for i in range(n): ...
 for i in range(1, 11): ...
 for x in [1, 2, 3]: ...
 for i, v in enumerate(arr): ...

DRY RUN:
 for i in range(3): print("Inside for loop :", i)
   -> 0, 1, 2 (each preceded by "Inside for loop :")
 print("Done")

COMPLEXITY: O(n) — n iterations.
"""


def basic_for_loop() -> None:
    print("--- basic ---")
    for i in range(3):              # 0, 1, 2
        print("Inside for loop :", i)
    print("Done")


def with_explicit_init() -> None:
    """No need to put init outside the for; range handles it."""
    print("\n--- range with start ---")
    for i in range(1, 6):           # 1..5 inclusive
        print(i)


def for_else_demo() -> None:
    """The else block runs ONLY if the loop completes without `break`."""
    print("\n--- for-else ---")
    target = 7
    for x in range(10):
        if x == target:
            print(f"found {target} -> breaking")
            break
    else:
        print("completed without finding")

    # Same loop without break
    for x in range(3):
        print(f"x = {x}")
    else:
        print("no break -> else runs")


def helpful_iter_helpers() -> None:
    """enumerate, zip, reversed -- common idioms."""
    print("\n--- enumerate / zip / reversed ---")
    arr = ["a", "b", "c"]
    for i, v in enumerate(arr):
        print(f"  index {i}: {v}")

    a = [1, 2, 3]
    b = ["x", "y", "z"]
    for x, y in zip(a, b):
        print(f"  pair {x}-{y}")

    for v in reversed(range(5)):
        print(f"  rev {v}")


def main() -> None:
    basic_for_loop()
    with_explicit_init()
    for_else_demo()
    helpful_iter_helpers()


if __name__ == "__main__":
    main()


# NOTES:
# - Java's `for (init; cond; update)` doesn't exist; Python uses `for in iterable`.
# - To replicate Java's index-based loop, use `range(...)`.
# - `range(start, stop, step)` step CAN be negative for descending.
# - `for-else` is unique to Python -- the else runs after a NORMAL completion.
# - Avoid `for i in range(len(arr))`; prefer `for i, v in enumerate(arr)`.
