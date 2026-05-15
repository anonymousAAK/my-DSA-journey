# Week 24

Each topic is implemented in all five languages: **Java, Python, C++, Rust, and Web (HTML/JS)**. The Java track is the primary detailed walkthrough; the others mirror it with idiomatic constructs.

## Topic index

| # | Topic | Java | Python | C++ | Rust | Web |
|---|-------|------|--------|-----|------|-----|
| 1 | ResearchLevelTopics | `java/1.ResearchLevelTopics.java` | `python/1.ResearchLevelTopics.py` | `cpp/1.ResearchLevelTopics.cpp` | `rust/s01_ResearchLevelTopics.rs` | `web/1.ResearchLevelTopics.html` |
| 2 | NPCompletenessAndApproximation | `java/2.NPCompletenessAndApproximation.java` | `python/2.NPCompletenessAndApproximation.py` | `cpp/2.NPCompletenessAndApproximation.cpp` | `rust/s02_NPCompletenessAndApproximation.rs` | `web/2.NPCompletenessAndApproximation.html` |

## Survey companions

Cross-cutting files that summarize the week or provide an interactive overview:

| Topic | Java | Python | C++ | Rust | Web |
|-------|------|--------|-----|------|-----|
| Research Level | — | `python/research_level.py` | `cpp/research_level.cpp` | `rust/research_level.rs` | — |
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

- **1. ResearchLevelTopics**
- **2. NPCompletenessAndApproximation**

## Tradeoff Matrix

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

## Anti-patterns to avoid

- **Calling something "NP-hard" without a polynomial-time reduction** — hardness needs a reduction from a known NP-hard problem. "It looks hard" is not a proof; you may have missed a polynomial algorithm.
- **Confusing NP-complete with "impossible"** — NP-hard problems can have great approximations, heuristics, FPT algorithms, or fast solvers on real-world (non-adversarial) inputs. SAT solvers handle millions of variables every day.
- **Implementing a 2-approximation and reporting "within 2× optimal" without proving the bound on your variant** — modifying the standard algorithm often breaks the proof. Cite the exact theorem or re-prove it.
- **Reducing in the wrong direction** — to show your problem X is hard, reduce a known-hard problem *to* X, not the other way around. Reducing X to SAT only shows X is in NP, which is much weaker.
- **Treating PTAS / FPTAS / APX as interchangeable** — a PTAS gives `(1+ε)`-approximation in time that may be doubly exponential in `1/ε`; an FPTAS keeps it polynomial in `1/ε`; APX is the class of constant-factor approximable. These are different guarantees.

## Reflection prompts

- Which topic this week was hardest, and what made it hard?
- Was there a pattern you didn't recognize and had to be told about? Which one?
- If you had to teach what "NP-complete" means to someone with only one minute, what's the one sentence you'd use?
- Looking at last week's anti-patterns list, did you commit any of them this week? Why?
- What's one problem you'd want to revisit in 3 weeks to see if you've internalized the pattern?
