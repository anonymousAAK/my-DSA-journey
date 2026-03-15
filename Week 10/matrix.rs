//! # Week 10: Matrix
//!
//! This module covers classic matrix algorithms in Rust.
//! Topics include:
//! - Transpose (in-place for square matrices, new matrix for general)
//! - Rotate 90 degrees clockwise
//! - Matrix multiplication
//! - Spiral order traversal
//! - Diagonal order traversal
//! - Search in a row-wise and column-wise sorted matrix
//! - Pascal's triangle generation
//!
//! ## Rust-Specific Notes for DSA Learners
//! - Matrices are represented as `Vec<Vec<i32>>` — a vector of row vectors.
//! - Rust doesn't have built-in 2D arrays with runtime dimensions; `Vec<Vec<T>>`
//!   is the standard approach. Each row is a separate heap allocation.
//! - For in-place square transpose, we use direct indexing with `matrix[i][j]`.
//!   Rust's borrow checker won't allow `&mut matrix[i][j]` and `&mut matrix[j][i]`
//!   simultaneously, so we use a temporary variable for the swap.

/// Type alias for a 2D matrix to improve readability.
type Matrix = Vec<Vec<i32>>;

// ---------------------------------------------------------------------------
// Transpose
// ---------------------------------------------------------------------------

/// Transposes a square matrix in place.
///
/// Swaps `matrix[i][j]` with `matrix[j][i]` for all `i < j`.
///
/// # Complexity
/// - Time:  O(n^2)
/// - Space: O(1) — in-place
fn transpose_square(matrix: &mut Matrix) {
    let n = matrix.len();
    for i in 0..n {
        for j in (i + 1)..n {
            // We can't take two mutable borrows of different rows via indexing
            // simultaneously in a straightforward way. Using a temp variable:
            let temp = matrix[i][j];
            matrix[i][j] = matrix[j][i];
            matrix[j][i] = temp;
        }
    }
}

/// Transposes a general (possibly non-square) matrix, returning a new matrix.
///
/// An `m x n` matrix becomes `n x m`.
///
/// # Complexity
/// - Time:  O(m * n)
/// - Space: O(m * n) — new matrix
fn transpose_general(matrix: &Matrix) -> Matrix {
    if matrix.is_empty() || matrix[0].is_empty() {
        return vec![];
    }
    let rows = matrix.len();
    let cols = matrix[0].len();
    let mut result = vec![vec![0i32; rows]; cols];
    for i in 0..rows {
        for j in 0..cols {
            result[j][i] = matrix[i][j];
        }
    }
    result
}

// ---------------------------------------------------------------------------
// Rotate 90 Degrees Clockwise
// ---------------------------------------------------------------------------

/// Rotates an `n x n` matrix 90 degrees clockwise in place.
///
/// Algorithm: transpose + reverse each row.
/// - Transpose swaps rows/columns.
/// - Reversing each row turns a transpose into a 90 CW rotation.
///
/// # Complexity
/// - Time:  O(n^2)
/// - Space: O(1) — in-place
fn rotate_90_cw(matrix: &mut Matrix) {
    transpose_square(matrix);
    for row in matrix.iter_mut() {
        row.reverse();
    }
}

// ---------------------------------------------------------------------------
// Matrix Multiplication
// ---------------------------------------------------------------------------

/// Multiplies two matrices `a` (m x n) and `b` (n x p), returning the `m x p` result.
///
/// # Panics
/// Panics if the dimensions are incompatible (a's columns != b's rows).
///
/// # Complexity
/// - Time:  O(m * n * p)
/// - Space: O(m * p) — the result matrix
fn matrix_multiply(a: &Matrix, b: &Matrix) -> Matrix {
    let m = a.len();
    let n = a[0].len();
    let p = b[0].len();
    assert_eq!(n, b.len(), "Incompatible dimensions for multiplication");

    let mut result = vec![vec![0i32; p]; m];
    for i in 0..m {
        for k in 0..n {
            // Loop reordering (i-k-j) is cache-friendly for row-major storage.
            let a_ik = a[i][k];
            for j in 0..p {
                result[i][j] += a_ik * b[k][j];
            }
        }
    }
    result
}

// ---------------------------------------------------------------------------
// Spiral Order Traversal
// ---------------------------------------------------------------------------

