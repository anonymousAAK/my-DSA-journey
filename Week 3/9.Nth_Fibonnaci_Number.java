/*
 * WEEK 3 - LOOPS & NUMBER THEORY
 * Topic: Nth Fibonacci Number
 * File: 9.Nth_Fibonnaci_Number.java
 *
 * CONCEPT:
 * The Fibonacci sequence is defined as F(n) = F(n-1) + F(n-2), where
 * F(1) = 0 and F(2) = 1. Each number is the sum of the two preceding ones.
 * This solution uses an iterative approach to compute the Nth term efficiently.
 *
 * KEY POINTS / ALGORITHM:
 * 1. Initialize two variables: a = 0 (F(1)) and b = 1 (F(2)).
 * 2. Iterate n times, computing c = a + b in each step.
 * 3. Shift values: a = b, b = c (slide the window forward).
 * 4. After n iterations, a holds the Nth Fibonacci number.
 * 5. This avoids the exponential cost of naive recursion.
 *
 * Time Complexity: O(n) - single loop from 0 to n
 * Space Complexity: O(1) - only three variables used (a, b, c)
 *
 * Input Format: Integer N
 * Output Format: Nth Fibonacci number
 *
 * Example: N=5 -> Sequence: 0, 1, 1, 2, 3 -> Output: 3
 */

import java.util.Scanner;
public class Solution {
      public static void main(String[] args) {
          Scanner s = new Scanner(System.in);
          int n = s.nextInt();           // read N: which Fibonacci number to find

          // Initialize first two Fibonacci numbers
          int a = 0;                     // F(1) = 0
          int b = 1;                     // F(2) = 1
          int c;                         // temporary variable to hold next value

          // Iterate n times to compute F(n)
          for(int i = 0; i < n; i++){
              c = a + b;                 // next Fibonacci = sum of previous two
              a = b;                     // shift: a now holds what b was
              b = c;                     // shift: b now holds the new value
          }

          System.out.println(a);         // a holds the Nth Fibonacci number
      }
}
