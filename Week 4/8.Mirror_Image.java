/*
 * WEEK 4 - PATTERN PROBLEMS
 * Topic: Mirror Image Number Pattern
 * File: 8.Mirror_Image.java
 *
 * PATTERN (for N=4):
 *    1
 *   12
 *  123
 * 1234
 * (dots/spaces replaced with actual spaces for right-alignment)
 *
 * CONCEPT:
 * Print a right-aligned triangle of ascending numbers. Each row i
 * contains numbers 1 through i, preceded by (N - i) leading spaces
 * to push the numbers to the right, creating a mirror-image effect.
 *
 * APPROACH:
 * - Outer loop: controls rows (currRow = 1 to N)
 * - First inner loop: prints (N - currRow) spaces for right-alignment
 * - Second inner loop: prints numbers 1 to currRow
 *
 * KEY INSIGHT:
 * This pattern requires TWO inner loops per row: one for leading spaces
 * and one for the numbers. The space count decreases as the row number
 * increases (N - currRow spaces), while the number count increases,
 * keeping the total width constant at N characters per row.
 *
 * Time Complexity: O(N^2) — nested loops
 * Space Complexity: O(1) — no extra data structures
 */
import java.util.Scanner;

public class Solution {

  public static void main(String[] args) {
    Scanner s = new Scanner(System.in);
    int n = s.nextInt();
    // Outer loop: iterate through each row (1 to N)
    int currRow = 1;
    while (currRow <= n) {
      int currCol = 1;
      // First inner loop: print (N - currRow) leading spaces for right-alignment
      int spaces = 1;
      while (spaces <= n - currRow) {
        System.out.print(“ “);
        spaces += 1;
      }
      // Second inner loop: print numbers 1 to currRow in ascending order
      while (currCol <= currRow) {
        System.out.print(currCol);
        currCol += 1;
      }
      // Move to the next line after completing one row
      System.out.println();
      currRow += 1;
    }
  }
}
