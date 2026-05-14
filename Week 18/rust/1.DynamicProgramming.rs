/*
 * WEEK 18 - RUST DSA
 * Topic: Dynamic Programming Fundamentals
 * File: 1.DynamicProgramming.rs
 *
 * CONCEPT:
 *     DP solves a problem by decomposing it into overlapping subproblems and
 *     storing each sub-answer. Two preconditions:
 *         1. Optimal substructure.
 *         2. Overlapping subproblems.
 *     Two implementation styles:
 *         TOP-DOWN  : recursion + memo (Vec or HashMap as cache).
 *         BOTTOM-UP : tabulation from base case upward (often faster, often
 *                     space-optimisable).
 *
 * KEY POINTS:
 *     - Identify state, recurrence, base case, evaluation order.
 *     - For 0/1 knapsack on a 1-D rolling array, iterate capacity in REVERSE
 *       so an item isn't reused.
 *     - Use i32::MAX or a "target+1" sentinel for "impossible" — Rust will
 *       panic on overflow in debug builds, so add carefully.
 *
 * ALGORITHM / APPROACH:
 *     Same five canonical problems as the Java reference:
 *         1. 0/1 Knapsack             (2-D and space-optimised 1-D)
 *         2. Longest Common Subseq.   (2-D)
 *         3. Coin change (min coins)  (1-D)
 *         4. Subset sum               (1-D boolean)
 *         5. Climbing stairs          (Fibonacci, O(1) state)
 *
 * RUST-SPECIFIC NOTES:
 *     - `vec![vec![0; W+1]; n+1]` is the canonical 2-D DP table.
 *     - For a top-down memo, the borrow checker rules out `RefCell<HashMap>`
 *       free-form recursion; idiomatic Rust prefers an explicit memo passed
 *       as `&mut Vec<...>` or simply iterative tabulation.
 *     - `usize` everywhere for indices; cast i32 with `as usize` carefully.
 *     - String slices use bytes() for ASCII inputs (LCS over ASCII strings).
 *
 * DRY RUN:
 *     Knapsack weights=[2,3,4,5], values=[3,4,5,6], W=5
 *         Final dp[4][5] = 7.
 *
 *     LCS("ABCBDAB","BDCABA") -> 4.
 *
 *     coin_change([1,2,5], 11) -> 3 (5+5+1).
 *
 *     subset_sum([3,1,5,9,12], 7) -> false; target=8 -> true.
 *
 * COMPLEXITY:
 *     knapsack          O(n*W) time, O(n*W) space (O(W) optimised)
 *     lcs               O(m*n) time, O(m*n) space
 *     coin_change       O(target * |coins|) time, O(target) space
 *     subset_sum        O(n * target) time, O(target) space
 *     climb_stairs      O(n) time, O(1) space
 */

use std::collections::HashMap;

// ---------- 0/1 KNAPSACK ----------
pub fn knapsack(weights: &[i32], values: &[i32], capacity: i32) -> i32 {
    let n = weights.len();
    let w_cap = capacity as usize;
    let mut dp = vec![vec![0i32; w_cap + 1]; n + 1];
    for i in 1..=n {
        let wi = weights[i - 1] as usize;
        let vi = values[i - 1];
        for w in 0..=w_cap {
            dp[i][w] = dp[i - 1][w];
            if wi <= w {
                let take = dp[i - 1][w - wi] + vi;
                if take > dp[i][w] { dp[i][w] = take; }
            }
        }
    }
    dp[n][w_cap]
}

pub fn knapsack_optimised(weights: &[i32], values: &[i32], capacity: i32) -> i32 {
    let w_cap = capacity as usize;
    let mut dp = vec![0i32; w_cap + 1];
    for i in 0..weights.len() {
        let wi = weights[i] as usize;
        let vi = values[i];
        for w in (wi..=w_cap).rev() {                         // REVERSE!
            let take = dp[w - wi] + vi;
            if take > dp[w] { dp[w] = take; }
        }
    }
    dp[w_cap]
}

// Top-down memo using HashMap (state = (i, capacity))
pub fn knapsack_memo(weights: &[i32], values: &[i32], capacity: i32) -> i32 {
    fn go(weights: &[i32], values: &[i32], i: usize, cap: i32,
          memo: &mut HashMap<(usize, i32), i32>) -> i32 {
        if i == weights.len() || cap == 0 { return 0; }
        if let Some(&v) = memo.get(&(i, cap)) { return v; }
        let skip = go(weights, values, i + 1, cap, memo);
        let take = if weights[i] <= cap {
            go(weights, values, i + 1, cap - weights[i], memo) + values[i]
        } else { 0 };
        let best = skip.max(take);
        memo.insert((i, cap), best);
        best
    }
    let mut memo = HashMap::new();
    go(weights, values, 0, capacity, &mut memo)
}

