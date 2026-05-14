// WEEK 28 - RUST ADVANCED TOPICS
// Topic: Nim Game
// File: nim.rs
//
// CONCEPT:
//   Bouton's theorem: first player wins Nim iff XOR of pile sizes != 0.
//   Constructive winning move: pick a pile p with (p XOR xor_sum) < p and
//   reduce it to that target.
//
// KEY POINTS:
//   - XOR captures the parity invariant of "P-positions" under Nim moves.
//   - Foundational case of Sprague-Grundy theory.
//
// ALGORITHM / APPROACH:
//   x = XOR of piles
//   if x == 0 -> losing for player to move
//   else find pile p with (p ^ x) < p; play to (p ^ x)
//
// RUST-SPECIFIC NOTES:
//   - iter().fold(0, std::ops::BitXor::bitxor) for the XOR sum.
//   - Option<(usize, i64)> for the winning move return.
//
// DRY RUN / EXAMPLE:
//   piles = [3,4,5]: XOR = 2, first wins. 3^2=1 < 3 -> reduce pile 0 to 1.
//
// COMPLEXITY:
//   Time O(n)   Space O(1)

pub fn nim_winner(piles: &[i64]) -> &'static str {
    let x: i64 = piles.iter().fold(0, |acc, &p| acc ^ p);
    if x != 0 { "First" } else { "Second" }
}

pub fn nim_winning_move(piles: &[i64]) -> Option<(usize, i64)> {
    let x: i64 = piles.iter().fold(0, |acc, &p| acc ^ p);
    if x == 0 { return None; }
    for (i, &p) in piles.iter().enumerate() {
        let target = p ^ x;
        if target < p { return Some((i, target)); }
    }
    None
}

fn main() {
    let piles = [3, 4, 5];
    println!("Piles [3,4,5]: winner = {}", nim_winner(&piles));
    if let Some((i, target)) = nim_winning_move(&piles) {
        println!("Winning move: reduce pile {} from {} to {}", i, piles[i], target);
    }
    let piles2 = [1, 2, 3];
    println!("Piles [1,2,3]: winner = {}", nim_winner(&piles2));
    println!("Has winning move: {}", nim_winning_move(&piles2).is_some());
}

// NOTES
// -----
// Differences from Java:
//   * Adds the constructive `nim_winning_move` alongside the decision result.
//   * Option<(usize, i64)> models "no winning move" cleanly.
