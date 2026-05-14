"""
WEEK 3 - PYTHON LOOPS & NUMBER THEORY
Topic: continue Statement
File: 4.continue.py

CONCEPT:
`continue` skips the REST of the current iteration and jumps to the next.
Same semantics as Java/C++.

KEY POINTS:
 - In a `for` loop, `continue` jumps to the next item from the iterable.
 - In a `while` loop, `continue` jumps back to the condition check.
 - CAUTION in while loops: increment your counter BEFORE `continue` or
   you'll create an infinite loop.

SYNTAX:
 for i in range(1, 6):
     if i == 3: continue
     print(i)

DRY RUN:
 i=1 -> print
 i=2 -> print
 i=3 -> continue (no print)
 i=4 -> print
 i=5 -> print
 Output: 1 2 4 5

COMPLEXITY: O(n).
"""


def continue_in_for() -> None:
    print("--- continue in for ---")
    for i in range(1, 6):
        if i == 3:
            continue
        print(i)


def continue_in_while() -> None:
    print("\n--- continue in while (increment FIRST!) ---")
    i = 1
    while i <= 5:
        if i == 3:
            i += 1               # CRITICAL: must advance before continue
            continue
        print(i)
        i += 1


def main() -> None:
    continue_in_for()
    continue_in_while()


if __name__ == "__main__":
    main()


# NOTES:
# - The for-loop counter advances automatically -- safe to `continue` freely.
# - The while-loop counter does NOT advance -- you must update it before `continue`.
# - Use `continue` to filter early; alternative is a guard `if cond: do_work()`.
