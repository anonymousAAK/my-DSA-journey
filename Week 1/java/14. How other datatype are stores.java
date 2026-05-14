/*
 * WEEK 1 - JAVA FUNDAMENTALS
 * Topic: How Float, Double, and Char are Stored
 * File: 14. How other datatype are stores.java
 *
 * CONCEPT:
 * Explains how floating-point numbers (float and double) and characters
 * are stored in memory. Covers the 'f' suffix requirement for float
 * literals, Unicode character representation, and char arithmetic.
 *
 * KEY POINTS:
 * - Decimal values default to double (8 bytes); use 'f' suffix for float (4 bytes)
 * - char in Java is 16-bit (2 bytes) using Unicode, range 0 to 65,536
 * - Characters are stored as their Unicode/ASCII code in binary form
 * - A char can be assigned an integer value (ASCII code): char ch = 88; // 'X'
 * - Adding int to char adds the int to the char's ASCII value
 *   e.g., 'a' + 1 = 97 + 1 = 98
 * - Adding two chars adds their ASCII values: 'a' + 'b' = 97 + 98 = 195
 * - Common pitfall: char arithmetic produces int, not char
 *
 * SYNTAX:
 * float f = 10.4f;  // 'f' suffix required for float literals
 * double d = 10.4;  // no suffix needed for double (default)
 * char ch = 'A';    // character literal in single quotes
 * char ch = 65;     // same as 'A' (using ASCII code directly)
 */

/*
b) Float and Double values


In Java, any value declared with decimal point is by default of type double (which is of 8 bytes). If we want to assign a float value (which is of 4 bytes), then we must
use ‘f’ or ‘F’ literal to specify that current value is “float”.

Example:

*/
float float_val = 10.4f; //float value
double val = 10.4; //double value

/*
c) How are characters stored
Java uses Unicode to represent characters. As we know system only understands binary language and thus everything has to be stored in the form binaries. So for
every character there is corresponding code – Unicode/ASCII code and binary equivalent of this code is actually stored in memory when we try to store a char.

Unicode defines a fully international character set that can represent all the characters found in all human languages. In Java, char is a 16-bit type. The range
of a char is 0 to 65,536.

*/ 

public static void main(String[] args) {
    char ch1, ch2;
      ch1 = 88; //ASCII value for ‘X’
      ch2 = ‘Y’;
      System.out.println(ch1 +" " +ch2);
    }
/*
Output:
X Y
*/

/*

Adding int to char


When we add int to char, we are basically adding two numbers i.e. one corresponding to the integer and other is corresponding code for the char.
Example code:   */


public static void main(String[] args) {
    System.out.println(‘a’ + 1);
}

Output:
98
  
/*  
Here, we added a character and an int, so it added the ASCII value of char ‘a’ i.e 97 and int 1. So, answer will be 98.

Similar logic applies to adding two chars as well, when two chars are added their codes are actually added i.e. ‘a’ + ‘b’ wil give 195.     */
