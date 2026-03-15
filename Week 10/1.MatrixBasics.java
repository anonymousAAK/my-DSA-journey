/*
 * WEEK 10 - 2D ARRAYS & MATRIX
 * Topic: Matrix Basics — Traversal, Transpose, Rotation
 *
 * A 2D array (matrix) is an array of arrays: int[][] mat = new int[rows][cols]
 * Element at row i, column j: mat[i][j]
 *
 * COVERED:
 * 1. Declare, initialize, print a matrix
 * 2. Transpose: swap rows and columns
 *    mat[i][j] → mat[j][i]
 *    Time: O(n²), Space: O(1) for square matrix
 * 3. Rotate 90° clockwise (in-place for square matrix):
 *    Step 1: Transpose
 *    Step 2: Reverse each row
 *    Time: O(n²), Space: O(1)
 * 4. Matrix multiplication: C = A × B
 *    C[i][j] = sum over k of A[i][k] * B[k][j]
 *    Time: O(n³) naive, O(n^2.37) with Strassen/Coppersmith-Winograd
 */

import java.util.Arrays;

public class MatrixBasics {

    static void printMatrix(int[][] mat) {
        for (int[] row : mat) System.out.println(Arrays.toString(row));
        System.out.println();
    }

    // Transpose (in-place for square matrix)
    static void transposeSquare(int[][] mat) {
        int n = mat.length;
        for (int i = 0; i < n; i++)
            for (int j = i + 1; j < n; j++) {
                int temp = mat[i][j];
                mat[i][j] = mat[j][i];
                mat[j][i] = temp;
            }
    }

    // Transpose for non-square matrix (returns new matrix)
    static int[][] transpose(int[][] mat) {
        int rows = mat.length, cols = mat[0].length;
        int[][] result = new int[cols][rows];
        for (int i = 0; i < rows; i++)
            for (int j = 0; j < cols; j++)
                result[j][i] = mat[i][j];
        return result;
    }

    // Reverse each row
    static void reverseRows(int[][] mat) {
        for (int[] row : mat) {
            int l = 0, r = row.length - 1;
            while (l < r) { int t = row[l]; row[l] = row[r]; row[r] = t; l++; r--; }
        }
    }

    // Rotate 90° clockwise (in-place, square matrix)
    static void rotate90CW(int[][] mat) {
        transposeSquare(mat);
        reverseRows(mat);
    }

    // Rotate 90° counter-clockwise
    static void rotate90CCW(int[][] mat) {
        reverseRows(mat);
        transposeSquare(mat);
    }

    // Matrix multiplication: A (m×k) × B (k×n) → C (m×n)
    static int[][] multiply(int[][] A, int[][] B) {
        int m = A.length, k = A[0].length, n = B[0].length;
        int[][] C = new int[m][n];
        for (int i = 0; i < m; i++)
            for (int j = 0; j < n; j++)
                for (int p = 0; p < k; p++)
                    C[i][j] += A[i][p] * B[p][j];
        return C;
    }

    public static void main(String[] args) {
        int[][] mat = {
            {1, 2, 3},
            {4, 5, 6},
            {7, 8, 9}
        };

        System.out.println("Original:");
        printMatrix(mat);

        int[][] mat2 = {
            {1, 2, 3},
            {4, 5, 6},
            {7, 8, 9}
        };
        transposeSquare(mat2);
        System.out.println("Transposed (square, in-place):");
        printMatrix(mat2);

        int[][] nonSquare = {{1, 2, 3}, {4, 5, 6}};
        System.out.println("Non-square (2x3):");
        printMatrix(nonSquare);
        System.out.println("Transposed (3x2):");
        printMatrix(transpose(nonSquare));

        int[][] mat3 = {
            {1, 2, 3},
            {4, 5, 6},
            {7, 8, 9}
        };
        rotate90CW(mat3);
        System.out.println("Rotated 90° CW:");
        printMatrix(mat3);
        // Expected:
        // [7, 4, 1]
        // [8, 5, 2]
        // [9, 6, 3]

        // Matrix multiplication
        int[][] A = {{1, 2}, {3, 4}};
        int[][] B = {{5, 6}, {7, 8}};
        System.out.println("A × B:");
        printMatrix(multiply(A, B));
        // [1*5+2*7, 1*6+2*8] = [19, 22]
        // [3*5+4*7, 3*6+4*8] = [43, 50]
    }
}
