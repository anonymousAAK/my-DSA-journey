/*
 * WEEK 4 - PATTERN PROBLEMS
 * Topic: Character Pattern
 * File: 6.Char_Pattern.java
 *
 * PATTERN (for N=4):
 * A
 * BC
 * CDE
 * DEFG
 *
 * CONCEPT:
 * Print a right-angled triangle of characters where each row starts
 * at a different letter and prints consecutive letters across columns.
 * Row i starts at ‘A’ + (i-1) and prints i consecutive characters.
 *
 * APPROACH:
 * - Outer loop: controls rows (currRow = 1 to N)
 * - Inner loop: controls columns (currCol = 1 to currRow)
 * - Starting character for row i: ch = ‘A’ + currRow - 1
 * - Character at column j: ch + (currCol - 1), incrementing across columns
 *
 * KEY INSIGHT:
 * The character depends on BOTH row and column: the starting character
 * shifts by one letter per row, and within each row the characters
 * advance consecutively (Row 3 starts at ‘C’ and prints C, D, E).
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
      // Starting character for this row: row 1 -> ‘A’, row 2 -> ‘B’, etc.
      char ch = (char) (‘A’ + currRow - 1);
      // Inner loop: print consecutive characters starting from ch
      while (currCol <= currRow) {
        // Offset by (currCol - 1) to get consecutive letters within the row
        System.out.print((char) (ch + currCol - 1));
        currCol += 1;
      }
      // Move to the next line after completing one row
      System.out.println();
      currRow += 1;
    }
  }
}
