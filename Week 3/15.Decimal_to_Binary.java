/*
 * WEEK 3 - LOOPS & NUMBER THEORY
 * Topic: Decimal to Binary Conversion
 * File: 15.Decimal_to_Binary.java
 *
 * CONCEPT:
 * Convert a decimal (base-10) number to its binary (base-2) representation.
 * The binary result is stored as a long integer to accommodate large binary
 * representations (e.g., decimal 255 = binary 11111111).
 *
 * KEY POINTS / ALGORITHM:
 * 1. Read the decimal number N.
 * 2. Initialize binary = 0 (result) and pow = 1 (place value: 1, 10, 100, ...).
 * 3. Loop while N > 0:
 *    a. Get the remainder: lastBit = N % 2 (gives 0 or 1).
 *    b. Place it in the result: binary += lastBit * pow.
 *    c. Move to next decimal place: pow *= 10.
 *    d. Integer-divide N by 2: N = N / 2.
 * 4. Print the binary representation.
 *
 * Example: 12 -> 12%2=0, 6%2=0, 3%2=1, 1%2=1 -> binary = 1100
 *
 * NOTE: Uses long for the binary result because binary representations
 * can exceed int range (e.g., 1000000000 for decimal 512).
 *
 * Time Complexity: O(log n) - number of bits in the binary representation
 * Space Complexity: O(1)
 *
 * Input Format: Integer N (decimal)
 * Output Format: Binary representation as a long integer
 */



import java.util.Scanner;
  public class Main {
      public static void main(String[] args) {
          Scanner s = new Scanner(System.in);
          int n = s.nextInt();           // read decimal number

          long binary = 0, pow = 1;      // binary = result (long to avoid overflow), pow = place value
          while(n > 0) {
             int lastBit = n % 2;        // get remainder: 0 or 1 (rightmost binary digit)
             binary += lastBit * pow;    // place the bit at the correct decimal position
              pow *= 10;                 // move to next place value (1 -> 10 -> 100 -> ...)
              n = n / 2;                 // divide n by 2 to process next bit
          }

          System.out.println(binary);    // print the binary representation
      }
}
