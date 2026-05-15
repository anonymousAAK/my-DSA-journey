# Bloom Filters for Safe Browsing

## The problem

Google's Safe Browsing service maintains a list of millions of URLs known to host malware or phishing. Chrome checks every URL you navigate to against this list and warns you before loading dangerous pages. The catch: shipping the entire list to every Chrome client is unreasonable — it's gigabytes. Querying Google for every URL you visit would leak your entire browsing history. So the local check has to be **on-device**, *fast*, and **compact**.

## Why the obvious approach didn't work

Option 1: ship the full list as a hash set. Storage is the killer: ~5M phishing/malware URLs × ~50 bytes/URL = 250 MB for storage. Adding the index pushes it higher. Updating it daily is a huge bandwidth hit on mobile.

Option 2: query Google with each URL. Privacy disaster — Google sees every page you visit.

Option 3: ship only hashes of URLs (say, SHA-1 prefixes). Smaller — say, 8 bytes per entry × 5M entries = 40 MB. Still big, and lookup is linear or needs an index.

The leap: do we need an *exact* answer? Almost all URLs you visit are not malicious. We need a structure that says **"definitely safe"** quickly (very common case) and **"might be unsafe, ask the server"** for the rare uncertain case. False positives are okay (a few extra server roundtrips). False negatives are catastrophic (missed malware).

A **Bloom filter** has exactly that asymmetry.

## What they actually use

A Bloom filter is a fixed-size bit array with k hash functions. To insert an element: hash it k ways, set those k bits to 1. To query: hash it k ways, return "maybe present" iff all k bits are 1.

- "All bits 1" can be a true present, OR a coincidence (false positive).
- "Some bit is 0" guarantees not present (no false negatives).

The probability of false positive depends on bit array size, number of items, and number of hash functions. For 5M URLs at 1% FP rate, you need ~9.6 bits per item × 5M = 6 MB. Quite a bit better than 250 MB.

In Chrome:
1. The bit array (a few MB) is shipped to the client and stored locally.
2. On a URL navigation, Chrome hashes the URL k times, checks the local Bloom filter.
3. If "definitely not on the list" → load page, no further work.
4. If "maybe on the list" → make a small query to Safe Browsing, sending only a *prefix* of the URL's hash (privacy: the server learns a hash prefix, not the URL). The server returns the full list of matching full hashes; Chrome compares locally. If a full hash matches, show the warning.

Google's actual Safe Browsing protocol uses a slightly fancier construct called a **Cuckoo filter** in newer versions, which improves on Bloom filters in two ways: it supports deletion, and the false positive rate vs. space tradeoff is a bit better at large sizes. But the basic idea is the same.

## The tradeoff

The textbook tradeoff: **false positives in exchange for space**. A 1% FP rate at 5M items means 100 unnecessary server roundtrips per 10,000 page loads — a tiny cost in practice. Storage drops by ~40x compared to a hash set. The privacy win is on top: Chrome doesn't have to send your full URL to Google for every page load.

Two big secondary tradeoffs:

1. **No deletion** in a standard Bloom filter. Setting a bit can't be undone (you might be unsetting a bit needed by some other element). To remove URLs (e.g., a site got cleaned up), you'd have to rebuild the filter from scratch. In practice Safe Browsing does this periodically — daily diff updates.

2. **Tuning k and m matters.** Too few hash functions → high FP. Too many → bits are saturated quickly, raising FP. The optimal k = (m/n) × ln(2) where m=bits, n=items. Get this wrong and your filter performs much worse than advertised.

3. **Counting Bloom filters** add a counter (small integer) per slot so you can decrement on deletion. They use more space per slot. Newer designs (Cuckoo filters, XOR filters) match or beat Bloom on most metrics but are slightly more complex to implement.

## You can implement a toy version of this using Week 13

- Week 13 (hashing) — implement multiple hash functions (e.g., MurmurHash with different seeds, or simply `(h1 + i * h2) mod m`).
- Implement a Bloom filter class in ~50 lines: `__init__(m, k)`, `add(item)`, `__contains__(item)`. Use a `bitarray` for the bit array.
- Insert 100,000 random strings, then test 100,000 *unrelated* strings — count the false positives, verify the rate matches the theoretical formula.

A weekend project: build a small malware-URL checker. Download a public list of bad URLs (e.g., from PhishTank). Insert all into your Bloom filter. Then run the filter against a stream of benign URLs and the bad list. Verify: zero false negatives on the bad URLs, ~1% false positives on the benign stream. Implement the "ask the server" fallback as a hash-set lookup in the original list. You'll see the entire Safe Browsing pattern in 100 lines of code.

Stretch: implement a Cuckoo filter and compare on the same workload. You'll get slightly better false-positive rates and the ability to delete items — at the cost of more complex code.

The deep lesson: **probabilistic data structures are a different toolbox.** They trade exactness for size, and that tradeoff is invaluable in three categories: cardinality estimation (HyperLogLog), set membership (Bloom/Cuckoo), and frequency estimation (Count-Min Sketch). Every distributed database and analytics system uses them. Week 13 hash tables are the gateway drug — once you understand how hashes spread, probabilistic structures stop feeling like black magic.
