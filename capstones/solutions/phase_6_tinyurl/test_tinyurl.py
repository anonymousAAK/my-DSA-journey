"""Tests for tinyurl.py. Run: python test_tinyurl.py"""
from __future__ import annotations

import sys

from tinyurl import (
    ConsistentHashRing,
    TinyURL,
    TokenBucket,
    decode_base62,
    encode_base62,
)


def test_base62_roundtrip() -> None:
    for n in [0, 1, 61, 62, 123, 999, 12345, 10**6, 10**12]:
        s = encode_base62(n)
        assert decode_base62(s) == n, f"{n} -> {s} -> {decode_base62(s)}"
    # Codes are short for the typical id range (a billion ids ~ 6 chars)
    assert len(encode_base62(10**9)) <= 6


def test_ring_basic() -> None:
    ring = ConsistentHashRing(virtual_nodes=16)
    for n in ["a", "b", "c"]:
        ring.add_node(n)
    # Every key should map to *some* live node.
    sample = [f"k{i}" for i in range(1000)]
    assert all(ring.get(k) in {"a", "b", "c"} for k in sample)


def test_ring_rebalance_property() -> None:
    """Adding a node should move only ~1/N of keys, not the whole world."""
    ring = ConsistentHashRing(virtual_nodes=128)
    for n in ["a", "b", "c"]:
        ring.add_node(n)
    keys = [f"key-{i}" for i in range(2000)]
    before = {k: ring.get(k) for k in keys}
    ring.add_node("d")
    after = {k: ring.get(k) for k in keys}
    moved = sum(1 for k in keys if before[k] != after[k])
    # Theoretical: ~1/4 = 25%. With 128 vnodes, in practice between 15% and 35%.
    frac = moved / len(keys)
    assert 0.10 < frac < 0.45, f"unexpected rebalance fraction {frac:.2%}"
    # Crucially, moved keys all go to the new node (consistent hash invariant).
    for k in keys:
        if before[k] != after[k]:
            assert after[k] == "d", f"{k}: moved to {after[k]} instead of d"


def test_ring_remove() -> None:
    ring = ConsistentHashRing(virtual_nodes=64)
    for n in ["a", "b", "c"]:
        ring.add_node(n)
    keys = [f"k{i}" for i in range(500)]
    ring.remove_node("b")
    for k in keys:
        owner = ring.get(k)
        assert owner in {"a", "c"}, f"{k} -> {owner}"


def test_shorten_resolve() -> None:
    svc = TinyURL(rate_capacity=10_000, rate_per_sec=10_000)
    codes = []
    urls = [f"https://example.com/page/{i}" for i in range(50)]
    for u in urls:
        codes.append(svc.shorten(u))
    # Codes are unique
    assert len(set(codes)) == len(codes)
    # Codes are decodable to monotonically increasing ids
    ids = [decode_base62(c) for c in codes]
    assert ids == sorted(ids)
    # Resolve returns the original URL
    for c, u in zip(codes, urls):
        assert svc.resolve(c) == u


def test_remove_shard_keeps_data_accessible() -> None:
    svc = TinyURL(nodes=["s1", "s2", "s3", "s4"],
                  rate_capacity=10_000, rate_per_sec=10_000)
    urls = [f"https://example.com/{i}" for i in range(40)]
    codes = [svc.shorten(u) for u in urls]
    # Remove a shard. Its data is re-homed.
    svc.remove_shard("s2")
    for c, u in zip(codes, urls):
        assert svc.resolve(c) == u, f"{c} lost after removing s2"


def test_rate_limiter_rejects_burst() -> None:
    rl = TokenBucket(capacity=5, rate=0)  # no refill
    allowed = sum(1 for _ in range(20) if rl.allow("1.1.1.1"))
    assert allowed == 5, f"expected 5 allowed, got {allowed}"
    # A different IP gets its own bucket
    assert rl.allow("2.2.2.2") is True


def test_rate_limiter_refill() -> None:
    rl = TokenBucket(capacity=2, rate=10)  # refills 10 tokens/sec
    ip = "3.3.3.3"
    # Burn through capacity
    assert rl.allow(ip, now=100.0) is True
    assert rl.allow(ip, now=100.0) is True
    assert rl.allow(ip, now=100.0) is False
    # After 0.2s we should have ~2 tokens back (capped at capacity)
    assert rl.allow(ip, now=100.5) is True


def test_shorten_rate_limited() -> None:
    svc = TinyURL(rate_capacity=3, rate_per_sec=0)
    for _ in range(3):
        svc.shorten("https://example.com", ip="hot")
    try:
        svc.shorten("https://example.com", ip="hot")
        raise AssertionError("expected PermissionError")
    except PermissionError:
        pass


def main() -> int:
    test_base62_roundtrip()
    test_ring_basic()
    test_ring_rebalance_property()
    test_ring_remove()
    test_shorten_resolve()
    test_remove_shard_keeps_data_accessible()
    test_rate_limiter_rejects_burst()
    test_rate_limiter_refill()
    test_shorten_rate_limited()
    print("tinyurl: all tests passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
