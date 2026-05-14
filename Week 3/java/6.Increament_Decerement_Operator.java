/*
 * WEEK 3 - LOOPS & NUMBER THEORY
 * Topic: Increment & Decrement Operators
 * File: 6.Increament_Decerement_Operator.java
 *
 * CONCEPT:
 * Increment (++) and decrement (--) operators modify a variable's value by 1.
 * They come in two forms: prefix (++a/--a) and postfix (a++/a--), which differ
 * in WHEN the modification happens relative to the expression evaluation.
 *
 * KEY POINTS / ALGORITHM:
 * 1. PRE-INCREMENT (++a): Increases value by 1 FIRST, then uses the new value.
 * 2. POST-INCREMENT (a++): Uses the CURRENT value, then increases by 1.
 * 3. PRE-DECREMENT (--a): Decreases value by 1 FIRST, then uses the new value.
 * 4. POST-DECREMENT (a--): Uses the CURRENT value, then decreases by 1.
 * 5. In for loops, i++ and ++i produce the same result (update happens separately).
 * 6. In Java (unlike C/C++), behavior is well-defined even in complex expressions
 *    because Java evaluates strictly left to right.
 *
 * Time Complexity: O(1) for each operation
 * Space Complexity: O(1)
 */

public class IncrementDecrementOperator {
    public static void main(String[] args) {
        int a = 5;
        System.out.println("Initial a = " + a);

        // Post-increment: use current value (5), then increment to 6
        System.out.println("a++ = " + (a++));  // prints 5
        System.out.println("a is now = " + a); // prints 6

        // Pre-increment: increment to 7 first, then use
        System.out.println("++a = " + (++a));  // prints 7
        System.out.println("a is now = " + a); // prints 7

        // Post-decrement: use current value (7), then decrement to 6
        System.out.println("a-- = " + (a--));  // prints 7
        System.out.println("a is now = " + a); // prints 6

        // Pre-decrement: decrement to 5 first, then use
        System.out.println("--a = " + (--a));  // prints 5
        System.out.println("a is now = " + a); // prints 5

        // Common patterns in loops
        System.out.println("\n--- In loops ---");
        int[] arr = {10, 20, 30, 40, 50};

        // Post-increment in loop (most common)
        System.out.print("Using i++: ");
        for (int i = 0; i < arr.length; i++) {
            System.out.print(arr[i] + " ");
        }
        System.out.println();

        // Pre-increment (same result in for loop)
        System.out.print("Using ++i: ");
        for (int i = 0; i < arr.length; ++i) {
            System.out.print(arr[i] + " ");
        }
        System.out.println();
    }
}