/// Returns the elements of a matrix in spiral order (clockwise from top-left).
///
/// We maintain four boundaries: top, bottom, left, right, and shrink them
/// after traversing each edge.
///
/// # Complexity
/// - Time:  O(m * n)
/// - Space: O(m * n) — the output vector
fn spiral_order(matrix: &Matrix) -> Vec<i32> {
    if matrix.is_empty() {
        return vec![];
    }

    let mut result = Vec::new();
    let mut top = 0i32;
    let mut bottom = matrix.len() as i32 - 1;
    let mut left = 0i32;
    let mut right = matrix[0].len() as i32 - 1;

    while top <= bottom && left <= right {
        // Traverse right across the top row.
        for col in left..=right {
            result.push(matrix[top as usize][col as usize]);
        }
        top += 1;

        // Traverse down the right column.
        for row in top..=bottom {
            result.push(matrix[row as usize][right as usize]);
        }
        right -= 1;

        // Traverse left across the bottom row (if there is one).
        if top <= bottom {
            for col in (left..=right).rev() {
                result.push(matrix[bottom as usize][col as usize]);
            }
            bottom -= 1;
        }

        // Traverse up the left column (if there is one).
        if left <= right {
            for row in (top..=bottom).rev() {
                result.push(matrix[row as usize][left as usize]);
            }
            left += 1;
        }
    }

    result
}

// ---------------------------------------------------------------------------
// Diagonal Order Traversal
// ---------------------------------------------------------------------------

/// Returns elements of a matrix in diagonal order.
///
/// Traverses diagonals from top-right to bottom-left, alternating direction:
/// even diagonals go up-right, odd diagonals go down-left.
///
/// # Complexity
/// - Time:  O(m * n)
/// - Space: O(m * n) — the output vector
fn diagonal_order(matrix: &Matrix) -> Vec<i32> {
    if matrix.is_empty() || matrix[0].is_empty() {
        return vec![];
    }

    let m = matrix.len();
    let n = matrix[0].len();
    let mut result = Vec::with_capacity(m * n);

    // There are (m + n - 1) diagonals.
    for d in 0..(m + n - 1) {
        if d % 2 == 0 {
            // Even diagonal: go upward (row decreases, col increases).
            let mut row = if d < m { d } else { m - 1 };
            let mut col = if d < m { 0 } else { d - m + 1 };
            while col < n {
                result.push(matrix[row][col]);
                if row == 0 {
                    break;
                }
                row -= 1;
                col += 1;
            }
        } else {
            // Odd diagonal: go downward (row increases, col decreases).
            let mut row = if d < n { 0 } else { d - n + 1 };
            let mut col = if d < n { d } else { n - 1 };
            while row < m {
                result.push(matrix[row][col]);
                if col == 0 {
                    break;
                }
                row += 1;
                col -= 1;
            }
        }
    }

    result
}

// ---------------------------------------------------------------------------
// Search in Sorted Matrix
// ---------------------------------------------------------------------------

/// Searches for `target` in a matrix where each row and each column is sorted
/// in ascending order (staircase search).
///
/// Starts from the top-right corner:
/// - If current == target, found.
/// - If current > target, move left (eliminate column).
/// - If current < target, move down (eliminate row).
///
/// # Complexity
/// - Time:  O(m + n)
/// - Space: O(1)
fn search_sorted_matrix(matrix: &Matrix, target: i32) -> Option<(usize, usize)> {
    if matrix.is_empty() || matrix[0].is_empty() {
        return None;
    }

    let m = matrix.len();
    let n = matrix[0].len();
    let mut row = 0usize;
    let mut col = n - 1; // Start at top-right corner.

    loop {
        let val = matrix[row][col];
        if val == target {
            return Some((row, col));
        } else if val > target {
            if col == 0 {
                break;
            }
            col -= 1;
        } else {
            row += 1;
            if row >= m {
                break;
            }
        }
    }
    None
}

// ---------------------------------------------------------------------------
// Pascal's Triangle
// ---------------------------------------------------------------------------

/// Generates the first `n` rows of Pascal's triangle.
///
/// Each element is the sum of the two elements directly above it.
/// Row `k` has `k + 1` elements; the first and last are always 1.
///
/// # Complexity
/// - Time:  O(n^2)
/// - Space: O(n^2) — all rows stored
fn pascals_triangle(n: usize) -> Vec<Vec<i32>> {
    let mut triangle: Vec<Vec<i32>> = Vec::with_capacity(n);

    for i in 0..n {
        let mut row = vec![1i32; i + 1];
        // Fill interior elements using the previous row.
        for j in 1..i {
            row[j] = triangle[i - 1][j - 1] + triangle[i - 1][j];
        }
        triangle.push(row);
    }

    triangle
}

// ===========================================================================
// Helper: print matrix
// ===========================================================================

fn print_matrix(label: &str, matrix: &Matrix) {
    println!("{}:", label);
    for row in matrix {
        println!("  {:?}", row);
    }
}

// ===========================================================================
// Main — demonstrations and test assertions
// ===========================================================================

