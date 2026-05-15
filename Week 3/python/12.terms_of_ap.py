"""
WEEK 3 - PYTHON LOOPS & NUMBER THEORY
Topic: Print First X Terms of 3N+2 NOT Divisible by 4
File: 12.terms_of_ap.py

PROBLEM:
Print the first X terms of the series 3N + 2 that are NOT multiples of 4,
separated by spaces.

The raw series 3*N+2 for N=1,2,3,... is 5, 8, 11, 14, 17, 20, 23, 26, ...
After filtering multiples of 4 (8, 20, ...): 5, 11, 14, 17, 23, 26, ...

CONCEPT:
Iterate N upwards; for each N compute term = 3*N+2; if term % 4 != 0,
emit it and increment a "found" counter. Stop after X terms.

KEY POINTS:
 - Two counters: count of terms emitted, current N.
 - itertools.count + filter + islice is a functional alternative.

SYNTAX:
 # imperative
 found = 0; n = 1
 while found < x:
     term = 3*n + 2
     if term % 4: print(term, end=" "); found += 1
     n += 1

 # functional
 import itertools
 terms = ((3*n + 2) for n in itertools.count(1))
 wanted = (t for t in terms if t % 4)
 first_x = list(itertools.islice(wanted, x))

DRY RUN:
 X=3 -> 5 11 14
"""

import sys
import itertools


def imperative(x: int) -> list[int]:
    out: list[int] = []
    found, n = 0, 1
    while found < x:
        t = 3 * n + 2
        if t % 4 != 0:
            out.append(t)
            found += 1
        n += 1
    return out


def functional(x: int) -> list[int]:
    terms  = ((3 * n + 2) for n in itertools.count(1))
    wanted = (t for t in terms if t % 4 != 0)
    return list(itertools.islice(wanted, x))


def main() -> None:
    if sys.stdin.isatty():
        x = 5
    else:
        x = int(sys.stdin.read().split()[0])
    print(" ".join(map(str, imperative(x))))
    print(" ".join(map(str, functional(x))))   # equivalent


if __name__ == "__main__":
    main()


# NOTES:
# - itertools.count(start) yields an infinite arithmetic progression.
# - itertools.islice(iter, n) takes the first n items lazily.
# - The functional pipeline is concise and reads like the problem description.
