//! # Week 18: Dynamic Programming
//!
//! Dynamic programming (DP) solves problems by breaking them into overlapping
//! subproblems and storing results to avoid redundant computation.
//!
//! ## Two Approaches
//! - **Top-down (memoization)**: Recursive with a cache
//! - **Bottom-up (tabulation)**: Iterative, filling a table from base cases
//!
//! ## Complexity Summary
//! | Problem                     | Time         | Space     |
//! |----------------------------|--------------|-----------|
//! | Climbing Stairs            | O(n)         | O(1)      |
//! | 0/1 Knapsack              | O(n*W)       | O(n*W) / O(W) |
//! | Longest Common Subsequence | O(m*n)       | O(m*n)    |
//! | Longest Increasing Subseq  | O(n log n)   | O(n)      |
//! | Coin Change               | O(n*amount)  | O(amount) |
//! | Subset Sum                | O(n*target)  | O(target) |
//! | Edit Distance             | O(m*n)       | O(m*n)    |

use std::cmp::min;

// =============================================================================
// Climbing Stairs
// =============================================================================

/// Returns the number of distinct ways to climb `n` stairs, taking 1 or 2
/// steps at a time.
///
/// # Recurrence
/// `dp[i] = dp[i-1] + dp[i-2]` — same as Fibonacci.
///
/// # Complexity
/// - Time: O(n)
/// - Space: O(1) — only need two previous values
fn climbing_stairs(n: u32) -> u64 {
    if n <= 1 {
        return 1;
    }

    let mut prev2 = 1u64; // dp[0]
    let mut prev1 = 1u64; // dp[1]

    for _ in 2..=n {
        let current = prev1 + prev2;
        prev2 = prev1;
        prev1 = current;
    }

    prev1
}

// =============================================================================
// 0/1 Knapsack — 2D table version
// =============================================================================

/// Solves the 0/1 knapsack problem using a 2D DP table.
///
/// Given `n` items with weights and values, and a knapsack of capacity `W`,
/// find the maximum total value without exceeding the weight capacity.
/// Each item can be taken at most once.
///
/// # Recurrence
/// ```text
/// dp[i][w] = max(
///     dp[i-1][w],                          // Skip item i
///     dp[i-1][w - weights[i]] + values[i]  // Take item i (if it fits)
/// )
/// ```
///
/// # Complexity
/// - Time: O(n * W)
/// - Space: O(n * W)
fn knapsack_01(weights: &[usize], values: &[i64], capacity: usize) -> i64 {
    let n = weights.len();
    // dp[i][w] = max value using first i items with capacity w
    let mut dp = vec![vec![0i64; capacity + 1]; n + 1];

    for i in 1..=n {
        for w in 0..=capacity {
            dp[i][w] = dp[i - 1][w]; // Don't take item i
            if weights[i - 1] <= w {
                let take = dp[i - 1][w - weights[i - 1]] + values[i - 1];
                dp[i][w] = dp[i][w].max(take);
            }
        }
    }

    dp[n][capacity]
}

/// Space-optimized 0/1 knapsack using a single 1D array.
///
/// # Key Insight
/// Each row `dp[i]` only depends on `dp[i-1]`, so we can use a single row.
/// We iterate weights in REVERSE to avoid using an item twice in the same row.
///
/// # Complexity
/// - Time: O(n * W)
/// - Space: O(W)
fn knapsack_01_optimized(weights: &[usize], values: &[i64], capacity: usize) -> i64 {
    let mut dp = vec![0i64; capacity + 1];

    for i in 0..weights.len() {
        // Iterate in reverse so dp[w - weights[i]] is still from the previous row
        for w in (weights[i]..=capacity).rev() {
            dp[w] = dp[w].max(dp[w - weights[i]] + values[i]);
        }
    }

    dp[capacity]
}

// =============================================================================
// Longest Common Subsequence — With string reconstruction
// =============================================================================

/// Finds the longest common subsequence (LCS) of two strings and returns
/// both its length and the actual subsequence.
///
/// # Recurrence
/// ```text
/// If s1[i] == s2[j]:  dp[i][j] = dp[i-1][j-1] + 1
/// Else:               dp[i][j] = max(dp[i-1][j], dp[i][j-1])
/// ```
///
/// # Reconstruction
/// Trace back from `dp[m][n]`: if characters match, include it and move
/// diagonally. Otherwise, move in the direction of the larger value.
///
/// # Complexity
/// - Time: O(m * n)
/// - Space: O(m * n) for the DP table
fn longest_common_subsequence(s1: &str, s2: &str) -> (usize, String) {
    let a: Vec<char> = s1.chars().collect();
    let b: Vec<char> = s2.chars().collect();
    let m = a.len();
    let n = b.len();

    // Build DP table
    let mut dp = vec![vec![0usize; n + 1]; m + 1];

    for i in 1..=m {
        for j in 1..=n {
            if a[i - 1] == b[j - 1] {
                dp[i][j] = dp[i - 1][j - 1] + 1;
            } else {
                dp[i][j] = dp[i - 1][j].max(dp[i][j - 1]);
            }
        }
    }

    // Reconstruct the LCS by tracing back through the table
    let mut lcs = Vec::new();
    let (mut i, mut j) = (m, n);
    while i > 0 && j > 0 {
        if a[i - 1] == b[j - 1] {
            lcs.push(a[i - 1]);
            i -= 1;
            j -= 1;
        } else if dp[i - 1][j] > dp[i][j - 1] {
            i -= 1;
        } else {
            j -= 1;
        }
    }
    lcs.reverse();

    let length = dp[m][n];
    let subsequence: String = lcs.into_iter().collect();
    (length, subsequence)
}

