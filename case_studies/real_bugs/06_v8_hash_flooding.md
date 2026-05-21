# Bug Case Study: V8 (and every other engine) DoS'd by hash flooding until SipHash arrived

**Project**: V8 / Node.js / Chrome (and concurrently CPython, Ruby, Perl, Java, .NET, Rust's old `SipHasher` debates). The class of bug was demonstrated by Klink & Wälde at 28C3 (2011) and exploited in the wild against PHP, Tomcat, Jetty, ASP.NET; V8 / Node hardened in 2012–2016.
**Date**: original disclosure December 2011; long mitigation tail through ~2017
**Severity**: security (denial of service)
**DSA principle**: hash functions must be *unpredictable to an adversary* when they key adversary-controlled data — Week 16 (hashing)

## What happened

Hash tables are O(1) amortized — *under the assumption that keys are well-distributed over the buckets*. If an attacker can force every key to hash to the same bucket, every insert becomes O(n) (collision chain walk), and N inserts become O(n²). On a server that accepts an HTTP POST with form fields, query parameters, or JSON keys, the attacker controls the keys directly: send 65,000 specially crafted keys in a single request, and the server spends *minutes* of CPU just parsing the request body before any handler runs.

The 2011 talk demonstrated this against essentially every major web stack. The targets all used some variant of DJBX33A, Murmur, or FNV — fast, non-cryptographic hash functions whose internal state was either constant or trivially recoverable. Given the function and a target bucket, an attacker could enumerate keys that all collide. A 1 MB POST body could pin a server's CPU at 100% for tens of minutes.

V8's response (and Node.js's, since it embeds V8) was the now-standard mitigation: **switch the hash table to a keyed hash function whose key is randomized per process**. SipHash-2-4 was the winner — it's fast (~1 cycle/byte), cryptographic enough that you can't cheaply find collisions without knowing the key, and the per-process key denies the attacker any way to precompute. Combined with PEP 456-style randomized seeds in Python, the same idea swept across language runtimes within ~2 years.

A subtler V8-specific footnote: the engine also has special-case representations for objects (hidden classes, `DictMode` fallback). A flood of unique keys can force a regular object out of its fast hidden-class representation into the slow dictionary representation — a *different* hash-flooding-adjacent DoS that SipHash alone doesn't fix. Mitigations include capping the number of properties before the engine just returns an error.

## The naive code

```js
// Adversary sends:  ?a=1&b=2&c=3&...   with thousands of params chosen so that
//                   hash("a") == hash("b") == hash("c") == ... mod table_size.
function parseQuery(qs) {
  const out = {};                                  // backed by a hash table
  for (const pair of qs.split("&")) {              // O(n)
    const [k, v] = pair.split("=");
    out[k] = v;                                    // O(n) per insert worst case
  }
  return out;                                      // total: O(n^2)
}
```

```c
/* the hash function inside the runtime (sketch, pre-fix) */
uint32_t string_hash(const char *s, size_t len) {
    uint32_t h = 0;
    for (size_t i = 0; i < len; i++)
        h = 31 * h + s[i];                         // deterministic, attacker can invert
    return h;
}
```

## The DSA insight

The O(1) amortized cost of a hash table is a *statistical* property, not an algebraic one. It relies on the keys being approximately uniformly distributed across the buckets. Two ways that assumption can fail:

1. **Naturally bad inputs** (e.g., user IDs that happen to share a common prefix that the hash function doesn't mix well). Mitigation: pick a hash function with good avalanche properties.
2. **Adversarial inputs** (the attacker chooses keys *to* collide). Mitigation: pick a hash function the attacker can't invert without per-table secret state.

Most cryptographic hashes (SHA-256) are overkill — they're slow because they're designed to resist preimage attacks across the whole 256-bit output. SipHash is the sweet spot: short output (64 or 128 bits), fast, but parameterized by a 128-bit key that lives in the process and is never exposed. Without the key, the attacker can't predict which bucket a string lands in, so they can't pile up collisions.

The Week 16 mental model: think of the hash function not as "a deterministic mapping" but as "a draw from a family of hash functions" — universal hashing, in the formal sense. The bucket distribution is uniform *over the choice of function*, so as long as the function is chosen secretly, any specific adversary input has uniform distribution from its perspective.

## The fix

```c
/* per-process random key, picked at startup from a cryptographic RNG */
static uint8_t siphash_key[16];

void runtime_init(void) {
    getrandom(siphash_key, sizeof(siphash_key), 0);
}

uint64_t string_hash(const char *s, size_t len) {
    return siphash24(siphash_key, (const uint8_t *)s, len);
}
```

Also: cap the number of properties or query-string entries you'll parse from a single request. Defense in depth — even with SipHash, parsing a billion keys is still expensive linearly.

## What you can learn

- Hash-table performance is an *assumption about input distribution*. If your input is adversary-controlled, you can't make that assumption — you must enforce it via key randomization.
- Don't confuse "fast hash" (Murmur, FNV, xxHash — great for non-adversarial workloads) with "keyed fast hash" (SipHash, HighwayHash — what you want when the input crosses a trust boundary).
- This bug class spans the language stack: parsers, JSON deserializers, header maps, form encoders, ORM caches. Anywhere user input becomes a hash-table key, this hazard exists.
- A "good amortized bound" is a contract between you and your inputs. If the inputs can violate the contract, the bound silently becomes worst-case quadratic.

## Related curriculum
- Week 16 (Hashing)
- Week 29 (System design — adversarial input, capacity planning)
- `tests/cases/hash_collisions.json` — synthesize a collision-heavy input set and measure the slowdown against a SipHash-keyed table
