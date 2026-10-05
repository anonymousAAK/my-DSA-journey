# Weekly Digest — 2026-10-05 (ISO 2026-W41)

One case study, one pattern drill, one challenge. Rotated weekly. Read these in any order; the goal is one bite-sized prompt per week to keep recognition warm even when you can't sit down for a full session.

## Case study
**How "Discover Weekly" is a Graph + Matrix Factorization Problem**

Every Monday, 500+ million Spotify users get a personalized 30-song playlist. Each playlist needs to feel like it understands you, contain songs you haven't heard before, and *not* repeat across weeks. With a catalog of ~100M tracks and hundreds of millions of users, generating 500M personalized playlists is the algorithmic equivalent of cooking 500M custom meals every week from a kitchen of 100M ingredients.

Read it in full: [`case_studies/real_world/02_spotify_discover_weekly_graph.md`](case_studies/real_world/02_spotify_discover_weekly_graph.md)

## Pattern drill
_From Week 22 (drill #2)._

> Given a directed graph that may contain negative edge weights (no negative cycles), find shortest distances from `s`. n ≤ 500.

Name the pattern in one word and justify in one sentence. Do **not** look at the answer key until you've written your guess down.

Drill source: [`Week 22/patterns.md`](Week 22/patterns.md)

## Hard-mode challenge
### Challenge 2 (Week 22): Negative-Weight Cycle Detection (Bellman–Ford)

**Spec**:
Read a weighted directed graph (edges may have negative weight). Print `YES` if there's a negative-weight cycle reachable from vertex 1, else print the shortest distance from 1 to every vertex (or `INF` if unreachable). Bellman–Ford: `n-1` relaxation rounds, then one more round — any edge that still relaxes lies on (or reaches) a negative cycle.

**Constraints**:
- `1 <= n <= 1000`, `1 <= m <= 10^4`, weights in `[-10^4, 10^4]`
- Time: O(n m)
- Memory: O(n)

**Test inputs**:
| Input | Expected output |
|

Full spec: [`Week 22/challenges.md`](Week 22/challenges.md)

---

Subscribe via RSS: point your reader at `https://raw.githubusercontent.com/anonymousAAK/my-DSA-journey/main/feed.xml`. See [`docs/NEWSLETTER.md`](docs/NEWSLETTER.md) for details.
