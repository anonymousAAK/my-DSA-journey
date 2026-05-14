/*
 * WEEK 2 - CONTROL FLOW
 * Topic: Infinite Loop Demonstration
 * File: 5.Infinite_Loop.java
 *
 * CONCEPT:
 * This file demonstrates how an infinite loop occurs in Java. When both
 * the loop variable and the comparison variable are incremented at the
 * same rate, the loop condition never becomes false, causing the loop
 * to run forever.
 *
 * KEY POINTS:
 * - An infinite loop occurs when the termination condition is never met
 * - Here, x and y both start equal and both increment by 1 each iteration
 * - Since x == y is always true (they increase together), the loop never ends
 * - Contrast with 4.While_Loop.java where assignment (x=5) prevents infinite looping
 *
 * APPROACH:
 * 1. Initialize x=5 and y=5
 * 2. Condition x==y is true (5==5), so loop body executes
 * 3. Both x and y are incremented: x=6, y=6
 * 4. Condition x==y is still true (6==6), loop continues indefinitely
 *
 * WARNING: This program will run forever and must be manually terminated (Ctrl+C).
 *
 * Time Complexity: O(infinity) - loop never terminates
 * Space Complexity: O(1)
 */

public static void main (String[] args) {
    int x=5;
    int y=5;
    while(x==y)           // Comparison: checks if x equals y (always true here)
    {
        System.out.println("Hello");  // Prints infinitely
        x++;              // x increments: 6, 7, 8, ...
        y++;              // y increments at the same rate: 6, 7, 8, ...
    }
}

//x and y are equal every time . Hence infinite loop.
