/*
 * WEEK 3 - LOOPS & NUMBER THEORY
 * Topic: Binary to Decimal Conversion
 * File: 14.Binary_to_Decimal.java
 *
 * CONCEPT:
 * Convert a binary number (given as an integer, e.g., 1100) to its decimal
 * equivalent. Each binary digit is multiplied by 2 raised to its positional
 * power, and the results are summed.
 *
 * KEY POINTS / ALGORITHM:
 * 1. Read the binary number as an integer (e.g., 1100).
 * 2. Initialize decimal = 0 (running sum) and pow = 1 (represents 2^0 = 1).
 * 3. Loop while num > 0:
 *    a. Extract last digit: last = num % 10 (gives 0 or 1).
 *    b. Add its weighted value: decimal += last * pow.
 *    c. Double the power: pow *= 2 (next position is 2x more).
 *    d. Remove last digit: num = num / 10.
 * 4. Print the decimal result.
 *
 * Example: 1100 -> 0*1 + 0*2 + 1*4 + 1*8 = 12
 *
 * Time Complexity: O(d) where d = number of binary digits (O(log N))
 * Space Complexity: O(1)
 *
 * Input Format: Integer N in binary form (e.g., 1100)
 * Output Format: Decimal equivalent (e.g., 12)
 */

import java.util.Scanner;

public class Main {

    public static void main(String[] args) {

          Scanner s = new Scanner(System.in);

          int num = s.nextInt();         // read binary number as integer

          int decimal = 0, pow = 1;      // decimal = result, pow = current power of 2

          while(num > 0) {               // process each binary digit right to left

              int last = num % 10;       // extract rightmost digit (0 or 1)

              decimal += last * pow;     // add digit's contribution: digit * 2^position

              pow *= 2;                  // next position: multiply power by 2

              num = num / 10;            // remove the rightmost digit

            }

          System.out.println(decimal);   // print the decimal equivalent

        }

}



