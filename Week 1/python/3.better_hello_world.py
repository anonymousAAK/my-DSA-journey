"""
WEEK 1 - PYTHON FUNDAMENTALS
Topic: print() — newlines, separators, and the `end` parameter
File: 3.better_hello_world.py

CONCEPT:
Java offers `System.out.print()` (no newline) and `System.out.println()`
(with newline). Python has a SINGLE function — `print()` — and you control
the trailing character with the keyword argument `end`. By default,
`end="\\n"`, which mimics Java's `println`. Setting `end=""` mimics `print`.

KEY POINTS:
- `print(*objects, sep=' ', end='\\n', file=sys.stdout, flush=False)`
- Multiple println-equivalent calls each end with their own newline
- Setting `end=""` keeps the next print on the same line
- `sep` controls how multiple positional args are joined
- `flush=True` forces the output buffer to flush immediately

SYNTAX:
print("text")             # prints "text\n"  (Java: System.out.println)
print("text", end="")     # prints "text"    (Java: System.out.print)
print("a", "b", "c")       # prints "a b c\n"
print("a", "b", sep="")    # prints "ab\n"

DRY RUN:
1. Three calls to `print("Hello World")` -> three lines on stdout.
2. Three calls to `print("Hello World", end="")` -> single line:
       Hello WorldHello WorldHello World
3. `print("X", "Y", sep="--", end="!\\n")` -> "X--Y!" then newline.
"""


def main() -> None:
    print("--- println-style (default end='\\n') ---")
    print("Hello World")
    print("Hello World")
    print("Hello World")

    print("\n--- print-style (end='') ---")
    print("Hello World", end="")
    print("Hello World", end="")
    print("Hello World")  # last one gets a newline

    print("\n--- mixed end values ---")
    print("Same", end=" ")
    print("line", end=" ")
    print("here.")

    print("\n--- custom separator with multiple args ---")
    print("X", "Y", "Z")               # default: "X Y Z"
    print("X", "Y", "Z", sep="")        # "XYZ"
    print("X", "Y", "Z", sep="--")      # "X--Y--Z"
    print("X", "Y", "Z", sep="--", end="!\n")  # "X--Y--Z!"


if __name__ == "__main__":
    main()


# NOTES:
# - Java's `print` vs `println` is a method choice; Python's is a parameter (`end=`).
# - Python's `print` joins multiple args with a space automatically (Java would
#   require explicit string concatenation with the `+` operator).
# - For formatted output, Python prefers f-strings: print(f"x = {x}").
#   Java's equivalent would be `System.out.printf("x = %d%n", x)`.
