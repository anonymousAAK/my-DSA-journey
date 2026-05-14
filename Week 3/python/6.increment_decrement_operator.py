"""
WEEK 3 - PYTHON LOOPS & NUMBER THEORY
Topic: Increment / Decrement (or lack thereof!)
File: 6.increment_decrement_operator.py

CONCEPT:
PYTHON HAS NO `++` OR `--` OPERATOR. Use `x += 1` and `x -= 1` instead.
Writing `x++` is a SYNTAX ERROR. Writing `++x` is interpreted as
`+(+x)` -- a no-op unary plus -- which is harmless but useless.

KEY POINTS:
 - `x += 1` and `x -= 1` are the canonical replacements.
 - There is no pre/post distinction because there is no `++/--` operator.
 - `x = x + 1` works too but is slightly slower for some types.
 - For loops, use `range(...)` instead of incrementing manually.

SYNTAX:
 x += 1   # increment
 x -= 1   # decrement
 # x++    # SYNTAX ERROR
 # ++x    # parsed as +(+x), no effect

DRY RUN:
 a = 5
 a += 1 -> a = 6
 a -= 1 -> a = 5

COMPLEXITY: O(1).
"""


def main() -> None:
    a = 5
    print(f"Initial a = {a}")

    # Increment
    a += 1
    print(f"After a += 1, a = {a}")

    # Decrement
    a -= 1
    print(f"After a -= 1, a = {a}")

    # Java-style demo
    print("\n--- Java's a++ / ++a / a-- / --a translated ---")
    a = 5
    print(f"a (current value)            = {a}")    # like a++ result
    a += 1
    print(f"a after a += 1               = {a}")
    a += 1
    print(f"++a equivalent (a += 1; a)   = {a}")
    a -= 1
    print(f"a-- equivalent (use a, then a -= 1)")
    print(f"a after a -= 1               = {a}")

    # ++x parses as +(+x) - a unary-plus chain - it does NOT increment
    print("\n--- The ++x trap ---")
    x = 5
    y = ++x
    print(f"y = ++x  ->  x = {x}, y = {y}   (++ did nothing!)")

    # In loops: prefer range() over manual increments
    print("\n--- idiomatic loops ---")
    arr = [10, 20, 30, 40, 50]
    for i, v in enumerate(arr):
        print(f"  arr[{i}] = {v}")


if __name__ == "__main__":
    main()


# NOTES:
# - Java/C/C++ have ++ and --; Python does NOT.
# - The intent of pre/post-increment is rarely needed in Python because:
#     * `for i in range(n)` handles loop counters.
#     * Lists / dicts / sets are iterated directly (no index math).
# - If you find yourself writing `i += 1` a lot, you probably want a `for` loop.
