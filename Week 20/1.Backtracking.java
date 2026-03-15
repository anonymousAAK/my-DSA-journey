/*
 * WEEK 20 - BACKTRACKING
 * Topic: Backtracking Template + Classic Problems
 *
 * BACKTRACKING:
 * Build a solution incrementally, step by step.
 * At each step, if the current partial solution cannot lead to a valid complete solution,
 * ABANDON it and backtrack to try other options.
 *
 * TEMPLATE:
 * void backtrack(State state) {
 *     if (isSolution(state)) { recordSolution(); return; }
 *     for (choice : getChoices(state)) {
 *         if (isValid(choice, state)) {
 *             makeChoice(choice, state);   // explore
 *             backtrack(state);
 *             undoChoice(choice, state);   // backtrack
 *         }
 *     }
 * }
 *
 * KEY: The "undo" step is what makes backtracking different from simple DFS.
 *
 * Time complexity: Usually exponential in the worst case (O(k^n) or O(n!)).
 * Pruning reduces the practical runtime significantly.
 *
 * PROBLEMS COVERED:
 * 1. Permutations of a list of numbers
 * 2. Subsets (power set)
 * 3. N-Queens
 * 4. Sudoku Solver
 * 5. Word Search in grid
 */

import java.util.*;

public class Backtracking {

    // PROBLEM 1: All Permutations
    // Time: O(n * n!), Space: O(n)
    static List<List<Integer>> permutations(int[] nums) {
        List<List<Integer>> result = new ArrayList<>();
        permute(nums, 0, result);
        return result;
    }
    static void permute(int[] nums, int start, List<List<Integer>> result) {
        if (start == nums.length) {
            List<Integer> perm = new ArrayList<>();
            for (int x : nums) perm.add(x);
            result.add(perm);
            return;
        }
        for (int i = start; i < nums.length; i++) {
            swap(nums, start, i);           // choose
            permute(nums, start + 1, result); // explore
            swap(nums, start, i);           // unchoose (backtrack)
        }
    }
    static void swap(int[] nums, int i, int j) { int t = nums[i]; nums[i] = nums[j]; nums[j] = t; }

    // PROBLEM 2: All Subsets (Power Set)
    // Time: O(2^n * n), Space: O(n)
    static List<List<Integer>> subsets(int[] nums) {
        List<List<Integer>> result = new ArrayList<>();
        subsetsHelper(nums, 0, new ArrayList<>(), result);
        return result;
    }
    static void subsetsHelper(int[] nums, int idx, List<Integer> current, List<List<Integer>> result) {
        result.add(new ArrayList<>(current)); // add current subset
        for (int i = idx; i < nums.length; i++) {
            current.add(nums[i]);           // include nums[i]
            subsetsHelper(nums, i + 1, current, result);
            current.remove(current.size() - 1); // exclude nums[i] (backtrack)
        }
    }

    // PROBLEM 3: N-Queens
    // Place N queens on NxN board such that no two queens attack each other.
    // Time: O(N!), Space: O(N)
    static List<List<String>> nQueens(int n) {
        List<List<String>> result = new ArrayList<>();
        int[] queens = new int[n]; // queens[row] = column of queen in that row
        Arrays.fill(queens, -1);
        nQueensHelper(queens, 0, n, result);
        return result;
    }
    static void nQueensHelper(int[] queens, int row, int n, List<List<String>> result) {
        if (row == n) { result.add(buildBoard(queens, n)); return; }
        for (int col = 0; col < n; col++) {
            if (isSafe(queens, row, col)) {
                queens[row] = col;
                nQueensHelper(queens, row + 1, n, result);
                queens[row] = -1; // backtrack
            }
        }
    }
    static boolean isSafe(int[] queens, int row, int col) {
        for (int r = 0; r < row; r++) {
            if (queens[r] == col) return false; // same column
            if (Math.abs(queens[r] - col) == Math.abs(r - row)) return false; // diagonal
        }
        return true;
    }
    static List<String> buildBoard(int[] queens, int n) {
        List<String> board = new ArrayList<>();
        for (int row = 0; row < n; row++) {
            char[] line = new char[n];
            Arrays.fill(line, '.');
            line[queens[row]] = 'Q';
            board.add(new String(line));
        }
        return board;
    }

    // PROBLEM 4: Word Search in Grid
    // Find if word exists in grid by traversing adjacent cells (up/down/left/right).
    static boolean wordSearch(char[][] board, String word) {
        int m = board.length, n = board[0].length;
        for (int i = 0; i < m; i++)
            for (int j = 0; j < n; j++)
                if (wordDFS(board, word, i, j, 0)) return true;
        return false;
    }
    static boolean wordDFS(char[][] board, String word, int i, int j, int k) {
        if (k == word.length()) return true;
        if (i < 0 || i >= board.length || j < 0 || j >= board[0].length) return false;
        if (board[i][j] != word.charAt(k)) return false;
        char temp = board[i][j];
        board[i][j] = '#'; // mark as visited
        boolean found = wordDFS(board, word, i+1, j, k+1)
                     || wordDFS(board, word, i-1, j, k+1)
                     || wordDFS(board, word, i, j+1, k+1)
                     || wordDFS(board, word, i, j-1, k+1);
        board[i][j] = temp; // restore (backtrack)
        return found;
    }

    public static void main(String[] args) {
        // Permutations
        System.out.println("=== Permutations of [1,2,3] ===");
        List<List<Integer>> perms = permutations(new int[]{1, 2, 3});
        perms.forEach(System.out::println);

        // Subsets
        System.out.println("\n=== Subsets of [1,2,3] ===");
        subsets(new int[]{1, 2, 3}).forEach(System.out::println);

        // N-Queens
        System.out.println("\n=== 4-Queens Solutions ===");
        List<List<String>> solutions = nQueens(4);
        System.out.println("Number of solutions: " + solutions.size());
        for (List<String> sol : solutions) {
            sol.forEach(System.out::println);
            System.out.println("---");
        }

        // Word Search
        System.out.println("=== Word Search ===");
        char[][] grid = {
            {'A','B','C','E'},
            {'S','F','C','S'},
            {'A','D','E','E'}
        };
        System.out.println("Search 'ABCCED': " + wordSearch(grid, "ABCCED")); // true
        System.out.println("Search 'SEE': " + wordSearch(grid, "SEE"));       // true
        System.out.println("Search 'ABCB': " + wordSearch(grid, "ABCB"));     // false (can't reuse)
    }
}