// ---------- LONGEST COMMON SUBSEQUENCE ----------
pub fn lcs(s1: &str, s2: &str) -> i32 {
    let a = s1.as_bytes();
    let b = s2.as_bytes();
    let m = a.len();
    let n = b.len();
    let mut dp = vec![vec![0i32; n + 1]; m + 1];
    for i in 1..=m {
        for j in 1..=n {
            dp[i][j] = if a[i - 1] == b[j - 1] {
                dp[i - 1][j - 1] + 1
            } else {
                dp[i - 1][j].max(dp[i][j - 1])
            };
        }
    }
    dp[m][n]
}

// ---------- COIN CHANGE (min coins) ----------
pub fn coin_change(coins: &[i32], target: i32) -> i32 {
    let t = target as usize;
    let inf = target + 1;                                     // sentinel
    let mut dp = vec![inf; t + 1];
    dp[0] = 0;
    for a in 1..=t {
        for &c in coins {
            let cu = c as usize;
            if c <= a as i32 && dp[a - cu] + 1 < dp[a] {
                dp[a] = dp[a - cu] + 1;
            }
        }
    }
    if dp[t] > target { -1 } else { dp[t] }
}

// ---------- SUBSET SUM ----------
pub fn subset_sum(nums: &[i32], target: i32) -> bool {
    let t = target as usize;
    let mut dp = vec![false; t + 1];
    dp[0] = true;
    for &x in nums {
        if x < 0 || x as usize > t { continue; }
        let xu = x as usize;
        for cap in (xu..=t).rev() {
            if dp[cap - xu] { dp[cap] = true; }
        }
    }
    dp[t]
}

// ---------- CLIMBING STAIRS ----------
pub fn climb_stairs(n: u32) -> u64 {
    if n <= 2 { return n as u64; }
    let (mut prev2, mut prev1) = (1u64, 2u64);
    for _ in 3..=n {
        let curr = prev1 + prev2;
        prev2 = prev1;
        prev1 = curr;
    }
    prev1
}

fn main() {
    println!("=== 0/1 Knapsack ===");
    let weights = [2, 3, 4, 5];
    let values  = [3, 4, 5, 6];
    println!("W=5  bottom-up: {}", knapsack(&weights, &values, 5));            // 7
    println!("W=10 bottom-up: {}", knapsack(&weights, &values, 10));           // 13
    println!("W=10 optimised: {}", knapsack_optimised(&weights, &values, 10));
    println!("W=10 memoised : {}", knapsack_memo(&weights, &values, 10));

    println!("\n=== LCS ===");
    println!("LCS('ABCBDAB','BDCABA') = {}", lcs("ABCBDAB", "BDCABA"));        // 4
    println!("LCS('AGGTAB','GXTXAYB') = {}", lcs("AGGTAB", "GXTXAYB"));        // 4

    println!("\n=== Coin Change ===");
    println!("coins=[1,2,5], amount=11: {}", coin_change(&[1, 2, 5], 11));     // 3
    println!("coins=[2],     amount=3 : {}", coin_change(&[2], 3));            // -1
    println!("coins=[1],     amount=0 : {}", coin_change(&[1], 0));            // 0

    println!("\n=== Subset Sum ===");
    println!("[3,1,5,9,12] target=8: {}", subset_sum(&[3, 1, 5, 9, 12], 8));   // true
    println!("[3,1,5,9,12] target=7: {}", subset_sum(&[3, 1, 5, 9, 12], 7));   // false

    println!("\n=== Climbing Stairs ===");
    for i in 1..=10u32 {
        println!("climb_stairs({:2}) = {}", i, climb_stairs(i));
    }
}

/*
 * NOTES (Rust vs Java):
 *   - `vec![vec![0; W+1]; n+1]` is the safe way to build a 2-D Vec; the
 *     macro clones the inner row each time (no aliasing pitfall).
 *   - i32 overflow panics in debug builds — picking a sentinel like
 *     `target + 1` is safer than i32::MAX when we later add 1.
 *   - Rust's top-down memo needs an explicit HashMap or &mut Vec; there's
 *     no @cache decorator. Iterative tabulation is usually preferred.
 *   - LCS over &str must convert to bytes (s.as_bytes()) for cheap indexing
 *     on ASCII; for full Unicode use s.chars().collect::<Vec<_>>().
 *   - climb_stairs uses u64 to avoid overflow for large n (Fibonacci grows fast).
 */
