"""
Week 7 — Strings
==================
Topics covered:
  - Palindrome check (two-pointer, ignoring non-alphanumeric characters)
  - Anagram check (sorting approach + frequency-count approach)
  - Reverse words in a string
  - String compression / run-length encoding
  - KMP (Knuth-Morris-Pratt) pattern matching:
      • Build the LPS (Longest Proper Prefix which is also Suffix) array
      • Search for a pattern in a text

Each function includes time/space complexity analysis in its docstring.
"""

from __future__ import annotations

from collections import Counter
from typing import List


# ---------------------------------------------------------------------------
# Palindrome Check (two-pointer, alphanumeric only)
# ---------------------------------------------------------------------------

def is_palindrome(s: str) -> bool:
    """Check if *s* is a palindrome, considering only alphanumeric characters
    and ignoring case.

    Example: "A man, a plan, a canal: Panama" → True

    Time:  O(n)
    Space: O(1)
    """
    left, right = 0, len(s) - 1
    while left < right:
        # Skip non-alphanumeric from the left
        while left < right and not s[left].isalnum():
            left += 1
        # Skip non-alphanumeric from the right
        while left < right and not s[right].isalnum():
            right -= 1
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    return True


# ---------------------------------------------------------------------------
# Anagram Check
# ---------------------------------------------------------------------------

def is_anagram_sort(s: str, t: str) -> bool:
    """Check if *s* and *t* are anagrams by sorting both strings.

    Time:  O(n log n)
    Space: O(n)  — sorted copies
    """
    return sorted(s.lower()) == sorted(t.lower())


def is_anagram_freq(s: str, t: str) -> bool:
    """Check if *s* and *t* are anagrams using character frequency counts.

    Time:  O(n)
    Space: O(1)  — at most 26 lowercase letters
    """
    return Counter(s.lower()) == Counter(t.lower())


# ---------------------------------------------------------------------------
# Reverse Words in a String
# ---------------------------------------------------------------------------

def reverse_words(s: str) -> str:
    """Reverse the order of words in *s*, collapsing multiple spaces.

    Example: "  the sky is blue  " → "blue is sky the"

    Time:  O(n)
    Space: O(n)
    """
    return " ".join(s.split()[::-1])


def reverse_words_manual(s: str) -> str:
    """Reverse words without relying on split/join — manual two-pass approach.

    1. Strip and collapse spaces, convert to a list (mutable).
    2. Reverse the entire character list.
    3. Reverse each individual word in-place.

    Time:  O(n)
    Space: O(n)  — the mutable character list
    """
    # Build a cleaned character list with single spaces
    chars: list[str] = []
    i, n = 0, len(s)
    while i < n:
        if s[i] != " ":
            if chars and chars[-1] != " ":
                # Only add a space if last char is not a space and chars is non-empty
                pass  # no space needed yet — we only add space between words
            # But we need to add a space *before* a new word (except the first)
            if chars and chars[-1] != " ":
                chars.append(" ")
            while i < n and s[i] != " ":
                chars.append(s[i])
                i += 1
        else:
            i += 1

    # Helper to reverse a slice of the list
    def _reverse(lo: int, hi: int) -> None:
        while lo < hi:
            chars[lo], chars[hi] = chars[hi], chars[lo]
            lo += 1
            hi -= 1

    # Reverse entire array
    _reverse(0, len(chars) - 1)

    # Reverse each word
    start = 0
    for idx in range(len(chars) + 1):
        if idx == len(chars) or chars[idx] == " ":
            _reverse(start, idx - 1)
            start = idx + 1

    return "".join(chars)


# ---------------------------------------------------------------------------
# String Compression / Run-Length Encoding
# ---------------------------------------------------------------------------

