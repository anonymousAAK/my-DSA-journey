"""
WEEK 7 - PYTHON DSA
Topic: Palindrome & Anagram Checks
File: 2.palindrome_and_anagram.py

CONCEPT:
    Palindrome:  reads the same forward and backward ("racecar").
    Anagram:     two strings using the same characters with the same
                 frequencies ("listen" vs "silent").

KEY POINTS:
    - Two-pointer palindrome check is O(n) time and O(1) space.
    - Three anagram approaches:
        1. Sort both, compare.       O(n log n)
        2. Frequency array (26).     O(n), O(1) for ASCII letters
        3. Counter / dict.           O(n), O(k) for any alphabet
    - The Pythonic palindrome short-circuit is `s == s[::-1]` — but
      that allocates a copy.

ALGORITHM / APPROACH:
    Palindrome (two-pointer):
        l, r = 0, len(s) - 1
        while l < r:
            if s[l] != s[r]: return False
            l += 1; r -= 1
        return True
    Palindrome ignoring punctuation:
        skip non-alphanumerics on both ends; compare lower-cased.

PYTHON-SPECIFIC NOTES:
    - collections.Counter(s) gives a hashmap of frequencies in one call.
    - sorted(s) returns a sorted list of characters.
    - str.isalnum() handles the alphanumeric filter cleanly.

DRY RUN:
    Palindrome on "level":
        l=0,r=4 'l'=='l' l=1 r=3
        l=1,r=3 'e'=='e' l=2 r=2 stop -> True
    Palindrome on "race a car" (ignore non-alpha):
        compare 'r'/'r','a'/'a','c'/'c','e'/'a' -> False

    Anagram on "listen"/"silent":
        sorted: 'eilnst' == 'eilnst' -> True

COMPLEXITY:
    Palindrome    : O(n) time, O(1) space
    Sort anagram  : O(n log n) time, O(n) space
    Freq anagram  : O(n) time, O(1) space (ASCII letters)
    Map  anagram  : O(n) time, O(k) space
"""

from collections import Counter
from typing import Dict


def is_palindrome(s: str) -> bool:
    """Two-pointer palindrome check, O(n) time, O(1) space."""
    l, r = 0, len(s) - 1
    while l < r:
        if s[l] != s[r]:
            return False
        l += 1
        r -= 1
    return True


def is_palindrome_ignore_non_alpha(s: str) -> bool:
    """Palindrome ignoring punctuation and case."""
    l, r = 0, len(s) - 1
    while l < r:
        while l < r and not s[l].isalnum():
            l += 1
        while l < r and not s[r].isalnum():
            r -= 1
        if s[l].lower() != s[r].lower():
            return False
        l += 1
        r -= 1
    return True


def is_anagram_sort(a: str, b: str) -> bool:
    """O(n log n) — sort both and compare lists."""
    if len(a) != len(b):
        return False
    return sorted(a) == sorted(b)


def is_anagram_freq(a: str, b: str) -> bool:
    """O(n) frequency-array approach for lowercase ASCII letters."""
    if len(a) != len(b):
        return False
    freq = [0] * 26
    for ch in a:
        freq[ord(ch) - ord('a')] += 1
    for ch in b:
        idx = ord(ch) - ord('a')
        freq[idx] -= 1
        if freq[idx] < 0:
            return False
    return True


def is_anagram_map(a: str, b: str) -> bool:
    """O(n) Counter-based approach; works for any characters."""
    if len(a) != len(b):
        return False
    return Counter(a) == Counter(b)


def main() -> None:
    print("=== Palindrome ===")
    for t in ["racecar", "hello", "level", "madam", "a", ""]:
        print(f'is_palindrome("{t}") = {is_palindrome(t)}')

    print("\nis_palindrome_ignore_non_alpha:")
    s1 = "A man, a plan, a canal: Panama"
    print(f'"{s1}" = {is_palindrome_ignore_non_alpha(s1)}')   # True
    s2 = "race a car"
    print(f'"{s2}" = {is_palindrome_ignore_non_alpha(s2)}')   # False

    print("\n=== Anagram ===")
    pairs = [("listen", "silent"), ("eat", "tea"), ("hello", "world"),
             ("anagram", "nagaram")]
    for a, b in pairs:
        print(f'"{a}" vs "{b}":')
        print(f"  Sort: {is_anagram_sort(a, b)}")
        print(f"  Freq: {is_anagram_freq(a, b)}")
        print(f"  Map:  {is_anagram_map(a, b)}")


if __name__ == "__main__":
    main()


"""
NOTES — Python vs Java:
    - collections.Counter compares directly with `==`, replacing two-pass loops.
    - str.isalnum() centralises the alphanumeric check.
    - sorted(str) returns a list of characters; comparison is lexicographic.
    - No char primitive — characters are length-1 strings.
"""