fn main() {
    println!("=== Week 10: Matrix ===\n");

    // --- Transpose ---
    println!("--- Transpose ---");
    let mut sq = vec![
        vec![1, 2, 3],
        vec![4, 5, 6],
        vec![7, 8, 9],
    ];
    transpose_square(&mut sq);
    assert_eq!(sq, vec![vec![1, 4, 7], vec![2, 5, 8], vec![3, 6, 9]]);
    print_matrix("Square transpose", &sq);

    let rect = vec![
        vec![1, 2, 3, 4],
        vec![5, 6, 7, 8],
    ];
    let rect_t = transpose_general(&rect);
    assert_eq!(rect_t, vec![vec![1, 5], vec![2, 6], vec![3, 7], vec![4, 8]]);
    print_matrix("General transpose (2x4 -> 4x2)", &rect_t);

    // --- Rotate 90 CW ---
    println!("\n--- Rotate 90 Degrees Clockwise ---");
    let mut mat = vec![
        vec![1, 2, 3],
        vec![4, 5, 6],
        vec![7, 8, 9],
    ];
    rotate_90_cw(&mut mat);
    assert_eq!(mat, vec![vec![7, 4, 1], vec![8, 5, 2], vec![9, 6, 3]]);
    print_matrix("Rotated 90 CW", &mat);

    // --- Matrix Multiply ---
    println!("\n--- Matrix Multiplication ---");
    let a = vec![
        vec![1, 2],
        vec![3, 4],
    ];
    let b = vec![
        vec![5, 6],
        vec![7, 8],
    ];
    let product = matrix_multiply(&a, &b);
    assert_eq!(product, vec![vec![19, 22], vec![43, 50]]);
    print_matrix("A * B", &product);

    // Non-square multiplication: (2x3) * (3x2) = (2x2)
    let c = vec![vec![1, 2, 3], vec![4, 5, 6]];
    let d = vec![vec![7, 8], vec![9, 10], vec![11, 12]];
    let cd = matrix_multiply(&c, &d);
    assert_eq!(cd, vec![vec![58, 64], vec![139, 154]]);
    print_matrix("C (2x3) * D (3x2)", &cd);

    // --- Spiral Order ---
    println!("\n--- Spiral Order ---");
    let spiral_mat = vec![
        vec![1,  2,  3,  4],
        vec![5,  6,  7,  8],
        vec![9,  10, 11, 12],
    ];
    let spiral = spiral_order(&spiral_mat);
    assert_eq!(spiral, vec![1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]);
    println!("Spiral: {:?}", spiral);

    // Square matrix
    let sq_mat = vec![
        vec![1, 2, 3],
        vec![4, 5, 6],
        vec![7, 8, 9],
    ];
    let spiral2 = spiral_order(&sq_mat);
    assert_eq!(spiral2, vec![1, 2, 3, 6, 9, 8, 7, 4, 5]);
    println!("Spiral (3x3): {:?}", spiral2);

    // --- Diagonal Order ---
    println!("\n--- Diagonal Order ---");
    let diag_mat = vec![
        vec![1, 2, 3],
        vec![4, 5, 6],
        vec![7, 8, 9],
    ];
    let diag = diagonal_order(&diag_mat);
    assert_eq!(diag, vec![1, 2, 4, 7, 5, 3, 6, 8, 9]);
    println!("Diagonal order: {:?}", diag);

    // --- Search Sorted Matrix ---
    println!("\n--- Search in Sorted Matrix ---");
    let sorted_mat = vec![
        vec![1,  4,  7,  11],
        vec![2,  5,  8,  12],
        vec![3,  6,  9,  16],
        vec![10, 13, 14, 17],
    ];
    assert_eq!(search_sorted_matrix(&sorted_mat, 5), Some((1, 1)));
    assert_eq!(search_sorted_matrix(&sorted_mat, 14), Some((3, 2)));
    assert_eq!(search_sorted_matrix(&sorted_mat, 20), None);
    println!("search(5)  = {:?}", search_sorted_matrix(&sorted_mat, 5));
    println!("search(14) = {:?}", search_sorted_matrix(&sorted_mat, 14));
    println!("search(20) = {:?}", search_sorted_matrix(&sorted_mat, 20));

    // --- Pascal's Triangle ---
    println!("\n--- Pascal's Triangle ---");
    let pascal = pascals_triangle(6);
    assert_eq!(pascal[0], vec![1]);
    assert_eq!(pascal[1], vec![1, 1]);
    assert_eq!(pascal[2], vec![1, 2, 1]);
    assert_eq!(pascal[3], vec![1, 3, 3, 1]);
    assert_eq!(pascal[4], vec![1, 4, 6, 4, 1]);
    assert_eq!(pascal[5], vec![1, 5, 10, 10, 5, 1]);
    println!("Pascal's triangle (6 rows):");
    for (i, row) in pascal.iter().enumerate() {
        // Indent for a triangle shape.
        let indent = " ".repeat((5 - i) * 2);
        let nums: Vec<String> = row.iter().map(|x| format!("{:>3}", x)).collect();
        println!("{}{}", indent, nums.join(" "));
    }

    println!("\nAll assertions passed!");
}
