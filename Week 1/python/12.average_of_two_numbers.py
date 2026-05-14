"""
WEEK 1 - PYTHON FUNDAMENTALS
Topic: Average of Three Numbers
File: 12.average_of_two_numbers.py

CONCEPT:
Read a name and three integers, then print the name and the average of the
three numbers. In Python `/` is true division — the average is automatically
a float. To match Java's integer-truncation behaviour use `//`.

KEY POINTS:
- `(a + b + c) / 3`  -> precise float average (Python `/` is true division)
- `(a + b + c) // 3` -> floor division, equivalent to Java's int / int
- Multiple inputs read with `map(int, input().split())` or token reading
- `statistics.mean(...)` is a stdlib alternative for arbitrary iterables

SYNTAX:
avg = (a + b + c) / 3       # float
avg = (a + b + c) // 3      # int (floor)

DRY RUN:
Stdin: "Bob 10 11 12"
  name = "Bob"
  (10+11+12) / 3 = 11.0
  (10+11+12) // 3 = 11
Stdin: "Bob 10 11 11"
  /  -> 10.6666...
  // -> 10  (Java int division would give the same)

COMPLEXITY: O(1) time, O(1) space
"""

import sys
from statistics import mean


def main() -> None:
    if sys.stdin.isatty():
        name, a, b, c = "Bob", 10, 11, 12
    else:
        tokens = sys.stdin.read().split()
        name = tokens[0]
        a, b, c = int(tokens[1]), int(tokens[2]), int(tokens[3])

    print(name)
    print(f"True average  = {(a + b + c) / 3}")     # float
    print(f"Floor average = {(a + b + c) // 3}")    # int (matches Java)
    print(f"statistics.mean = {mean([a, b, c])}")    # stdlib helper


if __name__ == "__main__":
    main()


# NOTES:
# - Java: `(a+b+c)/3` truncates because all operands are int. To keep precision
#   use `(a+b+c)/3.0`. Python is the inverse: `/` is float by default; use `//`
#   to truncate.
# - `statistics.mean([...])` returns float; `statistics.fmean([...])` is faster
#   for floats only.
