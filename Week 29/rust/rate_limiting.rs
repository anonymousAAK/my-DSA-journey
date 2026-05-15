// WEEK 29 - RUST ADVANCED TOPICS
// Topic: Rate Limiting - Token Bucket, Leaky Bucket, Sliding Window Log
// File: rate_limiting.rs
//
// CONCEPT:
//   Cap how often an action can occur:
//     - Token Bucket: capacity tokens refilled at rate; consume per req.
//     - Leaky Bucket: queue draining at constant rate; overflow rejected.
//     - Sliding Window Log: timestamps in last T; allow if count < limit.
//
// KEY POINTS:
//   - Token bucket allows bursts up to capacity; enforces average rate.
//   - Leaky bucket smooths bursts into a steady stream.
//   - Sliding log gives exact answers but O(limit) memory.
//
// ALGORITHM / APPROACH:
//   TOKEN:  refill = elapsed * rate; cap at capacity; consume if >= 1.
//   LEAKY:  water -= elapsed * rate (floored 0); if < cap admit + water+=1.
//   SLIDING: pop ts older than now-T; allow if len < limit; push now.
//
// RUST-SPECIFIC NOTES:
//   - std::time::Instant for monotonic clock.
//   - VecDeque<Instant> for sliding log (O(1) front pop).
//
// DRY RUN / EXAMPLE:
//   TokenBucket(5, 2.0) -> 5 reqs allowed back-to-back, 6th rejected;
//   after 500 ms one more allowed (one token refilled).
//
// COMPLEXITY:
//   Token/Leaky O(1) per op; Sliding O(window). Space O(window).

use std::collections::VecDeque;
use std::thread;
use std::time::{Duration, Instant};

pub struct TokenBucket { cap: f64, rate: f64, tokens: f64, last: Instant }
impl TokenBucket {
    pub fn new(cap: u32, rate_per_sec: f64) -> Self {
        Self { cap: cap as f64, rate: rate_per_sec, tokens: cap as f64, last: Instant::now() }
    }
    pub fn allow(&mut self) -> bool {
        let now = Instant::now();
        let elapsed = now.duration_since(self.last).as_secs_f64();
        self.tokens = (self.tokens + elapsed * self.rate).min(self.cap);
        self.last = now;
        if self.tokens >= 1.0 { self.tokens -= 1.0; true } else { false }
    }
}

pub struct LeakyBucket { cap: f64, rate: f64, water: f64, last: Instant }
impl LeakyBucket {
    pub fn new(cap: u32, rate_per_sec: f64) -> Self {
        Self { cap: cap as f64, rate: rate_per_sec, water: 0.0, last: Instant::now() }
    }
    pub fn allow(&mut self) -> bool {
        let now = Instant::now();
        let elapsed = now.duration_since(self.last).as_secs_f64();
        self.water = (self.water - elapsed * self.rate).max(0.0);
        self.last = now;
        if self.water < self.cap { self.water += 1.0; true } else { false }
    }
}

pub struct SlidingWindowLog { max: usize, window: Duration, log: VecDeque<Instant> }
impl SlidingWindowLog {
    pub fn new(max: usize, window_seconds: f64) -> Self {
        Self { max, window: Duration::from_secs_f64(window_seconds), log: VecDeque::new() }
    }
    pub fn allow(&mut self) -> bool {
        let now = Instant::now();
        while let Some(&front) = self.log.front() {
            if now.duration_since(front) > self.window { self.log.pop_front(); }
            else { break; }
        }
        if self.log.len() < self.max { self.log.push_back(now); true } else { false }
    }
}

fn main() {
    let mut tb = TokenBucket::new(5, 2.0);
    for i in 1..=7 {
        println!("  TokenBucket req {}: {}", i,
                 if tb.allow() { "ALLOWED" } else { "REJECTED" });
    }
    println!();
    let mut lb = LeakyBucket::new(3, 5.0);
    for i in 1..=5 {
        println!("  LeakyBucket req {}: {}", i,
                 if lb.allow() { "ALLOWED" } else { "REJECTED" });
    }
    println!();
    let mut sw = SlidingWindowLog::new(3, 0.05);
    for i in 1..=5 {
        println!("  SlidingWindow req {}: {}", i,
                 if sw.allow() { "ALLOWED" } else { "REJECTED" });
        // No sleep — burst test
    }
    // Demonstrate expiry
    thread::sleep(Duration::from_millis(60));
    println!("After 60 ms wait:");
    println!("  SlidingWindow req 6: {}", if sw.allow() { "ALLOWED" } else { "REJECTED" });
}

// NOTES
// -----
// Differences from Java:
//   * Adds leaky-bucket and sliding-window log for spec completeness.
//   * std::time::Instant + duration_since for monotonic clocks.
//   * VecDeque<Instant> is the idiomatic sliding-window buffer.
