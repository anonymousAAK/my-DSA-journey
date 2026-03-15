/*
 * WEEK 5 - FUNCTIONS & RECURSION
 * Topic: Tower of Hanoi
 *
 * PROBLEM:
 * Given 3 rods (Source, Auxiliary, Destination) and N disks on Source
 * (largest at bottom, smallest at top), move all disks to Destination.
 *
 * RULES:
 * 1. Move only ONE disk at a time.
 * 2. A larger disk can NEVER be placed on a smaller disk.
 *
 * RECURSIVE INSIGHT:
 * To move N disks from Source to Destination using Auxiliary:
 *   Step 1: Move top (N-1) disks from Source -> Auxiliary  (using Destination as helper)
 *   Step 2: Move the Nth (largest) disk from Source -> Destination
 *   Step 3: Move (N-1) disks from Auxiliary -> Destination (using Source as helper)
 *
 * BASE CASE: N == 0 → do nothing. Or N == 1 → move directly.
 *
 * Time Complexity: O(2^n) — the minimum number of moves is 2^n - 1
 * Space Complexity: O(n) — recursion depth
 *
 * This problem CANNOT be solved more efficiently than O(2^n) moves.
 * It's a beautiful example of a problem where exponential is optimal!
 */

public class TowerOfHanoi {

    static int moveCount = 0;

    /**
     * Move n disks from 'source' to 'destination' using 'auxiliary'.
     */
    static void hanoi(int n, char source, char auxiliary, char destination) {
        if (n == 0) return; // base case: no disks to move

        // Step 1: Move n-1 disks from source to auxiliary
        hanoi(n - 1, source, destination, auxiliary);

        // Step 2: Move the nth disk from source to destination
        moveCount++;
        System.out.println("Move disk " + n + ": " + source + " -> " + destination);

        // Step 3: Move n-1 disks from auxiliary to destination
        hanoi(n - 1, auxiliary, source, destination);
    }

    public static void main(String[] args) {
        System.out.println("=== Tower of Hanoi: 3 Disks ===");
        moveCount = 0;
        hanoi(3, 'A', 'B', 'C');
        System.out.println("Total moves for 3 disks: " + moveCount);
        System.out.println("Expected: " + ((int)Math.pow(2, 3) - 1));

        System.out.println("\n=== Tower of Hanoi: 4 Disks ===");
        moveCount = 0;
        hanoi(4, 'A', 'B', 'C');
        System.out.println("Total moves for 4 disks: " + moveCount);
        System.out.println("Expected: " + ((int)Math.pow(2, 4) - 1));

        // Show the exponential growth of move counts
        System.out.println("\n=== Move Counts by Disk Count ===");
        System.out.println("Disks | Moves | Formula (2^n - 1)");
        System.out.println("------+-------+------------------");
        for (int i = 1; i <= 20; i++) {
            long expected = (long)Math.pow(2, i) - 1;
            System.out.printf("  %2d  | %6d | %d%n", i, expected, expected);
        }
        System.out.println("\nAt n=64 disks: " + ((long)Math.pow(2, 64) - 1) + " moves!");
        System.out.println("That's 18.4 quintillion moves — even at 1 billion/sec, that's 585 years!");
    }
}
