/*
 * WEEK 2 - CONTROL FLOW
 * Topic: Data Types Review
 * File: 1.Data_Types_review.java
 *
 * CONCEPT:
 * This file reviews Java data types and their behavior during arithmetic
 * operations. It covers integer division, the modulo operator with different
 * types (int vs double), and relational operators.
 *
 * KEY POINTS:
 * - Integer division in Java truncates the decimal part (6/4 = 1, not 1.5)
 * - Storing an int result in a double variable does NOT recover the lost precision
 * - The modulo (%) operator works on both int and double types
 * - Relational operators (>, <, ==, etc.) return boolean values (true/false)
 * - Byte data type has a limited range of [-128, 127]; overflow causes compilation error
 *
 * APPROACH:
 * 1. Demonstrate byte overflow when multiplying beyond its range
 * 2. Show integer division behavior when stored in double vs int variables
 * 3. Illustrate modulo operator on double (5.5) and int (5) values
 * 4. Show relational operator returning a boolean result
 *
 * Time Complexity: O(1) - all operations are constant time
 * Space Complexity: O(1)
 */

//Some Codes for practice:

// --- Example 1: Byte Overflow ---
byte b = 50;
b = b * 50;  // Compilation error: result exceeds byte range

//This will convert b to int since bytes store in the range of [-128,127].


// --- Example 2: Integer Division Pitfall ---
public class  Solution{
    public static void main(String [] args)  {
        double a = 6 / 4;   // 6/4 is int division = 1, stored as 1.0 in double
        int b  = 6 / 4;     // 6/4 is int division = 1
        double c = a + b;   // 1.0 + 1 = 2.0
        System.out.println(c);
      
      /*
When 6 / 4 is performed, both the operands of / are integer. Hence answer will be an int i.e. 1.
When we store it in a (which is double), value of a will be 1.0 and value of b will be 1. Thus a + b will be 2.0.

*/
    }
}

// --- Example 3: Modulo Operator on double vs int ---
public class  Solution{
    public static void main(String [] args)  {
        double a = 55.5;
        int b = 55;
        a = a % 10;          // 55.5 % 10 = 5.5 (modulo preserves decimal for double)
        b = b % 10;          // 55 % 10 = 5
        System.out.println(a + " "  + b);
      /* 
      % operator gives remainder. So a % 10 will give us 5.5 and b % 10 will give us 5. Hence output is : 5.5 5
        */
      
      }
 }

 // --- Example 4: Relational Operator Returns Boolean ---
 public class  Solution {
    public static void main(String [] args)  {
        int var1 = 5;
        int var2 = 6;
        System.out.print(var1 > var2);  // Prints "false" since 5 is not greater than 6
     /*
     > is a relational operator. So it will give the result as true or false only. var1 is not greater than var2, hence result is false. */
    }
}
