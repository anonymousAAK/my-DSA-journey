"""
WEEK 3 - PYTHON LOOPS & NUMBER THEORY
Topic: Check if a Sequence is Decreasing then Increasing
File: 16.check_no_sequence.py

PROBLEM:
Given N integers, return True iff the sequence can be split into two parts:
 - first part: STRICTLY DECREASING
 - second part: STRICTLY INCREASING
The transition from decreasing to increasing may happen at most once. A
purely increasing or purely decreasing sequence is also valid. Equal
consecutive elements => False.

CONCEPT:
Walk the sequence, tracking whether we are currently in the DECREASING or
INCREASING phase. Once we transition to increasing, decreasing again is
forbidden.

KEY POINTS:
 - Two states: "decreasing" (initial) and "increasing".
 - Equal consecutive => False immediately.
 - O(n) single pass, O(1) extra space.

DRY RUN:
 [5,3,1,2,4]:
  3<5 dec; 1<3 dec; 2>1 transition; 4>2 inc -> True
 [1,2,3,4,5]: 2>1 transition immediately, then all > -> True
 [5,4,3,2,1]: all dec -> True
 [1,2,3,2,1]: 2>1 transition; 3>2 inc; 2<3 dec while in inc phase -> False
 [1,2,2,3]:   equal -> False

COMPLEXITY: O(n) time, O(1) space.
"""

import sys


def is_dec_then_inc(seq: list[int]) -> bool:
    if len(seq) < 2:
        return True
    is_dec = True            # start in decreasing phase
    for i in range(1, len(seq)):
        if seq[i] == seq[i-1]:
            return False
        if seq[i] < seq[i-1]:        # decreasing
            if not is_dec:
                return False
        else:                         # increasing
            if is_dec:
                is_dec = False        # transition once
    return True


def main() -> None:
    if sys.stdin.isatty():
        cases = [
            [5, 3, 1, 2, 4],
            [1, 2, 3, 4, 5],
            [5, 4, 3, 2, 1],
            [1, 2, 3, 2, 1],
            [1, 2, 2, 3],
        ]
        for c in cases:
            print(f"{c} -> {is_dec_then_inc(c)}")
        return

    toks = sys.stdin.read().split()
    n = int(toks[0])
    seq = list(map(int, toks[1:1 + n]))
    print(str(is_dec_then_inc(seq)).lower())


if __name__ == "__main__":
    main()


# NOTES:
# - Pythonic alternative using zip:
#       any equal? -> any(a == b for a, b in zip(seq, seq[1:]))
# - The "valley" shape (high -> low -> high) is sometimes called a V-sequence.
# - For O(1) space ALWAYS, avoid materialising lists when reading streams.
