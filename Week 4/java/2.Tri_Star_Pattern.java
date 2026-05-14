/*
 * WEEK 4 - PATTERN PROBLEMS
 * Topic: Triangular Star Pattern
 * File: 2.Tri_Star_Pattern.java
 *
 * PATTERN (for N=4):
 * *
 * **
 * ***
 * ****
 *
 * CONCEPT:
 * Print a right-angled triangle made of '*' characters.
 * Row i contains exactly i stars, so the number of columns
 * grows linearly with the row number.
 *
 * APPROACH:
 * - Outer loop: controls rows (i = 1 to N)
 * - Inner loop: controls columns (j = 1 to i)
 * - Print '*' at every position in the inner loop
 *
 * KEY INSIGHT:
 * The inner loop bound is 'i' (not N), so each row prints
 * exactly as many stars as its row number — creating the triangle shape.
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
            // Inner loop: print i stars for row i (columns grow with row number)
            for(int j = 1; j <=i ; j++){
                System.out.print('*');
            }
            // Move to the next line after completing one row
            System.out.println();
        }
	}

}
