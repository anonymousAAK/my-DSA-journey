// WEEK 28 - RUST ADVANCED TOPICS
// Topic: Sprague-Grundy Theorem and Grundy Numbers
// File: sprague_grundy.rs
//
// CONCEPT:
//   Every impartial game position s has a Grundy number g(s) =
//     mex { g(s') : s' reachable from s }
//   For a sum of independent games, XOR Grundy values; losing iff XOR=0.
//
// KEY POINTS:
//   - Generalises Bouton's theorem.
//   - DP up to max pile size; multi-pile via XOR.
//   - mex(S) = smallest non-negative integer absent from S.
//
// ALGORITHM / APPROACH:
//   for i in 0..=n: g[i] = mex(g[i-m] for m in moves if i-m>=0)
//   multi-pile: XOR g[piles[i]]
//
// RUST-SPECIFIC NOTES:
//   - HashSet<i32> for the reachable set.
//   - mex iterates from 0 upward.
//
// DRY RUN / EXAMPLE:
//   moves [1,3,4]: g(10) = 1. Two piles [10,6]: XOR(g(10),g(6))=XOR(1,2)=3,
//   first wins.
//
// COMPLEXITY:
//   Time O(n * |moves|)   Space O(n)

use std::collections::HashSet;

pub fn mex(s: &HashSet<i32>) -> i32 {
    let mut m = 0;
    while s.contains(&m) { m += 1; }
    m
}

pub fn grundy_subtraction(n: usize, moves: &[usize]) -> i32 {
    let mut g = vec![0i32; n + 1];
    for i in 1..=n {
        let mut reachable = HashSet::new();
        for &m in moves {
            if i >= m { reachable.insert(g[i - m]); }
        }
        g[i] = mex(&reachable);
    }
    g[n]
}

pub fn first_player_wins(piles: &[usize], moves: &[usize]) -> bool {
    if piles.is_empty() { return false; }
    let max_pos = *piles.iter().max().unwrap();
    let mut g = vec![0i32; max_pos + 1];
    for i in 1..=max_pos {
        let mut reachable = HashSet::new();
        for &m in moves { if i >= m { reachable.insert(g[i - m]); } }
        g[i] = mex(&reachable);
    }
    let x = piles.iter().fold(0, |acc, &p| acc ^ g[p]);
    x != 0
}

fn main() {
    let moves = [1usize, 3, 4];
    println!("Grundy table for moves [1,3,4]:");
    for i in 0..=10 {
        println!("  g({}) = {}", i, grundy_subtraction(i, &moves));
    }
    println!("grundy(10) = {}", grundy_subtraction(10, &moves));
    println!("Two piles [10,6]: first wins? {}",
             first_player_wins(&[10, 6], &moves));
}

// NOTES
// -----
// Differences from Java:
//   * Adds a multi-pile XOR wrapper on top of the single-pile grundy
//     function.
//   * HashSet<i32> replaces Java's HashSet<Integer>.
