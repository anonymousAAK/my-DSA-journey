/*
 * WEEK 4 - PATTERN PROBLEMS
 * Topic: Reverse Number Pattern
 * File: 4.Reverse_Num_Pattern.java
 *
 * PATTERN (for N=4):
 * 1
 * 21
 * 321
 * 4321
 *
 * CONCEPT:
 * Print a right-angled triangle where each row i contains numbers
 * counting down from i to 1. The inner loop runs in reverse,
 * starting from the row number and decrementing to 1.
 *
 * APPROACH:
 * - Outer loop: controls rows (currRow = 1 to N)
 * - Inner loop: controls columns (currCol = currRow down to 1)
 * - Print the current column value, which decreases each iteration
 *
 * KEY INSIGHT:
 * By starting the inner loop at currRow and decrementing, the numbers
 * naturally print in descending order (e.g., row 4 prints 4, 3, 2, 1).
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
      // Inner loop: start from currRow and count down to 1 (reverse order)
      int currCol = currRow;
      while (currCol >= 1) {
        System.out.print(currCol);
        currCol -= 1;
      }
      // Move to the next line after completing one row
      System.out.println();
      currRow += 1;
    }
  }
}
