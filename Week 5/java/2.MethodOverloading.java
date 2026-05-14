/*
 * WEEK 5 - FUNCTIONS & RECURSION
 * Topic: Method Overloading
 *
 * DEFINITION:
 * Method overloading = multiple methods with the SAME name but DIFFERENT
 * parameter lists (different number, type, or order of parameters).
 *
 * The compiler picks the right version at compile time — this is called
 * "compile-time polymorphism" or "static dispatch."
 *
 * RULES:
 * - Different parameter count OR different parameter types
 * - Return type alone does NOT distinguish overloaded methods
 *
 * WHY IT MATTERS FOR DSA:
 * Many utility methods (e.g., print, compare, swap) benefit from overloading
 * to handle different data types without renaming.
 *
 * Time Complexity: O(1) per call
 */

public class MethodOverloading {

    // Version 1: two ints
    static int add(int a, int b) {
        System.out.println("add(int, int) called");
        return a + b;
    }

    // Version 2: three ints
    static int add(int a, int b, int c) {
        System.out.println("add(int, int, int) called");
        return a + b + c;
    }

    // Version 3: two doubles
    static double add(double a, double b) {
        System.out.println("add(double, double) called");
        return a + b;
    }

    // Overloaded print utility — prints an array of any primitive type
    static void printArray(int[] arr) {
        System.out.print("int[]: ");
        for (int x : arr) System.out.print(x + " ");
        System.out.println();
    }

    static void printArray(double[] arr) {
        System.out.print("double[]: ");
        for (double x : arr) System.out.print(x + " ");
        System.out.println();
    }

    static void printArray(char[] arr) {
        System.out.print("char[]: ");
        for (char c : arr) System.out.print(c + " ");
        System.out.println();
    }

    public static void main(String[] args) {
        System.out.println(add(2, 3));          // calls version 1
        System.out.println(add(1, 2, 3));       // calls version 2
        System.out.println(add(1.5, 2.5));      // calls version 3

        printArray(new int[]{1, 2, 3});
        printArray(new double[]{1.1, 2.2, 3.3});
        printArray(new char[]{'a', 'b', 'c'});
    }
}
