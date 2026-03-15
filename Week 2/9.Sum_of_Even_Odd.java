/*
 * WEEK 2 - CONTROL FLOW
 * Topic: Sum of Even and Odd Digits
 * File: 9.Sum_of_Even_Odd.java
 *
 * CONCEPT:
 * This file demonstrates digit extraction using modulo and division operators
 * combined with a while loop. It separates the digits of a number into even
 * and odd categories and computes their respective sums.
 *
 * KEY POINTS:
 * - num % 10 extracts the last (rightmost) digit
 * - num / 10 removes the last digit, shifting all digits right
 * - The loop continues until all digits are processed (num becomes 0)
 * - Each digit is classified as even or odd using the % 2 operator
 *
 * APPROACH:
 * 1. Read the number N from input
 * 2. Initialize evenSum = 0 and oddSum = 0
 * 3. While N > 0:
 *    a. Extract last digit using N % 10
 *    b. If digit is even (digit % 2 == 0), add to evenSum
 *    c. Otherwise, add to oddSum
 *    d. Remove last digit: N = N / 10
 * 4. Print evenSum and oddSum
 *
 * Time Complexity: O(d) where d is the number of digits in N
 * Space Complexity: O(1)
 */

/*
Sum of even & odd


Write a program to input an integer N and print the sum of all its even digits and sum of all its odd digits separately.
  
Digits mean numbers, not the places! That is, if the given integer is "13245", even digits are 2 & 4 and odd digits are 1, 3 & 5.
  
  
Input format :
 Integer N
 
 
Output format :
Sum_of_Even_Digits Sum_of_Odd_Digits (Print first even sum and then odd sum separated by space)
*/
/*
How to approach?
1. Take the number as input from the user.
2. Initialize both even sum and odd sum from 0.
3. Now, start picking up the last digit by taking modulo 10 while number is greater than 0
and check whether the last digit is odd or even.
4. If the last digit is odd then, add it to then odd sum otherwise add it to the even sum and
pass the number by dividing it to 10 to the next iteration.
5. Print even sum and odd sum.

*/

import java.util.Scanner;
public class Main {
    public static void main(String[] args) {
        Scanner s = new Scanner(System.in);
        int num = s.nextInt();             // Read the integer N
        int evenSum = 0, oddSum = 0;       // Accumulators for even and odd digit sums
        while(num > 0) {                   // Process digits until number becomes 0
            int last = num % 10;           // Extract the last digit
            if(last % 2 == 0) {            // Check if the digit is even
                evenSum += last;           // Add to even sum
          } else {
                oddSum += last;            // Add to odd sum
          }
            num = num / 10;               // Remove the last digit
          }
        System.out.println(evenSum + " " + oddSum);
    }
}
