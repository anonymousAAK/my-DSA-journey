// WEEK 28 - RUST ADVANCED TOPICS
// Topic: Alpha-Beta Pruning
// File: alpha_beta.rs
//
// CONCEPT:
//   Same value as minimax with branch pruning when the [alpha, beta] window
//   guarantees a value outside what the parent would accept.
//
// KEY POINTS:
//   - alpha = best for Max so far; beta = best for Min so far.
//   - When alpha >= beta we prune. With good move ordering, b -> sqrt(b).
//
// ALGORITHM / APPROACH:
//   alphabeta(s, a, b, max_turn):
//     terminal -> utility(s)
//     iterate children, updating a or b; break on a >= b.
//
// RUST-SPECIFIC NOTES:
//   - Pass alpha and beta as i32 by value.
//   - i32::MIN / i32::MAX represent unbounded windows; do not pass through
//     -INT_MIN territory.
//
// DRY RUN / EXAMPLE:
//   Empty TTT board, X to move -> value 0. Node counter exposes pruning.
//
// COMPLEXITY:
//   Time O(b^d) worst; O(b^(d/2)) ideal ordering. Space O(d).

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
fn utility(b: &Board) -> i32 { match winner(b) { 'X' => 1, 'O' => -1, _ => 0 } }

fn alphabeta(b: Board, mut alpha: i32, mut beta: i32, max_turn: bool, counter: &mut u64) -> i32 {
    *counter += 1;
    if winner(&b) != '.' || is_full(&b) { return utility(&b); }
    if max_turn {
        let mut v = i32::MIN;
        for i in 0..9 {
            if b[i] != '.' { continue; }
            let mut c = b;
            c[i] = 'X';
            v = v.max(alphabeta(c, alpha, beta, false, counter));
            alpha = alpha.max(v);
            if alpha >= beta { break; }
        }
        v
    } else {
        let mut v = i32::MAX;
        for i in 0..9 {
            if b[i] != '.' { continue; }
            let mut c = b;
            c[i] = 'O';
            v = v.min(alphabeta(c, alpha, beta, true, counter));
            beta = beta.min(v);
            if alpha >= beta { break; }
        }
        v
    }
}

fn best_move(b: Board, max_turn: bool) -> usize {
    let mut counter = 0u64;
    let mut idx = usize::MAX;
    let mut bv = if max_turn { i32::MIN } else { i32::MAX };
    for i in 0..9 {
        if b[i] != '.' { continue; }
        let mut c = b;
        c[i] = if max_turn { 'X' } else { 'O' };
        let v = alphabeta(c, i32::MIN, i32::MAX, !max_turn, &mut counter);
        if (max_turn && v > bv) || (!max_turn && v < bv) {
            bv = v;
            idx = i;
        }
    }
    idx
}

fn main() {
    let empty: Board = ['.'; 9];
    let mut counter = 0u64;
    println!("Alpha-beta value: {}",
             alphabeta(empty, i32::MIN, i32::MAX, true, &mut counter));
    println!("Nodes explored: {}", counter);
    println!("Best opening move for X: cell {}", best_move(empty, true));
}

// NOTES
// -----
// Differences from Java:
//   * Java's game_theory.java has no alpha-beta; we add it.
//   * i32::MIN / i32::MAX as initial bounds; avoid arithmetic on them.
//   * A `counter` parameter threads the node-count without globals.
