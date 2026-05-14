/*
 * WEEK 1 - JAVA FUNDAMENTALS
 * Topic: Data Types in Java
 * File: 9.Data_Types.java
 *
 * CONCEPT:
 * Introduces Java's primitive data types and their memory sizes. The OS
 * allocates memory based on the declared type, and each type determines
 * what values can be stored in that memory.
 *
 * KEY POINTS:
 * - Java has 8 primitive data types: byte, short, int, long, float, double, char, boolean
 * - char: 2 bytes (Java uses Unicode, not ASCII, for character storage)
 * - byte: 1 byte (-128 to 127); short: 2 bytes; int: 4 bytes; long: 8 bytes
 * - float: 4 bytes (suffix 'f' required); double: 8 bytes (default for decimals)
 * - boolean: true/false (size not precisely defined by JVM spec)
 * - String is NOT a primitive type; it is a class (reference type)
 * - next() reads a single token (word), unlike nextLine() which reads the full line
 *
 * SYNTAX:
 * String str = s.next();    // reads one word (stops at whitespace)
 * String str = s.nextLine(); // reads entire line
 */

package fundamentals;
import java.util.Scanner;
public class ArithematicOperators {
    public static void main(String args[]) {
        Scanner s = new Scanner(System.in);
        String str;         // Declare a String variable (reference type, not primitive)
        str = s.next();     // Read a single word/token from input
        System.out.print(str);  // Print without newline using print() instead of println()
    }
}

/*

Based on the data type of a variable, the operating system allocates memory and
decides what can be stored in the reserved memory. Therefore, by assigning
different data types to variables, we can store integers, decimals, or characters in
these variables.



DATA TYPE        DEFAULT VALUE         DEFAULT SIZE
   char       '\0' (nullcharacter)      2 bytes
   byte              0                  1 byte
   short             0                  2 bytes
    int              0                  4 bytes
    long             0L                 8 bytes
   Float             0.0f               4 bytes
   Double            0.0d               8 bytes
   Boolean           false              Not specified
