# Week 12 — Pattern Recognition Drills

These problems are described in plain English. For each one, identify which stack pattern applies and write a 1-line justification. **Don't code anything yet.** Try without peeking at the answer key.

## Drills

### 1. Given a string of parentheses `()[]{}` of length up to 10^5, decide if it is balanced.
Pattern: ______
Why: ______

### 2. Evaluate a postfix arithmetic expression with tokens `+ - * /` and integer operands. Length up to 10^5.
Pattern: ______
Why: ______

### 3. Convert an infix expression to postfix. Operators: `+ - * /`, with standard precedence.
Pattern: ______
Why: ______

### 4. Given an array of n daily temperatures, for each day output how many days until a warmer one. If none exists, output 0. n ≤ 10^5.
Pattern: ______
Why: ______

### 5. Given an array of building heights, compute the largest rectangle that fits inside the histogram. n ≤ 10^5.
Pattern: ______
Why: ______

### 6. Given a string with letters and the special character `#` denoting a backspace, return the resulting string after processing all backspaces. Length up to 10^5.
Pattern: ______
Why: ______

### 7. Implement a stack that also reports the minimum element in O(1) at any time.
Pattern: ______
Why: ______

### 8. Distractor: Given a stream of integers, report the current median efficiently after every insertion. (Why is this *not* a stack problem?)
Pattern: ______
Why: ______

### 9. Given an array, for each index `i` output the index of the *previous greater element* (or −1 if none). n ≤ 10^5.
Pattern: ______
Why: ______

### 10. Given a string like `"3[a2[bc]]"`, decode it (k[X] means X repeated k times). Length ≤ 10^4, nesting up to 10 deep.
Pattern: ______
Why: ______

---

## Answer Key

<details><summary>Click to reveal</summary>

1. **Pattern**: Stack of openers. **Why**: every closer must match the top of the stack.
2. **Pattern**: Operand stack. **Why**: push numbers, pop two on operator, push result — postfix is literally stack-machine code.
3. **Pattern**: Shunting-yard with operator stack. **Why**: pop higher/equal precedence operators when a new one arrives.
4. **Pattern**: Monotonic decreasing stack of indices. **Why**: pop while current > top → fill answer with index distance.
5. **Pattern**: Monotonic increasing stack of indices. **Why**: each bar's max rectangle ends when a shorter bar appears — pop on dip.
6. **Pattern**: Stack of kept characters. **Why**: push letter, pop on `#` — output is stack contents.
7. **Pattern**: Two stacks (main + min-tracking) or paired pushes. **Why**: maintain running minima alongside values.
8. **Pattern**: Distractor — two heaps (Week 15), not a stack. **Why**: median needs ordered access from both ends, which a stack cannot provide.
9. **Pattern**: Monotonic decreasing stack. **Why**: stack stores indices of values not yet exceeded; top of stack at query time is previous greater.
10. **Pattern**: Stack of `(prefix, count)` frames. **Why**: push state on `[`, pop and concatenate on `]` — recursion via stack.

</details>
