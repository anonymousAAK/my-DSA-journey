/*
 * WEEK 1 - JAVA FUNDAMENTALS
 * Topic: Computing the Average of Numbers
 * File: 12.Average_of_two_numbers.java
 *
 * CONCEPT:
 * Reads a name and three integers from user input, then calculates and
 * displays the average. Demonstrates combining String and numeric input
 * in a practical program.
 *
 * KEY POINTS:
 * - Integer division: (a+b+c)/3 truncates the decimal portion
 *   e.g., (10+11+12)/3 = 11, but (10+11+11)/3 = 10 (not 10.666...)
 * - To get a precise average, use double: (a+b+c)/3.0
 * - Parentheses around (a+b+c) ensure addition happens before division
 * - Without parentheses, only c would be divided by 3 due to precedence
 *
 * SYNTAX:
 * (a + b + c) / 3   // integer average (truncated)
 * (a + b + c) / 3.0 // precise average (as double)
 *
 * Time Complexity: O(1) - constant time operations
 * Space Complexity: O(1) - fixed number of variables
 */

import java.util.Scanner;
public class Average {


	public static void main(String[] args) {

		Scanner sc = new Scanner(System.in);
        String name = sc.next();    // Read the user's name
        int a=sc.nextInt();         // Read first number
        int b=sc.nextInt();         // Read second number
        int c=sc.nextInt();         // Read third number
        System.out.println(name);
        System.out.println((a+b+c)/3);  // Integer division: result is truncated, not rounded

	}

}
