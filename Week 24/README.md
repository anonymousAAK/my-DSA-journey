# Week 24 — Research-Level Topics

> Self-check: `./scripts/journey quiz 24`  |  Next session: `./scripts/journey next`

## Today's session (~45 min)

1. **Concept** (10 min) — Read [`python/1.ResearchLevelTopics.py`](python/1.ResearchLevelTopics.py) (CONCEPT + KEY POINTS blocks).
2. **Recognize the pattern** (5 min) — Try drills 1-5 in [`patterns.md`](patterns.md) cold.
3. **Implement from spec** (20 min) — Pick Challenge 1 from [`challenges.md`](challenges.md). Code it in `workbook/week_24/attempts/`.
4. **Verify YOUR code** (5 min) — `./scripts/journey verify amortized_methods workbook/week_24/attempts/<your-file>.py`
5. **Mastery quiz** (5 min) — `./scripts/journey quiz 24`

If you got stuck: open [`python/1.ResearchLevelTopics.py`](python/1.ResearchLevelTopics.py) and diff against your attempt.
If you finish early: drills 6-10 in `patterns.md`, or Challenge 2.

**Primary language: Python.** Want to compare implementations? See the per-language table below.

---

## Topic overview

This week covers **Research-Level Topics**. You'll touch: ResearchLevelTopics, NPCompletenessAndApproximation. The flagship algorithm/concept for the week is implemented in all five languages, and the Python file listed in Today's session is the canonical walkthrough.

## Related materials

| Resource | Use it when |
|----------|-------------|
| [`problems.md`](problems.md) | You want extra practice with company-tagged problems |

## Reference: per-language topic index

<details>
<summary>All implementations (Java / Python / C++ / Rust / Web)</summary>

**Topic index**


| # | Topic | Java | Python | C++ | Rust | Web |
|---|-------|------|--------|-----|------|-----|
| 1 | ResearchLevelTopics | `java/1.ResearchLevelTopics.java` | `python/1.ResearchLevelTopics.py` | `cpp/1.ResearchLevelTopics.cpp` | `rust/s01_ResearchLevelTopics.rs` | `web/1.ResearchLevelTopics.html` |
| 2 | NPCompletenessAndApproximation | `java/2.NPCompletenessAndApproximation.java` | `python/2.NPCompletenessAndApproximation.py` | `cpp/2.NPCompletenessAndApproximation.cpp` | `rust/s02_NPCompletenessAndApproximation.rs` | `web/2.NPCompletenessAndApproximation.html` |

**Survey companions**


Cross-cutting files that summarize the week or provide an interactive overview:

| Topic | Java | Python | C++ | Rust | Web |
|-------|------|--------|-----|------|-----|
| Research Level | — | `python/research_level.py` | `cpp/research_level.cpp` | `rust/research_level.rs` | — |
| Interactive index | — | — | — | — | `web/index.html` |

**Topic roadmap**


- **1. ResearchLevelTopics**
- **2. NPCompletenessAndApproximation**

</details>

## Reference: tradeoff matrix

<details>
<summary>Approach x Time x Space x When-to-prefer</summary>


Flagship topic: NP-completeness and approximation algorithms.

| Approach (NP-hard problem strategies) | Quality | Time | When to prefer |
|----------|------|------|----------------|
| Exact exponential (DP, B&B) | Optimal | Exponential | Small inputs (n ≤ 30-50 with good pruning) |
| Approximation algorithm | Bounded factor (e.g. 2× optimal) | Polynomial | Need a worst-case guarantee |
| Heuristic / local search | No guarantee, often great | Polynomial | Real-world solvers (SAT, TSP) |
| Randomized (Las Vegas / Monte Carlo) | Probabilistic guarantee | Polynomial expected | When randomness breaks adversarial inputs |
| Parameterized / FPT algorithms | Optimal | f(k) · poly(n) | Small "parameter" k even if n is large |
| ILP solver | Optimal | Black-box exponential | When modeling beats hand-coding |

| Approach (Vertex Cover) | Approximation ratio | Time | When to prefer |
|----------|------|------|----------------|
| Greedy by highest degree | log n | O(E log V) | Quick baseline |
| Pick both endpoints of any uncovered edge | 2 | O(E) | Provable 2-approximation |
| LP relaxation + rounding | 2 | poly | When you already have an LP solver |
| Exact branch & bound | 1 | Exponential | Small graphs |

</details>

## Reference: anti-patterns to avoid

<details>
<summary>Common mistakes specific to this week's topic</summary>


- **Calling something "NP-hard" without a polynomial-time reduction** — hardness needs a reduction from a known NP-hard problem. "It looks hard" is not a proof; you may have missed a polynomial algorithm.
- **Confusing NP-complete with "impossible"** — NP-hard problems can have great approximations, heuristics, FPT algorithms, or fast solvers on real-world (non-adversarial) inputs. SAT solvers handle millions of variables every day.
- **Implementing a 2-approximation and reporting "within 2× optimal" without proving the bound on your variant** — modifying the standard algorithm often breaks the proof. Cite the exact theorem or re-prove it.
- **Reducing in the wrong direction** — to show your problem X is hard, reduce a known-hard problem *to* X, not the other way around. Reducing X to SAT only shows X is in NP, which is much weaker.
- **Treating PTAS / FPTAS / APX as interchangeable** — a PTAS gives `(1+ε)`-approximation in time that may be doubly exponential in `1/ε`; an FPTAS keeps it polynomial in `1/ε`; APX is the class of constant-factor approximable. These are different guarantees.

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
- If you had to teach what "NP-complete" means to someone with only one minute, what's the one sentence you'd use?
- Looking at last week's anti-patterns list, did you commit any of them this week? Why?
- What's one problem you'd want to revisit in 3 weeks to see if you've internalized the pattern?
