"""
WEEK 12 - PYTHON DSA
Topic: Stack Implementation + Classic Problems
File: 1.StackImplementation.py

CONCEPT:
A stack is a LIFO (Last-In, First-Out) container. push, pop, peek, isEmpty
are all O(1). Implementations: array-backed (Python list) or linked-list
based. Python's `list` already gives stack semantics via append/pop.

KEY POINTS:
- Operations: push, pop, peek/top, is_empty.
- Classic apps:
    1. Balanced parentheses
    2. Next greater element (monotonic stack)
    3. Min stack (O(1) min)
    4. Postfix expression evaluation

ALGORITHM / APPROACH:
- ArrayStack: fixed-capacity wrapper around a list.
- MinStack: keep an auxiliary stack of running mins; on each push push
  min(new, current_min) onto it.
- isBalanced: scan string, push opens, pop+match on closes.
- nextGreaterElement: scan left->right, maintain a stack of indices whose
  next-greater hasn't been resolved; pop when a larger value appears.
- evalPostfix: scan tokens, push operands, pop two when an operator appears.

PYTHON-SPECIFIC NOTES:
- The standard library's `list` already supports stack ops:
    push  -> list.append(x)
    pop   -> list.pop()
    peek  -> list[-1]
- For multithreaded programs use queue.LifoQueue.
- We expose pop() raising IndexError instead of returning sentinel.
- Type hints with Optional and List.

DRY RUN:
Example 1: isBalanced("([]{})")
  '(' push -> ['(']
  '['  push -> ['(','[']
  ']'  pop '[' OK -> ['(']
  '{'  push -> ['(','{']
  '}'  pop '{' OK -> ['(']
  ')'  pop '(' OK -> []
  Empty at end -> True

Example 2: nextGreaterElement([4,5,2,10,8])
  i=0 (4): stack=[]; push 0 -> stack=[0]
  i=1 (5): 5>arr[0]=4, pop 0, result[0]=5; push 1 -> stack=[1]
  i=2 (2): 2<5; push 2 -> stack=[1,2]
  i=3 (10): 10>arr[2]=2 pop 2 result[2]=10; 10>arr[1]=5 pop 1 result[1]=10; push 3
  i=4 (8): 8<10; push 4 -> stack=[3,4]
  Final: [5,10,10,-1,-1]

COMPLEXITY:
  All core ops O(1); next-greater & postfix O(n); each element pushed/popped
  at most once (amortized O(n) total).
"""

from __future__ import annotations
from typing import List, Optional


# ---------- Array-backed stack with capacity check (educational) ----------

class ArrayStack:
    """Fixed-capacity stack backed by a Python list."""

    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self._data: List[int] = []

    def push(self, x: int) -> None:
        if len(self._data) == self.capacity:
            raise OverflowError("Stack overflow")
        self._data.append(x)

    def pop(self) -> int:
        if not self._data:
            raise IndexError("Stack underflow")
        return self._data.pop()

    def peek(self) -> int:
        if not self._data:
            raise IndexError("Stack is empty")
        return self._data[-1]

    def is_empty(self) -> bool: return not self._data
    def __len__(self) -> int: return len(self._data)


# ---------- Min Stack: O(1) getMin ----------

class MinStack:
    """Supports push/pop/peek/get_min all in O(1)."""

    def __init__(self) -> None:
        self._stack: List[int] = []
        self._mins: List[int] = []  # running minimums; top = current min

    def push(self, x: int) -> None:
        self._stack.append(x)
        self._mins.append(x if not self._mins else min(x, self._mins[-1]))

    def pop(self) -> int:
        self._mins.pop()
        return self._stack.pop()

    def peek(self) -> int: return self._stack[-1]
    def get_min(self) -> int: return self._mins[-1]


# ---------- Classic problems ----------

def is_balanced(s: str) -> bool:
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


def next_greater_element(arr: List[int]) -> List[int]:
    n = len(arr)
    result = [-1] * n
    stack: List[int] = []  # indices, values strictly decreasing
    for i in range(n):
        while stack and arr[i] > arr[stack[-1]]:
            result[stack.pop()] = arr[i]
        stack.append(i)
    return result


def eval_postfix(expr: str) -> int:
    stack: List[int] = []
    for tok in expr.split():
        if tok in '+-*/':
            b = stack.pop()
            a = stack.pop()
            if tok == '+': stack.append(a + b)
            elif tok == '-': stack.append(a - b)
            elif tok == '*': stack.append(a * b)
            else: stack.append(int(a / b))  # truncate toward zero like Java int division? we use // for ints
        else:
            stack.append(int(tok))
    return stack.pop()


def main() -> None:
    print("=== Array Stack ===")
    s = ArrayStack(10)
    s.push(1); s.push(2); s.push(3)
    print("peek:", s.peek())  # 3
    print("pop:", s.pop())    # 3
    print("pop:", s.pop())    # 2
    print("size:", len(s))    # 1

    print("\n=== Min Stack ===")
    ms = MinStack()
    for v in [5, 3, 7, 2]:
        ms.push(v)
    print(f"peek={ms.peek()} min={ms.get_min()}")  # 2 2
    ms.pop()
    print(f"After pop: peek={ms.peek()} min={ms.get_min()}")  # 7 3

    print("\n=== Balanced Parentheses ===")
    for t in ["([]{})", "(])", "((()))", "{[}]", ""]:
        print(f"{t!r}: {is_balanced(t)}")

    print("\n=== Next Greater Element ===")
    arr = [4, 5, 2, 10, 8]
    print("Array:", arr)
    print("NGE:  ", next_greater_element(arr))  # [5,10,10,-1,-1]

    print("\n=== Postfix Evaluation ===")
    print('"3 4 +" =', eval_postfix("3 4 +"))           # 7
    print('"3 4 + 2 *" =', eval_postfix("3 4 + 2 *"))   # 14
    print('"15 7 1 1 + - / 3 * 2 1 1 + + -" =',
          eval_postfix("15 7 1 1 + - / 3 * 2 1 1 + + -"))  # 5


if __name__ == "__main__":
    main()


"""
NOTES (vs. Java):
- Java's ArrayDeque is the recommended Stack; in Python we use plain list
  with append/pop. There's also collections.deque (O(1) on both ends).
- No primitive int distinction; Python ints have arbitrary precision.
- We preserved Java's truncate-toward-zero division using int(a/b) instead
  of Python's // (which is floor division — different for negatives!).
"""
