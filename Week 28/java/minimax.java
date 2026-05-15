/*
 * WEEK 28 - JAVA ADVANCED TOPICS
 * Topic: Minimax (Zero-Sum Game Tree Search)
 * File: minimax.java
 *
 * CONCEPT:
 *     For a two-player, perfect-information, zero-sum game, minimax assigns
 *     a value v(s) to every state s representing the score the *maximising*
 *     player can guarantee against an optimally-playing *minimising*
 *     opponent. The recurrence:
 *
 *         v(s) = utility(s)                           if s is terminal
 *              = max over moves of v(child(s))        if Max to move
 *              = min over moves of v(child(s))        if Min to move
 *
 *     The depth-first traversal of the full game tree computes v(root).
 *
 * KEY POINTS:
 *     - Evaluates every reachable leaf -> O(b^d). Use alpha-beta to prune.
 *     - Memoisation (transposition table) helps when the same state is
 *       reachable by multiple move orderings.
 *     - For non-finite games use a depth limit + heuristic evaluator.
 *
 * ALGORITHM / APPROACH:
 *     minimax(state, maxTurn):
 *         if terminal(state): return utility(state)
 *         if maxTurn: return max over children of minimax(child, false)
 *         else:       return min over children of minimax(child, true)
 *
 * DRY RUN / EXAMPLE:
 *     Empty 3x3 tic-tac-toe with X to move -> minimax returns 0 (draw with
 *     optimal play). Best opening grabs the centre (or any corner).
 *
 * COMPLEXITY:
 *     Time:  O(b^d) without pruning; here d <= 9 for TTT -> ~360k positions.
 *     Space: O(d) recursion; O(|states|) when memoised.
 */

// snake_case filename is fine; class Minimax is package-private.

import java.util.HashMap;
import java.util.Map;

class Minimax {

    static final int[][] LINES = {
        {0, 1, 2}, {3, 4, 5}, {6, 7, 8},
        {0, 3, 6}, {1, 4, 7}, {2, 5, 8},
        {0, 4, 8}, {2, 4, 6}
    };

    static char winner(char[] board) {
        for (int[] line : LINES) {
            char a = board[line[0]];
            if (a != '.' && a == board[line[1]] && a == board[line[2]]) return a;
        }
        return 0;
    }

    static boolean isFull(char[] board) {
        for (char c : board) if (c == '.') return false;
        return true;
    }

    static int utility(char[] board) {
        char w = winner(board);
        if (w == 'X') return +1;
        if (w == 'O') return -1;
        return 0;
    }

    // Memoisation cache keyed by board string and side to move.
    static Map<String, Integer> memo = new HashMap<>();

    static int minimax(char[] board, boolean maxTurn) {
        char w = winner(board);
        if (w != 0 || isFull(board)) return utility(board);

        String key = new String(board) + (maxTurn ? 'X' : 'O');
        Integer cached = memo.get(key);
        if (cached != null) return cached;

        int best = maxTurn ? -2 : +2;
        char mark = maxTurn ? 'X' : 'O';
        for (int i = 0; i < 9; i++) {
            if (board[i] != '.') continue;
            board[i] = mark;
            int v = minimax(board, !maxTurn);
            board[i] = '.';
            if (maxTurn) best = Math.max(best, v);
            else         best = Math.min(best, v);
        }
        memo.put(key, best);
        return best;
    }

    /** Returns the optimal move index (0..8) for the side to move. */
    static int bestMove(char[] board, boolean maxTurn) {
        int bestIdx = -1;
        int bestVal = maxTurn ? -3 : +3;
        char mark = maxTurn ? 'X' : 'O';
        for (int i = 0; i < 9; i++) {
            if (board[i] != '.') continue;
            board[i] = mark;
            int v = minimax(board, !maxTurn);
            board[i] = '.';
            if (maxTurn && v > bestVal) { bestVal = v; bestIdx = i; }
            if (!maxTurn && v < bestVal) { bestVal = v; bestIdx = i; }
        }
        return bestIdx;
    }

    public static void main(String[] args) {
        char[] empty = "........." .toCharArray();
        System.out.println("Minimax value of empty TTT (X to move): " + minimax(empty, true));
        System.out.println("Best opening move for X: cell " + bestMove(empty, true));

        // X already in a corner -> minimax value still 0 against optimal O.
        char[] board = "X........".toCharArray();
        System.out.println("After X corner, minimax value: " + minimax(board, false));
    }
}

/*
 * NOTES
 * -----
 * Differences from the Python implementation in minimax.py:
 *   - Python uses tuples + @lru_cache; Java memoises via a HashMap keyed by
 *     the board string + side-to-move character.
 *   - We mutate a single char[] board in/out, which is faster than rebuilding
 *     immutable tuples on every recursive call.
 *   - The companion game_theory.java does NOT cover minimax; this file fills
 *     the gap, mirroring the Python and C++ splits.
 */
