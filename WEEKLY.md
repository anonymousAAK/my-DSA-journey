# Weekly Digest — 2026-05-21 (ISO 2026-W21)

One case study, one pattern drill, one challenge. Rotated weekly. Read these in any order; the goal is one bite-sized prompt per week to keep recognition warm even when you can't sit down for a full session.

## Case study
**How "Discover Weekly" is a Graph + Matrix Factorization Problem**

Every Monday, 500+ million Spotify users get a personalized 30-song playlist. Each playlist needs to feel like it understands you, contain songs you haven't heard before, and *not* repeat across weeks. With a catalog of ~100M tracks and hundreds of millions of users, generating 500M personalized playlists is the algorithmic equivalent of cooking 500M custom meals every week from a kitchen of 100M ingredients.

Read it in full: [`case_studies/real_world/02_spotify_discover_weekly_graph.md`](case_studies/real_world/02_spotify_discover_weekly_graph.md)

## Pattern drill
_From Week 2 (drill #2)._

> Read an integer score 0–100 and print the letter grade: A (>=90), B (>=80), C (>=70), D (>=60), F otherwise.

Name the pattern in one word and justify in one sentence. Do **not** look at the answer key until you've written your guess down.

Drill source: [`Week 2/patterns.md`](Week 2/patterns.md)

## Hard-mode challenge
### Challenge 2 (Week 2): Tax Bracket Salary Computer

**Spec**:
Read a non-negative integer gross annual salary in USD. Compute the take-home pay using these progressive brackets (in order):
- 0% on the first 10,000
- 10% on the next 30,000 (i.e., income from 10,001 to 40,000)
- 20% on the next 60,000 (40,001 to 100,000)
- 30% on the next 150,000 (100,001 to 250,000)
- 40% on everything above 250,000

Print the net salary as an integer (round half-to-even). Use only `if/else` control flow — no arrays, no maps. The challenge is to compose the conditional structure cleanly.

**Constraints**:
- Input size: salary in `[0, 10^9]`
- Time: O(1)
- Memory: O(1)

**Test inputs**:
| Input | Expected output |
|

Full spec: [`Week 2/challenges.md`](Week 2/challenges.md)

---

Subscribe via RSS: point your reader at `https://raw.githubusercontent.com/anonymousAAK/my-DSA-journey/main/feed.xml`. See [`docs/NEWSLETTER.md`](docs/NEWSLETTER.md) for details.
