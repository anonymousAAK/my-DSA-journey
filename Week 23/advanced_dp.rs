//! # Week 23: Advanced Dynamic Programming
//!
//! This module covers advanced DP techniques including bitmask DP, optimal
//! binary search, matrix chain multiplication, and digit DP.
//!
//! ## Complexity Summary
//! | Problem                     | Time            | Space         |
//! |----------------------------|-----------------|---------------|
//! | TSP (Bitmask DP)           | O(n^2 * 2^n)   | O(n * 2^n)    |
//! | LIS (O(n log n))           | O(n log n)      | O(n)          |
//! | Matrix Chain Multiplication| O(n^3)          | O(n^2)        |
//! | Digit DP                   | O(D * 2 * 10)   | O(D * 2)      |
//!
//! Where D = number of digits in N.

use std::cmp::min;

// =============================================================================
// TSP Bitmask — Traveling Salesman Problem
// =============================================================================

/// Solves the Traveling Salesman Problem using bitmask DP.
///
/// # Problem
/// Given a complete weighted graph with `n` cities, find the minimum cost
/// to visit every city exactly once and return to the starting city.
///
/// # State
/// `dp[mask][i]` = minimum cost to reach city `i` having visited exactly
/// the set of cities represented by `mask`, starting from city 0.
///
/// - `mask` is a bitmask: bit `j` is set if city `j` has been visited.
/// - Transition: `dp[mask | (1 << j)][j] = min(dp[mask][i] + dist[i][j])`
///   for each unvisited city `j` adjacent to `i`.
///
/// # Complexity
/// - Time: O(n^2 * 2^n) — for each of 2^n masks and n cities, try n transitions
/// - Space: O(n * 2^n) — the DP table
///
/// # Practical Limit
/// Feasible for n <= ~20 due to exponential state space.
fn tsp_bitmask(dist: &[Vec<i64>]) -> i64 {
    let n = dist.len();
    let full_mask = (1 << n) - 1;
    let inf = i64::MAX / 2;

    // dp[mask][i] = min cost to reach city i with visited set = mask
    let mut dp = vec![vec![inf; n]; 1 << n];
    dp[1][0] = 0; // Start at city 0, only city 0 visited (mask = 0b...001)

    for mask in 1..(1 << n) {
        for u in 0..n {
            if dp[mask][u] >= inf {
                continue;
            }
            // Bit u must be set in mask (we are at city u)
            if mask & (1 << u) == 0 {
                continue;
            }

            // Try visiting each unvisited city
            for v in 0..n {
                if mask & (1 << v) != 0 {
                    continue; // Already visited
                }
                let new_mask = mask | (1 << v);
                let new_cost = dp[mask][u] + dist[u][v];
                if new_cost < dp[new_mask][v] {
                    dp[new_mask][v] = new_cost;
                }
            }
        }
    }

    // Find minimum cost to complete the tour (return to city 0)
    let mut result = inf;
    for u in 0..n {
        if dp[full_mask][u] < inf && dist[u][0] < inf {
            result = min(result, dp[full_mask][u] + dist[u][0]);
        }
    }

    result
}

// =============================================================================
// LIS Optimal — O(n log n) Longest Increasing Subsequence
// =============================================================================

/// Finds the length of the longest strictly increasing subsequence using
/// the patience sorting algorithm.
///
/// # Algorithm
/// Maintain a vector `tails` where `tails[i]` = smallest tail element of
/// any increasing subsequence of length `i + 1` found so far.
///
/// `tails` is always sorted, enabling binary search via `partition_point`.
///
/// For each element `num`:
/// - Binary search for the leftmost position where `tails[pos] >= num`.
/// - If `pos == tails.len()`, `num` extends the longest subsequence.
/// - Otherwise, `tails[pos] = num` (replace to keep tail minimal).
///
/// # Why O(n log n)?
/// - n elements processed, each with an O(log n) binary search.
///
/// # Rust Note
/// `partition_point` is Rust's built-in binary search that finds the first
/// index where the predicate returns `false`. It's equivalent to C++'s
/// `lower_bound`.
///
/// # Complexity
/// - Time: O(n log n)
/// - Space: O(n)
fn lis_optimal(nums: &[i32]) -> usize {
    if nums.is_empty() {
        return 0;
    }

    let mut tails: Vec<i32> = Vec::new();

    for &num in nums {
        let pos = tails.partition_point(|&x| x < num);
        if pos == tails.len() {
            tails.push(num);
        } else {
            tails[pos] = num;
        }
    }

    tails.len()
}

