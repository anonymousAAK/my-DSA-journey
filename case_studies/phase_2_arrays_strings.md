# Phase 2: Arrays & Strings — Longest Stable Trading Streak

## The Word Problem

> Risk team needs a new chart on the dashboard. For each ticker, they want to know "the longest stretch of consecutive trading days where the price never dropped more than 10% from the running max within that stretch." They tried describing it three different ways and I'm still confused. Basically — find the longest window where, if you took the highest price seen so far in the window, no price in the window is below 90% of it. Some of these tickers have 30 years of daily data (~7,500 points) and we want to compute this for ~12,000 tickers nightly. Right now Greg has a Jupyter notebook doing it in pandas and it takes 40 minutes per ticker. Help.

## Step 1: Restate the problem precisely

- **Input**: array `prices[0..n-1]` of positive floats.
- **Output**: the length (and ideally the indices) of the longest subarray `prices[l..r]` such that for every `i` in `[l, r]`, `prices[i] >= 0.9 * max(prices[l..i])`.
- The constraint is **window-local**: the "running max" resets when the window starts. A 20% drawdown from a much earlier peak is fine if that peak isn't in our window.
- **Note**: the running max is measured from the *left edge of the window up to position i*, not over the whole window. Worth re-reading the PM's message to be sure. (Asking the PM: "is the cap the window's max-so-far, or the window's overall max?" — they'll say "same thing in my head" and we have to gently explain it isn't.) For this case study we'll go with **max from `l` up to `i` inclusive**, which is the more natural sliding-window framing.

## Step 2: Identify constraints

