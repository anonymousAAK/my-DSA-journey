# Phase 4: Graphs & DP — Smallest Reaching Set in a Social Graph

## The Word Problem

> Growth wants to seed a "share with your friends" feature. The plan: pick a small group of users; we'll send each of them a free month if they share. Constraint: the group's friends-of-friends (just one hop out!) need to cover the entire user base of 4.2M people. They want the *smallest* such group. They asked me how long this would take to compute and I said "uh." Can you take a look? Bonus points if it's actually optimal but I told them a "good" answer would be fine if optimal is hopeless. We have an edge list export from the social graph, ~310M edges.

## Step 1: Restate the problem precisely

Inputs:
- Undirected graph G = (V, E), with |V| = 4.2M users, |E| = 310M friendships.
- "1-hop reach" of a vertex v = {v} ∪ neighbors(v).

Output: smallest subset S ⊆ V such that ⋃_{v ∈ S} reach(v) = V.

In other words, every user must be either in S or be a friend of someone in S.

This is **Dominating Set** — a textbook NP-hard problem. The PM has stumbled into one of the canonically intractable problems. There is no polynomial-time algorithm for the exact answer (assuming P ≠ NP). What we need is a **good approximation**, fast.

It's also exactly **Set Cover** in disguise: the universe is V; for each vertex v we have the set reach(v); we want the minimum number of sets that cover the universe.

## Step 2: Identify constraints

- |V| = 4.2M, |E| = 310M. Average degree ≈ 147.
- Memory: adjacency list, undirected, each edge stored twice → 620M ints. At 4 bytes per int that's 2.5 GB. Manageable on a single big box, painful on a laptop.
- Time budget: PM said "how long would this take" — implication is "I want it tonight." So aim for minutes-to-an-hour, not days.
- We will **not** find the optimum. We'll commit to a known approximation algorithm.
- Edge cases:
  - Isolated users (no friends) → must be in S themselves.
  - Tiny clusters → at least one member per cluster.
  - Influencers with millions of friends → essentially free covers.
  - Multiple disconnected components → solve each independently.

## Step 3: Brute force first

Exhaustive search: try every subset of V, in increasing size, and check coverage. There are 2^(4.2M) subsets. We will never finish. Brute force is genuinely infeasible here, not just slow — that's the *point* of NP-hard.

ILP (integer linear programming) on this size: also infeasible. Modern solvers handle thousands of variables; 4.2M is out of reach.

So brute force is dead. We need an approximation by design.

## Step 4: Identify wasted work

For Set Cover, there's a classical result: the **greedy algorithm achieves an H_n ≈ ln n approximation**, and you cannot do better in polynomial time unless P = NP. For n = 4.2M, ln n ≈ 15.25. So greedy will give us a set at most ~15x optimal. In practice on real graphs, it's usually within 2-3x.

The greedy:
1. Pick the vertex v whose reach(v) covers the most *uncovered* users.
2. Mark those users covered. Remove v from consideration.
3. Repeat until all users are covered.

The wasted work in the naïve implementation: every iteration we re-scan every vertex to find the one with max uncovered neighbors. That's O(V) per iteration × O(|S|) iterations × O(deg(v)) per check → O(V · |S| · avg_deg). For |S| in the thousands, that's ~10^15 operations. Dead on arrival.

Two pieces of waste:
- We re-compute "uncovered count" for every vertex from scratch each iteration. But when we cover vertex u, only u's *neighbors* see their uncovered count drop by 1. Everyone else is unchanged.
- We re-scan everyone to find the max. We should maintain a **priority queue** keyed by uncovered count.

## Step 5: Optimize

**Lazy max-heap (Week 11) + neighbor-update gossip:**

Data structures:
- `covered`: a bitset of size |V|, all zeros initially.
- `uncov_count[v]`: number of uncovered users in reach(v). Initially = degree(v) + 1 (the +1 is v itself, if not yet covered).
- `heap`: max-heap of (uncov_count[v], v). Stale entries are tolerated via the same lazy-heap trick from Phase 3.

