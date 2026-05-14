/*
 * WEEK 2 - CONTROL FLOW
 * Topic: While Loop Basics
 * File: 4.While_Loop.java
 *
 * CONCEPT:
 * This file demonstrates while loop behavior in Java, specifically the
 * subtle difference between assignment (=) and comparison (==) inside
 * a loop condition. It shows how assignment in a condition can limit
 * loop execution to a single iteration.
 *
 * KEY POINTS:
 * - The while loop repeats a block of code as long as the condition is true
 * - Using assignment (x=5) in a condition resets x to 5 every iteration
 * - Since x is reset to 5 each time, the loop only runs when y also equals 5
 * - After one iteration y becomes 6, but x is reset to 5, so the condition fails
 *
 * APPROACH:
 * 1. Initialize x=5 and y=5
 * 2. Loop condition: (x=5)==y assigns 5 to x, then compares with y
 * 3. First iteration: x=5, y=5 -> true, prints "Hello", x becomes 6, y becomes 6
 * 4. Second check: x is reassigned to 5, y=6, so (5)==6 is false -> loop ends
 * 5. Result: "Hello" is printed exactly once
 *
 * Time Complexity: O(1) - loop runs exactly once
 * Space Complexity: O(1)
 */

/*
Loops can execute a block of code as long as a specified condition is reached.

Loops are handy because they save time, reduce errors, and they make code more readable.
  
Java While Loop

The while loop loops through a block of code as long as a specified condition is true:

Syntax

while (condition) {
  // code block to be executed
}

*/

//Q.The number of Hello printed on the screen for the following code will be:


public static void main (String[] args) {
    int x=5;
    int y=5;
    while((x=5)==y)       // Assignment: x is set to 5, then compared with y
    {
        System.out.println("Hello");  // Prints only once (when y is still 5)
        x++;              // x becomes 6, but will be reset to 5 on next condition check
        y++;              // y becomes 6, making condition (5==6) false next time
    }
}

// The loop is executed only once when y=5.

// The condition is false when y=6.
