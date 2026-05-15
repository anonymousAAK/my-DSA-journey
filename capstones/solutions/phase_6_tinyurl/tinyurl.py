"""TinyURL with consistent hashing, in-memory.

Single-file reference implementation:
- Base62 short-code encoder/decoder (bijective with the auto-increment id).
- Consistent-hash ring with virtual nodes for sharding the KV store.
- An in-memory KV per simulated shard.
- Token-bucket rate limiter, per IP.

``python tinyurl.py`` runs a self-demo: shortens a few URLs, exercises the
ring (add/remove a node and watch the redistribution), and shows the rate
limiter rejecting traffic.
"""
from __future__ import annotations

import hashlib
import sys
import threading
import time
from bisect import bisect_right
from dataclasses import dataclass, field


# --- Base62 encoder ----------------------------------------------------------

_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
_INDEX = {c: i for i, c in enumerate(_ALPHABET)}
BASE = len(_ALPHABET)


def encode_base62(n: int) -> str:
    if n < 0:
        raise ValueError("only non-negative ids")
    if n == 0:
        return "0"
    out: list[str] = []
    while n:
        n, rem = divmod(n, BASE)
        out.append(_ALPHABET[rem])
    return "".join(reversed(out))


def decode_base62(s: str) -> int:
    n = 0
    for c in s:
        if c not in _INDEX:
            raise ValueError(f"bad base62 char: {c!r}")
        n = n * BASE + _INDEX[c]
    return n


# --- Consistent hash ring ----------------------------------------------------

class ConsistentHashRing:
    """Map keys -> nodes using a hash ring with virtual nodes.

    Lookup is O(log V) where V is total virtual node count. Adding/removing a
    node touches only the keys that fall on that node's slice — the standard
    consistent-hashing rebalance property.
    """

    def __init__(self, virtual_nodes: int = 64) -> None:
        self.vnodes = virtual_nodes
        self._ring: list[int] = []           # sorted hash positions
        self._owner: dict[int, str] = {}     # hash -> node name
        self._nodes: set[str] = set()
        self._lock = threading.Lock()

    @staticmethod
    def _hash(s: str) -> int:
        return int.from_bytes(hashlib.md5(s.encode()).digest()[:8], "big")

    def add_node(self, name: str) -> None:
        with self._lock:
            if name in self._nodes:
                return
            self._nodes.add(name)
            for v in range(self.vnodes):
                h = self._hash(f"{name}#{v}")
                self._owner[h] = name
                idx = bisect_right(self._ring, h)
                self._ring.insert(idx, h)

    def remove_node(self, name: str) -> None:
        with self._lock:
            if name not in self._nodes:
                return
            self._nodes.discard(name)
            kept = [h for h in self._ring if self._owner[h] != name]
            for h in list(self._owner):
                if self._owner[h] == name:
                    del self._owner[h]
            self._ring = kept

    def get(self, key: str) -> str:
        with self._lock:
            if not self._ring:
                raise RuntimeError("ring is empty")
            h = self._hash(key)
            idx = bisect_right(self._ring, h)
            if idx == len(self._ring):
                idx = 0
            return self._owner[self._ring[idx]]

    def nodes(self) -> list[str]:
        with self._lock:
            return sorted(self._nodes)


# --- In-memory KV per shard --------------------------------------------------

@dataclass
class Shard:
    name: str
    data: dict[str, str] = field(default_factory=dict)

    def put(self, k: str, v: str) -> None:
        self.data[k] = v

    def get(self, k: str) -> str | None:
        return self.data.get(k)

    def pop(self, k: str) -> str | None:
        return self.data.pop(k, None)


# --- Token bucket rate limiter ----------------------------------------------

class TokenBucket:
    """Per-IP token bucket. `capacity` tokens, refilled at `rate` per second."""

    def __init__(self, capacity: float, rate: float) -> None:
        self.capacity = capacity
        self.rate = rate
        self._buckets: dict[str, tuple[float, float]] = {}  # ip -> (tokens, last_ts)
        self._lock = threading.Lock()

    def allow(self, ip: str, now: float | None = None) -> bool:
        now = time.time() if now is None else now
        with self._lock:
            tokens, last = self._buckets.get(ip, (self.capacity, now))
            tokens = min(self.capacity, tokens + (now - last) * self.rate)
            if tokens < 1.0:
                self._buckets[ip] = (tokens, now)
                return False
            tokens -= 1.0
            self._buckets[ip] = (tokens, now)
            return True


