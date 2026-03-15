/*
 * WEEK 3 - LOOPS & NUMBER THEORY
 * Topic: Bitwise Operators
 * File: 7.Bitwise_Operator.java
 *
 * CONCEPT:
 * Bitwise operators perform operations at the individual bit level of integers.
 * They are fundamental for low-level programming, optimization, and problems
 * involving binary representations of numbers.
 *
 * KEY POINTS / ALGORITHM:
 * 1. AND  (a & b)  - 1 only if BOTH bits are 1.
 * 2. OR   (a | b)  - 1 if EITHER bit is 1.
 * 3. XOR  (a ^ b)  - 1 if bits are DIFFERENT.
 * 4. NOT  (~a)      - Inverts all bits (unary complement); result = -(a+1).
 * 5. LEFT SHIFT  (n << p) - Shifts bits left by p positions; equivalent to n * 2^p.
 * 6. RIGHT SHIFT (n >> p) - Arithmetic shift right by p; preserves sign bit.
 * 7. UNSIGNED RIGHT SHIFT (n >>> p) - Logical shift right; fills with 0s.
 *
 * Time Complexity: O(1) - bitwise operations are constant time
 * Space Complexity: O(1)
 */

/*
 * BITWISE OPERATORS REFERENCE TABLE:
 *   Operator    Name              Example       Result    Description
 *     a & b     AND                 4 & 6          4      1 if both bits are 1
 *     a | b     OR                  4 | 6          6      1 if either bit is 1
 *     a ^ b     XOR                 4 ^ 6          2      1 if both bits are different
 *       ~a      NOT (complement)      ~4          -5      Inverts all bits
 *     n << p    Left Shift         3 << 2         12      Shifts bits left p positions
 *     n >> p    Right Shift        5 >> 2          1      Arithmetic right shift (preserves sign)
 *     n >>> p   Unsigned R-Shift  -4 >>> 28       15      Logical right shift (fills with 0s)
 */


// Example Code demonstrating all bitwise operators
public static void main(String args[]) {
          int a = 19; // 19 in binary = 10011
          int b = 28; // 28 in binary = 11100
          int c = 0;

          // AND: bits are 1 only where BOTH a and b have 1
          c = a & b; // 10011 & 11100 = 10000 = 16
          System.out.println("a & b = " + c );

          // OR: bits are 1 where EITHER a or b has 1
          c = a | b; // 10011 | 11100 = 11111 = 31
          System.out.println("a | b = " + c );

          // XOR: bits are 1 where a and b DIFFER
          c = a ^ b; // 10011 ^ 11100 = 01111 = 15
          System.out.println("a ^ b = " + c );

          // NOT: inverts all bits; for signed int, ~a = -(a+1)
          c = ~a; // ~19 = -20
          System.out.println("~a = " + c );

          // LEFT SHIFT: shifts bits left by 2; equivalent to a * 4 (2^2)
          c = a << 2; // 10011 << 2 = 1001100 = 76
          System.out.println("a << 2 = " + c );

          // RIGHT SHIFT (arithmetic): shifts bits right by 2; equivalent to a / 4
          c = a >> 2; // 10011 >> 2 = 00100 = 4
          System.out.println("a >> 2 = " + c );

          // UNSIGNED RIGHT SHIFT: same as >> for positive numbers; differs for negative
          c = a >>> 2; // 10011 >>> 2 = 00100 = 4
          System.out.println("a >>> 2 = " + c );
    }


/*
Output:
a & b = 16
a | b = 31
a ^ b = 15
~a = -20
a << 2 = 76
a >> 2 = 4
a >>> 2 = 4
*/
