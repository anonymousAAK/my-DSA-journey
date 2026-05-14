/*
 * WEEK 1 - JAVA FUNDAMENTALS
 * Topic: Adding Two Numbers with User Input
 * File: 8.Add_two_number_better.java
 *
 * CONCEPT:
 * An improved version of the Add Two Numbers program that reads values
 * from user input instead of hardcoding them. Combines Scanner input
 * with arithmetic operations for a dynamic, interactive program.
 *
 * KEY POINTS:
 * - Reads integers dynamically from user rather than hardcoding values
 * - Expression (a+b) is evaluated directly inside println() - no need for
 *   a separate variable to store the result
 * - Scanner must be created before reading input
 * - This pattern (read -> process -> output) is fundamental to most programs
 *
 * SYNTAX:
 * System.out.println(expression); // expression is evaluated before printing
 */

package fundamentals;
import java.util.Scanner;
public class ArithematicOperators {
    public static void main(String args[]) {

        Scanner s = new Scanner(System.in);
        int a = s.nextInt();  // Read first number from user
        int b = s.nextInt();  // Read second number from user
        System.out.println(a+b);  // Compute and print sum directly
    }
}
