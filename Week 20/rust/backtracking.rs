//! # Week 20: Backtracking
//!
//! Backtracking is a systematic way to explore all potential solutions by
//! incrementally building candidates and abandoning ("backtracking") a
//! candidate as soon as it cannot lead to a valid solution.
//!
//! ## Pattern
//! ```text
//! fn backtrack(state, choices):
//!     if is_solution(state):
//!         record(state)
//!         return
//!     for choice in choices:
//!         if is_valid(choice):
//!             make(choice)
//!             backtrack(state, remaining_choices)
//!             undo(choice)  // <-- the "backtrack" step
//! ```
//!
//! ## Complexity Summary
//! | Problem              | Time           | Space     |
//! |---------------------|----------------|-----------|
//! | Permutations        | O(n! * n)      | O(n)      |
//! | Subsets (Power Set) | O(2^n * n)     | O(n)      |
//! | N-Queens            | O(n!)          | O(n)      |
//! | Word Search         | O(m*n*4^L)     | O(L)      |
//! | Generate Parentheses| O(4^n / sqrt(n))| O(n)     |

// =============================================================================
// Permutations
// =============================================================================

/// Generates all permutations of the given slice.
///
/// # Algorithm
/// Use a `used` boolean array to track which elements are in the current
/// permutation. At each level of recursion, try each unused element.
///
/// # Complexity
/// - Time: O(n! * n) — n! permutations, each of length n to copy
/// - Space: O(n) for the recursion stack and current permutation
///
/// # Ownership Note
/// We pass `current` and `used` as mutable references, modifying and then
/// restoring them (backtracking) to avoid allocating new collections at
/// each recursive call.
fn permutations(nums: &[i32]) -> Vec<Vec<i32>> {
    let mut result = Vec::new();
    let mut current = Vec::new();
    let mut used = vec![false; nums.len()];

    fn backtrack(
        nums: &[i32],
        current: &mut Vec<i32>,
        used: &mut Vec<bool>,
        result: &mut Vec<Vec<i32>>,
    ) {
        if current.len() == nums.len() {
            result.push(current.clone()); // Must clone — current will be modified
            return;
        }

        for i in 0..nums.len() {
            if !used[i] {
                used[i] = true;
                current.push(nums[i]);

                backtrack(nums, current, used, result);

                // Backtrack: undo the choice
                current.pop();
                used[i] = false;
            }
        }
    }

    backtrack(nums, &mut current, &mut used, &mut result);
    result
}

// =============================================================================
// Subsets (Power Set)
// =============================================================================

/// Generates all subsets of the given slice (the power set).
///
/// # Algorithm
/// At each index, we have two choices: include the element or skip it.
/// This generates all 2^n subsets.
///
/// # Complexity
/// - Time: O(2^n * n) — 2^n subsets, each up to length n to copy
/// - Space: O(n) recursion depth
fn subsets(nums: &[i32]) -> Vec<Vec<i32>> {
    let mut result = Vec::new();
    let mut current = Vec::new();

    fn backtrack(
        nums: &[i32],
        start: usize,
        current: &mut Vec<i32>,
        result: &mut Vec<Vec<i32>>,
    ) {
        // Every state is a valid subset (including empty)
        result.push(current.clone());

        for i in start..nums.len() {
            current.push(nums[i]);
            backtrack(nums, i + 1, current, result);
            current.pop(); // Backtrack
        }
    }

    backtrack(nums, 0, &mut current, &mut result);
    result
}

// =============================================================================
// N-Queens
// =============================================================================

