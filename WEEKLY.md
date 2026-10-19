# Weekly Digest — 2026-10-19 (ISO 2026-W43)

One case study, one pattern drill, one challenge. Rotated weekly. Read these in any order; the goal is one bite-sized prompt per week to keep recognition warm even when you can't sit down for a full session.

## Case study
**Caching Strategies in DNS Resolvers**

Every time you type a URL, your machine needs to translate the domain name (`github.com`) into an IP address. The authoritative source of that mapping is a DNS server somewhere in the world — possibly multiple hops away. If every page load required a fresh DNS lookup, the internet would feel like the 1990s again. Resolvers cache aggressively. But DNS records are sometimes wrong, sometimes change, and operators *need* changes to propagate within bounded time — so the cache can't be eternal.

Read it in full: [`case_studies/real_world/04_dns_caching.md`](case_studies/real_world/04_dns_caching.md)

## Pattern drill
_From Week 24 (drill #4)._

> Given n ≤ 10^4 jobs each with weight `w_i` and value `v_i` and a knapsack capacity 10^9, maximize value subject to capacity. Distractor flavor.

Name the pattern in one word and justify in one sentence. Do **not** look at the answer key until you've written your guess down.

Drill source: [`Week 24/patterns.md`](Week 24/patterns.md)

## Hard-mode challenge
### Challenge 4 (Week 24): Subset Sum FPTAS (Fully Polynomial-Time Approximation)

**Spec**:
Read `n`, target `T`, integers `a_1..a_n`, and accuracy parameter `ε > 0`. Output a sum `S <= T` such that `S >= (1 - ε) * OPT`, where OPT is the best achievable sum `<= T`. Implementation: maintain a list of reachable sums; after each insertion, "trim" the list so consecutive entries differ by factor `>= 1 + ε/(2n)`. Polynomial in `n` and `1/ε`.

**Constraints**:
- `1 <= n <= 100`, values up to `10^9`, `ε` in `(0, 1)`
- Time: O(n^2 / ε)
- Memory: O(n / ε)

**Test inputs**:
| Input | Expected behavior |
|

Full spec: [`Week 24/challenges.md`](Week 24/challenges.md)

---

Subscribe via RSS: point your reader at `https://raw.githubusercontent.com/anonymousAAK/my-DSA-journey/main/feed.xml`. See [`docs/NEWSLETTER.md`](docs/NEWSLETTER.md) for details.
