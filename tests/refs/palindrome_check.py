"""Reference: palindrome check (case- and punctuation-insensitive).

Matches Week 7's `is_palindrome_ignore_non_alpha` semantics so "A man, a plan,
a canal: Panama" is True.
"""

from __future__ import annotations


def isPalindrome(s: str) -> bool:
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
