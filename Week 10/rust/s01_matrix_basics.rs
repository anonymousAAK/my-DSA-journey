/*
 * WEEK 10 - RUST DSA
 * Topic: Matrix Basics
 * File: 1.matrix_basics.rs
 *
 * CONCEPT:
 *     A 2D matrix as Vec<Vec<i32>>. Supports transpose (square in-place
 *     and general), row reverse, 90° CW/CCW rotation, naive multiply.
 *
 * KEY POINTS:
 *     - In-place transpose only works for square matrices.
 *     - 90° CW = transpose + reverse each row.
 *     - 90° CCW = reverse each row + transpose.
 *
 * ALGORITHM / APPROACH:
 *     See per-function code; same as Java/Python.
 *
 * RUST-SPECIFIC NOTES:
 *     - Use Vec<Vec<i32>> for the row-major matrix; a flat Vec<i32> with
 *       manual indexing is the cache-friendlier alternative.
 *     - .reverse() on a slice mutates in place.
 *     - For high-performance numeric work use the ndarray or nalgebra crates.
 *
 * DRY RUN:
 *     [[1,2,3],[4,5,6],[7,8,9]]
 *         transpose: [[1,4,7],[2,5,8],[3,6,9]]
 *         rotate CW: [[7,4,1],[8,5,2],[9,6,3]]
 *     [[1,2],[3,4]] x [[5,6],[7,8]] = [[19,22],[43,50]]
 *
 * COMPLEXITY:
 *     Transpose      : O(rows*cols)
 *     Rotation       : O(n^2)
 *     Multiplication : O(m*n*k)
 */

type Matrix = Vec<Vec<i32>>;

fn print_matrix(mat: &Matrix) {
    for row in mat {
        println!("{:?}", row);
    }
    println!();
}

fn transpose_square(mat: &mut Matrix) {
    let n = mat.len();
    for i in 0..n {
        for j in (i + 1)..n {
            let tmp = mat[i][j];
            mat[i][j] = mat[j][i];
            mat[j][i] = tmp;
        }
    }
}

fn transpose(mat: &Matrix) -> Matrix {
    let rows = mat.len();
    let cols = mat[0].len();
    let mut result: Matrix = vec![vec![0; rows]; cols];
    for i in 0..rows {
        for j in 0..cols {
            result[j][i] = mat[i][j];
        }
    }
    result
}

fn reverse_rows(mat: &mut Matrix) {
    for row in mat.iter_mut() {
        row.reverse();
    }
}

fn rotate_90_cw(mat: &mut Matrix) {
    transpose_square(mat);
    reverse_rows(mat);
}

fn rotate_90_ccw(mat: &mut Matrix) {
    reverse_rows(mat);
    transpose_square(mat);
}

fn multiply(a: &Matrix, b: &Matrix) -> Matrix {
    let m = a.len();
    let k = a[0].len();
    let n = b[0].len();
    let mut c: Matrix = vec![vec![0; n]; m];
    for i in 0..m {
        for j in 0..n {
            let mut sum = 0;
            for p in 0..k {
                sum += a[i][p] * b[p][j];
            }
            c[i][j] = sum;
        }
    }
    c
}

fn main() {
    let mat: Matrix = vec![
        vec![1, 2, 3],
        vec![4, 5, 6],
        vec![7, 8, 9],
    ];
    println!("Original:");
    print_matrix(&mat);

    let mut mat2 = mat.clone();
    transpose_square(&mut mat2);
    println!("Transposed (square, in-place):");
    print_matrix(&mat2);

    let non_square: Matrix = vec![vec![1, 2, 3], vec![4, 5, 6]];
    println!("Non-square (2x3):");
    print_matrix(&non_square);
    println!("Transposed (3x2):");
    print_matrix(&transpose(&non_square));

    let mut mat3 = mat.clone();
    rotate_90_cw(&mut mat3);
    println!("Rotated 90° CW:");
    print_matrix(&mat3);

    let a: Matrix = vec![vec![1, 2], vec![3, 4]];
    let b: Matrix = vec![vec![5, 6], vec![7, 8]];
    println!("A x B:");
    print_matrix(&multiply(&a, &b));

    // Rotate CCW demo
    let mut mat4 = mat.clone();
    rotate_90_ccw(&mut mat4);
    println!("Rotated 90° CCW:");
    print_matrix(&mat4);
}

/*
 * NOTES — Rust vs Java:
 *     - vec![vec![0; cols]; rows] avoids the aliasing trap that
 *       Python's [[0]*cols]*rows hits.
 *     - .reverse() on a slice/Vec mutates in place.
 *     - For real numeric work prefer the ndarray crate (cache-friendly,
 *       BLAS-backed multiplications).
 */
