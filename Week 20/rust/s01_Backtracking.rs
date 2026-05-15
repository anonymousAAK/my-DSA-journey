/*
 * WEEK 20 - RUST DSA
 * Topic: Backtracking — Template + Classic Problems
 * File: 1.Backtracking.rs
 *
 * CONCEPT:
 *     Backtracking builds a candidate solution incrementally. After each
 *     extension it checks whether the partial solution can still lead to
 *     a valid full answer; otherwise it ABANDONS that branch and undoes
 *     the last choice.
 *
 * TEMPLATE:
 *     fn backtrack(state: &mut State, ...) {
 *         if is_solution(state) { record(state); return; }
 *         for c in choices(state) {
 *             if is_valid(c, state) {
 *                 apply(c, state);                 // choose
 *                 backtrack(state, ...);           // explore
 *                 undo(c, state);                  // backtrack
 *             }
 *         }
 *     }
 *
 * KEY POINTS:
 *     - Worst-case is exponential (O(k^n) or O(n!)).
 *     - Pruning ("is_valid") is the practical accelerator.
 *     - Use Vec::push / Vec::pop for the mutable partial-solution state.
 *
 * ALGORITHM / APPROACH:
 *     Four canonical problems (matching the Java reference):
 *         1. Permutations of a Vec
 *         2. Subsets (power set)
 *         3. N-Queens
 *         4. Word Search in 2-D grid
 *
 * RUST-SPECIFIC NOTES:
 *     BORROW CHECKER concerns: a recursive backtracking fn typically takes
 *       `&mut Vec<T>` (the partial solution) and pushes results into another
 *       `&mut Vec<Vec<T>>`. Both must be DISJOINT mutable borrows -- pass
 *       them as separate parameters rather than as two fields of the same
 *       struct.
 *     IDIOMS:
 *       - `nums.swap(i, j)` for in-place swap.
 *       - `state.push(x)`, `state.pop()` -- Vec is the perfect backtracking stack.
 *       - `state.clone()` snapshots the partial solution before recording.
 *
 * DRY RUN:
 *     permutations(&mut vec![1,2,3]) emits 6 permutations.
 *     subsets(&[1,2,3]) emits 8 subsets.
 *     n_queens(4) yields 2 solutions.
 *     word_search "ABCCED" -> true; "ABCB" -> false.
 *
 * COMPLEXITY:
 *     permutations    O(n * n!) time
 *     subsets         O(n * 2^n) time
 *     n_queens        worst O(n!), pruned in practice
 *     word_search     O(m*n * 4^|word|)
 */

// 1. PERMUTATIONS
pub fn permutations(mut nums: Vec<i32>) -> Vec<Vec<i32>> {
    let mut out = Vec::new();
    fn go(nums: &mut Vec<i32>, start: usize, out: &mut Vec<Vec<i32>>) {
        if start == nums.len() {
            out.push(nums.clone());
            return;
        }
        for i in start..nums.len() {
            nums.swap(start, i);             // choose
            go(nums, start + 1, out);        // explore
            nums.swap(start, i);             // undo
        }
    }
    go(&mut nums, 0, &mut out);
    out
}

// 2. SUBSETS
pub fn subsets(nums: &[i32]) -> Vec<Vec<i32>> {
    let mut out = Vec::new();
    let mut current: Vec<i32> = Vec::new();
    fn go(nums: &[i32], idx: usize,
          current: &mut Vec<i32>, out: &mut Vec<Vec<i32>>) {
        out.push(current.clone());
        for i in idx..nums.len() {
            current.push(nums[i]);
            go(nums, i + 1, current, out);
            current.pop();                   // backtrack
        }
    }
    go(nums, 0, &mut current, &mut out);
    out
}

