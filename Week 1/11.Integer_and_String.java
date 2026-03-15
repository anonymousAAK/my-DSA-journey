/*
 * WEEK 1 - JAVA FUNDAMENTALS
 * Topic: Mixing Integer and String Input
 * File: 11.Integer_and_String.java
 *
 * CONCEPT:
 * Demonstrates reading a String followed by an integer, and concatenating
 * them for output. Shows string concatenation with the + operator, which
 * converts non-String values to their String representation automatically.
 *
 * KEY POINTS:
 * - The + operator with Strings performs concatenation, not addition
 * - When mixing String and int with +, Java auto-converts int to String
 * - " " (space in quotes) is a String literal used as a separator
 * - Order of input matters: read String first with next(), then int with nextInt()
 * - Common pitfall: if you read nextInt() before next(), leftover newline
 *   characters can cause unexpected behavior
 *
 * SYNTAX:
 * System.out.print(str + " " + a); // concatenates str, space, and a
 */

package fundamentals;
import java.util.Scanner;
public class ArithematicOperators {

    Scanner s = new Scanner(System.in);
    String str = s.next();       // Read a word (String token) first
     int a = s.nextInt();        // Then read an integer
    System.out.print(str + " " + a);  // Concatenate and print: string + space + integer
}
}
