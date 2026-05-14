/*
 * WEEK 1 - JAVA FUNDAMENTALS
 * Topic: Comprehensive Scanner Input Methods
 * File: 7.Taking_Input_all.java
 *
 * CONCEPT:
 * Demonstrates all major Scanner input methods for reading different data
 * types. Shows how to read integers, strings, characters, doubles, and
 * longs from user input in a single program.
 *
 * KEY POINTS:
 * - nextInt() reads an int token; nextDouble() reads a double token
 * - nextLong() reads a long token; next() reads a single word (token)
 * - nextLine() reads the entire line including spaces
 * - charAt(index) retrieves a character at a specific position in a String
 * - Java has no nextChar() method; use next().charAt(0) to read a single char
 * - Tokens are delimited by whitespace (space, tab, newline)
 *
 * SYNTAX:
 * s.nextInt()     // read int
 * s.nextDouble()  // read double
 * s.nextLong()    // read long
 * s.next()        // read single word (token)
 * s.nextLine()    // read entire line
 */

 package fundamentals;
import java.util.Scanner;
public class ArithematicOperators {
    public static void main(String args[]) {
      int a,b;
      Scanner s=new Scanner(System.in);
      a=s.nextInt();   // Read first integer
      b=s.nextInt();   // Read second integer
      int c=a+b;       // Sum the two integers

      String str=s.nextLine();   // Read rest of line (caution: consumes leftover newline)
      char ch=str.charAt(0);     // Get first character of the string
      System.out.println(ch);
      s.nextDouble();  // Read a double-precision floating point value
      s.nextLong();    // Read a long integer value
    }
}

/*

The Java Scanner class breaks the input into tokens using a delimiter that is
whitespace by default. It provides many ways to read and parse various
primitive values.
In order to use scanner you have to write this import statement at the top –
import java.util.Scanner;


Sample Input:
10 5

Here, s.nextInt() scans and returns the next token as int. A token is part of entered
line that is separated from other tokens by space, tab or newline. So when input
line is: “10 5” then s.nextInt() returns the first token i.e. “10” as int and s.nextInt()
again returns the next token i.e. “5” as int  
  */
