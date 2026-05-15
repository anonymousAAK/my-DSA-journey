# Week 6

Each topic is implemented in all five languages: **Java, Python, C++, Rust, and Web (HTML/JS)**. The Java track is the primary detailed walkthrough; the others mirror it with idiomatic constructs.

## Topic index

| # | Topic | Java | Python | C++ | Rust | Web |
|---|-------|------|--------|-----|------|-----|
| 1 | ReturnArraySum | `java/1.ReturnArraySum.java` | `python/1.return_array_sum.py` | `cpp/1.return_array_sum.cpp` | `rust/s01_return_array_sum.rs` | `web/1.return_array_sum.html` |
| 2 | LinearSearch | `java/2.LinearSearch.java` | `python/2.linear_search.py` | `cpp/2.linear_search.cpp` | `rust/s02_linear_search.rs` | `web/2.linear_search.html` |
| 3 | ArrayReverseAndRotate | `java/3.ArrayReverseAndRotate.java` | `python/3.array_reverse_and_rotate.py` | `cpp/3.array_reverse_and_rotate.cpp` | `rust/s03_array_reverse_and_rotate.rs` | `web/3.array_reverse_and_rotate.html` |
| 4 | PrefixSumAndKadane | `java/4.PrefixSumAndKadane.java` | `python/4.prefix_sum_and_kadane.py` | `cpp/4.prefix_sum_and_kadane.cpp` | `rust/s04_prefix_sum_and_kadane.rs` | `web/4.prefix_sum_and_kadane.html` |
| 5 | DutchNationalFlagAndMissing | `java/5.DutchNationalFlagAndMissing.java` | `python/5.dutch_national_flag_and_missing.py` | `cpp/5.dutch_national_flag_and_missing.cpp` | `rust/s05_dutch_national_flag_and_missing.rs` | `web/5.dutch_national_flag_and_missing.html` |

## Survey companions

Cross-cutting files that summarize the week or provide an interactive overview:

| Topic | Java | Python | C++ | Rust | Web |
|-------|------|--------|-----|------|-----|
| Arrays | — | `python/arrays.py` | `cpp/arrays.cpp` | `rust/arrays.rs` | — |
| Interactive index | — | — | — | — | `web/index.html` |

## How to run a topic file

From the week's directory:

```bash
# Java
javac java/<file>.java && java -cp java <ClassName>

# Python
python3 python/<file>.py

# C++
g++ -std=c++17 cpp/<file>.cpp -o /tmp/a && /tmp/a

# Rust
rustc --edition 2021 rust/<file>.rs -o /tmp/a && /tmp/a

# Web — open in a browser
open web/<file>.html   # macOS
xdg-open web/<file>.html   # Linux
```

## Topic roadmap

- **1. ReturnArraySum**
- **2. LinearSearch**
- **3. ArrayReverseAndRotate**
- **4. PrefixSumAndKadane**
- **5. DutchNationalFlagAndMissing**

## Tradeoff Matrix

Flagship topic: Maximum Subarray Sum (covered in PrefixSumAndKadane).

| Approach | Time | Space | Code complexity | When to prefer |
|----------|------|-------|-----------------|----------------|
| Brute force (all pairs) | O(N²) | O(1) | Low | N ≤ 10³, or as a sanity oracle |
| Divide & conquer | O(N log N) | O(log N) | Medium | When recursion is required for pedagogy |
| Kadane's algorithm | O(N) | O(1) | Low | Always — this is the right answer |
| Prefix sum + running min | O(N) | O(N) | Low | When you also need range-sum queries later |

| Approach (Dutch National Flag) | Time | Space | Code complexity | When to prefer |
|----------|------|-------|-----------------|----------------|
| Two passes counting | O(N) | O(1) | Low | When stability is irrelevant |
| Sort | O(N log N) | O(1) | Low | If sorting library is already in use |
| Three-pointer in-place | O(N) | O(1) | Medium | When you need a single pass and constant extra space |

## Anti-patterns to avoid

- **Resetting Kadane's running sum to 0 instead of `max(0, sum + a[i])`** — if all numbers are negative, the "reset to 0" version returns 0 instead of the largest (least-negative) element. Initialize `best = a[0]` and don't reset.
- **Rotating an array by `k` with `k` separate single-shifts** — that's O(N·k). Use the reverse-three-times trick (reverse all, reverse first k, reverse rest) for O(N) and no extra memory.
- **Using `array.length()` instead of `array.length`** — arrays use the field `length`, not a method. Strings and collections use methods. Mixing them is the most common Java syntax error in this section.
- **Finding the "missing number" with a HashSet** — works but uses O(N) memory. The Gauss sum (`n(n+1)/2 − Σa[i]`) or XOR trick (`x ^ x = 0`) does it in O(1) extra space.
- **Mutating an array while iterating with an enhanced-for** — the iterator's view of the array doesn't update for primitive arrays the way you might expect; for collections it throws ConcurrentModificationException. Use an index-based loop when you need to mutate.

## Reflection prompts

- Which topic this week was hardest, and what made it hard?
- Was there a pattern you didn't recognize and had to be told about? Which one?
- If you had to teach Kadane's algorithm to someone with only one minute, what's the one sentence you'd use?
- Looking at last week's anti-patterns list, did you commit any of them this week? Why?
- What's one problem you'd want to revisit in 3 weeks to see if you've internalized the pattern?
