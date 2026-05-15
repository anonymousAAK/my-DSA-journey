"""
WEEK 3 - PYTHON LOOPS & NUMBER THEORY
Topic: For Loop Variations
File: 2.for_loop_variations.py

CONCEPT:
Python doesn't expose Java's `(init; cond; update)` triple, so the
"variations" trick (omitting one of the three parts) doesn't apply
verbatim. Instead, we show idiomatic Python equivalents:
  - explicit start/stop/step in `range`
  - infinite loop via `itertools.count` or `while True`
  - loop over multiple iterables together via `zip`

KEY POINTS:
 - `range(0, 5)`     -> 0,1,2,3,4    (start defaults to 0)
 - `range(0, 0)`     -> empty range (no iterations)
 - `range(0, 5, 2)`  -> 0, 2, 4
 - `itertools.count(start, step)` -> infinite iterator (start, start+step, ...)
 - `zip(a, b)` for parallel iteration like Java's two-counter trick.
 - To loop with multiple variables: `for (i, j) in zip(range(0,5), range(4,-1,-1))`.

SYNTAX:
 for i in range(0, 5): ...
 for i in itertools.count(0): ...   # use break to stop
 for x, y in zip(a, b): ...

DRY RUN:
 range(0, 3) -> 0, 1, 2
 zip(range(0,5), range(4,-1,-1)) -> (0,4), (1,3), (2,2), (3,1), (4,0)
"""

import itertools


def variation_1_basic() -> None:
    print("--- range(0, 3) ---")
    for i in range(0, 3):
        print(i)


def variation_2_step() -> None:
    print("\n--- range(0, 10, 2) ---")
    for i in range(0, 10, 2):
        print(i)


def variation_3_descending() -> None:
    print("\n--- range(5, 0, -1) ---")
    for i in range(5, 0, -1):
        print(i)


def variation_4_infinite_with_break() -> None:
    """`itertools.count` creates an infinite sequence; break out manually."""
    print("\n--- itertools.count + break ---")
    for i in itertools.count(0):
        if i >= 3:
            break
        print(i)


def variation_5_two_counters() -> None:
    """The Java idiom `for (i=0, j=4; ...; i++, j--)` becomes a zip."""
    print("\n--- two counters via zip ---")
    for i, j in zip(range(0, 5), range(4, -1, -1)):
        print(f"  {i} {j}")


def variation_6_no_iter() -> None:
    """`for ... in []` runs zero times -- the equivalent of an immediately-false condition."""
    print("\n--- empty range ---")
    ran = False
    for _ in range(0):
        ran = True
    print(f"loop ran? {ran}")


def main() -> None:
    variation_1_basic()
    variation_2_step()
    variation_3_descending()
    variation_4_infinite_with_break()
    variation_5_two_counters()
    variation_6_no_iter()


if __name__ == "__main__":
    main()


# NOTES:
# - You CANNOT split `init / cond / update` across an `in` clause as in Java.
# - Use `itertools.count` for an infinite arithmetic progression.
# - `zip(a, b)` parallel iteration replaces Java's "two variables in for header" trick.
# - For "until-condition" loops, prefer `while not cond: ...` over a manually-incrementing for.
