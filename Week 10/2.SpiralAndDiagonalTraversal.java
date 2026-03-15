/*
 * WEEK 10 - 2D ARRAYS & MATRIX
 * Topic: Spiral Traversal & Diagonal Traversal
 *
 * SPIRAL TRAVERSAL:
 * Traverse matrix in spiral order: right → down → left → up → repeat.
 * Use four boundaries: top, bottom, left, right.
 * Shrink boundaries as you go.
 * Time: O(m*n), Space: O(1) extra (or O(m*n) for result list)
 *
 * DIAGONAL TRAVERSAL:
 * Print all diagonals of a matrix (anti-diagonals: direction toggles).
 * Time: O(m*n), Space: O(1)
 *
 * SEARCH IN ROW-AND-COLUMN SORTED MATRIX:
 * Matrix where each row and column is sorted.
 * Start at top-right corner:
 * - If element == target: found!
 * - If element > target: move left (eliminate column)
 * - If element < target: move down (eliminate row)
 * Time: O(m + n), much better than O(m*n) brute force
 */

import java.util.ArrayList;
import java.util.List;

public class SpiralAndDiagonalTraversal {

    // Spiral order traversal
    static List<Integer> spiralOrder(int[][] mat) {
        List<Integer> result = new ArrayList<>();
        if (mat == null || mat.length == 0) return result;
        int top = 0, bottom = mat.length - 1;
        int left = 0, right = mat[0].length - 1;

        while (top <= bottom && left <= right) {
            // Traverse right
            for (int i = left; i <= right; i++) result.add(mat[top][i]);
            top++;
            // Traverse down
            for (int i = top; i <= bottom; i++) result.add(mat[i][right]);
            right--;
            // Traverse left (if still valid)
            if (top <= bottom) {
                for (int i = right; i >= left; i--) result.add(mat[bottom][i]);
                bottom--;
            }
            // Traverse up (if still valid)
            if (left <= right) {
                for (int i = bottom; i >= top; i--) result.add(mat[i][left]);
                left++;
            }
        }
        return result;
    }

    // Diagonal (anti-diagonal zigzag) traversal
    static int[] diagonalOrder(int[][] mat) {
        int m = mat.length, n = mat[0].length;
        int[] result = new int[m * n];
        int idx = 0;
        for (int d = 0; d < m + n - 1; d++) {
            if (d % 2 == 0) { // going up
                int r = Math.min(d, m - 1);
                int c = d - r;
                while (r >= 0 && c < n) result[idx++] = mat[r--][c++];
            } else { // going down
                int c = Math.min(d, n - 1);
                int r = d - c;
                while (c >= 0 && r < m) result[idx++] = mat[r++][c--];
            }
        }
        return result;
    }

    // Search in row-and-column sorted matrix
    static boolean searchSortedMatrix(int[][] mat, int target) {
        int row = 0, col = mat[0].length - 1; // start at top-right
        while (row < mat.length && col >= 0) {
            if (mat[row][col] == target) return true;
            else if (mat[row][col] > target) col--; // too big, go left
            else row++;                              // too small, go down
        }
        return false;
    }

    public static void main(String[] args) {
        int[][] mat = {
            {1,  2,  3,  4},
            {5,  6,  7,  8},
            {9, 10, 11, 12}
        };

        System.out.println("Matrix:");
        for (int[] row : mat) System.out.println(java.util.Arrays.toString(row));

        System.out.println("\nSpiral order: " + spiralOrder(mat));
        // Expected: [1,2,3,4,8,12,11,10,9,5,6,7]

        int[][] sq = {{1,2,3},{4,5,6},{7,8,9}};
        System.out.println("\nSquare matrix:");
        for (int[] row : sq) System.out.println(java.util.Arrays.toString(row));
        System.out.println("Spiral: " + spiralOrder(sq));
        System.out.println("Diagonal: " + java.util.Arrays.toString(diagonalOrder(sq)));
        // Expected diagonal: [1,2,4,7,5,3,6,8,9]

        // Search in sorted matrix
        int[][] sorted = {
            { 1,  4,  7, 11, 15},
            { 2,  5,  8, 12, 19},
            { 3,  6,  9, 16, 22},
            {10, 13, 14, 17, 24},
            {18, 21, 23, 26, 30}
        };
        System.out.println("\nSearch in sorted matrix:");
        System.out.println("Search 5:  " + searchSortedMatrix(sorted, 5));   // true
        System.out.println("Search 20: " + searchSortedMatrix(sorted, 20));  // false
        System.out.println("Search 1:  " + searchSortedMatrix(sorted, 1));   // true
        System.out.println("Search 30: " + searchSortedMatrix(sorted, 30));  // true
    }
}
