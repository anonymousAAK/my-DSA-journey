/*
 * WEEK 2 - CONTROL FLOW
 * Topic: If-Else Conditional Statements
 * File: 2.If_else.java
 *
 * CONCEPT:
 * This file demonstrates the if-else conditional statement in Java. It shows
 * how to branch program execution based on a boolean condition, and highlights
 * that statements outside the if-else block always execute regardless of the condition.
 *
 * KEY POINTS:
 * - The if block executes when the condition evaluates to true
 * - The else block executes when the condition evaluates to false
 * - Code after the if-else structure runs unconditionally
 * - Relational operators (<, >, <=, >=, ==, !=) produce boolean results for conditions
 *
 * APPROACH:
 * 1. Compare two integers a and b using the > operator
 * 2. Print "a " if a > b, otherwise print "b "
 * 3. "is greater" prints regardless because it is outside the if-else block
 *
 * Time Complexity: O(1)
 * Space Complexity: O(1)
 */

/*
Java supports the usual logical conditions from mathematics:
    Less than: a < b
    Less than or equal to: a <= b
    Greater than: a > b
    Greater than or equal to: a >= b
    Equal to a == b
    Not Equal to: a != b

Java has the following conditional statements:

    Use if to specify a block of code to be executed, if a specified condition is true
    Use else to specify a block of code to be executed, if the same condition is false
    Use else if to specify a new condition to test, if the first condition is false
    Use switch to specify many alternative blocks of code to be executed
    
    
    Various Operators are discussed in Week 1 :-  " https://github.com/anonymousAAK/my-DSA-journey/blob/main/Week%201/16.Operators_in_java "
    */

public static void main(String args[])
{
    int a=10,b=15;       // Initialize two integers to compare
    if(a>b)              // Condition: is a greater than b?
    {
        System.out.print("a ");    // Executes only if a > b (skipped here since 10 < 15)
    }
    else
    {
        System.out.print("b ");    // Executes when a is NOT greater than b (this runs)
    }
    System.out.print("is greater");  // Always executes - outside if-else block
}

// "is greater" is written outside if-else so it would always print