// =============================================================================
// Matrix Chain Multiplication
// =============================================================================

/// Finds the minimum number of scalar multiplications needed to multiply
/// a chain of matrices.
///
/// # Problem
/// Given matrices A1 (p0 x p1), A2 (p1 x p2), ..., An (p(n-1) x pn),
/// find the optimal parenthesization that minimizes total multiplications.
///
/// # Recurrence
/// `dp[i][j]` = minimum multiplications to compute matrices i through j.
/// ```text
/// dp[i][j] = min over k in [i, j-1] of:
///     dp[i][k] + dp[k+1][j] + dims[i-1] * dims[k] * dims[j]
/// ```
///
/// # Complexity
/// - Time: O(n^3) — three nested loops
/// - Space: O(n^2)
///
/// # Parameters
/// - `dims`: array of dimensions where matrix i has dimensions
///   `dims[i-1] x dims[i]`. Length is n+1 for n matrices.
fn matrix_chain_multiplication(dims: &[i64]) -> i64 {
    let n = dims.len() - 1; // Number of matrices
    if n <= 1 {
        return 0;
    }

    // dp[i][j] = min cost to multiply matrices i..j (1-indexed)
    let mut dp = vec![vec![0i64; n + 1]; n + 1];

    // l = chain length (2 to n)
    for l in 2..=n {
        for i in 1..=n - l + 1 {
            let j = i + l - 1;
            dp[i][j] = i64::MAX;

            // Try all possible split points
            for k in i..j {
                let cost = dp[i][k] + dp[k + 1][j] + dims[i - 1] * dims[k] * dims[j];
                if cost < dp[i][j] {
                    dp[i][j] = cost;
                }
            }
        }
    }

    dp[1][n]
}

// =============================================================================
// Digit DP — Count numbers in [1, N] that don't contain digit 4
// =============================================================================

/// Counts how many numbers in the range [1, N] do NOT contain the digit 4.
///
/// # Digit DP Framework
/// Process the number digit by digit (most significant to least significant).
/// At each position, maintain:
/// - `tight`: whether we're still bounded by the original number N
///   (if true, the next digit can be at most `digits[pos]`; if false,
///   any digit 0-9 is allowed)
///
/// # State
/// `dp[pos][tight]` = count of valid numbers formed by digits at positions
/// `pos..end`, given the `tight` constraint.
///
/// # Complexity
/// - Time: O(D * 2 * 10) where D = number of digits in N
/// - Space: O(D * 2) for memoization
///
/// # Counting Trick
/// We compute count(0..=N) and subtract 1 to exclude 0, giving count(1..=N).
fn digit_dp_no_four(n: u64) -> u64 {
    if n == 0 {
        return 0;
    }

    let digits: Vec<u32> = n.to_string()
        .chars()
        .map(|c| c.to_digit(10).unwrap())
        .collect();

    let len = digits.len();

    // Memoization: memo[pos][tight]
    // -1 means not computed yet
    let mut memo = vec![vec![-1i64; 2]; len];

    fn solve(
        pos: usize,
        tight: bool,
        digits: &[u32],
        memo: &mut Vec<Vec<i64>>,
    ) -> i64 {
        if pos == digits.len() {
            return 1; // Successfully formed a valid number
        }

        let tight_idx = if tight { 1 } else { 0 };
        if memo[pos][tight_idx] != -1 {
            return memo[pos][tight_idx];
        }

        let upper = if tight { digits[pos] } else { 9 };
        let mut count = 0i64;

        for d in 0..=upper {
            if d == 4 {
                continue; // Skip digit 4
            }
            count += solve(
                pos + 1,
                tight && d == upper,
                digits,
                memo,
            );
        }

        memo[pos][tight_idx] = count;
        count
    }

    let total = solve(0, true, &digits, &mut memo);
    // Subtract 1 to exclude the number 0 (which has no digit 4 but isn't in [1, N])
    (total - 1) as u64
}

