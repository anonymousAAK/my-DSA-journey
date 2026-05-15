# Week 3 — Pattern Recognition Drills

These problems are described in plain English. For each one, identify which loop/bitwise pattern applies and write a 1-line justification. **Don't code anything yet.** Try without peeking at the answer key.

## Drills

### 1. Given `n` up to 10^6, print the sum of all integers from 1 to n. Time limit 1 s.
Pattern: ______
Why: ______

### 2. Read integers until a 0 is entered. Print how many positive and how many negative numbers were entered.
Pattern: ______
Why: ______

### 3. Given an integer `n`, determine whether it is a power of two. n fits in 32 bits.
Pattern: ______
Why: ______

### 4. Print the binary representation of an unsigned 32-bit integer with leading zeros.
Pattern: ______
Why: ______

### 5. Given two integers `a` and `b`, compute `a * b` using only addition and a loop. (Pretend the `*` operator is forbidden.)
Pattern: ______
Why: ______

### 6. Given `n`, count the number of set bits (`1`s in binary). n up to 10^9.
Pattern: ______
Why: ______

### 7. Distractor: Given an array of 10^7 integers, find the maximum. (Why isn't a `while` enough?)
Pattern: ______
Why: ______

### 8. Print all integers from 1 to 100, skipping multiples of 3 *or* 5.
Pattern: ______
Why: ______

### 9. Toggle the k-th bit of a number `n` (0-indexed from the LSB).
Pattern: ______
Why: ______

### 10. Given a positive integer, reverse its digits (e.g. 1234 → 4321). Do not convert to string.
Pattern: ______
Why: ______

---

## Answer Key

<details><summary>Click to reveal</summary>

1. **Pattern**: Closed-form `n*(n+1)/2` — or a simple `for` loop. **Why**: 10^6 iterations is fine, but recognize the O(1) shortcut.
2. **Pattern**: `while` with sentinel terminator. **Why**: loop continues until input == 0; two running counters.
3. **Pattern**: Bitwise trick `n > 0 && (n & (n-1)) == 0`. **Why**: powers of two have exactly one set bit.
4. **Pattern**: Loop right-shift + `& 1` from bit 31 to 0. **Why**: extract each bit by shifting.
5. **Pattern**: `for` loop accumulating sum, `b` times. **Why**: literal definition of multiplication as repeated addition.
6. **Pattern**: Brian Kernighan trick `while(n){ n &= n-1; count++; }`. **Why**: clears lowest set bit each iteration — O(popcount).
7. **Pattern**: Distractor — requires arrays (Week 6). **Why**: loops alone can iterate values, but "an array of 10^7" implies array storage, not Week 3.
8. **Pattern**: `for` with compound condition / `continue`. **Why**: filter inside the loop body using `i%3==0 || i%5==0`.
9. **Pattern**: XOR with a single-bit mask: `n ^ (1<<k)`. **Why**: XOR with 1 flips a bit; AND-NOT clears, OR sets, XOR toggles.
10. **Pattern**: Mod/div loop accumulating reversed value: `r = r*10 + n%10; n/=10;`. **Why**: digit extraction primitive.

</details>
