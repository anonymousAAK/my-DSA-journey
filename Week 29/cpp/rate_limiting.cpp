/*
 * WEEK 29 - C++ ADVANCED TOPICS
 * Topic: Rate Limiting - Token Bucket, Leaky Bucket, Sliding Window
 * File: rate_limiting.cpp
 *
 * CONCEPT:
 *   Rate limiters cap how often an action may occur:
 *     - Token Bucket: capacity tokens refilling at rate; consume per req.
 *     - Leaky Bucket: queue draining at constant rate; overflow rejected.
 *     - Sliding Window Log: timestamps in last T; allow if count < limit.
 *
 * KEY POINTS:
 *   - Token bucket allows bursts up to capacity; enforces average rate.
 *   - Leaky bucket smooths bursts into a steady stream.
 *   - Sliding log gives exact answers but O(limit) memory.
 *
 * ALGORITHM / APPROACH:
 *   TOKEN:  refill = elapsed * rate; cap at capacity; consume if >=1.
 *   LEAKY:  drain by elapsed * rate; admit if water < cap; water += 1.
 *   SLIDING: pop timestamps older than now-T; allow if size < max; push now.
 *
 * C++-SPECIFIC NOTES:
 *   - std::chrono::steady_clock for monotonic clock.
 *   - std::deque<TimePoint> for the sliding window log.
 *
 * DRY RUN / EXAMPLE:
 *   TokenBucket(5, 2 tok/s) -> first 5 requests allowed, 6th rejected;
 *   500 ms later one more allowed.
 *
 * COMPLEXITY:
 *   Token/Leaky O(1); Sliding O(window). Space O(window).
 */

#include <iostream>
#include <chrono>
#include <deque>
#include <thread>

using namespace std;
using namespace std::chrono;

class TokenBucket {
    int cap;
    double rate;
    double tokens;
    steady_clock::time_point last;
public:
    TokenBucket(int c, double r) : cap(c), rate(r), tokens(c), last(steady_clock::now()) {}
    bool allow() {
        auto now = steady_clock::now();
        double elapsed = duration<double>(now - last).count();
        tokens = min((double)cap, tokens + elapsed * rate);
        last = now;
        if (tokens >= 1.0) { tokens -= 1.0; return true; }
        return false;
    }
};

class LeakyBucket {
    int cap;
    double rate;
    double water;
    steady_clock::time_point last;
public:
    LeakyBucket(int c, double r) : cap(c), rate(r), water(0), last(steady_clock::now()) {}
    bool allow() {
        auto now = steady_clock::now();
        double elapsed = duration<double>(now - last).count();
        water = max(0.0, water - elapsed * rate);
        last = now;
        if (water < cap) { water += 1.0; return true; }
        return false;
    }
};

class SlidingWindowLog {
    int maxReq;
    duration<double> window;
    deque<steady_clock::time_point> log;
public:
    SlidingWindowLog(int n, double seconds) : maxReq(n), window(seconds) {}
    bool allow() {
        auto now = steady_clock::now();
        while (!log.empty() && log.front() <= now - window) log.pop_front();
        if ((int)log.size() < maxReq) { log.push_back(now); return true; }
        return false;
    }
};

int main() {
    TokenBucket tb(5, 2.0);
    for (int i = 1; i <= 7; ++i)
        cout << "  TokenBucket req " << i << ": " << (tb.allow() ? "ALLOWED" : "REJECTED") << "\n";

    cout << "\n";
    LeakyBucket lb(3, 5.0);
    for (int i = 1; i <= 5; ++i)
        cout << "  LeakyBucket req " << i << ": " << (lb.allow() ? "ALLOWED" : "REJECTED") << "\n";

    cout << "\n";
    SlidingWindowLog sw(3, 0.05);
    for (int i = 1; i <= 5; ++i)
        cout << "  SlidingWindow req " << i << ": " << (sw.allow() ? "ALLOWED" : "REJECTED") << "\n";
    return 0;
}

/*
 * NOTES
 * -----
 * Differences from Java:
 *   - We add leaky bucket and sliding-window log for spec completeness.
 *   - std::chrono::steady_clock for the monotonic clock.
 *   - duration<double> in seconds keeps arithmetic clean.
 */
