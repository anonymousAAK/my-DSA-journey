# Week 5 — Functions & Recursion

> Self-check: `./scripts/journey quiz 5`  |  Next session: `./scripts/journey next`

## Today's session (~45 min)

1. **Concept** (10 min) — Read [`python/3.recursion_basics.py`](python/3.recursion_basics.py) (CONCEPT + KEY POINTS blocks).
2. **Recognize the pattern** (5 min) — Try drills 1-5 in [`patterns.md`](patterns.md) cold.
3. **Implement from spec** (20 min) — Pick Challenge 1 from [`challenges.md`](challenges.md). Code it in `workbook/week_05/attempts/`.
4. **Verify YOUR code** (5 min) — `./scripts/journey verify recursion workbook/week_05/attempts/<your-file>.py`
5. **Mastery quiz** (5 min) — `./scripts/journey quiz 5`

If you got stuck: open [`python/3.recursion_basics.py`](python/3.recursion_basics.py) and diff against your attempt.
If you finish early: drills 6-10 in `patterns.md`, or Challenge 2.

**Primary language: Python.** Want to compare implementations? See the per-language table below.

---

## Topic overview

This week covers **Functions & Recursion**. You'll touch: MethodBasics, MethodOverloading, RecursionBasics, FibonacciRecursion, TowerOfHanoi, RecursionPatterns. The flagship algorithm/concept for the week is implemented in all five languages, and the Python file listed in Today's session is the canonical walkthrough.

## Related materials

| Resource | Use it when |
|----------|-------------|
| Visualization: [`viz/recursion_tree.html`](../viz/recursion_tree.html) | You want to SEE recursion unfold as a call tree |
| Capstone: [`capstones/phase_1_cli_calculator.md`](../capstones/phase_1_cli_calculator.md) | Phase 1 capstone — apply what you learned in weeks 1-5 |
| [`problems.md`](problems.md) | You want extra practice with company-tagged problems |

## Reference: per-language topic index

<details>
<summary>All implementations (Java / Python / C++ / Rust / Web)</summary>

**Topic index**


| # | Topic | Java | Python | C++ | Rust | Web |
|---|-------|------|--------|-----|------|-----|
| 1 | MethodBasics | `java/1.MethodBasics.java` | `python/1.method_basics.py` | `cpp/1.method_basics.cpp` | `rust/s01_method_basics.rs` | `web/1.method_basics.html` |
| 2 | MethodOverloading | `java/2.MethodOverloading.java` | `python/2.method_overloading.py` | `cpp/2.method_overloading.cpp` | `rust/s02_method_overloading.rs` | `web/2.method_overloading.html` |
| 3 | RecursionBasics | `java/3.RecursionBasics.java` | `python/3.recursion_basics.py` | `cpp/3.recursion_basics.cpp` | `rust/s03_recursion_basics.rs` | `web/3.recursion_basics.html` |
| 4 | FibonacciRecursion | `java/4.FibonacciRecursion.java` | `python/4.fibonacci_recursion.py` | `cpp/4.fibonacci_recursion.cpp` | `rust/s04_fibonacci_recursion.rs` | `web/4.fibonacci_recursion.html` |
| 5 | TowerOfHanoi | `java/5.TowerOfHanoi.java` | `python/5.tower_of_hanoi.py` | `cpp/5.tower_of_hanoi.cpp` | `rust/s05_tower_of_hanoi.rs` | `web/5.tower_of_hanoi.html` |
| 6 | RecursionPatterns | `java/6.RecursionPatterns.java` | `python/6.recursion_patterns.py` | `cpp/6.recursion_patterns.cpp` | `rust/s06_recursion_patterns.rs` | `web/6.recursion_patterns.html` |

**Survey companions**


Cross-cutting files that summarize the week or provide an interactive overview:

| Topic | Java | Python | C++ | Rust | Web |
|-------|------|--------|-----|------|-----|
| Recursion | — | `python/recursion.py` | `cpp/recursion.cpp` | `rust/recursion.rs` | — |
| Interactive index | — | — | — | — | `web/index.html` |

**Topic roadmap**


- **1. MethodBasics**
- **2. MethodOverloading**
- **3. RecursionBasics**
- **4. FibonacciRecursion**
- **5. TowerOfHanoi**
- **6. RecursionPatterns**

</details>

## Reference: tradeoff matrix

<details>
<summary>Approach x Time x Space x When-to-prefer</summary>


Flagship topic: solving the Tower of Hanoi (recursion).

| Approach | Time | Space | Code complexity | When to prefer |
|----------|------|-------|-----------------|----------------|
| Classic recursion (move n-1, move 1, move n-1) | O(2ⁿ) | O(n) stack | Low | The canonical solution — clearest expression of the recurrence |
| Iterative (binary counter / Frame–Stewart) | O(2ⁿ) | O(1) | High | When stack depth is a real concern |
| Bitwise enumeration of moves | O(2ⁿ) | O(1) | High | Curiosity / understanding the move sequence |

| Approach (Fibonacci recursion) | Time | Space | Code complexity | When to prefer |
|----------|------|-------|-----------------|----------------|
| Plain recursion | O(φⁿ) | O(n) | Low | Pedagogy only |
| Memoized recursion | O(n) | O(n) | Medium | When you also need a recursion-shaped solution |
| Tail-recursion-style iteration | O(n) | O(1) | Low | Production |

</details>

## Reference: anti-patterns to avoid

<details>
<summary>Common mistakes specific to this week's topic</summary>


- **Calling a recursive method without a base case** — the first recursive call you write should immediately return on the smallest input. Without that, you get StackOverflowError instantly.
- **Putting the base case after the recursive call** — order matters. The check must run *before* recursing, or you recurse one extra level into invalid input.
- **Confusing "what the function returns" with "what it prints"** — pick one contract per method. Methods that both print and return are hard to test and hard to compose.
- **Method overloading by argument *order* of the same types** — `foo(int a, int b)` and `foo(int b, int a)` are the same signature. Overloads must differ in count or types.
- **Believing recursion is "elegant" therefore always correct** — elegant code with exponential complexity is still exponentially slow. Verify the recurrence's complexity before celebrating.

</details>

## Reference: how to run a topic file

<details>
<summary>Java / Python / C++ / Rust / Web one-liners</summary>


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

</details>

## Reflection prompts


- Which topic this week was hardest, and what made it hard?
- Was there a pattern you didn't recognize and had to be told about? Which one?
- If you had to teach Tower of Hanoi to someone with only one minute, what's the one sentence you'd use?
- Did writing the base case first vs last make a difference for you? Why?
- What's one problem you'd want to revisit in 3 weeks to see if you've internalized the pattern?
