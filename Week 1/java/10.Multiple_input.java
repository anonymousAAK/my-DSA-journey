/*
 * WEEK 1 - JAVA FUNDAMENTALS
 * Topic: Reading Multiple Input Types
 * File: 10.Multiple_input.java
 *
 * CONCEPT:
 * Demonstrates reading multiple data types (int and String) in sequence
 * from user input. Also showcases the Scanner class methods reference
 * for all supported data types.
 *
 * KEY POINTS:
 * - Different Scanner methods can be chained to read mixed-type input
 * - next() reads a single token (word); nextLine() reads the full line
 * - nextByte(), nextShort(), nextInt(), nextLong() for integer types
 * - nextFloat(), nextDouble() for floating point types
 * - print() and println() can be mixed for formatting output
 * - print(a) followed by println(str) prints them on the same line with
 *   a newline only after str
 *
 * SYNTAX:
 * int a = s.nextInt();    // read integer token
 * String str = s.next();  // read string token
 */

package fundamentals;
import java.util.Scanner;
public class ArithematicOperators {
    public static void main(String args[]) {


        Scanner s = new Scanner(System.in);
        int a = s.nextInt();    // Read an integer from input
        String str = s.next();  // Read the next word/token as a String
        System.out.print(a);    // Print integer (no newline)
        System.out.println(str);  // Print string (with newline) - appears on same line as 'a'
    }
}

/*


Other scanner options


Some commonly used Scanner class methods are as follows:
METHOD                                            DESCRIPTION
public String next()                    It returns the next token from the Scanner.
public String nextLine()                It moves the Scanner position to the next line and returns the value as a string.
public byte nextByte()                  It scans the next token as a byte.
public short nextShort()                It scans the next token as a short value.
public int nextInt()                    It scans the next token as an int value.
public long nextLong()                  It scans the next token as a long value.
public float nextFloat()                It scans the next token as a float value.
public double nextDouble()              It scans the next token as a double value.



*/
