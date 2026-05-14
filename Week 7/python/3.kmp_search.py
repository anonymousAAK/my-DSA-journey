"""
WEEK 7 - PYTHON DSA
Topic: KMP String Search Algorithm
File: 3.kmp_search.py

CONCEPT:
    Find all occurrences of a pattern P in a text T in O(n + m) time
    using the KMP (Knuth-Morris-Pratt) algorithm.

KEY POINTS:
    - The "failure function" / LPS array encodes how much we already
      matched after a mismatch, so we never re-scan the text.
    - Build LPS in O(m); search in O(n).
    - LPS[i] = length of the longest proper prefix of pattern[0..i]
      which is also a suffix of pattern[0..i].

ALGORITHM / APPROACH:
    Build LPS:
        lps[0] = 0; len_ = 0; i = 1
        while i < m:
            if pat[i] == pat[len_]: len_+=1; lps[i]=len_; i+=1
            elif len_ != 0:        len_ = lps[len_-1]
            else:                  lps[i] = 0; i += 1
    Search:
        i = j = 0
        while i < n:
            if text[i] == pat[j]: i+=1; j+=1
            if j == m: record (i - j); j = lps[j-1]
            elif i < n and text[i] != pat[j]:
                j = lps[j-1] if j else (i := i + 1) and j

PYTHON-SPECIFIC NOTES:
    - Strings index in O(1); s[i] returns a length-1 string.
    - Built-in alternatives: str.find(), all overlapping with re.finditer.
    - We implement KMP for didactic value.

DRY RUN:
    pattern = "AABA"
        i=1: pat[1]=A == pat[0]=A -> len=1 lps=[0,1] i=2
        i=2: pat[2]=B != pat[1]=A; len=1 -> len = lps[0] = 0
             pat[2]=B != pat[0]=A; len=0 -> lps[2]=0 i=3
        i=3: pat[3]=A == pat[0]=A -> len=1 lps[3]=1 i=4
        lps = [0,1,0,1]

    Search "AABAACAADAABAABA" for "AABA":
        matches at indices 0, 9, 12

COMPLEXITY:
    Build LPS : O(m) time, O(m) space
    KMP search: O(n + m) time
"""

from typing import List


def build_lps(pattern: str) -> List[int]:
    """Longest-proper-prefix-suffix array for the KMP failure function."""
    m = len(pattern)
    lps = [0] * m
    if m == 0:
        return lps
    length = 0
    i = 1
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps


def kmp_search(text: str, pattern: str) -> List[int]:
    """All starting indices of pattern in text (0-indexed)."""
    positions: List[int] = []
    n, m = len(text), len(pattern)
    if m == 0 or m > n:
        return positions
    lps = build_lps(pattern)
    i = j = 0
    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
        if j == m:
            positions.append(i - j)
            j = lps[j - 1]
        elif i < n and text[i] != pattern[j]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return positions


def naive_search(text: str, pattern: str) -> List[int]:
    """O(n * m) reference implementation for cross-checking."""
    positions: List[int] = []
    n, m = len(text), len(pattern)
    if m == 0:
        return positions
    for i in range(n - m + 1):
        if text[i:i + m] == pattern:
            positions.append(i)
    return positions


def main() -> None:
    text1 = "AABAACAADAABAABA"
    pat1 = "AABA"
    print(f"Text:    {text1}")
    print(f"Pattern: {pat1}")
    print(f"KMP found at:   {kmp_search(text1, pat1)}")
    print(f"Naive found at: {naive_search(text1, pat1)}")

    text2 = "AAAAABAAABA"
    pat2 = "AAAA"
    print(f"\nText:    {text2}")
    print(f"Pattern: {pat2}")
    print(f"LPS: {build_lps(pat2)}")
    print(f"KMP found at: {kmp_search(text2, pat2)}")

    print(f"\nKMP('hello', 'xyz')   = {kmp_search('hello', 'xyz')}")
    print(f"KMP('hi', 'hello')    = {kmp_search('hi', 'hello')}")


if __name__ == "__main__":
    main()


"""
NOTES — Python vs Java:
    - String slicing replaces explicit charAt() calls; very readable.
    - List + append replaces ArrayList<Integer>.
    - No need for explicit ArrayList -> Integer conversion.
    - For raw speed, str.find / re.finditer are implemented in C and
      typically beat hand-rolled KMP in Python.
"""