/// Solves the N-Queens problem: place N queens on an NxN board so that no
/// two queens attack each other (same row, column, or diagonal).
///
/// # Algorithm
/// Place queens row by row. For each row, try each column. Check validity
/// by ensuring no column conflict or diagonal conflict with previously
/// placed queens.
///
/// Diagonal check: two queens at (r1, c1) and (r2, c2) share a diagonal iff
/// `|r1-r2| == |c1-c2|`.
///
/// # Complexity
/// - Time: O(n!) — at most n choices for first row, n-1 for second, etc.
/// - Space: O(n^2) for the board, O(n) for recursion
///
/// # Returns
/// All valid board configurations as `Vec<Vec<String>>` where each String
/// represents a row with '.' for empty and 'Q' for a queen.
fn n_queens(n: usize) -> Vec<Vec<String>> {
    let mut result = Vec::new();
    let mut queens: Vec<usize> = Vec::new(); // queens[row] = column

    fn is_valid(queens: &[usize], row: usize, col: usize) -> bool {
        for (r, &c) in queens.iter().enumerate() {
            // Check column conflict
            if c == col {
                return false;
            }
            // Check diagonal conflict
            let row_diff = row - r; // Always positive since row > r
            let col_diff = if col > c { col - c } else { c - col };
            if row_diff == col_diff {
                return false;
            }
        }
        true
    }

    fn backtrack(
        n: usize,
        queens: &mut Vec<usize>,
        result: &mut Vec<Vec<String>>,
    ) {
        let row = queens.len();
        if row == n {
            // Convert queen positions to board representation
            let board: Vec<String> = queens
                .iter()
                .map(|&col| {
                    let mut row_str = vec!['.'; n];
                    row_str[col] = 'Q';
                    row_str.into_iter().collect()
                })
                .collect();
            result.push(board);
            return;
        }

        for col in 0..n {
            if is_valid(queens, row, col) {
                queens.push(col);
                backtrack(n, queens, result);
                queens.pop(); // Backtrack
            }
        }
    }

    backtrack(n, &mut queens, &mut result);
    result
}

// =============================================================================
// Word Search in 2D Grid
// =============================================================================

/// Checks if a word exists in the grid by following adjacent cells
/// (horizontal or vertical). Each cell can be used at most once per path.
///
/// # Algorithm
/// For each cell matching the first character, start a DFS. Mark cells as
/// visited by temporarily modifying them (using '#'), then restore on backtrack.
///
/// # Complexity
/// - Time: O(m * n * 4^L) where m*n is grid size, L is word length
/// - Space: O(L) for recursion stack
///
/// # Ownership Note
/// We take `&mut Vec<Vec<char>>` to temporarily mark visited cells in-place,
/// avoiding extra allocation for a visited matrix. The grid is restored
/// after each backtrack.
fn word_search(board: &mut Vec<Vec<char>>, word: &str) -> bool {
    let word: Vec<char> = word.chars().collect();
    let rows = board.len();
    if rows == 0 {
        return word.is_empty();
    }
    let cols = board[0].len();

    fn dfs(
        board: &mut Vec<Vec<char>>,
        word: &[char],
        idx: usize,
        r: usize,
        c: usize,
        rows: usize,
        cols: usize,
    ) -> bool {
        if idx == word.len() {
            return true;
        }
        if r >= rows || c >= cols || board[r][c] != word[idx] {
            return false;
        }

        // Mark as visited by replacing with a sentinel
        let original = board[r][c];
        board[r][c] = '#';

        // Explore all 4 directions
        let directions: [(isize, isize); 4] = [(0, 1), (0, -1), (1, 0), (-1, 0)];
        for (dr, dc) in &directions {
            let nr = r as isize + dr;
            let nc = c as isize + dc;
            if nr >= 0 && nc >= 0 {
                if dfs(board, word, idx + 1, nr as usize, nc as usize, rows, cols) {
                    board[r][c] = original; // Restore before returning
                    return true;
                }
            }
        }

        // Backtrack: restore the cell
        board[r][c] = original;
        false
    }

    for r in 0..rows {
        for c in 0..cols {
            if dfs(board, &word, 0, r, c, rows, cols) {
                return true;
            }
        }
    }

    false
}

// =============================================================================
// Generate Parentheses
// =============================================================================

