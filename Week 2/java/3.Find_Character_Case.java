/*
 * WEEK 2 - CONTROL FLOW
 * Topic: Character Case Detection using ASCII Values
 * File: 3.Find_Character_Case.java
 *
 * CONCEPT:
 * This file demonstrates how to determine whether a character is uppercase,
 * lowercase, or not an alphabet at all, by leveraging ASCII value ranges.
 * Characters in Java are internally stored as integer ASCII values.
 *
 * KEY POINTS:
 * - Lowercase letters 'a'-'z' have ASCII values 97-122
 * - Uppercase letters 'A'-'Z' have ASCII values 65-90
 * - Characters can be implicitly cast to int to get their ASCII value
 * - If-else-if ladder is used to check mutually exclusive conditions
 *
 * APPROACH:
 * 1. Read a character from input
 * 2. Convert to its ASCII integer value
 * 3. Check if it falls in lowercase range (97-122) -> print 0
 * 4. Else check if it falls in uppercase range (65-90) -> print 1
 * 5. Otherwise it is not an alphabet -> print -1
 *
 * Time Complexity: O(1)
 * Space Complexity: O(1)
 */

/*

Problem Statement:-

Write a program that takes a character as input and prints either 1, 0 or -1 according to the following rules.
1, if the character is an uppercase alphabet (A - Z)
0, if the character is a lowercase alphabet (a - z)
-1, if the character is not an alphabet

*/

// Input Format :- Single Character


/*How to approach?
1. Take the input character form the user.
2. Check for the conditions if the given character lies between “A” and “Z”, this means we
have uppercase in the input character then print 1, if it lies between “a” and “z”, we have
lowercase in the input character then print 0 otherwise print -1.   */

import java.util.Scanner;

public class C_Case {
    
    public static void main(String[] args) {
        Scanner s = new Scanner(System.in);
		    String str = s.next();           // Read input as string
		    char ch = str.charAt(0);         // Extract the first character
		    int i = ch;   // Since characters are stored as their ASCII value
        int a= 1 ,b = 0, c  =-1;

          // Check if ASCII value falls in lowercase range (a=97 to z=122)
          if(i>= 97 && i<= 122) {
			        System.out.println(0);
		          }
		      // Check if ASCII value falls in uppercase range (A=65 to Z=90)
		      else if(i>=65 && i<=90) {
			        System.out.println(1);
		        }
		      // Not an alphabetic character
		      else {
			        System.out.println(-1);
		    }
    }
}
