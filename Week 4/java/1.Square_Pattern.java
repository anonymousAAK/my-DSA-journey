/*
 * WEEK 4 - PATTERN PROBLEMS
 * Topic: Square Pattern
 * File: 1.Square_Pattern.java
 *
 * PATTERN (for N=4):
 * 4444
 * 4444
 * 4444
 * 4444
 *
 * CONCEPT:
 * Print an N x N grid where every cell contains the value N.
 * Both the outer and inner loops run exactly N times, forming a square.
 *
 * APPROACH:
 * - Outer loop: controls rows (i = 1 to N)
 * - Inner loop: controls columns (j = 1 to N)
 * - At every position, print the value N (not i or j)
 *
 * KEY INSIGHT:
 * The printed value is always N regardless of row or column position,
 * making this the simplest pattern — a uniform square grid.
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
        for(int i = 1 ; i <= n; i++){
            // Inner loop: print N columns per row, each containing the value N
            for(int j = 1 ; j <= n; j++){

                System.out.print(n);


            }
            // Move to the next line after completing one row
            System.out.println();
        }

	  }
}

 
