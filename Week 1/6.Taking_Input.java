/*
 * WEEK 1 - JAVA FUNDAMENTALS
 * Topic: Taking User Input with Scanner
 * File: 6.Taking_Input.java
 *
 * CONCEPT:
 * Introduces the Scanner class for reading user input from the console.
 * Scanner breaks input into tokens using whitespace as a delimiter and
 * provides methods to parse various primitive types.
 *
 * KEY POINTS:
 * - Must import java.util.Scanner before use
 * - Scanner reads tokens separated by whitespace (spaces, tabs, newlines)
 * - nextInt() reads the next token as an integer
 * - nextLine() reads the entire remaining line as a String
 * - charAt(0) extracts the first character from a String
 * - Common pitfall: nextLine() after nextInt() may read leftover newline
 *
 * SYNTAX:
 * Scanner s = new Scanner(System.in);  // create Scanner for console input
 * int val = s.nextInt();               // read integer
 * String line = s.nextLine();          // read entire line
 */

package fundamentals;
import java.util.Scanner;
public class ArithematicOperators {
    public static void main(String args[]) {
      int a,b;
      Scanner s=new Scanner(System.in);  // Create Scanner to read from standard input
      a=s.nextInt();  // Read first integer token
      b=s.nextInt();  // Read second integer token
      int c;

      c =a+b;

      String str=s.nextLine();  // Read remaining text on the line
      char ch=str.charAt(0);    // Extract first character from the string
      System.out.println(ch);
      s.nextDouble();  // Demonstrates reading a double value
      s.nextLong();    // Demonstrates reading a long value
      
  
