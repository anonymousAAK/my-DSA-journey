// WEEK 28 - RUST ADVANCED TOPICS
// Topic: Minimax (Zero-Sum Game Tree Search)
// File: minimax.rs
//
// CONCEPT:
//   Recursively evaluate the value of every game-tree node where Max picks
//   the maximum of children and Min picks the minimum. Returns the game's
//   value with optimal play.
//
// KEY POINTS:
//   - O(b^d). Memoise hashable states for repeated subtrees.
//   - For non-finite games combine with depth limits + heuristic eval.
//
// ALGORITHM / APPROACH:
//   minimax(s, max_turn):
//     terminal -> utility(s)
//     else (max | min) over moves of minimax(child, !max_turn)
//
// RUST-SPECIFIC NOTES:
//   - Board as [char; 9] (Copy, Hash).
//   - HashMap<[char;9], i32> memoises.
//   - 'X' = +1, 'O' = -1.
//
// DRY RUN / EXAMPLE:
//   Empty TTT board, X to move -> value 0 (draw with optimal play).
//
// COMPLEXITY:
//   Time O(b^d); Space O(d) recursion + O(|states|) memo.

use std::collections::HashMap;

type Board = [char; 9];

const LINES: [[usize; 3]; 8] = [
    [0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]
];

fn winner(b: &Board) -> char {
    for l in LINES.iter() {
        if b[l[0]] != '.' && b[l[0]] == b[l[1]] && b[l[1]] == b[l[2]] {
            return b[l[0]];
        }
    }
    '.'
}

fn is_full(b: &Board) -> bool { !b.iter().any(|&c| c == '.') }

fn utility(b: &Board) -> i32 {
    match winner(b) { 'X' => 1, 'O' => -1, _ => 0 }
}

fn minimax(b: Board, max_turn: bool, memo: &mut HashMap<Board, i32>) -> i32 {
    if winner(&b) != '.' || is_full(&b) { return utility(&b); }
    if let Some(&v) = memo.get(&b) { return v; }
    let mut best = if max_turn { -2 } else { 2 };
    for i in 0..9 {
        if b[i] != '.' { continue; }
        let mut c = b;
        c[i] = if max_turn { 'X' } else { 'O' };
        let v = minimax(c, !max_turn, memo);
        if max_turn { if v > best { best = v; } } else { if v < best { best = v; } }
    }
    memo.insert(b, best);
    best
}

fn best_move(b: Board, max_turn: bool, memo: &mut HashMap<Board, i32>) -> usize {
    let mut idx = usize::MAX;
    let mut bv = if max_turn { -3 } else { 3 };
    for i in 0..9 {
        if b[i] != '.' { continue; }
        let mut c = b;
        c[i] = if max_turn { 'X' } else { 'O' };
        let v = minimax(c, !max_turn, memo);
        if (max_turn && v > bv) || (!max_turn && v < bv) {
            bv = v;
            idx = i;
        }
    }
    idx
}

fn main() {
    let mut memo: HashMap<Board, i32> = HashMap::new();
    let empty: Board = ['.'; 9];
    println!("Minimax value of empty TTT: {}", minimax(empty, true, &mut memo));
    println!("Best opening move for X: cell {}", best_move(empty, true, &mut memo));
}

// NOTES
// -----
// Differences from Java:
//   * Java's game_theory.java does not include minimax; we add it.
//   * [char; 9] is a Copy + Hash type, perfect for fast memo keys.
//   * Explicit HashMap memo is more straightforward in Rust than wrapping
//     a mutable closure.
