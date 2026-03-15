/*
 * Increment & Decrement Operators
 *
 * PRE-INCREMENT (++a):
 *   Increases value by 1 FIRST, then uses the new value in the expression.
 *
 * POST-INCREMENT (a++):
 *   Uses the CURRENT value in the expression, then increases by 1.
 *
 * PRE-DECREMENT (--a):
 *   Decreases value by 1 FIRST, then uses the new value.
 *
 * POST-DECREMENT (a--):
 *   Uses the CURRENT value, then decreases by 1.
 *
 * IMPORTANT: In Java (unlike C/C++), the behavior of these operators is
 * well-defined even in complex expressions — Java evaluates left to right.
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