// =============================================================================
// Main — Test cases
// =============================================================================

fn main() {
    println!("=== Week 23: Advanced DP ===\n");

    // --- TSP Bitmask ---
    println!("--- TSP Bitmask ---");
    let dist = vec![
        vec![0, 10, 15, 20],
        vec![10, 0, 35, 25],
        vec![15, 35, 0, 30],
        vec![20, 25, 30, 0],
    ];
    let result = tsp_bitmask(&dist);
    println!("TSP minimum tour cost: {} (expected 80)", result);
    assert_eq!(result, 80); // 0->1->3->2->0: 10+25+30+15=80

    // Smaller test
    let dist2 = vec![
        vec![0, 1, 2],
        vec![1, 0, 3],
        vec![2, 3, 0],
    ];
    let result2 = tsp_bitmask(&dist2);
    println!("TSP (3 cities): {} (expected 6)", result2);
    assert_eq!(result2, 6); // 0->1->2->0: 1+3+2=6
    println!("PASS\n");

    // --- LIS Optimal ---
    println!("--- LIS Optimal (O(n log n)) ---");
    let lis = lis_optimal(&[10, 9, 2, 5, 3, 7, 101, 18]);
    println!("LIS([10,9,2,5,3,7,101,18]) = {} (expected 4)", lis);
    assert_eq!(lis, 4);

    let lis2 = lis_optimal(&[0, 1, 0, 3, 2, 3]);
    assert_eq!(lis2, 4);

    let lis3 = lis_optimal(&[7, 7, 7, 7]);
    assert_eq!(lis3, 1);

    let lis4 = lis_optimal(&[1, 2, 3, 4, 5]);
    assert_eq!(lis4, 5); // Already sorted

    let lis5 = lis_optimal(&[5, 4, 3, 2, 1]);
    assert_eq!(lis5, 1); // Reverse sorted
    println!("PASS\n");

    // --- Matrix Chain Multiplication ---
    println!("--- Matrix Chain Multiplication ---");
    // Matrices: A1 (10x30), A2 (30x5), A3 (5x60)
    let dims = vec![10, 30, 5, 60];
    let result = matrix_chain_multiplication(&dims);
    println!("MCM([10,30,5,60]) = {} (expected 4500)", result);
    assert_eq!(result, 4500); // (A1*A2)*A3: 10*30*5 + 10*5*60 = 1500+3000

    // 4 matrices: A1 (40x20), A2 (20x30), A3 (30x10), A4 (10x30)
    let dims2 = vec![40, 20, 30, 10, 30];
    let result2 = matrix_chain_multiplication(&dims2);
    println!("MCM([40,20,30,10,30]) = {} (expected 26000)", result2);
    assert_eq!(result2, 26000);
    println!("PASS\n");

    // --- Digit DP ---
    println!("--- Digit DP (no digit 4) ---");
    let count = digit_dp_no_four(10);
    println!("Numbers in [1,10] without digit 4: {} (expected 9)", count);
    // 1,2,3,5,6,7,8,9,10 — only 4 is excluded
    assert_eq!(count, 9);

    let count2 = digit_dp_no_four(100);
    println!("Numbers in [1,100] without digit 4: {} (expected 81)", count2);
    // 1-digit: 8, 2-digit (10-99): 8*9=72, plus 100 -> 81
    assert_eq!(count2, 81);

    let count3 = digit_dp_no_four(4);
    println!("Numbers in [1,4] without digit 4: {} (expected 3)", count3);
    assert_eq!(count3, 3); // 1, 2, 3

    let count4 = digit_dp_no_four(44);
    println!("Numbers in [1,44] without digit 4: {}", count4);
    // 1-digit: 8 (1,2,3,5,6,7,8,9)
    // 2-digit 10-39: first digit {1,2,3} (3 choices), second {0-9}\{4} (9) = 27
    // 40-44: first digit 4 -> skip all
    // Total = 8 + 27 = 35
    assert_eq!(count4, 35);
    println!("PASS\n");

    println!("All Week 23 tests passed!");
}
