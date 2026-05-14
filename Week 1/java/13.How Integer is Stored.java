/*
 * WEEK 1 - JAVA FUNDAMENTALS
 * Topic: How Integers are Stored in Memory
 * File: 13.How Integer is Stored.java
 *
 * CONCEPT:
 * Explains the binary representation of integers in Java. Positive numbers
 * are stored as their direct binary equivalent, while negative numbers use
 * Two's Complement representation. This is fundamental to understanding
 * integer overflow and bitwise operations.
 *
 * KEY POINTS:
 * - int is a signed 32-bit type (range: -2,147,483,648 to 2,147,483,647)
 * - Positive integers: directly converted to binary
 * - Negative integers: stored as Two's Complement
 * - Two's Complement steps: (1) get binary of absolute value,
 *   (2) flip all bits (1's complement), (3) add 1
 * - Two's Complement has only ONE representation for zero (unlike sign-magnitude)
 * - Subtraction can be performed using addition logic with Two's Complement
 *
 * Space Complexity: int always uses exactly 4 bytes (32 bits) regardless of value
 */

/*
a) How are integers stored ?


The most commonly used integer type is int which is a signed 32-bit type. When you store an integer, its corresponding binary value is stored. The way
integers are stored differs for negative and positive numbers. For positive numbers the integral value is simple converted into binary value and for negative
numbers their 2’s compliment form is stored.


Let’s discuss How are Negative Numbers Stored?


Computers use 2's complement in representing signed integers because:
1. There is only one representation for the number zero in 2's complement, instead of two representations in sign-magnitude and 1's complement.
2. Positive and negative integers can be treated together in addition and subtraction. Subtraction can be carried out using the "addition logic".


Example:   */

int i = -4;

/*
Steps to calculate Two’s Complement of -4 are as follows:

Step 1: Take Binary Equivalent of the positive value (4 in this case)
0000 0000 0000 0000 0000 0000 0000 0100


Step 2: Write 1's complement of the binary representation by inverting the bits
1111 1111 1111 1111 1111 1111 1111 1011


Step 3: Find 2's complement by adding 1 to the corresponding 1's complement
1111 1111 1111 1111 1111 1111 1111 1011
+0000 0000 0000 0000 0000 0000 0000 0001
------------------------------------------------------------
1111 1111 1111 1111 1111 1111 1111 1100


Thus, integer -4 is represented by the binary sequence (1111 1111 1111 1111
1111 1111 1111 1100) in Java.
*/