Greedy loop:
1. Pop max from heap. If its count is stale (doesn't match `uncov_count[v]`), discard and pop again.
2. Add v to S.
3. For every u in reach(v) that is uncovered: mark u covered. For every neighbor w of u, decrement `uncov_count[w]` and push the new value into the heap.
4. Repeat until everyone is covered.

The total work in step 3, summed across all iterations, is bounded by Σ_u deg(u) · (each u covered exactly once → each edge touched ≈ twice) = O(E) **total**, not per iteration. So the algorithm is O((V + E) log V) overall, dominated by heap ops. On our graph, that's about 5 billion log ops — minutes on a single machine, easily.

Disconnected components: handle automatically — each component's vertices are reached separately. Isolated vertices must be in S (their `uncov_count` is 1, and only they themselves can cover them).

Tie-breaking for the heap: when two vertices have the same `uncov_count`, prefer higher original degree (the "denser" vertex tends to be more useful later, too). Cheap heuristic.

### Even better tradeoff: heuristic seeding

For real social graphs, a great practical heuristic before greedy:
- Sort vertices by degree, descending.
- Start by adding the top-k highest-degree vertices to S unconditionally (k=10, say). Influencers cover huge swaths instantly.
- Then run greedy from there.

This isn't theoretically better but cuts wall-clock significantly because the heap stays small once the bulk of users are covered.

## Step 6: Implementation gotchas

- **Loading 310M edges**: don't read into Python lists. Use `numpy` arrays of int32 or `scipy.sparse.csr_matrix`. Pure-Python adjacency lists for 4.2M nodes will OOM.
- **Bitset for `covered`**: don't use a Python `set` of 4.2M ints. Use `numpy` boolean array or `bitarray`.
- **Heap of 4.2M entries**: Python's `heapq` is fine, but expect 100-300 MB of heap entries with the lazy trick. Periodically rebuild the heap if its size exceeds 3x |V|.
- **Edge duplication**: friendships are symmetric; make sure your edge list doesn't store both (a,b) and (b,a) twice if you're building adjacency lists.
- **Isolated nodes**: handle the edge case BEFORE the main loop — pre-add them to S so the heap never has to surface them as winners with count=1.
- **Approximation quality monitoring**: log the size of S as a function of iterations. If it's growing way faster than ln(V), something's wrong.
- **Stopping early**: PM said "good enough is fine." If at some point 99% of users are covered with |S| = 1000, ask whether the last 1% (tail of isolated cliques) is worth doubling |S|. Often it isn't.

## Step 7: Verification

- Toy graph: K_5 (complete graph on 5 nodes). Any single vertex covers all 5. Optimum = 1. Greedy = 1.
- Star graph (1 hub, n-1 leaves). Optimum = 1 (the hub). Greedy = 1.
- Path graph P_5. Optimum = 2 (vertices at positions 1 and 3, 0-indexed, cover all). Greedy might pick the middle first, then need one more — also 2.
- Disjoint components: each handled independently.
- Stress: generate random Erdős-Rényi graphs at small scale (n=20-50), compute optimum via brute force (ILP or 2^n enumeration), compare to greedy. Ratio should empirically stay below 2x for realistic densities.

## Step 8: Reflection

What made this hard: recognizing it's NP-hard, **accepting that**, and choosing the right approximation. The leap from "this is hard" to "I won't find optimum, I'll find a 15x-from-optimum solution in O((V+E) log V)" is the senior-engineer move. A junior engineer either grinds on exact algorithms or gives up.

Patterns at play:
- **Set cover** as a framing device. Once you see a real-world problem as set cover, you have a toolkit.
- **Greedy with priority queue** (Week 16). The heap turns O(V²) into O(V log V).
- **Lazy heap deletion** (same trick as Phase 3 — patterns rhyme).
- **Connected components** as a preprocessing step (Week 17).

Where set cover lives in real systems:
- Test case selection — find smallest test set that hits all branches.
- Database query plan selection — cover all required columns with fewest indexes.
- Sensor placement — fewest cameras to cover a building.
- Vaccine targeting — fewest people to vaccinate to protect a population (epidemiology version of this exact problem).

Curriculum tie-in: BFS (Week 16), graph representation (Week 16), heaps (Week 11), and the very important Week 19 lesson — **knowing when to stop looking for optimum**.
