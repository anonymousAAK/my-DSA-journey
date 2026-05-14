"""
WEEK 8 - PYTHON DSA
Topic: Binary Search on the Answer
File: 2.binary_search_on_answer.py

CONCEPT:
    Apply binary search not to find a value in an array, but to find the
    minimum/maximum value X such that some monotonic predicate(X) holds.

KEY POINTS:
    - Works whenever predicate(X) is monotonic — once it flips True/False
      it stays that way along the range.
    - Template:
        lo, hi = min_answer, max_answer
        while lo < hi:
            mid = lo + (hi - lo) // 2
            if predicate(mid): hi = mid     # try smaller
            else:              lo = mid + 1 # need larger
        return lo

ALGORITHM / APPROACH:
    Problems demonstrated:
      1. Integer square root: largest x with x*x <= n.
      2. Koko eating bananas: minimum speed so hours <= H.
      3. Ship packages in D days: minimum capacity so days_needed <= D.

PYTHON-SPECIFIC NOTES:
    - math.isqrt(n) is the standard-library integer square root.
    - max(piles) and sum(weights) are convenient bounds.
    - Use ceiling: (pile + speed - 1) // speed.

DRY RUN:
    sqrt(17):
        lo=1 hi=8 mid=5  25>17 hi=4
        lo=1 hi=4 mid=3  9<=17 lo=3
        lo=3 hi=4 mid=4  16<=17 lo=4
        lo=4 hi=4 -> 4

    Koko piles=[3,6,7,11], H=8:
        lo=1 hi=11 mid=6 hours=1+1+2+2=6<=8 hi=6
        lo=1 hi=6 mid=3 hours=1+2+3+4=10>8 lo=4
        lo=4 hi=6 mid=5 hours=1+2+2+3=8<=8 hi=5
        lo=4 hi=5 mid=4 hours=1+2+2+3=8<=8 hi=4
        return 4

COMPLEXITY:
    O(log(range) * cost_of_predicate).
"""

from typing import List


def sqrt_int(n: int) -> int:
    """Largest integer x with x*x <= n."""
    if n < 2:
        return n
    lo, hi = 1, n // 2
    while lo < hi:
        mid = lo + (hi - lo + 1) // 2  # +1 to avoid infinite loop when hi = lo+1
        if mid * mid <= n:
            lo = mid
        else:
            hi = mid - 1
    return lo


def can_finish(piles: List[int], h: int, speed: int) -> bool:
    """Can Koko eat all piles in h hours at given speed?"""
    hours = 0
    for pile in piles:
        hours += (pile + speed - 1) // speed
    return hours <= h


def min_eating_speed(piles: List[int], h: int) -> int:
    lo, hi = 1, max(piles)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if can_finish(piles, h, mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


def can_ship(weights: List[int], days: int, capacity: int) -> bool:
    current_load = 0
    days_needed = 1
    for w in weights:
        if w > capacity:
            return False
        if current_load + w > capacity:
            days_needed += 1
            current_load = 0
        current_load += w
    return days_needed <= days


def min_ship_capacity(weights: List[int], days: int) -> int:
    lo = max(weights)   # at least the heaviest package
    hi = sum(weights)   # at most ship everything in one day
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if can_ship(weights, days, mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


def main() -> None:
    print("=== Integer Square Root ===")
    for n in [0, 1, 4, 8, 9, 16, 17, 100]:
        print(f"sqrt({n:3d}) = {sqrt_int(n)}")

    print("\n=== Koko Eating Bananas ===")
    piles = [3, 6, 7, 11]
    print(f"Piles: {piles}")
    print(f"Min speed for H=8: {min_eating_speed(piles, 8)}")  # 4

    piles2 = [30, 11, 23, 4, 20]
    print(f"Piles: {piles2}")
    print(f"Min speed for H=5: {min_eating_speed(piles2, 5)}")  # 30
    print(f"Min speed for H=6: {min_eating_speed(piles2, 6)}")  # 23

    print("\n=== Ship Packages ===")
    weights = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(f"Weights: {weights}")
    print(f"Min capacity for D=5 days:  {min_ship_capacity(weights, 5)}")   # 15
    print(f"Min capacity for D=10 days: {min_ship_capacity(weights, 10)}")  # 10


if __name__ == "__main__":
    main()


"""
NOTES — Python vs Java:
    - max() and sum() handle Java's Arrays.stream(...).max/.sum verbose forms.
    - math.isqrt(n) is the production-grade integer sqrt; we implement
      manually here to illustrate the technique.
    - Python ints are unbounded — no overflow concern when computing mid.
"""