// 3. N-QUEENS
fn is_safe(queens: &[i32], row: usize, col: i32) -> bool {
    for r in 0..row {
        let c = queens[r];
        if c == col { return false; }
        if (c - col).abs() == (r as i32 - row as i32).abs() {
            return false;
        }
    }
    true
}
fn build_board(queens: &[i32]) -> Vec<String> {
    let n = queens.len();
    queens.iter().map(|&c| {
        let mut row = vec![b'.'; n];
        row[c as usize] = b'Q';
        String::from_utf8(row).unwrap()
    }).collect()
}
pub fn n_queens(n: usize) -> Vec<Vec<String>> {
    let mut out = Vec::new();
    let mut queens: Vec<i32> = vec![-1; n];
    fn go(queens: &mut Vec<i32>, row: usize, n: usize,
          out: &mut Vec<Vec<String>>) {
        if row == n {
            out.push(build_board(queens));
            return;
        }
        for col in 0..n {
            if is_safe(queens, row, col as i32) {
                queens[row] = col as i32;
                go(queens, row + 1, n, out);
                queens[row] = -1;            // backtrack
            }
        }
    }
    go(&mut queens, 0, n, &mut out);
    out
}

// 4. WORD SEARCH
pub fn word_search(board: &mut Vec<Vec<char>>, word: &str) -> bool {
    let m = board.len();
    let n = board[0].len();
    let word_bytes: Vec<char> = word.chars().collect();
    fn dfs(board: &mut Vec<Vec<char>>, word: &[char],
           i: i32, j: i32, k: usize) -> bool {
        if k == word.len() { return true; }
        let m = board.len() as i32;
        let n = board[0].len() as i32;
        if i < 0 || i >= m || j < 0 || j >= n { return false; }
        let ui = i as usize;
        let uj = j as usize;
        if board[ui][uj] != word[k] { return false; }
        let tmp = board[ui][uj];
        board[ui][uj] = '#';                 // visited marker
        let found = dfs(board, word, i+1, j, k+1)
                 || dfs(board, word, i-1, j, k+1)
                 || dfs(board, word, i, j+1, k+1)
                 || dfs(board, word, i, j-1, k+1);
        board[ui][uj] = tmp;                 // restore
        found
    }
    for i in 0..m {
        for j in 0..n {
            if dfs(board, &word_bytes, i as i32, j as i32, 0) {
                return true;
            }
        }
    }
    false
}

fn main() {
    println!("=== Permutations of [1,2,3] ===");
    for p in permutations(vec![1, 2, 3]) {
        println!("{:?}", p);
    }

    println!("\n=== Subsets of [1,2,3] ===");
    for s in subsets(&[1, 2, 3]) {
        println!("{:?}", s);
    }

    println!("\n=== 4-Queens ===");
    let sols = n_queens(4);
    println!("Number of solutions: {}", sols.len());
    for sol in &sols {
        for row in sol { println!("{}", row); }
        println!("---");
    }

    println!("=== Word Search ===");
    let make_grid = || -> Vec<Vec<char>> { vec![
        "ABCE".chars().collect(),
        "SFCS".chars().collect(),
        "ADEE".chars().collect(),
    ]};
    let mut g = make_grid();
    println!("Search 'ABCCED': {}", word_search(&mut g, "ABCCED")); // true
    let mut g = make_grid();
    println!("Search 'SEE'   : {}", word_search(&mut g, "SEE"));    // true
    let mut g = make_grid();
    println!("Search 'ABCB'  : {}", word_search(&mut g, "ABCB"));   // false
}

/*
 * NOTES (Rust vs Java):
 *   - Vec::push / Vec::pop is the canonical backtracking stack -- both O(1)
 *     amortised, identical to Java's ArrayList.
 *   - To snapshot a Vec into the results list we call .clone(); Java does
 *     `new ArrayList<>(current)`.
 *   - The borrow checker forbids two simultaneous &mut self borrows, so the
 *     recursion helpers take their state vectors as explicit parameters --
 *     this matches the textbook recursive signature anyway.
 *   - For the N-queens char-board we build a row as a Vec<u8> of '.' bytes
 *     and overwrite one with 'Q' before converting to a String.
 *   - Word search uses i32 indices internally to allow temporary -1 values
 *     during the recursive bounds check.
 */
