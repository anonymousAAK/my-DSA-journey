# Bug Case Study: A CDN Bloom filter served wrong content because m and k were sized to the wrong N

**Project**: This is an approximate reconstruction of a class of bug seen across CDN edge caches, ad-tech bid filters, and pre-2010 Bitcoin-era SPV clients. Cloudflare and Akamai have both published postmortems whose root cause boils down to "the Bloom filter was sized for last year's working set."
**Date**: ongoing pattern; concretely visible in tuning guides for `bloomd`, `RedisBloom`, and embedded filters in Cassandra / Parquet
**Severity**: correctness *or* performance (depending on what the filter guards)
**DSA principle**: a Bloom filter's false-positive rate is a function of (m, k, n) — Week 16 (hashing / probabilistic structures)

## What happened

A CDN edge node serves billions of requests a day from a hot cache and falls back to a slower origin lookup on miss. To keep origin traffic low, the edge maintains a Bloom filter of "URLs known to be in the origin's bad-bot blocklist." A request whose URL is in the filter is rejected at the edge; everything else passes through.

The filter was provisioned for n = 10 million URLs at a target false-positive rate (FPR) of 1%. The classic formulas give m ≈ 95 million bits (~12 MB) and k ≈ 7 hash functions. So far so good. Six months later, the blocklist had grown to n = 50 million URLs — but nobody had grown the filter. The actual FPR at n = 50M with m = 95M, k = 7 is *not* 5x worse; it's substantially worse than that, because the FPR formula `(1 - e^(-kn/m))^k` is non-linear in n. Plug in the numbers and you get an FPR around 30%.

The visible failure: ~30% of legitimate users hit the "blocked" path, sometimes intermittently (because different requests for the same URL got the same false positive, but small URL perturbations gave a clean lookup). Ops thought it was a routing flap. The DSA insight came late.

A second variant of the same class: a CDN that used a Bloom filter to skip origin checks for *content already on the edge*. Here a false positive meant "we wrongly believed we have it" → serve nothing or serve a 404. As the cache grew past the sized n, the FPR climbed, and the rate of bogus 404s climbed with it.

## The naive code

```python
class BloomFilter:
    def __init__(self, m_bits, k_hashes):
        self.bits = bitarray(m_bits)
        self.k = k_hashes

    def add(self, key):
        for i in range(self.k):
            self.bits[hash((i, key)) % len(self.bits)] = 1

    def __contains__(self, key):
        return all(self.bits[hash((i, key)) % len(self.bits)] for i in range(self.k))

# Provisioned once for n=10M, fpr=1%:
bf = BloomFilter(m_bits=95_000_000, k_hashes=7)

# 6 months later, n is 50M. No alarm. fpr is now ~30%.
```

## The DSA insight

A Bloom filter's false-positive rate depends on **three** parameters, not one:

- `m` — bit-array size,
- `k` — number of hash functions,
- `n` — number of items inserted so far.

The textbook formula (assuming independent uniform hashes):

```
fpr(m, k, n) = (1 - e^(-k n / m))^k
```

For a fixed (m, k), the FPR grows *very* nonlinearly in n. Doubling n doesn't double the FPR; near the saturation point it can square or worse. The optimal k for a given (m, n) is `k* = (m / n) * ln 2`, which gives FPR ≈ `(0.6185)^(m/n)`. The bits-per-element ratio `m/n` is what actually controls FPR; if you let n grow without growing m, you fall off the cliff.

The fix is not to "tune" a static filter — it's to **bound n**, or to **switch to a structure that handles growing n gracefully**:

1. **Scalable Bloom Filter** (Almeida et al., 2007): a sequence of progressively larger filters with shrinking target FPRs, so the *combined* FPR stays bounded as n grows. Insert into the newest filter; query checks all of them.
2. **Cuckoo filter** (Fan et al., 2014): supports deletion (Bloom doesn't) and has slightly better cache behavior, but still requires sizing for n.
3. **Stable Bloom filter** (Deng & Rafiei, 2006): trades a tiny false-negative rate for stable behavior under unbounded streams — good for "membership in the last K items," not absolute membership.

The deeper lesson: a probabilistic data structure has a **contract** with you (here: "FPR ≤ ε for n ≤ N"). When you exceed N, the contract is void, and the failure mode is silent (the filter still answers; the answers are just wrong more often). Monitoring n vs. provisioned N is therefore not optional — it's part of using the structure correctly.

## The fix

```python
class ScalableBloomFilter:
    """As inserts pile up, allocate progressively larger sub-filters whose
    target FPRs shrink geometrically so the union FPR stays bounded."""
    def __init__(self, initial_n, target_fpr=0.01, growth=4, tightening=0.5):
        self.target = target_fpr
        self.growth = growth
        self.tightening = tightening
        self.filters = [self._mk(initial_n, target_fpr)]

    def _mk(self, n, fpr):
        m = int(-n * math.log(fpr) / (math.log(2) ** 2))
        k = max(1, int((m / n) * math.log(2)))
        return BloomFilter(m, k)

    def add(self, key):
        cur = self.filters[-1]
        if cur.fill_ratio() > 0.5:                  # filling up
            n = cur.capacity * self.growth
            fpr = self.target * (self.tightening ** len(self.filters))
            self.filters.append(self._mk(n, fpr))
            cur = self.filters[-1]
        cur.add(key)

    def __contains__(self, key):
        return any(key in f for f in self.filters)
```

Also: emit a metric `bloom_filter_load_ratio = n / N_provisioned` and alert above ~0.7. The vast majority of "the filter is broken" tickets are answered by that one graph.

## What you can learn

- A Bloom filter's three knobs (m, k, n) are not independent; n is the one that grows on its own and breaks the others.
- The relationship `m / n ≈ 1.44 × log2(1/fpr)` is the one number to remember: 10 bits per element ≈ 1% FPR; 14 bits per element ≈ 0.1% FPR.
- Probabilistic data structures have *silent* failure modes — wrong answers, not crashes. Always monitor "am I still inside the contract I sized for?"
- "Scalable" variants exist for a reason; pick them when n is unknown or unbounded.

## Related curriculum
- Week 16 (Hashing — Bloom filters and other probabilistic structures)
- Week 24 / capstone 5 (Sketches: Count-Min, HyperLogLog, Bloom)
- `tests/cases/bloom_filter.json` — instrument the canonical fixture to plot empirical FPR vs. n, and verify it matches the analytical formula
