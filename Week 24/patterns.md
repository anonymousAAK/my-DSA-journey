# Week 24 — Pattern Recognition Drills

These problems are described in plain English. For each one, identify whether the problem is tractable, and if not, what approximation/heuristic pattern you'd reach for. **Don't code anything yet.** Try without peeking at the answer key.

## Drills

### 1. Given n ≤ 50 cities with arbitrary pairwise distances, find a tour shorter than any other (i.e., the optimum).
Pattern: ______
Why: ______

### 2. Given an undirected graph with n ≤ 100, decide whether it contains a clique of size 30.
Pattern: ______
Why: ______

### 3. Given a CNF formula with 10^4 clauses over 10^3 variables, decide satisfiability within reasonable time on a laptop.
Pattern: ______
Why: ______

### 4. Given n ≤ 10^4 jobs each with weight `w_i` and value `v_i` and a knapsack capacity 10^9, maximize value subject to capacity. Distractor flavor.
Pattern: ______
Why: ______

### 5. Given an undirected graph, find a *minimum* vertex cover. n ≤ 30. n ≤ 10^5.
Pattern: ______
Why: ______

### 6. Given a metric TSP instance with n ≤ 10^4, produce a tour at most twice the optimum.
Pattern: ______
Why: ______

### 7. Given an arbitrary 3-SAT instance, produce an assignment satisfying at least 7/8 of clauses in expectation.
Pattern: ______
Why: ______

### 8. Given n ≤ 20 items with weights and a knapsack capacity, find the *exact* optimum. (Should you despair?)
Pattern: ______
Why: ______

### 9. Distractor: Given a flow network with n ≤ 500 and m ≤ 10^4, find the maximum flow. (Is this NP?)
Pattern: ______
Why: ______

### 10. Given a real-world optimization problem you suspect is NP-hard, outline the decision framework you would apply before writing any algorithm.
Pattern: ______
Why: ______

---

## Answer Key

<details><summary>Click to reveal</summary>

1. **Pattern**: Exact TSP (Held–Karp 2^n·n^2). **Why**: 50 is too big for Held–Karp (~2.8·10^16). Branch-and-bound or ILP solver, or accept heuristic.
2. **Pattern**: NP-hard (Clique). **Why**: at n=100, k=30, only branch-and-bound / approximation; recognize hopelessness of brute force C(100,30).
3. **Pattern**: SAT solver (CDCL). **Why**: industrial SAT instances are routinely solved; don't write your own.
4. **Pattern**: Distractor — knapsack DP is pseudo-polynomial, but `W=10^9` kills it. Use meet-in-the-middle (2^(n/2)) or value-DP (`n·V`) or FPTAS.
5. **Pattern**: Branch-and-bound / exponential FPT at small n; greedy 2-approx (sum of matching) for large n. **Why**: minimum vertex cover is NP-hard.
6. **Pattern**: Christofides (or MST-based 2-approx). **Why**: metric (triangle inequality) admits constant-factor approximation.
7. **Pattern**: Random assignment. **Why**: each clause satisfied with prob ≥ 7/8 by uniform random — classic derandomization gives deterministic.
8. **Pattern**: 0/1 knapsack DP (Week 18) or subset-sum bitmask. **Why**: n=20 makes 2^n exact methods fine — exponential is OK when n is small.
9. **Pattern**: Distractor — max flow is in P. **Why**: Edmonds-Karp / Dinic / Push-relabel (Week 26). Recognize what is and isn't NP.
10. **Pattern**: Decision framework: (a) prove or look up complexity; (b) check if input size allows brute force or DP; (c) check for special structure (planar, sparse, metric, bounded treewidth); (d) consider approximation/heuristic/ILP. **Why**: the meta-skill of Week 24.

</details>
