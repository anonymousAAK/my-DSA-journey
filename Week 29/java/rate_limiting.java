/*
 * WEEK 29 - JAVA ADVANCED TOPICS
 * Topic: Rate Limiting -- Token Bucket, Leaky Bucket, Sliding Window
 * File: rate_limiting.java
 *
 * CONCEPT:
 *     Rate limiters cap how often an action may occur. Three common designs:
 *       1. TOKEN BUCKET: a bucket of `capacity` tokens refilled at `rate`
 *          tokens/sec; each request consumes one. Allows bursts up to
 *          capacity; enforces average rate `rate`.
 *       2. LEAKY BUCKET: a fixed-size queue that drains at constant rate.
 *          Smooths bursts to a constant outflow.
 *       3. SLIDING WINDOW LOG: store request timestamps; allow if count in
 *          the last T seconds < limit.
 *
 * KEY POINTS:
 *     - Token bucket is the de-facto API gateway algorithm (Stripe, AWS,
 *       nginx limit_req).
 *     - Leaky bucket is great for shaping traffic to a downstream that
 *       tolerates only constant rate.
 *     - Sliding window log gives an exact answer but uses O(requests) space.
 *
 * ALGORITHM / APPROACH:
 *     TOKEN:    on each call, add rate * elapsed tokens (capped at capacity).
 *               if tokens >= 1: tokens -= 1; allow. else reject.
 *     LEAKY:    drain queue by rate * elapsed; if room: enqueue + allow.
 *     SLIDING:  pop timestamps older than now-T; if size < limit allow,
 *               else reject; append timestamp.
 *
 * DRY RUN / EXAMPLE:
 *     TokenBucket(capacity=5, rate=2 tok/sec). 5 back-to-back calls -> all
 *     allowed. Immediate 6th -> rejected. Wait 0.5s -> ~1 token refilled,
 *     next call allowed.
 *
 * COMPLEXITY:
 *     Token / Leaky: O(1) per request. Space O(1).
 *     Sliding log:   O(1) amortised per op; Space O(limit).
 */

// snake_case filename is fine; class RateLimiting is package-private.

import java.util.ArrayDeque;
import java.util.Deque;

class RateLimiting {

    static class TokenBucket {
        final int cap;
        final double rate;
        double tokens;
        long last;

        TokenBucket(int cap, double ratePerSec) {
            this.cap = cap;
            this.rate = ratePerSec;
            this.tokens = cap;
            this.last = System.nanoTime();
        }

        synchronized boolean allow() {
            long now = System.nanoTime();
            tokens = Math.min(cap, tokens + (now - last) / 1e9 * rate);
            last = now;
            if (tokens >= 1.0) {
                tokens -= 1.0;
                return true;
            }
            return false;
        }
    }

    static class LeakyBucket {
        final int cap;
        final double rate;
        double water;
        long last;

        LeakyBucket(int cap, double leakRatePerSec) {
            this.cap = cap;
            this.rate = leakRatePerSec;
            this.water = 0.0;
            this.last = System.nanoTime();
        }

        synchronized boolean allow() {
            long now = System.nanoTime();
            water = Math.max(0.0, water - (now - last) / 1e9 * rate);
            last = now;
            if (water < cap) {
                water += 1.0;
                return true;
            }
            return false;
        }
    }

    static class SlidingWindowLog {
        final int max;
        final long windowNanos;
        final Deque<Long> log = new ArrayDeque<>();

        SlidingWindowLog(int maxRequests, double windowSeconds) {
            this.max = maxRequests;
            this.windowNanos = (long)(windowSeconds * 1_000_000_000L);
        }

        synchronized boolean allow() {
            long now = System.nanoTime();
            while (!log.isEmpty() && log.peekFirst() <= now - windowNanos) log.pollFirst();
            if (log.size() < max) {
                log.offerLast(now);
                return true;
            }
            return false;
        }
    }

    public static void main(String[] args) throws InterruptedException {
        TokenBucket tb = new TokenBucket(5, 2.0);
        for (int i = 1; i <= 7; i++)
            System.out.println("  TokenBucket req " + i + ": " + (tb.allow() ? "ALLOWED" : "REJECTED"));

        System.out.println();
        LeakyBucket lb = new LeakyBucket(3, 5.0);
        for (int i = 1; i <= 6; i++)
            System.out.println("  LeakyBucket req " + i + ": " + (lb.allow() ? "ALLOWED" : "REJECTED"));

        System.out.println();
        SlidingWindowLog sw = new SlidingWindowLog(3, 0.05);
        for (int i = 1; i <= 5; i++)
            System.out.println("  SlidingWindow req " + i + ": " + (sw.allow() ? "ALLOWED" : "REJECTED"));
    }
}

/*
 * NOTES
 * -----
 * Differences from the Python implementation in rate_limiting.py:
 *   - Java uses System.nanoTime() instead of time.monotonic(). We convert
 *     to seconds with /1e9 inside the formula.
 *   - allow() methods are `synchronized` to make the limiters thread-safe;
 *     Python's GIL provides a coarser equivalent.
 *   - ArrayDeque<Long> replaces collections.deque for the sliding-window
 *     log; pollFirst is O(1) just like popleft.
 *   - The companion system_design.java has only the token bucket; we add
 *     leaky bucket and sliding window for parity with the Python split.
 */
