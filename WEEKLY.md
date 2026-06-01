# Weekly Digest — 2026-06-01 (ISO 2026-W23)

One case study, one pattern drill, one challenge. Rotated weekly. Read these in any order; the goal is one bite-sized prompt per week to keep recognition warm even when you can't sit down for a full session.

## Case study
**Caching Strategies in DNS Resolvers**

Every time you type a URL, your machine needs to translate the domain name (`github.com`) into an IP address. The authoritative source of that mapping is a DNS server somewhere in the world — possibly multiple hops away. If every page load required a fresh DNS lookup, the internet would feel like the 1990s again. Resolvers cache aggressively. But DNS records are sometimes wrong, sometimes change, and operators *need* changes to propagate within bounded time — so the cache can't be eternal.

Read it in full: [`case_studies/real_world/04_dns_caching.md`](case_studies/real_world/04_dns_caching.md)

## Pattern drill
_From Week 4 (drill #4)._

> Print Pascal's triangle up to row `n` (n ≤ 20), each row centered.

Name the pattern in one word and justify in one sentence. Do **not** look at the answer key until you've written your guess down.

Drill source: [`Week 4/patterns.md`](Week 4/patterns.md)

## Hard-mode challenge
### Challenge 1 (Week 4): Hollow Diamond With Border

**Spec**:
Read an odd integer `n >= 3`. Print a "hollow diamond" of total height `n`. The diamond has `*` on its border only — interior is spaces. The widest row has `n` stars positioned with the leftmost and rightmost being `*` and everything between being a space (or just one `*` for n = 1 / first row). Use only nested loops over rows and columns. No string multiplication operators.

**Constraints**:
- Input size: `n` odd, `3 <= n <= 99`
- Time: O(n^2)
- Memory: O(1) extra

**Test inputs**:
| Input | Expected output |
|

Full spec: [`Week 4/challenges.md`](Week 4/challenges.md)

---

Subscribe via RSS: point your reader at `https://raw.githubusercontent.com/anonymousAAK/my-DSA-journey/main/feed.xml`. See [`docs/NEWSLETTER.md`](docs/NEWSLETTER.md) for details.