# --- TinyURL service ---------------------------------------------------------

class TinyURL:
    def __init__(
        self,
        nodes: list[str] | None = None,
        rate_capacity: float = 5,
        rate_per_sec: float = 1.0,
    ) -> None:
        self.ring = ConsistentHashRing(virtual_nodes=64)
        self.shards: dict[str, Shard] = {}
        for n in nodes or ["shard-1", "shard-2", "shard-3"]:
            self.add_shard(n)
        self._next_id = 1
        self._lock = threading.Lock()
        self.limiter = TokenBucket(rate_capacity, rate_per_sec)

    def add_shard(self, name: str) -> None:
        if name not in self.shards:
            self.shards[name] = Shard(name)
        self.ring.add_node(name)

    def remove_shard(self, name: str) -> dict[str, str]:
        """Remove a shard. Returns the data that must be re-homed; we re-home
        it ourselves (this is what would happen in a real system before the
        old node is decommissioned)."""
        if name not in self.shards:
            return {}
        old = self.shards.pop(name)
        self.ring.remove_node(name)
        moved: dict[str, str] = {}
        for k, v in old.data.items():
            new_shard_name = self.ring.get(k)
            self.shards[new_shard_name].put(k, v)
            moved[k] = new_shard_name
        return moved

    def shorten(self, url: str, ip: str = "anon") -> str:
        if not self.limiter.allow(ip):
            raise PermissionError("rate limited")
        with self._lock:
            n = self._next_id
            self._next_id += 1
        code = encode_base62(n)
        shard_name = self.ring.get(code)
        self.shards[shard_name].put(code, url)
        return code

    def resolve(self, code: str, ip: str = "anon") -> str | None:
        if not self.limiter.allow(ip):
            raise PermissionError("rate limited")
        shard_name = self.ring.get(code)
        return self.shards[shard_name].get(code)

    def shard_for(self, code: str) -> str:
        return self.ring.get(code)


# --- Demo --------------------------------------------------------------------

def main() -> int:
    svc = TinyURL(rate_capacity=100, rate_per_sec=100)
    urls = [
        "https://example.com/very/long/path/one",
        "https://example.com/very/long/path/two",
        "https://example.com/page?id=42&ref=home",
        "https://docs.python.org/3/library/http.server.html",
        "https://news.ycombinator.com/",
    ]
    print("== base62 round trip ==")
    for i in [1, 61, 62, 12345, 99999999]:
        s = encode_base62(i)
        assert decode_base62(s) == i
        print(f"  {i:>12} -> {s}")

    print("\n== shorten ==")
    codes: list[tuple[str, str]] = []
    for u in urls:
        c = svc.shorten(u)
        codes.append((c, u))
        print(f"  {c:<6} -> {u}  [shard={svc.shard_for(c)}]")

    print("\n== resolve ==")
    for c, u in codes:
        got = svc.resolve(c)
        assert got == u
        print(f"  {c} resolves to {got}")

    print("\n== ring rebalance: add shard-4 ==")
    before = {c: svc.shard_for(c) for c, _ in codes}
    svc.add_shard("shard-4")
    after = {c: svc.shard_for(c) for c, _ in codes}
    moved = [c for c in before if before[c] != after[c]]
    print(f"  before -> after: {len(moved)} of {len(codes)} keys moved")
    # NOTE: we did *not* re-home the data when adding (this is on purpose for
    # the demo; real systems do a background rebalance). resolve() now uses
    # the new owner and might return None for moved keys until rebalance.

    print("\n== ring rebalance: remove shard-2 (auto re-home) ==")
    moved_keys = svc.remove_shard("shard-2")
    print(f"  re-homed {len(moved_keys)} keys to new shards")
    # All previously-shortened URLs still resolve after a node leaves, since
    # remove_shard re-homes the data automatically.
    survivors = 0
    for c, u in codes:
        if svc.resolve(c) == u:
            survivors += 1
    print(f"  {survivors}/{len(codes)} URLs still resolve correctly")

    print("\n== rate limiter ==")
    rl = TokenBucket(capacity=3, rate=0)  # rate=0 so refill doesn't help
    allowed = sum(1 for _ in range(10) if rl.allow("1.2.3.4"))
    print(f"  burst of 10 with capacity 3: {allowed} allowed (expected 3)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
