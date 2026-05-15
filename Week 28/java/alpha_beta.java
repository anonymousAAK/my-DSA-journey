/*
 * WEEK 28 - JAVA ADVANCED TOPICS
 * Topic: Alpha-Beta Pruning
 * File: alpha_beta.java
 *
 * CONCEPT:
 *     Alpha-beta pruning enhances minimax: as we explore the game tree we
 *     maintain a window [alpha, beta] where alpha is the best already-
 *     guaranteed value for Max and beta the best for Min. When a node's
 *     value falls outside this window we prune the remaining children
 *     because they cannot influence the parent's choice.
 *
 *     Same value as minimax but with a much smaller effective branching
 *     factor. With perfect move ordering the time complexity drops from
 *     O(b^d) to O(b^(d/2)) -- effectively double the search depth.
 *
 * KEY POINTS:
 *     - alpha = lower bound on Max's value at this node.
 *     - beta  = upper bound on Min's value at this node.
 *     - When alpha >= beta: prune (beta-cutoff at Max nodes, alpha-cutoff at
 *       Min nodes).
 *     - Move ordering is critical to realise the asymptotic speedup.
 *
 * ALGORITHM / APPROACH:
 *     ab(state, alpha, beta, maxTurn):
 *         if terminal: return utility(state)
 *         if maxTurn:
 *             v = -INF
 *             for child in moves: v = max(v, ab(child, alpha, beta, false))
 *                                 alpha = max(alpha, v)
 *                                 if alpha >= beta: break (beta cutoff)
 *             return v
 *         else:
 *             v = +INF
 *             for child: v = min(v, ab(child, alpha, beta, true))
 *                        beta = min(beta, v)
 *                        if alpha >= beta: break (alpha cutoff)
 *             return v
 *
 * DRY RUN / EXAMPLE:
 *     Empty TTT, X to move -> alpha-beta returns 0 like minimax but visits
 *     far fewer nodes. We expose a `nodeCount` counter to make the savings
 *     visible.
 *
 * COMPLEXITY:
 *     Time:  O(b^d) worst case; O(b^(d/2)) with good ordering.
 *     Space: O(d) recursion.
 */

// snake_case filename is fine; class AlphaBeta is package-private.

class AlphaBeta {

    static final int[][] LINES = {
        {0, 1, 2}, {3, 4, 5}, {6, 7, 8},
        {0, 3, 6}, {1, 4, 7}, {2, 5, 8},
        {0, 4, 8}, {2, 4, 6}
    };

    static int nodeCount = 0;

    static char winner(char[] board) {
        for (int[] line : LINES) {
            char a = board[line[0]];
            if (a != '.' && a == board[line[1]] && a == board[line[2]]) return a;
        }
        return 0;
    }

    static int utility(char[] board) {
        char w = winner(board);
        if (w == 'X') return +1;
        if (w == 'O') return -1;
        return 0;
    }

    static boolean isFull(char[] board) {
        for (char c : board) if (c == '.') return false;
        return true;
    }

    static int alphabeta(char[] board, int alpha, int beta, boolean maxTurn) {
        nodeCount++;
        char w = winner(board);
        if (w != 0 || isFull(board)) return utility(board);
        if (maxTurn) {
            int v = Integer.MIN_VALUE;
            for (int i = 0; i < 9; i++) {
                if (board[i] != '.') continue;
                board[i] = 'X';
                v = Math.max(v, alphabeta(board, alpha, beta, false));
                board[i] = '.';
                alpha = Math.max(alpha, v);
                if (alpha >= beta) break; // beta cutoff
            }
            return v;
        } else {
            int v = Integer.MAX_VALUE;
            for (int i = 0; i < 9; i++) {
                if (board[i] != '.') continue;
                board[i] = 'O';
                v = Math.min(v, alphabeta(board, alpha, beta, true));
                board[i] = '.';
                beta = Math.min(beta, v);
                if (alpha >= beta) break; // alpha cutoff
            }
            return v;
        }
    }

    static int bestMove(char[] board, boolean maxTurn) {
        int bestIdx = -1;
        int bestVal = maxTurn ? Integer.MIN_VALUE : Integer.MAX_VALUE;
        char mark = maxTurn ? 'X' : 'O';
        for (int i = 0; i < 9; i++) {
            if (board[i] != '.') continue;
            board[i] = mark;
            int v = alphabeta(board, Integer.MIN_VALUE, Integer.MAX_VALUE, !maxTurn);
            board[i] = '.';
            if (maxTurn && v > bestVal) { bestVal = v; bestIdx = i; }
            if (!maxTurn && v < bestVal) { bestVal = v; bestIdx = i; }
        }
        return bestIdx;
    }

    public static void main(String[] args) {
        char[] empty = ".........".toCharArray();
        nodeCount = 0;
        int val = alphabeta(empty, Integer.MIN_VALUE, Integer.MAX_VALUE, true);
        System.out.println("Alpha-beta value of empty TTT: " + val);
        System.out.println("Nodes explored: " + nodeCount);
        System.out.println("Best opening move for X: cell " + bestMove(empty, true));
    }
}

/*
 * NOTES
 * -----
 * Differences from the Python implementation in alpha_beta.py:
 *   - Java uses Integer.MIN_VALUE / Integer.MAX_VALUE in place of math.inf.
 *   - We mutate a single char[] board for speed; Python uses immutable
 *     tuples.
 *   - The companion game_theory.java does NOT cover alpha-beta; this file
 *     fills the gap mirroring the Python / C++ / Rust splits.
 */