def compress(s: str) -> str:
    """Perform basic run-length encoding.

    Consecutive duplicate characters are replaced by the character followed
    by its count.  If the compressed string is not shorter, return the
    original.

    Example: "aabcccccaaa" → "a2b1c5a3"

    Time:  O(n)
    Space: O(n)
    """
    if not s:
        return s

    parts: list[str] = []
    count = 1
    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            count += 1
        else:
            parts.append(f"{s[i - 1]}{count}")
            count = 1
    parts.append(f"{s[-1]}{count}")

    compressed = "".join(parts)
    return compressed if len(compressed) < len(s) else s


def decompress(s: str) -> str:
    """Decode a run-length encoded string.

    Example: "a2b1c5a3" → "aabcccccaaa"

    Time:  O(n)  — n is length of the decoded string
    Space: O(n)
    """
    parts: list[str] = []
    i = 0
    while i < len(s):
        char = s[i]
        i += 1
        num_start = i
        while i < len(s) and s[i].isdigit():
            i += 1
        count = int(s[num_start:i])
        parts.append(char * count)
    return "".join(parts)


# ---------------------------------------------------------------------------
# KMP Pattern Matching
# ---------------------------------------------------------------------------

def build_lps(pattern: str) -> List[int]:
    """Build the Longest Proper Prefix which is also Suffix (LPS) array.

    lps[i] = length of the longest proper prefix of pattern[0..i]
             that is also a suffix of pattern[0..i].

    Time:  O(m)  where m = len(pattern)
    Space: O(m)
    """
    m = len(pattern)
    lps = [0] * m
    length = 0  # length of the previous longest prefix suffix
    i = 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                # Fall back — do NOT increment i
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps


def kmp_search(text: str, pattern: str) -> List[int]:
    """Return all starting indices where *pattern* occurs in *text*.

    Uses the KMP algorithm with the LPS (failure function) array for
    efficient back-tracking.

    Time:  O(n + m)  where n = len(text), m = len(pattern)
    Space: O(m)      for the LPS array
    """
    if not pattern:
        return list(range(len(text) + 1))

    n, m = len(text), len(pattern)
    lps = build_lps(pattern)
    matches: list[int] = []

    i = 0  # pointer into text
    j = 0  # pointer into pattern

    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
        if j == m:
            matches.append(i - j)
            j = lps[j - 1]  # look for next match
        elif i < n and text[i] != pattern[j]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return matches


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # ---- Palindrome ----
    assert is_palindrome("A man, a plan, a canal: Panama") is True
    assert is_palindrome("race a car") is False
    assert is_palindrome("") is True
    assert is_palindrome(" ") is True
    print("[PASS] Palindrome check (two-pointer, alphanumeric)")

    # ---- Anagram ----
    for fn in (is_anagram_sort, is_anagram_freq):
        assert fn("listen", "silent") is True
        assert fn("hello", "world") is False
        assert fn("Anagram", "nagaram") is True
        assert fn("", "") is True
    print("[PASS] Anagram check (sort & freq)")

    # ---- Reverse Words ----
    for fn in (reverse_words, reverse_words_manual):
        assert fn("the sky is blue") == "blue is sky the"
        assert fn("  hello world  ") == "world hello"
        assert fn("a") == "a"
    print("[PASS] Reverse words in a string")

    # ---- Compression ----
    assert compress("aabcccccaaa") == "a2b1c5a3"
    assert compress("abc") == "abc"  # not shorter
    assert compress("") == ""
    assert decompress("a2b1c5a3") == "aabcccccaaa"
    print("[PASS] String compression / run-length encoding")

    # ---- KMP ----
    assert kmp_search("AABAACAADAABAABA", "AABA") == [0, 9, 12]
    assert kmp_search("abcdef", "xyz") == []
    assert kmp_search("aaaaaa", "aaa") == [0, 1, 2, 3]
    lps = build_lps("AAACAAAA")
    assert lps == [0, 1, 2, 0, 1, 2, 3, 3]
    print("[PASS] KMP pattern matching")

    print("\nAll Week 7 tests passed!")
