/*
 * WEEK 2 - CONTROL FLOW
 * Topic: Finding Factors of a Number
 * File: 10.Factors.java
 *
 * CONCEPT:
 * This file demonstrates finding all factors of a number (excluding 1 and
 * the number itself) using a while loop. A factor is a number that divides
 * evenly into another number with no remainder.
 *
 * KEY POINTS:
 * - A factor of n is any integer i where n % i == 0
 * - Only need to check up to n/2 since no factor (other than n) can exceed n/2
 * - The loop starts at 2 to exclude 1, and the upper bound n/2 excludes n itself
 * - The modulo operator (%) is used to test divisibility
 *
 * APPROACH:
 * 1. Read the number n from input
 * 2. Initialize i = 2 (skip 1 as per requirement)
 * 3. Loop while i <= n/2 (factors beyond n/2 cannot exist, except n itself)
 * 4. If n % i == 0, then i is a factor -> print it
 * 5. Increment i by 1
 *
 * Time Complexity: O(n) - checks all values from 2 to n/2
 * Space Complexity: O(1)
 */

/*
Factors


Write a program to print all the factors of a number other than 1 and the number itself.
  
  
Input Format :
A single integer, n


Output Format :
All the factors of n excluding 1 and the number itself

*/

import java.util.Scanner;
public class Solution {
    public static void main(String[] args) {
        Scanner s = new Scanner(System.in);
        int n = s.nextInt();          // Read the number to find factors of
        int i = 2;                    // Start from 2 (excluding 1)
        while(i <= n / 2) {          // Only check up to n/2 (no larger factor exists besides n)
            if(n % i == 0) {          // If i divides n evenly, it's a factor
                System.out.print(i + " ");
               }
            i += 1;                   // Check next candidate
            }
        }
}
