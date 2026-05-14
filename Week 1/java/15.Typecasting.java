/*
 * WEEK 1 - JAVA FUNDAMENTALS
 * Topic: Typecasting (Widening and Narrowing Conversions)
 * File: 15.Typecasting.java
 *
 * CONCEPT:
 * Typecasting is converting a value from one data type to another. Java
 * supports two kinds: automatic (widening) when converting to a larger
 * type, and explicit (narrowing) when converting to a smaller type.
 *
 * KEY POINTS:
 * - Widening (automatic): smaller type -> larger type, no data loss
 *   byte -> short -> int -> long -> float -> double
 * - Narrowing (explicit): larger type -> smaller type, may lose data
 *   Requires cast operator: (targetType) value
 * - Example: int to long is automatic; double to long requires (long)
 * - Narrowing truncates (does not round): (long)100.99 = 100
 * - Common pitfall: narrowing can silently lose precision or overflow
 *
 * SYNTAX:
 * long l = i;          // widening: int -> long (automatic)
 * long l = (long) d;   // narrowing: double -> long (explicit, truncates decimal)
 */

/*
Typecasting


1. Widening or Automatic type conversion: 

In Java, automatic type conversion takes place when the two types are compatible and size of destination type is larger than source type.
  
  
2. Narrowing or Explicit type conversion:
When we are assigning a larger type value to a variable of smaller type, then we need to perform explicit type casting.
Example code:

*/
public static void main(String[] args) {
    int i = 100;
    long l1 = i; //automatic type casting
    double d = 100.04;
    long l2 = (long)d; //explicit type casting
    System.out.println(i);
    System.out.println(l1);
    System.out.println(d);
    System.out.println(l2);
}

/*
Output:
100
100
100.04
100

*/
