/*
 * WEEK 4 - PATTERN PROBLEMS
 * Topic: Triangle Number Pattern
 * File: 3.Tri_No_pattern.java
 *
 * PATTERN (for N=4):
 * 1
 * 22
 * 333
 * 4444
 *
 * CONCEPT:
 * Print a right-angled triangle where each row i contains the
 * digit i repeated i times. Combines the triangular shape with
 * row-dependent content.
 *
 * APPROACH:
 * - Outer loop: controls rows (i = 1 to N)
 * - Inner loop: controls columns (j = 1 to i)
 * - Print the row number 'i' at every column position in that row
 *
 * KEY INSIGHT:
 * The printed value depends only on the row number (i), not the
 * column number (j). Row i prints the digit i exactly i times.
 *
 * Time Complexity: O(N^2) — nested loops
 * Space Complexity: O(1) — no extra data structures
 */
import java.util.Scanner;

public class Solution {

	public static void main(String[] args) {

		int n;
		Scanner s = new Scanner(System.in);
		n = s.nextInt();

		// Outer loop: iterate through each row (1 to N)
		for(int i = 1; i <=n ; i++){
            // Inner loop: print the row number i exactly i times
            for(int j = 1; j <= i ; j++){
                System.out.print(i);
            }
            // Move to the next line after completing one row
            System.out.println();
        }


	}

}
