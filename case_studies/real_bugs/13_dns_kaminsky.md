# Bug Case Study: DNS cache poisoning (Kaminsky) — predictable IDs are a structural bug

**Project**: BIND, dnsmasq, Microsoft DNS, Cisco IOS — essentially every DNS resolver. The vulnerability was disclosed coordinated in July 2008 (CVE-2008-1447); Dan Kaminsky's USENIX talk that August. The mitigation (source-port randomization, eventually DNSSEC) shipped across the ecosystem within weeks.
**Date**: vulnerability latent since DNS's design in the 1980s; weaponized in 2008
**Severity**: security (full domain takeover; widespread)
**DSA principle**: the "data structure" of a protocol nonce must have enough entropy that an adversary can't enumerate it — Week 16 (hashing / randomness) and Week 29 (system design)

## What happened

A recursive DNS resolver asks an authoritative server "what's the A record for example.com?" The query carries a 16-bit *transaction ID* (TXID). The authoritative server's response must echo that TXID. The resolver accepts the first response with the matching TXID and caches the answer.

Two structural weaknesses combined into Kaminsky's attack:

1. **TXID was only 16 bits** (~65,000 values). Even with random generation, an attacker who can send a response per nanosecond can sweep the space in 65 μs.
2. **TXID was not always randomly generated**. Many resolvers used a per-process counter, or a poorly seeded PRNG, making the next TXID guessable from one observed query.

The attack: the attacker triggers the resolver to look up `1.example.com`, `2.example.com`, `3.example.com`, ... — each a fresh query the resolver hasn't cached. For each query, the attacker races the legitimate authoritative server by sending forged responses (one per guessed TXID) that say "the answer is 1.example.com IN A 6.6.6.6, and by the way the authority server for *all of example.com* is `evil.com`." If any forged response wins the race with a matching TXID, the resolver poisons its *entire* cache for example.com with the attacker's nameserver. Banking, email, every TLS-validated host — all pointed at the attacker's IP.

The classic mitigation: **add source-port randomization**. Recursive queries had historically gone out from a fixed UDP source port (often 53). After the patch, each query went from a random port in the ephemeral range. The attacker now had to guess 16 bits of TXID *and* ~16 bits of source port — 2³² possibilities, infeasible to brute-force on a per-query basis. (DNSSEC's signed-response model is the proper fix; source-port randomization was the band-aid that bought time.)

## The naive code

```c
struct dns_query {
    uint16_t txid;          /* 16 bits: ~65k values, easily exhausted */
    uint16_t flags;
    /* ... */
};

uint16_t next_txid(void) {
    static uint16_t counter = 0;
    return counter++;        /* perfectly predictable */
}

int send_query(const char *host) {
    int s = socket(AF_INET, SOCK_DGRAM, 0);
    /* source port: always 53 — completely predictable */
    bind(s, &sa_53, sizeof(sa_53));
    struct dns_query q = { .txid = next_txid(), .flags = 0x0100 };
    /* ... */
}
```

## The DSA insight

A "transaction ID" / "nonce" / "session token" is functionally a *key into a hash map of pending operations*. For that key to be useful as authentication-by-knowledge (only the legitimate sender knows it), it must have two properties:

1. **Large enough space** that an attacker cannot enumerate it in the available window.
2. **Unpredictable enough** that an attacker cannot guess the next one from observation.

The first is just bit-width — a "1 in 2^k" attack succeeds in expected `2^(k-1)` tries, so k must be large enough that 2^(k-1) operations exceed the attacker's per-query budget. The second is a property of the *generator*: a counter has 0 unpredictable bits; a well-seeded CSPRNG (e.g., `/dev/urandom`) has all of them.

The Week 16 view: a hash table's keys aren't supposed to be derivable from public state. The same logic applies to any token that must be unguessable — TXIDs, CSRF tokens, session cookies, OAuth state parameters, JWT `jti` claims, idempotency keys. They're all *keys into a structure*; if the keys are guessable, the structure has zero authentication value.

The Week 29 / system-design view: protocols designed in environments where adversaries didn't exist (DNS was a 1980s academic-network protocol) often have nonces that were sized for collision avoidance, not for resistance to enumeration. The same hazard exists in NTP (mode 6/7 amplification), SNMPv1 (community strings), and any pre-2000 plaintext UDP protocol. Adding entropy is sometimes a literal one-line code change with enormous security impact.

## The fix

```c
uint16_t next_txid(void) {
    uint16_t txid;
    arc4random_buf(&txid, sizeof(txid));   /* CSPRNG */
    return txid;
}

int send_query(const char *host) {
    int s = socket(AF_INET, SOCK_DGRAM, 0);
    /* let the kernel pick a random ephemeral port */
    struct sockaddr_in sa = { .sin_family = AF_INET, .sin_port = 0 };
    bind(s, (struct sockaddr *)&sa, sizeof(sa));
    /* now query carries ~32 bits of unguessable state */
}
```

For the deeper fix, **DNSSEC**: every response is signed by the authoritative zone, so the resolver can verify cryptographically that the answer came from the right server — TXID and source-port guessing become irrelevant.

## What you can learn

- "Random" is a *data-structure invariant*: a nonce / token / ID is only useful for authentication-by-knowledge if it's both wide and unpredictable. Auditing for "is this thing actually generated from CSPRNG?" catches this class of bug fast.
- Bit width and randomness are independent. A 128-bit counter is still completely predictable; a 16-bit truly-random value is still brute-forceable. You need both — width *and* entropy.
- Old protocols often have token sizes set for the threat model of their time. Reviewing protocol-level identifiers under modern adversary assumptions is a high-leverage activity.
- Source-port randomization shows that you can sometimes vastly raise an attacker's cost by combining two independently-randomized fields, even when neither is large enough on its own.

## Related curriculum
- Week 16 (Hashing & randomness — universal hashing, why per-process secrets matter)
- Week 29 (System design — protocols, capacity, threat modeling)
- `tests/cases/hash_collisions.json` — adapt to model a TXID guessing attack with varying field widths and seed quality
