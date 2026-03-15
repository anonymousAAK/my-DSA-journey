/*
 * WEEK 1 - JAVA FUNDAMENTALS
 * Topic: Print Statements - println vs print
 * File: 3.Better_Hello_World.java
 *
 * CONCEPT:
 * Demonstrates the difference between print() and println() methods.
 * println() appends a newline character after the output, while print()
 * does not. Multiple println() calls produce output on separate lines.
 *
 * KEY POINTS:
 * - System.out.println() adds a newline (\n) after the output
 * - System.out.print() does NOT add a newline; next output continues on same line
 * - Multiple println() calls will each print on a new line
 * - Both methods accept String arguments enclosed in double quotes
 *
 * SYNTAX:
 * System.out.println("text"); // prints with newline
 * System.out.print("text");   // prints without newline
 */

package fundamentals;
public class HelloWorld {
    public static void main(String args[]) {
// println prints a new line at the end

     System.out.println("Hello World");
     System.out.println("Hello World");
     System.out.println("Hello World");
    }
}


/* In order to print things to console we have to write - 
System.out.println("HelloWorld").
Again for now we should leave System.out.print mean, and should write it as it is The built-in method print() is used to display the string which is passed to it. This
output string is not followed by a newline, i.e., the next output will start on thesame line. 

The built-in method println() is similar to print(), except that println()  outputs a newline after each call. */ 