// =============================================================================
// Longest Increasing Subsequence — O(n log n) with binary search
// =============================================================================

/// Finds the length of the longest strictly increasing subsequence.
///
/// # Algorithm (Patience Sorting)
/// Maintain a vector `tails` where `tails[i]` is the smallest possible tail
/// element of an increasing subsequence of length `i + 1`.
///
/// For each element:
/// - If it's larger than all tails, extend the longest subsequence.
/// - Otherwise, binary search for the first tail >= element and replace it.
///
/// `tails` is always sorted, enabling binary search.
///
/// # Complexity
/// - Time: O(n log n) — n elements, each with a binary search O(log n)
/// - Space: O(n)
fn longest_increasing_subsequence(nums: &[i32]) -> usize {
    if nums.is_empty() {
        return 0;
    }

    let mut tails: Vec<i32> = Vec::new();

    for &num in nums {
        // Binary search for the leftmost position where tails[pos] >= num
        let pos = tails.partition_point(|&x| x < num);

        if pos == tails.len() {
            tails.push(num); // Extend the longest subsequence
        } else {
            tails[pos] = num; // Replace to keep the tail as small as possible
        }
    }

    tails.len()
}

// =============================================================================
// Coin Change — Minimum coins to make amount
// =============================================================================

/// Returns the minimum number of coins needed to make the given amount,
/// or -1 if it's impossible.
///
/// # Recurrence
/// ```text
/// dp[a] = min over all coins c { dp[a - c] + 1 } where a - c >= 0
/// ```
///
/// # Complexity
/// - Time: O(n * amount) where n = number of coin denominations
/// - Space: O(amount)
fn coin_change(coins: &[i32], amount: i32) -> i32 {
    let amount = amount as usize;
    // dp[i] = minimum coins to make amount i; i32::MAX means impossible
    let mut dp = vec![i32::MAX; amount + 1];
    dp[0] = 0; // Base case: 0 coins to make amount 0

    for a in 1..=amount {
        for &coin in coins {
            let c = coin as usize;
            if c <= a && dp[a - c] != i32::MAX {
                dp[a] = min(dp[a], dp[a - c] + 1);
            }
        }
    }

    if dp[amount] == i32::MAX { -1 } else { dp[amount] }
}

// =============================================================================
// Subset Sum
// =============================================================================

/// Determines if any subset of `nums` sums to exactly `target`.
///
/// # Recurrence
/// `dp[s]` is true if some subset of the first i items sums to s.
/// ```text
/// dp[s] = dp[s] || dp[s - nums[i]]
/// ```
///
/// # Complexity
/// - Time: O(n * target)
/// - Space: O(target) — single boolean array
fn subset_sum(nums: &[i32], target: i32) -> bool {
    if target < 0 {
        return false;
    }
    let target = target as usize;
    let mut dp = vec![false; target + 1];
    dp[0] = true; // Empty subset sums to 0

    for &num in nums {
        let num = num as usize;
        // Iterate in reverse to avoid using the same element twice
        for s in (num..=target).rev() {
            if dp[s - num] {
                dp[s] = true;
            }
        }
    }

    dp[target]
}

// =============================================================================
// Edit Distance (Levenshtein Distance)
// =============================================================================

/// Computes the minimum number of single-character edits (insert, delete,
/// replace) to transform `word1` into `word2`.
///
/// # Recurrence
/// ```text
/// If word1[i] == word2[j]:
///     dp[i][j] = dp[i-1][j-1]         // Characters match, no edit needed
/// Else:
///     dp[i][j] = 1 + min(
///         dp[i-1][j],    // Delete from word1
///         dp[i][j-1],    // Insert into word1
///         dp[i-1][j-1]   // Replace in word1
///     )
/// ```
///
/// # Complexity
/// - Time: O(m * n)
/// - Space: O(m * n)
fn edit_distance(word1: &str, word2: &str) -> usize {
    let a: Vec<char> = word1.chars().collect();
    let b: Vec<char> = word2.chars().collect();
    let m = a.len();
    let n = b.len();

    // dp[i][j] = edit distance between a[0..i] and b[0..j]
    let mut dp = vec![vec![0usize; n + 1]; m + 1];

    // Base cases: transforming to/from empty string
    for i in 0..=m {
        dp[i][0] = i; // Delete all characters from word1
    }
    for j in 0..=n {
        dp[0][j] = j; // Insert all characters of word2
    }

    for i in 1..=m {
        for j in 1..=n {
            if a[i - 1] == b[j - 1] {
                dp[i][j] = dp[i - 1][j - 1]; // No edit needed
            } else {
                dp[i][j] = 1 + min(
                    dp[i - 1][j - 1], // Replace
                    min(dp[i - 1][j], dp[i][j - 1]), // Delete or Insert
                );
            }
        }
    }

    dp[m][n]
}

