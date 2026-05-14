/*
 * WEEK 2 - CONTROL FLOW
 * Topic: Multiplication Table using While Loop
 * File: 8.Multiplication_Table.java
 *
 * CONCEPT:
 * This file demonstrates using a while loop to print the multiplication
 * table (first 10 multiples) of a given number. It is a classic example
 * of counter-controlled loop iteration.
 *
 * KEY POINTS:
 * - A counter variable (i) controls the number of iterations (1 to 10)
 * - Each iteration computes i * n and prints the result
 * - The counter is manually incremented (i = i + 1) at the end of each iteration
 * - The loop terminates when the counter exceeds 10
 *
 * APPROACH:
 * 1. Read the number n from input
 * 2. Initialize counter i = 1
 * 3. Loop while i <= 10
 * 4. In each iteration, compute j = i * n and print j
 * 5. Increment i by 1
 *
 * Time Complexity: O(1) - always exactly 10 iterations
 * Space Complexity: O(1)
 */

/*
Multiplication Table

Write a program to print multiplication table of n


Input Format :
A single integer, n



Output Format :
First 10 multiples of n each printed in new line

*/

import java.util.Scanner;
public class Main {
	
	public static void main(String[] args) {
        int n;
		Scanner s = new Scanner(System.in);
		n = s.nextInt();       // Read the number whose table is to be printed
		int i = 1;             // Counter starts at 1
		while(i<=10) {         // Loop 10 times (for multiples 1 through 10)
			int j = i*n;       // Compute the i-th multiple of n
			System.out.println(j);  // Print the multiple
			i = i+1;          // Increment counter
		}

	}
}
