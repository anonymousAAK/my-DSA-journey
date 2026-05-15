"""Reference: balanced parentheses checker for "(){}[]"."""

from __future__ import annotations
from typing import List


def isBalanced(s: str) -> bool:
    pairs = {')': '(', ']': '[', '}': '{'}
    stack: List[str] = []
    for c in s:
        if c in '([{':
            stack.append(c)
        elif c in ')]}':
            if not stack or stack[-1] != pairs[c]:
                return False
            stack.pop()
    return not stack