/// Generates all valid combinations of `n` pairs of parentheses.
///
/// # Algorithm
/// At each position, we can add '(' if we haven't used all n, or add ')'
/// if the number of ')' is less than the number of '(' (to keep it valid).
///
/// # Complexity
/// - Time: O(4^n / sqrt(n)) — the n-th Catalan number
/// - Space: O(n) for the recursion stack and current string
fn generate_parentheses(n: usize) -> Vec<String> {
    let mut result = Vec::new();
    let mut current = String::new();

    fn backtrack(
        current: &mut String,
        open: usize,
        close: usize,
        n: usize,
        result: &mut Vec<String>,
    ) {
        if current.len() == 2 * n {
            result.push(current.clone());
            return;
        }

        if open < n {
            current.push('(');
            backtrack(current, open + 1, close, n, result);
            current.pop(); // Backtrack
        }

        if close < open {
            current.push(')');
            backtrack(current, open, close + 1, n, result);
            current.pop(); // Backtrack
        }
    }

    backtrack(&mut current, 0, 0, n, &mut result);
    result
}

// =============================================================================
// Main — Test cases
// =============================================================================

fn main() {
    println!("=== Week 20: Backtracking ===\n");

    // --- Permutations ---
    println!("--- Permutations ---");
    let perms = permutations(&[1, 2, 3]);
    println!("Permutations of [1,2,3]: {} total", perms.len());
    for p in &perms {
        println!("  {:?}", p);
    }
    assert_eq!(perms.len(), 6); // 3! = 6
    assert!(perms.contains(&vec![1, 2, 3]));
    assert!(perms.contains(&vec![3, 2, 1]));
    println!("PASS\n");

    // --- Subsets ---
    println!("--- Subsets (Power Set) ---");
    let subs = subsets(&[1, 2, 3]);
    println!("Subsets of [1,2,3]: {} total", subs.len());
    for s in &subs {
        println!("  {:?}", s);
    }
    assert_eq!(subs.len(), 8); // 2^3 = 8
    assert!(subs.contains(&vec![]));
    assert!(subs.contains(&vec![1, 2, 3]));
    println!("PASS\n");

    // --- N-Queens ---
    println!("--- N-Queens ---");
    let solutions_4 = n_queens(4);
    println!("4-Queens solutions: {}", solutions_4.len());
    for (i, board) in solutions_4.iter().enumerate() {
        println!("  Solution {}:", i + 1);
        for row in board {
            println!("    {}", row);
        }
    }
    assert_eq!(solutions_4.len(), 2);

    let solutions_8 = n_queens(8);
    println!("8-Queens solutions: {}", solutions_8.len());
    assert_eq!(solutions_8.len(), 92);
    println!("PASS\n");

    // --- Word Search ---
    println!("--- Word Search ---");
    let mut board = vec![
        vec!['A', 'B', 'C', 'E'],
        vec!['S', 'F', 'C', 'S'],
        vec!['A', 'D', 'E', 'E'],
    ];
    assert!(word_search(&mut board, "ABCCED"));
    println!("word_search(board, \"ABCCED\") = true");

    assert!(word_search(&mut board, "SEE"));
    println!("word_search(board, \"SEE\") = true");

    assert!(!word_search(&mut board, "ABCB"));
    println!("word_search(board, \"ABCB\") = false (can't reuse cells)");
    println!("PASS\n");

    // --- Generate Parentheses ---
    println!("--- Generate Parentheses ---");
    let parens = generate_parentheses(3);
    println!("generate_parentheses(3):");
    for p in &parens {
        println!("  {}", p);
    }
    assert_eq!(parens.len(), 5); // Catalan(3) = 5
    assert!(parens.contains(&"((()))".to_string()));
    assert!(parens.contains(&"(()())".to_string()));
    assert!(parens.contains(&"(())()".to_string()));
    assert!(parens.contains(&"()(())".to_string()));
    assert!(parens.contains(&"()()()".to_string()));

    let parens1 = generate_parentheses(1);
    assert_eq!(parens1, vec!["()"]);
    println!("PASS\n");

    println!("All Week 20 tests passed!");
}
