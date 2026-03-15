/*
 * WEEK 2 - CONTROL FLOW
 * Topic: Computing Power of a Number (x^n)
 * File: 11.Find_Power.java
 *
 * CONCEPT:
 * This file demonstrates using a for loop to compute exponentiation (x^n)
 * through repeated multiplication. This is the brute-force linear approach;
 * a more efficient O(log n) method is covered in Week 5.
 *
 * KEY POINTS:
 * - Exponentiation x^n means multiplying x by itself n times
 * - The result variable (ans) is initialized to 1 (multiplicative identity)
 * - Uses long for the result to handle large values that exceed int range
 * - 0^0 is treated as 1 by convention in this problem
 *
 * PROBLEM:
 * Given integers x and n, compute x raised to the power n.
 * Note: 0^0 is defined as 1 for this problem.
 *
 * APPROACH:
 * 1. Take x and n as input.
 * 2. Initialize ans = 1.
 * 3. Multiply x with ans, n times using a for loop.
 * 4. Print the final result.
 *
 * Time Complexity: O(n) - we multiply n times
 * Space Complexity: O(1)
 *
 * NOTE: See Week 5 for O(log n) fast exponentiation.
 */

import java.util.Scanner;

public class FindPower {
    public static void main(String[] args) {
        Scanner s = new Scanner(System.in);
        System.out.print("Enter base x and exponent n: ");
        int x = s.nextInt();
        int n = s.nextInt();

        long ans = 1;                   // Start with 1 (x^0 = 1)
        for (int i = 0; i < n; i++) {   // Multiply x, n times
            ans *= x;                   // ans = ans * x
        }
        System.out.println(x + "^" + n + " = " + ans);
        s.close();
    }
}
