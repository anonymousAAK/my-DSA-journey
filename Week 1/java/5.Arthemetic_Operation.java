/*
 * WEEK 1 - JAVA FUNDAMENTALS
 * Topic: Arithmetic Operations & Operator Precedence
 * File: 5.Arthemetic_Operation.java
 *
 * CONCEPT:
 * Demonstrates arithmetic operations in Java, particularly integer division
 * and operator precedence. When dividing integers, Java performs integer
 * division (truncates the decimal part).
 *
 * KEY POINTS:
 * - Integer division truncates the result (10/6 = 1, not 1.666...)
 * - Parentheses () override default operator precedence
 * - Multiplication and division have higher precedence than addition/subtraction
 * - Common pitfall: integer division loses precision; use double/float for decimals
 *
 * SYNTAX:
 * +  Addition
 * -  Subtraction
 * *  Multiplication
 * /  Division (integer division for int types)
 * %  Modulus (remainder)
 */

package fundamentals;
public class ArithematicOperators {
    public static void main(String args[]) {
      int a=3;
      int b=10;
      int c=b/(2*a);  // Evaluates as 10/6 = 1 (integer division truncates decimal)
      System.out.println(c);

    }
}
