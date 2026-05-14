/*
 * WEEK 4 - PATTERN PROBLEMS
 * Topic: Alpha Pattern
 * File: 5.Alpha_Pattern.java
 *
 * PATTERN (for N=4):
 * A
 * BB
 * CCC
 * DDDD
 *
 * CONCEPT:
 * Print a right-angled triangle of alphabetic characters where
 * row i contains the i-th letter of the alphabet repeated i times.
 * Uses ASCII arithmetic to map row numbers to characters.
 *
 * APPROACH:
 * - Outer loop: controls rows (currRow = 1 to N)
 * - Inner loop: controls columns (currCol = 1 to currRow)
 * - Compute the character for each row: ch = 'A' + currRow - 1
 * - Print the same character ch across all columns in that row
 *
 * KEY INSIGHT:
 * The character is determined solely by the row number using
 * ASCII offset: 'A' + (row - 1). Row 1 = 'A', Row 2 = 'B', etc.
 * Each row prints that single character repeated row-number times.
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
      // Map row number to character: row 1 -> 'A', row 2 -> 'B', etc.
      char ch = (char) ('A' + currRow - 1);
      // Inner loop: print the character ch exactly currRow times
      while (currCol <= currRow) {
        System.out.print(ch);
        currCol += 1;
      }
      // Move to the next line after completing one row
      System.out.println();
      currRow += 1;
    }
  }
}
