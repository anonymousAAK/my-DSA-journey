"""
WEEK 3 - PYTHON LOOPS & NUMBER THEORY
Topic: break Statement
File: 3.break.py

CONCEPT:
`break` exits the INNERMOST loop immediately. The outer loop continues if
present. Python has NO labelled break, but the same effect can be achieved
with a function + `return`, or by raising a custom exception.

KEY POINTS:
 - `break` only affects the innermost enclosing loop.
 - `for-else` / `while-else` skip the `else` clause when broken out of.
 - To break out of nested loops cleanly, refactor into a function.

SYNTAX:
 for i in range(10):
     if i == 5: break
     print(i)

DRY RUN:
 for i in range(1, 10): print(i); if i==5: break
   prints 1,2,3,4,5 then exits

COMPLEXITY: O(k) where k is the number of iterations before break.
"""


def basic_break_for() -> None:
    print("--- break inside for ---")
    for i in range(1, 10):
        print(i)
        if i == 5:
            break


def basic_break_while() -> None:
    print("\n--- break inside while ---")
    i = 1
    while i <= 10:
        print(i)
        if i == 5:
            break
        i += 1


def nested_break() -> None:
    print("\n--- break only escapes inner loop ---")
    for i in range(1, 4):
        print(f"i={i}")
        for j in range(1, 6):
            print(f"  in (j={j})")
            if j == 1:
                break    # only escapes inner; outer i continues


def labelled_break_via_function() -> None:
    """Idiom: wrap nested loops in a function; `return` exits both."""
    print("\n--- labelled break via function ---")
    def find_first(target: int) -> tuple[int, int] | None:
        for i in range(5):
            for j in range(5):
                if i * j == target:
                    return (i, j)
        return None
    print("first (i,j) with i*j == 6 =", find_first(6))


def main() -> None:
    basic_break_for()
    basic_break_while()
    nested_break()
    labelled_break_via_function()


if __name__ == "__main__":
    main()


# NOTES:
# - Python has NO labelled break (Java's `break label;`); use functions + return.
# - `break` skips the `else` clause of a for/while loop.
# - For "search" loops, the for-else pattern is elegant:
#       for x in items:
#           if x == target: break
#       else:
#           print("not found")
