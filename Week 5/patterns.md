# Week 5 — Pattern Recognition Drills

These problems are described in plain English. For each one, identify which method/recursion pattern applies and write a 1-line justification. **Don't code anything yet.** Try without peeking at the answer key.

## Drills

### 1. Compute `n!` for n up to 20. Return as `long`.
Pattern: ______
Why: ______

### 2. Given two disks-on-pegs configuration with `n` disks, print the moves required to transfer them following the classic three-peg constraint.
Pattern: ______
Why: ______

### 3. Compute the n-th Fibonacci number for n ≤ 40 (no DP needed — just demonstrate the recursive definition).
Pattern: ______
Why: ______

### 4. Given an integer `n`, print all its digits *in reverse* using only recursion (no loops, no string conversion).
Pattern: ______
Why: ______

### 5. Compute `gcd(a, b)` for positive integers a, b ≤ 10^9.
Pattern: ______
Why: ______

### 6. Compute `power(x, n)` for integer n ≥ 0 in O(log n) multiplications.
Pattern: ______
Why: ______

### 7. Distractor: Compute the n-th Fibonacci number for n ≤ 10^6 in under 1 s. (How does the recognition change?)
Pattern: ______
Why: ______

### 8. Write a method `sumDigits(int n)` that returns the sum of decimal digits of `n`. Implement it recursively.
Pattern: ______
Why: ______

### 9. Given two methods `foo(int)` and `bar(int)` where `foo(n)` calls `bar(n-1)` and `bar(n)` calls `foo(n-1)`, with a base case at 0 — what overall pattern does this illustrate?
Pattern: ______
Why: ______

### 10. Define a method that, given a non-negative integer `n`, returns the number of bits set in its binary representation, **using recursion only**.
Pattern: ______
Why: ______

---

## Answer Key

<details><summary>Click to reveal</summary>

1. **Pattern**: Linear recursion (or loop). **Why**: `fact(n) = n * fact(n-1)`, base `fact(0)=1`.
2. **Pattern**: Tower-of-Hanoi recursion. **Why**: move n-1 to spare, move biggest, recurse — classic divide-and-conquer with three subproblems.
3. **Pattern**: Naïve binary recursion. **Why**: `fib(n) = fib(n-1) + fib(n-2)` — exponential but ok at n≤40 (~10^8 calls borderline; teach memoization later).
4. **Pattern**: Tail-style recursion peeling least-significant digit. **Why**: print `n%10`, recurse on `n/10`.
5. **Pattern**: Euclidean recursion. **Why**: `gcd(a,b) = gcd(b, a%b)`, base `gcd(a,0)=a`.
6. **Pattern**: Fast exponentiation by halving. **Why**: `power(x, n/2)` squared, plus extra `x` if n odd → O(log n).
7. **Pattern**: Distractor — pure recursion is too slow; need memoization/iteration/fast doubling. **Why**: n≤10^6 needs O(n) or O(log n), not O(φ^n).
8. **Pattern**: Linear recursion on `n/10`. **Why**: `sumDigits(n) = n%10 + sumDigits(n/10)`, base 0.
9. **Pattern**: Mutual recursion. **Why**: two functions reference each other; well-defined when there's a converging base case.
10. **Pattern**: Recursion on `n/2` (or `n & (n-1)`). **Why**: `popcount(n) = (n&1) + popcount(n>>1)`, base 0.

</details>
