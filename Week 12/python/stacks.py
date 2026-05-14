"""
Week 12 — Stacks
==================
Topics covered:
  - Stack class using a Python list
  - Balanced parentheses check
  - Next greater element (monotonic stack)
  - Min stack (O(1) push, pop, getMin)
  - Evaluate postfix (Reverse Polish Notation) expression

Each class/function includes time/space complexity analysis.
"""

from __future__ import annotations

from typing import List


# ===========================================================================
# Stack Implementation
# ===========================================================================

class Stack:
    """LIFO stack backed by a Python list.

    All operations are amortized O(1).
    """

    def __init__(self) -> None:
        self._data: list[int] = []

    def push(self, val: int) -> None:
        """Push *val* onto the stack.  O(1) amortized."""
        self._data.append(val)

    def pop(self) -> int:
        """Remove and return the top element.  Raises IndexError if empty."""
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._data.pop()

    def peek(self) -> int:
        """Return the top element without removing it."""
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._data[-1]

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def size(self) -> int:
        return len(self._data)

    def __repr__(self) -> str:
        return f"Stack({self._data})"


# ===========================================================================
# Balanced Parentheses
# ===========================================================================

def is_balanced(s: str) -> bool:
    """Check if a string of brackets is balanced.

    Supports '()', '[]', '{}'.

    Time:  O(n)
    Space: O(n)  — the stack
    """
    matching = {")": "(", "]": "[", "}": "{"}
    stack: list[str] = []

    for ch in s:
        if ch in "([{":
            stack.append(ch)
        elif ch in ")]}":
            if not stack or stack[-1] != matching[ch]:
                return False
            stack.pop()

    return len(stack) == 0


# ===========================================================================
# Next Greater Element (Monotonic Stack)
# ===========================================================================

def next_greater_element(arr: List[int]) -> List[int]:
    """For each element, find the next element to the right that is greater.

    Returns a list where result[i] is the next greater element for arr[i],
    or -1 if none exists.

    Uses a monotonic decreasing stack: we process elements left to right
    and pop elements from the stack that are smaller than the current
    element (the current element is their "next greater").

    Time:  O(n) — each element is pushed and popped at most once
    Space: O(n)
    """
    n = len(arr)
    result = [-1] * n
    stack: list[int] = []  # stores indices

    for i in range(n):
        while stack and arr[stack[-1]] < arr[i]:
            idx = stack.pop()
            result[idx] = arr[i]
        stack.append(i)

    return result


# ===========================================================================
# Min Stack
# ===========================================================================

class MinStack:
    """A stack that supports push, pop, top, and retrieving the minimum
    element — all in O(1) time.

    We maintain a parallel stack that tracks the current minimum at each
    level of the main stack.

    Space: O(n)
    """

    def __init__(self) -> None:
        self._stack: list[int] = []
        self._min_stack: list[int] = []

    def push(self, val: int) -> None:
        """Push *val* and update the min tracker.  O(1)"""
        self._stack.append(val)
        current_min = min(val, self._min_stack[-1]) if self._min_stack else val
        self._min_stack.append(current_min)

    def pop(self) -> int:
        """Pop and return the top element.  O(1)"""
        if not self._stack:
            raise IndexError("pop from empty MinStack")
        self._min_stack.pop()
        return self._stack.pop()

    def top(self) -> int:
        """Return the top element without removing it.  O(1)"""
        if not self._stack:
            raise IndexError("top from empty MinStack")
        return self._stack[-1]

    def get_min(self) -> int:
        """Return the minimum element in the stack.  O(1)"""
        if not self._min_stack:
            raise IndexError("get_min from empty MinStack")
        return self._min_stack[-1]


# ===========================================================================
# Evaluate Postfix Expression
# ===========================================================================

def eval_postfix(tokens: List[str]) -> int:
    """Evaluate a postfix (Reverse Polish Notation) expression.

    Supported operators: +, -, *, /  (integer division truncated toward zero).

    Time:  O(n)
    Space: O(n)

    Example:
        ["2", "1", "+", "3", "*"]  →  9   because (2+1)*3 = 9
    """
    stack: list[int] = []

    for token in tokens:
        if token in ("+", "-", "*", "/"):
            b = stack.pop()
            a = stack.pop()
            if token == "+":
                stack.append(a + b)
            elif token == "-":
                stack.append(a - b)
            elif token == "*":
                stack.append(a * b)
            else:
                # Truncate toward zero (Python's // rounds toward -inf)
                stack.append(int(a / b))
        else:
            stack.append(int(token))

    return stack[0]


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # ---- Stack class ----
    s = Stack()
    s.push(10)
    s.push(20)
    s.push(30)
    assert s.peek() == 30
    assert s.pop() == 30
    assert s.size() == 2
    assert s.is_empty() is False
    print("[PASS] Stack class")

    # ---- Balanced Parentheses ----
    assert is_balanced("()[]{}") is True
    assert is_balanced("([{}])") is True
    assert is_balanced("(]") is False
    assert is_balanced("([)]") is False
    assert is_balanced("") is True
    assert is_balanced("{[()]}") is True
    print("[PASS] Balanced parentheses")

    # ---- Next Greater Element ----
    assert next_greater_element([4, 5, 2, 25]) == [5, 25, 25, -1]
    assert next_greater_element([13, 7, 6, 12]) == [-1, 12, 12, -1]
    assert next_greater_element([1, 2, 3, 4]) == [2, 3, 4, -1]
    assert next_greater_element([4, 3, 2, 1]) == [-1, -1, -1, -1]
    print("[PASS] Next greater element (monotonic stack)")

    # ---- Min Stack ----
    ms = MinStack()
    ms.push(-2)
    ms.push(0)
    ms.push(-3)
    assert ms.get_min() == -3
    ms.pop()
    assert ms.top() == 0
    assert ms.get_min() == -2
    ms.push(-1)
    assert ms.get_min() == -2
    print("[PASS] Min stack")

    # ---- Evaluate Postfix ----
    assert eval_postfix(["2", "1", "+", "3", "*"]) == 9
    assert eval_postfix(["4", "13", "5", "/", "+"]) == 6
    assert eval_postfix(["10", "6", "9", "3", "+",
                          "-11", "*", "/", "*", "17", "+", "5", "+"]) == 22
    print("[PASS] Evaluate postfix expression")

    print("\nAll Week 12 tests passed!")
