/*
 * WEEK 28 - JAVA ADVANCED TOPICS
 * Topic: Sprague-Grundy Theorem and Grundy Numbers
 * File: sprague_grundy.java
 *
 * CONCEPT:
 *     The Sprague-Grundy theorem generalises Bouton's rule for Nim: every
 *     impartial game (no draws, no chance, both players have the same legal
 *     moves from any position) is equivalent to a single Nim pile whose
 *     size equals the position's Grundy number. The Grundy number g(s) is:
 *
 *         g(s) = mex { g(s') : s' is a position reachable from s in one move }
 *
 *     where `mex` is the minimum excludant -- the smallest non-negative
 *     integer not present in the set.
 *
 *     For a sum of independent games, the overall Grundy value is the XOR
 *     of the components, so the position is losing for the player to move
 *     iff the XOR is 0.
 *
 * KEY POINTS:
 *     - Analyses subtraction games, Nim variants, green-Hackenbush trees,
 *       Wythoff, etc.
 *     - Memoisation is crucial; many recursions revisit the same state.
 *     - mex(S) runs in O(|S|) by counting from 0.
 *
 * ALGORITHM / APPROACH:
 *     grundy(state):
 *         if no moves: return 0
 *         reachable = { grundy(child) for child in moves(state) }
 *         return mex(reachable)
 *
 * DRY RUN / EXAMPLE:
 *     Subtraction game: from n stones, remove 1, 3, or 4. Grundy(n):
 *         g(0)=0
 *         g(1)=mex{g(0)}=mex{0}=1
 *         g(2)=mex{g(1)}=mex{1}=0
 *         g(3)=mex{g(2),g(0)}=mex{0,0}=1
 *         g(4)=mex{g(3),g(1),g(0)}=mex{1,1,0}=2
 *         g(5)=mex{g(4),g(2),g(1)}=mex{2,0,1}=3
 *         g(6)=mex{g(5),g(3),g(2)}=mex{3,1,0}=2
 *         ...
 *         g(10)=1.
 *
 * COMPLEXITY:
 *     Time:  O(n * |moves|) for a one-pile subtraction game up to n.
 *     Space: O(n).
 */

// snake_case filename is fine; class SpragueGrundy is package-private.

import java.util.HashSet;
import java.util.Set;

class SpragueGrundy {

    static int mex(Set<Integer> values) {
        int m = 0;
        while (values.contains(m)) m++;
        return m;
    }

    /** Grundy number of a one-pile subtraction game with given allowed moves. */
    static int grundySubtraction(int n, int[] moves) {
        int[] g = new int[n + 1];
        for (int i = 1; i <= n; i++) {
            Set<Integer> reachable = new HashSet<>();
            for (int m : moves) if (i - m >= 0) reachable.add(g[i - m]);
            g[i] = mex(reachable);
        }
        return g[n];
    }

    /** Multi-pile subtraction game: XOR Grundy values; true iff first player wins. */
    static boolean firstPlayerWins(int[] positions, int[] moves) {
        if (positions.length == 0) return false;
        int maxPos = 0;
        for (int p : positions) maxPos = Math.max(maxPos, p);
        int[] g = new int[maxPos + 1];
        for (int i = 1; i <= maxPos; i++) {
            Set<Integer> reachable = new HashSet<>();
            for (int m : moves) if (i - m >= 0) reachable.add(g[i - m]);
            g[i] = mex(reachable);
        }
        int xor = 0;
        for (int p : positions) xor ^= g[p];
        return xor != 0;
    }

    public static void main(String[] args) {
        int[] moves = {1, 3, 4};
        System.out.println("Grundy table for subtraction moves {1,3,4}:");
        for (int i = 0; i <= 10; i++) {
            System.out.println("  g(" + i + ") = " + grundySubtraction(i, moves));
        }
        System.out.println("\ngrundy(10) = " + grundySubtraction(10, moves));
        int[] positions = {10, 6};
        System.out.println("Two piles [10, 6]: first player wins? "
            + firstPlayerWins(positions, moves));
    }
}

/*
 * NOTES
 * -----
 * Differences from the Python implementation in sprague_grundy.py:
 *   - Java uses HashSet<Integer> for reachable values; Python used set
 *     comprehensions.
 *   - The companion game_theory.java only has grundy(); we add a multi-pile
 *     XOR wrapper firstPlayerWins() to mirror the Python split.
 *   - No @lru_cache equivalent here; we just pre-fill the int[] table.
 */
