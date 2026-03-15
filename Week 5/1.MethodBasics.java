/*
 * WEEK 5 - FUNCTIONS & RECURSION
 * Topic: Method Basics in Java
 *
 * KEY CONCEPTS:
 * - A method (function) is a block of reusable code with a name.
 * - Syntax: returnType methodName(parameterList) { body }
 * - 'void' means the method returns nothing.
 * - 'return' exits a method and optionally passes a value back.
 *
 * WHY USE METHODS?
 * 1. Reusability: write once, call many times.
 * 2. Readability: break big problems into small named pieces.
 * 3. Maintainability: change behavior in one place.
 *
 * CALL STACK:
 * Each method call creates a new "frame" on the call stack.
 * When the method returns, its frame is popped off the stack.
 *
 * Time Complexity: O(1) per call for the examples below
 * Space Complexity: O(1) per call (one stack frame)
 */

import java.util.Scanner;

public class MethodBasics {

    // --- Static methods (can be called without creating an object) ---

    // Method with no parameters and no return value
    static void greet() {
        System.out.println("Hello from a method!");
    }

    // Method with parameters but no return value
    static void printSum(int a, int b) {
        System.out.println("Sum of " + a + " and " + b + " = " + (a + b));
    }

    // Method with parameters AND a return value
    static int add(int a, int b) {
        return a + b;
    }

    // Method demonstrating local variables (scope)
    static int multiply(int x, int y) {
        int result = x * y; // 'result' only exists inside this method
        return result;
    }

    // Method that demonstrates pass-by-value (Java always passes primitives by value)
    static void tryToChange(int n) {
        n = 999; // This only changes the LOCAL copy; the original is unaffected
        System.out.println("Inside tryToChange: n = " + n);
    }

    public static void main(String[] args) {
        // --- Calling methods ---

        greet(); // Output: Hello from a method!

        printSum(3, 7); // Output: Sum of 3 and 7 = 10

        int result = add(5, 6);
        System.out.println("add(5, 6) = " + result); // 11

        System.out.println("multiply(4, 3) = " + multiply(4, 3)); // 12

        // Pass-by-value demo
        int x = 42;
        tryToChange(x);
        System.out.println("After tryToChange: x = " + x); // Still 42

        // --- Interactive example ---
        Scanner sc = new Scanner(System.in);
        System.out.print("Enter two numbers to add: ");
        int a = sc.nextInt();
        int b = sc.nextInt();
        System.out.println("Result: " + add(a, b));
        sc.close();
    }
}
