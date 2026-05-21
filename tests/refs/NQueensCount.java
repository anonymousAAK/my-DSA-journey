/*
 * Reference Java implementation for tests/cases/n_queens_count.json.
 * Backtracking count of distinct n-queens placements.
 */
public class NQueensCount {
    private static int[] queens;
    private static int count;
    private static int N;

    private static boolean isSafe(int row, int col) {
        for (int r = 0; r < row; ++r) {
            int c = queens[r];
            if (c == col || Math.abs(c - col) == Math.abs(r - row)) return false;
        }
        return true;
    }

    private static void go(int row) {
        if (row == N) { count++; return; }
        for (int col = 0; col < N; ++col) {
            if (isSafe(row, col)) {
                queens[row] = col;
                go(row + 1);
                queens[row] = -1;
            }
        }
    }

    public static long nQueensCount(long n) {
        N = (int) n;
        count = 0;
        queens = new int[N];
        for (int i = 0; i < N; ++i) queens[i] = -1;
        if (N > 0) go(0);
        return count;
    }
}