// =============================================================================
// Main — Test cases
// =============================================================================

fn main() {
    println!("=== Week 18: Dynamic Programming ===\n");

    // --- Climbing Stairs ---
    println!("--- Climbing Stairs ---");
    assert_eq!(climbing_stairs(0), 1);
    assert_eq!(climbing_stairs(1), 1);
    assert_eq!(climbing_stairs(2), 2);
    assert_eq!(climbing_stairs(5), 8);
    assert_eq!(climbing_stairs(10), 89);
    println!("climbing_stairs(5) = {}", climbing_stairs(5));
    println!("climbing_stairs(10) = {}", climbing_stairs(10));
    println!("PASS\n");

    // --- 0/1 Knapsack ---
    println!("--- 0/1 Knapsack ---");
    let weights = vec![2, 3, 4, 5];
    let values = vec![3, 4, 5, 6];
    let capacity = 5;

    let result = knapsack_01(&weights, &values, capacity);
    let result_opt = knapsack_01_optimized(&weights, &values, capacity);
    println!("Knapsack (2D): max value = {}", result);
    println!("Knapsack (1D): max value = {}", result_opt);
    assert_eq!(result, 7); // Take items with weight 2,3 → value 3+4=7
    assert_eq!(result, result_opt);
    println!("PASS\n");

    // --- Longest Common Subsequence ---
    println!("--- Longest Common Subsequence ---");
    let (len, lcs) = longest_common_subsequence("abcde", "ace");
    println!("LCS(\"abcde\", \"ace\") = \"{}\" (length {})", lcs, len);
    assert_eq!(len, 3);
    assert_eq!(lcs, "ace");

    let (len2, lcs2) = longest_common_subsequence("AGGTAB", "GXTXAYB");
    println!("LCS(\"AGGTAB\", \"GXTXAYB\") = \"{}\" (length {})", lcs2, len2);
    assert_eq!(len2, 4);
    assert_eq!(lcs2, "GTAB");
    println!("PASS\n");

    // --- Longest Increasing Subsequence ---
    println!("--- Longest Increasing Subsequence (O(n log n)) ---");
    let lis = longest_increasing_subsequence(&[10, 9, 2, 5, 3, 7, 101, 18]);
    println!("LIS([10,9,2,5,3,7,101,18]) = {}", lis);
    assert_eq!(lis, 4); // e.g., [2, 3, 7, 101]

    let lis2 = longest_increasing_subsequence(&[0, 1, 0, 3, 2, 3]);
    assert_eq!(lis2, 4); // [0, 1, 2, 3]

    let lis3 = longest_increasing_subsequence(&[7, 7, 7, 7]);
    assert_eq!(lis3, 1);
    println!("PASS\n");

    // --- Coin Change ---
    println!("--- Coin Change ---");
    let result = coin_change(&[1, 5, 10, 25], 30);
    println!("coin_change([1,5,10,25], 30) = {} coins", result);
    assert_eq!(result, 2); // 25 + 5

    let result2 = coin_change(&[2], 3);
    println!("coin_change([2], 3) = {}", result2);
    assert_eq!(result2, -1); // Impossible

    let result3 = coin_change(&[1, 2, 5], 11);
    assert_eq!(result3, 3); // 5 + 5 + 1
    println!("PASS\n");

    // --- Subset Sum ---
    println!("--- Subset Sum ---");
    assert!(subset_sum(&[3, 34, 4, 12, 5, 2], 9));  // 4 + 5
    assert!(!subset_sum(&[3, 34, 4, 12, 5, 2], 30)); // No subset sums to 30
    assert!(subset_sum(&[1, 2, 3], 6));               // 1 + 2 + 3
    assert!(subset_sum(&[], 0));                       // Empty subset
    println!("subset_sum([3,34,4,12,5,2], 9) = true");
    println!("subset_sum([3,34,4,12,5,2], 30) = false");
    println!("PASS\n");

    // --- Edit Distance ---
    println!("--- Edit Distance ---");
    let dist = edit_distance("horse", "ros");
    println!("edit_distance(\"horse\", \"ros\") = {}", dist);
    assert_eq!(dist, 3);

    let dist2 = edit_distance("intention", "execution");
    println!("edit_distance(\"intention\", \"execution\") = {}", dist2);
    assert_eq!(dist2, 5);

    assert_eq!(edit_distance("", "abc"), 3);
    assert_eq!(edit_distance("abc", "abc"), 0);
    println!("PASS\n");

    println!("All Week 18 tests passed!");
}