- Input size: n up to ~7,500 per ticker. 12,000 tickers nightly = 90 million total data points.
- Time budget: an O(n²) algorithm at 7,500 points is ~56M ops per ticker; times 12,000 tickers = 6.7e11 ops. That's the 40-minute notebook. Need O(n) or O(n log n).
- Memory: trivial per ticker; we can stream.
- Edge cases:
  - All prices equal (whole array is valid).
  - Strictly increasing (whole array is valid — max only grows, nothing violates).
  - Strictly decreasing (window is whatever fits within 10% drop).
  - Single price spike: `[100, 100, 100, 200, 100]` — the 100 after the 200 violates (100 < 0.9*200 = 180).
  - Zero or negative prices (shouldn't happen, but defend).
  - Two prices: `[100, 89]` — violates. `[100, 90]` — okay (exactly at boundary, decide ≥ vs >).
  - Empty array.

## Step 3: Brute force first

For each pair `(l, r)`, scan the subarray, track running max, check the condition. O(n³). For n=7,500 that's 4.2e11 — completely infeasible.

Smarter brute force: fix `l`, walk `r` forward, maintaining running max and checking each new price. As soon as we violate, record the length, increment `l`, **start over**. O(n²). For n=7,500 that's 56M — that's Greg's notebook. Still too slow at scale.

## Step 4: Identify wasted work

Two huge sources of repeated work:

1. **When `l` advances by 1, we re-scan from scratch.** But almost the entire window we just verified is still valid! We threw away the information that prices `[l+1..r-1]` had a known running max.

2. **The running max is only ever broken by a new high.** If the window has been growing and the max hasn't changed, we don't need to re-check old prices — they were fine against a lower (or equal) max before, and they're still fine against the same max now.

The key monotonicity insight: as `r` increases by one, only one thing can change about the constraint — `prices[r]` is a new max, OR it's not.

- If `prices[r]` is not a new max, we only need to check `prices[r] >= 0.9 * current_max`.
- If `prices[r]` IS a new max, **older prices in the window might now violate**. Specifically, any price below `0.9 * prices[r]` now becomes invalid.

This is the structure that screams "monotonic deque" or "two pointers with a max-tracking structure."

## Step 5: Optimize

**Sliding window with a monotonic deque tracking the max.**

Maintain `l, r` and a deque of indices whose prices form a non-increasing sequence (so the front of the deque is always the index of the current window's max).

For each new `r`:
1. Pop from the back of the deque while `prices[back] <= prices[r]` (they can never be the max again — `prices[r]` dominates them within any window containing both).
2. Push `r` onto the deque.
3. Now `prices[deque.front()]` is the max of the window `[l..r]`.
4. While `prices[r] < 0.9 * prices[deque.front()]` (new price violates) OR while `prices[deque.front()] * 0.9 > min_price_in_window` (some older price violates the new max): **advance `l`**.

Wait — step 4 is where this gets tricky. The violation can come from either side: a new low against the old max, or a new high making an old price violate. We need both checks.

Cleaner reformulation: **for each `r`, find the smallest `l` such that the window `[l..r]` is valid**. The constraint is: for every `i in [l..r]`, `prices[i] >= 0.9 * max(prices[l..i])`. Equivalently, no price in `[l..r]` is below 0.9 times the running max from `l` up to that price.

The clean observation: a violation at position `i` happens when `prices[i] < 0.9 * max(prices[l..i])`. The relevant max is the prefix max from `l`. So if we've found a violation at index `i`, **we must move `l` past whatever caused the running max to be that high** — specifically, past the index of the violating max.

Algorithm:
- Maintain a deque of "candidate max" indices in non-increasing order of price (front is current max from `l` onward).
- For each `r`:
  - Remove from back while `prices[back] < prices[r]`.
  - Push `r`.
  - The running max from `l` to `r` is `prices[deque.front()]`.
  - If `prices[r] < 0.9 * prices[deque.front()]`, we have a violation *at position r*. Advance `l` to `argmax + 1` (where `argmax` is the front index), then drop the front of the deque.
- Update best length = `r - l + 1` whenever the window is valid.

Each index is pushed and popped at most once from the deque → **O(n) total**.

For 7,500 points: 7,500 ops. For 12,000 tickers: 90M ops. At ~100ns per op that's ~9 seconds total. From 40 minutes per ticker to seconds total.

## Step 6: Implementation gotchas

- **Floating point**: `0.9 * max` should probably use `>=` not `>` to avoid boundary flakiness. Document the convention.
- **Ties**: when `prices[back] == prices[r]`, pop or keep? Either works correctness-wise; popping keeps the deque shorter.
- **Off-by-one on window length**: `r - l + 1`, not `r - l`.
- **Empty deque**: shouldn't happen if you push before reading the front, but defend.
- **What if a violation can't be resolved by advancing `l` once?** Make sure the loop continues advancing until valid. Use `while`, not `if`.
- **Stocks split/dividend adjustments**: out of scope, but flag to the PM. Garbage in, garbage out.

## Step 7: Verification

- Trivial: `[100]` → 1.
- Monotone: `[1, 2, 3, 4, 5]` → 5.
- Hard violation: `[100, 89]` → 1 (both alone are valid windows of length 1).
- The example: `[100, 100, 100, 200, 100]`. Window `[0..3]` has max 200, but price 100 at index 0/1/2 violates (100 < 180). So the long valid windows are `[0..2]` (length 3), `[3..3]` (length 1), or `[3..4]`? Price 100 at index 4 against max 200 → violates. So `[3..4]` invalid. Answer: length 3.
- Stress: generate random walks, compare O(n) result against the O(n²) brute force on n=200 inputs, 1000 trials.

## Step 8: Reflection

What made this hard: the **window-local** running max. If the constraint had been "no price below 90% of the *global* max" it would have been trivial. The fact that the max resets with the window is what forces the deque.

Pattern: **sliding window with monotonic deque**. The deque is what makes "max over a sliding window" O(1) amortized. Other places this exact pattern shows up:

- "Largest rectangle in histogram" (Week 7 — uses a monotonic stack, sibling structure).
- "Stock span" problems (Week 7).
- Network packet rate limiting over a moving window (we'll see this in Phase 6).
- Audio/video signal processing — running max for envelope detection.

Curriculum tie-in: Week 7 (sliding window) and Week 8 (monotonic stack/deque) combined. The hardest part is *recognizing* the window-local-max structure in the PM's prose. That recognition skill is what separates "I know algorithms" from "I can solve real problems."
