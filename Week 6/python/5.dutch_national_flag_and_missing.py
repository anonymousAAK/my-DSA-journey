"""
WEEK 6 - PYTHON DSA
Topic: Dutch National Flag + Missing / Duplicate Numbers
File: 5.dutch_national_flag_and_missing.py

CONCEPT:
    PART A — Dutch National Flag:
        Sort an array of only 0s, 1s, 2s in O(n) using three pointers
        (low, mid, high) — Dijkstra's three-way partition.

    PART B — Missing Number:
        Given a permutation of [0..n] with one element absent, find it
        either by the sum formula n(n+1)/2 - sum(arr) or by XOR-ing
        all indices with all elements (overflow-safe).

    PART C — Find the Duplicate (Floyd's cycle detection):
        Treat values as "next pointers"; the duplicate creates a cycle
        whose entry point IS the duplicated value.

KEY POINTS:
    - Dutch flag is a single in-place pass — O(n) time, O(1) space.
    - XOR variant of missing-number avoids overflow on huge n.
    - Floyd's cycle detection is the same algorithm used for linked
      lists — array indices simulate the linked list.

ALGORITHM / APPROACH:
    Dutch flag:
        low = mid = 0,  high = n-1
        while mid <= high:
            if arr[mid] == 0: swap(arr,low,mid); low++; mid++
            elif arr[mid] == 1: mid++
            else: swap(arr,mid,high); high--
    Missing (sum):
        return n*(n+1)//2 - sum(arr)    # n = len(arr)
    Missing (XOR):
        x = 0
        for i in 0..n: x ^= i
        for v in arr: x ^= v
        return x
    Duplicate (Floyd):
        slow = fast = arr[0]
        do slow=arr[slow], fast=arr[arr[fast]] until slow==fast
        slow = arr[0]
        while slow != fast: slow=arr[slow]; fast=arr[fast]
        return slow

PYTHON-SPECIFIC NOTES:
    - Tuple swap (`a[i], a[j] = a[j], a[i]`) replaces a temp variable.
    - Python ints have arbitrary precision, so the sum approach never
      overflows; XOR is still useful didactically.
    - functools.reduce(operator.xor, iter, 0) is a one-liner XOR fold.

DRY RUN:
    Dutch flag on [2,0,2,1,1,0]:
        low=0 mid=0 high=5
        arr[0]=2 -> swap(0,5): [0,0,2,1,1,2], high=4
        arr[0]=0 -> swap(0,0): low=1 mid=1
        arr[1]=0 -> swap(1,1): low=2 mid=2
        arr[2]=2 -> swap(2,4): [0,0,1,1,2,2], high=3
        arr[2]=1 -> mid=3
        arr[3]=1 -> mid=4 > high=3 stop
        result: [0,0,1,1,2,2]

    Missing on [3,0,1] (n=3, expected 0+1+2+3=6, actual 4) -> 2.

    Duplicate on [1,3,4,2,2]:
        Phase 1 finds intersection within cycle.
        Phase 2 walks both at speed 1; meet at duplicate value 2.

COMPLEXITY:
    All three problems: O(n) time, O(1) space.
"""

from typing import List


def dutch_flag(arr: List[int]) -> None:
    """In-place 3-way partition for {0,1,2}."""
    low, mid, high = 0, 0, len(arr) - 1
    while mid <= high:
        if arr[mid] == 0:
            arr[low], arr[mid] = arr[mid], arr[low]
            low += 1
            mid += 1
        elif arr[mid] == 1:
            mid += 1
        else:  # arr[mid] == 2
            arr[mid], arr[high] = arr[high], arr[mid]
            high -= 1


def missing_number_sum(arr: List[int]) -> int:
    """Numbers should be 0..n (n = len(arr)); one is missing."""
    n = len(arr)
    expected = n * (n + 1) // 2
    return expected - sum(arr)


def missing_number_xor(arr: List[int]) -> int:
    """XOR-based missing-number; pairs cancel, leaving the missing value."""
    n = len(arr)
    x = 0
    for i in range(n + 1):
        x ^= i
    for v in arr:
        x ^= v
    return x


def find_duplicate(arr: List[int]) -> int:
    """Floyd's tortoise & hare cycle detection — O(n) time, O(1) space."""
    slow = arr[0]
    fast = arr[0]
    # Phase 1: find an intersection inside the cycle.
    while True:
        slow = arr[slow]
        fast = arr[arr[fast]]
        if slow == fast:
            break
    # Phase 2: locate the cycle's entry — that is the duplicate.
    slow = arr[0]
    while slow != fast:
        slow = arr[slow]
        fast = arr[fast]
    return slow


def main() -> None:
    # --- Dutch National Flag ---
    colors = [2, 0, 2, 1, 1, 0]
    print(f"Before: {colors}")
    dutch_flag(colors)
    print(f"After:  {colors}")

    colors2 = [2, 2, 2, 0, 0, 1]
    dutch_flag(colors2)
    print(f"Sorted: {colors2}")

    # --- Missing Number ---
    arr1 = [3, 0, 1]  # missing 2
    print(f"\narr = {arr1}")
    print(f"Missing (sum): {missing_number_sum(arr1)}")
    print(f"Missing (XOR): {missing_number_xor(arr1)}")

    arr2 = [9, 6, 4, 2, 3, 5, 7, 0, 1]  # missing 8
    print(f"\narr = {arr2}")
    print(f"Missing (sum): {missing_number_sum(arr2)}")
    print(f"Missing (XOR): {missing_number_xor(arr2)}")

    # --- Find Duplicate ---
    dup = [1, 3, 4, 2, 2]
    print(f"\narr = {dup}")
    print(f"Duplicate: {find_duplicate(dup)}")  # 2

    dup2 = [3, 1, 3, 4, 2]
    print(f"arr = {dup2}")
    print(f"Duplicate: {find_duplicate(dup2)}")  # 3


if __name__ == "__main__":
    main()


"""
NOTES — Python vs Java:
    - Tuple swaps make the partition code visibly cleaner than the Java
      `int t = ...; ... = t;` triplet.
    - Python ints are arbitrary-precision, so sum() never overflows.
    - functools.reduce + operator.xor offers a one-line XOR fold.
"""
