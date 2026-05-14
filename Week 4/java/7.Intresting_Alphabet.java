/*
 * WEEK 4 - PATTERN PROBLEMS
 * Topic: Interesting Alphabets
 * File: 7.Intresting_Alphabet.java
 *
 * PATTERN (for N=4):
 * D
 * CD
 * BCD
 * ABCD
 *
 * (for N=5):
 * E
 * DE
 * CDE
 * BCDE
 * ABCDE
 *
 * CONCEPT:
 * Print a right-angled triangle where each row ends at the N-th letter
 * and the starting letter moves backward as rows increase. The last row
 * always starts at ‘A’ and ends at the N-th character.
 *
 * APPROACH:
 * - Outer loop: controls rows (currRow = 1 to N)
 * - Inner loop: controls columns (currCol = 1 to currRow)
 * - Starting character for row i: ch = ‘A’ + N - currRow
 * - Characters increment consecutively across columns from the start
 *
 * KEY INSIGHT:
 * The starting character is calculated as ‘A’ + (N - currRow), so it
 * shifts one letter earlier in the alphabet with each subsequent row.
 * Every row always ends at the same letter (‘A’ + N - 1), creating the
 * “interesting” reverse-building effect toward the full alphabet.
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
      // Starting character shifts backward: row 1 starts near end, last row starts at ‘A’
      char ch = (char) (‘A’ + n - currRow);
      // Inner loop: print consecutive characters starting from ch
      while (currCol <= currRow) {
        System.out.print((char) (ch + currCol - 1));
        currCol += 1;
      }
      // Move to the next line after completing one row
      System.out.println();
      currRow += 1;
    }
  }
}
