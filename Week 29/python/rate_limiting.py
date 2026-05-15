"""
WEEK 29 - PYTHON ADVANCED TOPICS
Topic: Rate Limiting - Token Bucket, Leaky Bucket, Sliding Window
File: rate_limiting.py

CONCEPT:
    Rate limiters cap how often an action may occur. Three common designs:
      1. TOKEN BUCKET: a bucket of `capacity` tokens refilled at `rate`
         tokens/sec; each request consumes one. Allows bursts up to
         capacity; enforces average rate `rate`.
      2. LEAKY BUCKET: a fixed-size queue that drains at constant rate.
         Smooths bursts to a constant outflow.
      3. SLIDING WINDOW LOG: store request timestamps; allow if count in
         the last T seconds < limit.

KEY POINTS:
    - Token bucket is the de-facto API gateway algorithm (Stripe, AWS,
      nginx limit_req).
    - Leaky bucket is great for shaping traffic to a downstream that
      tolerates only constant rate.
    - Sliding window log gives an exact answer but uses O(requests) space.

ALGORITHM / APPROACH:
    TOKEN:    on each call, add rate * elapsed tokens (capped at capacity).
              if tokens >= 1: tokens -= 1; allow. else reject.
    LEAKY:    drain queue by rate * elapsed; if room: enqueue + allow.
    SLIDING:  pop timestamps older than now-T; len(queue) < limit -> allow,
              else reject. Append timestamp.

PYTHON-SPECIFIC NOTES:
    - Use time.monotonic() for monotonic clocks.
    - `collections.deque` for the sliding-window log (O(1) popleft).

DRY RUN / EXAMPLE:
    TokenBucket(capacity=5, rate=2 tok/sec). 5 calls back-to-back -> all
    allowed; immediately the 6th -> rejected. Wait 0.5s -> ~1 token
    refilled, next call allowed.

COMPLEXITY:
    Token / Leaky: O(1) per request. Space O(1).
    Sliding log:   O(log limit) amortised; Space O(limit).
"""

from __future__ import annotations

import time
from collections import deque
from typing import Deque


class TokenBucket:
    def __init__(self, capacity: int, refill_rate_per_sec: float) -> None:
        self.cap = capacity
        self.rate = refill_rate_per_sec
        self.tokens = float(capacity)
        self.last = time.monotonic()

    def allow(self) -> bool:
        now = time.monotonic()
        self.tokens = min(self.cap, self.tokens + (now - self.last) * self.rate)
        self.last = now
        if self.tokens >= 1.0:
            self.tokens -= 1.0
            return True
        return False


class LeakyBucket:
    """Fixed-capacity queue draining at constant rate."""

    def __init__(self, capacity: int, leak_rate_per_sec: float) -> None:
        self.cap = capacity
        self.rate = leak_rate_per_sec
        self.water = 0.0
        self.last = time.monotonic()

    def allow(self) -> bool:
        now = time.monotonic()
        self.water = max(0.0, self.water - (now - self.last) * self.rate)
        self.last = now
        if self.water < self.cap:
            self.water += 1.0
            return True
        return False


class SlidingWindowLog:
    def __init__(self, max_requests: int, window_seconds: float) -> None:
        self.max = max_requests
        self.window = window_seconds
        self.log: Deque[float] = deque()

    def allow(self) -> bool:
        now = time.monotonic()
        while self.log and self.log[0] <= now - self.window:
            self.log.popleft()
        if len(self.log) < self.max:
            self.log.append(now)
            return True
        return False


def _demo() -> None:
    tb = TokenBucket(5, 2.0)
    for i in range(1, 8):
        print(f"  TokenBucket req {i}: {'ALLOWED' if tb.allow() else 'REJECTED'}")

    print()
    lb = LeakyBucket(3, 5.0)
    for i in range(1, 6):
        print(f"  LeakyBucket req {i}: {'ALLOWED' if lb.allow() else 'REJECTED'}")

    print()
    sw = SlidingWindowLog(max_requests=3, window_seconds=0.05)
    for i in range(1, 6):
        print(f"  SlidingWindow req {i}: {'ALLOWED' if sw.allow() else 'REJECTED'}")


if __name__ == "__main__":
    _demo()


# NOTES
# -----
# Differences from Java:
#   * Java's system_design.java only shows the token bucket. We add leaky
#     bucket and sliding-window log for spec completeness.
#   * collections.deque is the natural sliding-window log data structure.
#   * time.monotonic() avoids issues with wall-clock changes during runs.
