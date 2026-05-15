/*
 * WEEK 23 - RUST ADVANCED DSA
 * Topic: Advanced Dynamic Programming (Bitmask, Tree, Digit DP, LIS)
 * File: 1.AdvancedDP.rs
 *
 * CONCEPT:
 *   Bitmask DP encodes a subset of n items in an integer (n <= ~20).
 *   DP on Trees uses post-order recursion; subproblem = subtree.
 *   Digit DP iterates over digits, tracking a "tight" flag.
 *   LIS via patience sorting reaches O(n log n).
 *
 * KEY POINTS:
 *   - Use i64 or i32 for cost arrays; INF = i32::MAX / 4 to avoid overflow.
 *   - Bit ops on usize are fine for masks if n <= 32.
 *   - For LIS use slice::binary_search and partition_point.
 *
 * ALGORITHM / APPROACH:
 *   See sibling files; identical recurrences.
 *
 * RUST-SPECIFIC NOTES vs JAVA:
 *   - Rust enforces explicit borrowing rules; for tree DP we pass &[Vec<usize>]
 *     immutably and mutate dp via index access (no aliasing).
 *   - No `static` recursion-friendly closures: write a free fn and pass
 *     state, or use a recursive struct method.
 *   - For digit DP we pass digits as &[u32]; memo as a Vec<Option<i64>>.
 *
 * DRY RUN:
 *   TSP for the 4-city matrix in main: 80.
 *   count_no_four(10) -> 9. LIS([10,9,2,5,3,7,101,18]) -> 4.
 *
 * COMPLEXITY:
 *   TSP O(n^2 * 2^n), Tree DP O(n), Digit DP O(D*10), LIS O(n log n).
 */

const INF: i32 = i32::MAX / 4;

pub fn tsp_min_cost(dist: &Vec<Vec<i32>>) -> i32 {
    let n = dist.len();
    let full = (1usize << n) - 1;
    let mut dp = vec![vec![INF; n]; 1 << n];
    dp[1][0] = 0;
    for mask in 1..=full {
        for u in 0..n {
            if (mask & (1 << u)) == 0 || dp[mask][u] == INF { continue; }
            for v in 0..n {
                if (mask & (1 << v)) != 0 { continue; }
                let nm = mask | (1 << v);
                let cand = dp[mask][u] + dist[u][v];
                if cand < dp[nm][v] { dp[nm][v] = cand; }
            }
        }
    }
    let mut ans = i32::MAX;
    for u in 1..n {
        if dp[full][u] != INF {
            let c = dp[full][u] + dist[u][0];
            if c < ans { ans = c; }
        }
    }
    ans
}

fn dfs_tree(u: usize, weight: &[i32], children: &Vec<Vec<usize>>,
            dp: &mut Vec<[i32; 2]>, visited: &mut Vec<bool>) {
    visited[u] = true;
    dp[u][1] = weight[u];
    dp[u][0] = 0;
    let kids = children[u].clone();
    for c in kids {
        if !visited[c] {
            dfs_tree(c, weight, children, dp, visited);
            dp[u][1] += dp[c][0];
            dp[u][0] += std::cmp::max(dp[c][0], dp[c][1]);
        }
    }
}

pub fn max_indep_set(weight: &[i32], children: &Vec<Vec<usize>>) -> i32 {
    let n = weight.len();
    let mut dp = vec![[0i32; 2]; n];
    let mut visited = vec![false; n];
    dfs_tree(0, weight, children, &mut dp, &mut visited);
    std::cmp::max(dp[0][0], dp[0][1])
}

// Digit DP: count integers in [1..N] without digit '4'
fn rec(digits: &[u32], pos: usize, tight: bool, started: bool,
       memo: &mut Vec<Option<i64>>) -> i64 {
    if pos == digits.len() {
        return if started { 1 } else { 0 };
    }
    if !tight && started {
        if let Some(v) = memo[pos] { return v; }
    }
    let limit = if tight { digits[pos] } else { 9 };
    let mut total = 0i64;
    for d in 0..=limit {
        if d == 4 { continue; }
        total += rec(digits, pos + 1, tight && (d == limit), started || (d != 0), memo);
    }
    if !tight && started { memo[pos] = Some(total); }
    total
}

pub fn count_no_four(n: i64) -> i64 {
    let s = n.to_string();
    let digits: Vec<u32> = s.chars().map(|c| c.to_digit(10).unwrap()).collect();
    let mut memo: Vec<Option<i64>> = vec![None; digits.len()];
    rec(&digits, 0, true, false, &mut memo)
}

// LIS in O(n log n) via patience sorting
pub fn lis_optimal(nums: &[i32]) -> usize {
    let mut tails: Vec<i32> = Vec::new();
    for &x in nums {
        let i = tails.partition_point(|&t| t < x);
        if i == tails.len() { tails.push(x); }
        else { tails[i] = x; }
    }
    tails.len()
}

fn main() {
    println!("=== TSP with Bitmask DP ===");
    let dist4 = vec![
        vec![0,10,15,20],
        vec![10,0,35,25],
        vec![15,35,0,30],
        vec![20,25,30,0]
    ];
    println!("TSP (4 cities): {}", tsp_min_cost(&dist4));

    println!("\n=== Max Independent Set on Tree ===");
    let weights = vec![1, 2, 3, 4, 5];
    let children: Vec<Vec<usize>> = vec![vec![1,2], vec![3,4], vec![], vec![], vec![]];
    println!("Max weight independent set: {}", max_indep_set(&weights, &children));

    println!("\n=== Digit DP: Count numbers without digit 4 ===");
    println!("Count in [1..10]:  {}", count_no_four(10));
    println!("Count in [1..40]:  {}", count_no_four(40));
    println!("Count in [1..100]: {}", count_no_four(100));

    println!("\n=== LIS O(n log n) ===");
    for t in [vec![10,9,2,5,3,7,101,18], vec![0,1,0,3,2,3], vec![7,7,7,7,7]] {
        println!("{:?} -> LIS = {}", t, lis_optimal(&t));
    }
}
