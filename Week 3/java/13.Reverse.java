/*
 * WEEK 3 - LOOPS & NUMBER THEORY
 * Topic: Reverse of a Number
 * File: 13.Reverse.java
 *
 * CONCEPT:
 * Given a number N, reverse its digits and print the result. Trailing zeros
 * in the original number are dropped in the reversed output (e.g., reverse
 * of 10400 is 401, not 00401).
 *
 * KEY POINTS / ALGORITHM:
 * 1. Read the input number N; store in temp for processing.
 * 2. Initialize revNum = 0 to build the reversed number.
 * 3. Loop while temp > 0:
 *    a. Extract last digit: lastDigit = temp % 10
 *    b. Remove last digit from temp: temp = temp / 10
 *    c. Append digit to reversed number: revNum = revNum * 10 + lastDigit
 * 4. Print revNum.
 * 5. The multiplication by 10 shifts existing digits left, making room for the new digit.
 *
 * Time Complexity: O(d) where d = number of digits in N (i.e., O(log N))
 * Space Complexity: O(1)
 *
 * Input Format: Integer N
 * Output Format: Reversed integer
 *
 * Example: N = 1234 -> revNum builds as: 1 -> 12 -> 123 -> 1234 (wait, that's wrong)
 *          Actually: 4 -> 43 -> 432 -> 4321
 */

import java.util.Scanner;

public class Main {

    public static void main(String[] args) {

        Scanner s = new Scanner(System.in);

        int n = s.nextInt();             // read the number to reverse

        int temp = n, revNum = 0;        // temp for processing, revNum for result

        while(temp > 0) {                // process until all digits are extracted

            int lastDigit = temp % 10;   // extract the rightmost digit

            temp = temp / 10;            // remove the rightmost digit from temp

            revNum = revNum * 10 + lastDigit; // shift revNum left and add new digit

          }



          System.out.println(revNum);   // print the reversed number

      }

}
