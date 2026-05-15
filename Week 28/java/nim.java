/*
 * WEEK 28 - JAVA ADVANCED TOPICS
 * Topic: Nim Game (Bouton's Theorem)
 * File: nim.java
 *
 * CONCEPT:
 *     The game of Nim is the prototypical impartial combinatorial game.
 *     Two players alternate; on each turn, the current player removes any
 *     positive number of stones from exactly one of several piles. The
 *     player unable to move loses (normal play convention).
 *
 *     BOUTON'S THEOREM (1901):
 *         The first player wins iff the XOR of all pile sizes is non-zero.
 *
 *     Intuition: pile sizes in binary, XOR=0 means each bit position has an
 *     even number of 1's. Any move flips at least one bit, so from XOR=0
 *     every move leads to a non-zero state (losing for opponent); from any
 *     non-zero state there exists a move back to XOR=0.
 *
 * KEY POINTS:
 *     - Winning strategy: pick a pile whose XOR with the running XOR is
 *       smaller, reduce that pile to the XOR value.
 *     - Sprague-Grundy theory generalises Nim's XOR rule to arbitrary
 *       impartial games via Grundy numbers.
 *
 * ALGORITHM / APPROACH:
 *     xorSum = XOR of all pile sizes
 *     if xorSum == 0: second player wins
 *     else:
 *         for each pile p:
 *             target = p XOR xorSum
 *             if target < p: winning move is reducing that pile to target
 *
 * DRY RUN / EXAMPLE:
 *     piles = {3, 4, 5}
 *     XOR = 3 ^ 4 ^ 5 = 0b011 ^ 0b100 ^ 0b101 = 0b010 = 2 -> first wins.
 *     Find p with (p XOR 2) < p: 3 XOR 2 = 1 < 3, so reduce pile 0 to 1.
 *
 * COMPLEXITY:
 *     Time:  O(n).
 *     Space: O(1).
 */

// snake_case filename is fine; class Nim is package-private.

class Nim {

    static String nimWinner(int[] piles) {
        int xor = 0;
        for (int p : piles) xor ^= p;
        return xor != 0 ? "First" : "Second";
    }

    /** Returns {pileIndex, newSize} for a winning move; null if losing. */
    static int[] nimWinningMove(int[] piles) {
        int xor = 0;
        for (int p : piles) xor ^= p;
        if (xor == 0) return null;
        for (int i = 0; i < piles.length; i++) {
            int target = piles[i] ^ xor;
            if (target < piles[i]) return new int[]{i, target};
        }
        return null; // unreachable when xor != 0
    }

    public static void main(String[] args) {
        int[] piles = {3, 4, 5};
        System.out.println("Piles [3,4,5]: winner = " + nimWinner(piles));
        int[] move = nimWinningMove(piles);
        if (move != null) {
            System.out.println("Winning move: reduce pile " + move[0]
                + " from " + piles[move[0]] + " to " + move[1]);
        }

        int[] piles2 = {1, 2, 3};
        System.out.println("Piles [1,2,3]: winner = " + nimWinner(piles2));
        System.out.println("Winning move: " + (nimWinningMove(piles2) == null ? "none (losing)" : "exists"));
    }
}

/*
 * NOTES
 * -----
 * Differences from the Python implementation in nim.py:
 *   - Python uses functools.reduce(xor, piles, 0); Java uses a plain for-each
 *     loop, equally idiomatic.
 *   - Java returns int[] with {pileIndex, newSize}; Python returns a tuple
 *     or None.
 *   - The companion game_theory.java only covers nimWinner; this file adds
 *     the constructive winning-move helper for parity with the Python split.
 */
