/*
 * WEEK 10 - RUST DSA
 * Topic: Spiral & Diagonal Traversal + Sorted-Matrix Search
 * File: 2.spiral_and_diagonal_traversal.rs
 *
 * CONCEPT:
 *     Spiral: walk the perimeter inward, shrinking four boundaries.
 *     Diagonal: alternate direction per anti-diagonal index.
 *     Sorted-matrix search: top-right corner walk in O(m + n).
 *
 * KEY POINTS:
 *     - Spiral needs four boundary integers.
 *     - Diagonal uses i64 for the start coordinates to avoid usize underflow
 *       on the downward-going branch.
 *     - Sorted search eliminates a row or column per step.
 *
 * ALGORITHM / APPROACH:
 *     See per-function code; identical to Java/Python.
 *
 * RUST-SPECIFIC NOTES:
 *     - Vec<i32> for output.
 *     - Loop ranges (i..=j) are inclusive; (i..j).rev() iterates descending.
 *     - i64 for boundary trackers makes "high = -1" safe.
 *
 * DRY RUN:
 *     Spiral on 3x4 -> [1,2,3,4,8,12,11,10,9,5,6,7]
 *     Diagonal on 3x3 -> [1, 2,4, 7,5,3, 6,8, 9]
 *     Sorted search of 5 in the 5x5 sample -> true.
 *
 * COMPLEXITY:
 *     Spiral / Diagonal: O(m*n).
 *     Sorted search    : O(m + n).
 */

type Matrix = Vec<Vec<i32>>;

fn spiral_order(mat: &Matrix) -> Vec<i32> {
    let mut result: Vec<i32> = Vec::new();
    if mat.is_empty() || mat[0].is_empty() {
        return result;
    }
    let mut top: i64 = 0;
    let mut bottom: i64 = mat.len() as i64 - 1;
    let mut left: i64 = 0;
    let mut right: i64 = mat[0].len() as i64 - 1;
    while top <= bottom && left <= right {
        // right along top row
        for i in left..=right {
            result.push(mat[top as usize][i as usize]);
        }
        top += 1;
        // down along right column
        for i in top..=bottom {
            result.push(mat[i as usize][right as usize]);
        }
        right -= 1;
        // left along bottom row
        if top <= bottom {
            let mut i = right;
            while i >= left {
                result.push(mat[bottom as usize][i as usize]);
                i -= 1;
            }
            bottom -= 1;
        }
        // up along left column
        if left <= right {
            let mut i = bottom;
            while i >= top {
                result.push(mat[i as usize][left as usize]);
                i -= 1;
            }
            left += 1;
        }
    }
    result
}

fn diagonal_order(mat: &Matrix) -> Vec<i32> {
    let m = mat.len() as i64;
    let n = mat[0].len() as i64;
    let mut result: Vec<i32> = Vec::with_capacity((m * n) as usize);
    for d in 0..(m + n - 1) {
        if d % 2 == 0 {
            // going up
            let mut r = std::cmp::min(d, m - 1);
            let mut c = d - r;
            while r >= 0 && c < n {
                result.push(mat[r as usize][c as usize]);
                r -= 1;
                c += 1;
            }
        } else {
            // going down
            let mut c = std::cmp::min(d, n - 1);
            let mut r = d - c;
            while c >= 0 && r < m {
                result.push(mat[r as usize][c as usize]);
                r += 1;
                c -= 1;
            }
        }
    }
    result
}

fn search_sorted_matrix(mat: &Matrix, target: i32) -> bool {
    if mat.is_empty() || mat[0].is_empty() {
        return false;
    }
    let rows = mat.len() as i64;
    let mut row: i64 = 0;
    let mut col: i64 = mat[0].len() as i64 - 1;
    while row < rows && col >= 0 {
        let v = mat[row as usize][col as usize];
        if v == target {
            return true;
        } else if v > target {
            col -= 1;
        } else {
            row += 1;
        }
    }
    false
}

fn main() {
    let mat: Matrix = vec![
        vec![1, 2, 3, 4],
        vec![5, 6, 7, 8],
        vec![9, 10, 11, 12],
    ];
    println!("Matrix:");
    for row in &mat {
        println!("{:?}", row);
    }
    println!("\nSpiral order: {:?}", spiral_order(&mat));

    let sq: Matrix = vec![
        vec![1, 2, 3],
        vec![4, 5, 6],
        vec![7, 8, 9],
    ];
    println!("\nSquare matrix:");
    for row in &sq {
        println!("{:?}", row);
    }
    println!("Spiral:   {:?}", spiral_order(&sq));
    println!("Diagonal: {:?}", diagonal_order(&sq));

    let sorted: Matrix = vec![
        vec![1, 4, 7, 11, 15],
        vec![2, 5, 8, 12, 19],
        vec![3, 6, 9, 16, 22],
        vec![10, 13, 14, 17, 24],
        vec![18, 21, 23, 26, 30],
    ];
    println!("\nSearch in sorted matrix:");
    println!("Search 5:  {}", search_sorted_matrix(&sorted, 5));
    println!("Search 20: {}", search_sorted_matrix(&sorted, 20));
    println!("Search 1:  {}", search_sorted_matrix(&sorted, 1));
    println!("Search 30: {}", search_sorted_matrix(&sorted, 30));
}

/*
 * NOTES — Rust vs Java:
 *     - Use i64 for boundary trackers; usize underflows would panic.
 *     - .rev() on a Range iterator is ergonomic but doesn't allow inclusive
 *       descend through 0 across usize boundaries, so we use a manual while.
 *     - For numeric workloads, the ndarray crate provides idiomatic slicing.
 */
