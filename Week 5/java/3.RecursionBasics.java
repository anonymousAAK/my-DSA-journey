/*
 * WEEK 5 - FUNCTIONS & RECURSION
 * Topic: Recursion Basics
 *
 * WHAT IS RECURSION?
 * A function that calls itself to solve a smaller version of the same problem.
 *
 * EVERY RECURSIVE FUNCTION NEEDS:
 * 1. BASE CASE  — the condition that stops recursion (prevents infinite loop)
 * 2. RECURSIVE CASE — the function calling itself with a smaller/simpler input
 *
 * THE CALL STACK:
 * Each recursive call adds a new frame to the call stack.
 * When the base case is reached, frames are popped in reverse order.
 *
 * COMMON MISTAKE: Forgetting the base case → StackOverflowError
 *
 * PROBLEMS COVERED:
 * 1. Print numbers from N down to 1
 * 2. Factorial (N!)
 * 3. Sum of first N natural numbers
 * 4. Power (base^exp)
 *
 * Time Complexity:
 * - Factorial / Sum: O(n) — n recursive calls
 * - Power (naive): O(exp)
 * - Power (fast exponentiation): O(log exp)
 *
 * Space Complexity: O(n) for the call stack (n frames)
 */

public class RecursionBasics {

    // 1. Print N down to 1
    // Base case: n == 0 → stop
    static void printDesc(int n) {
        if (n == 0) return;       // base case
        System.out.print(n + " ");
        printDesc(n - 1);         // recursive call with smaller n
    }

    // 2. Print 1 up to N (print AFTER the recursive call)
    static void printAsc(int n) {
        if (n == 0) return;
        printAsc(n - 1);
        System.out.print(n + " ");
    }

    // 3. Factorial: N! = N * (N-1)!
    // Base case: 0! = 1, 1! = 1
    // Recurrence: fact(n) = n * fact(n-1)
    static long factorial(int n) {
        if (n <= 1) return 1;     // base case
        return n * factorial(n - 1);
    }

    // 4. Sum of first N natural numbers
    // Recurrence: sum(n) = n + sum(n-1)
    static int sum(int n) {
        if (n == 0) return 0;
        return n + sum(n - 1);
    }

    // 5. Power (base^exp) — naive O(exp)
    static long power(long base, int exp) {
        if (exp == 0) return 1;
        return base * power(base, exp - 1);
    }

    // 6. Fast Power (base^exp) — O(log exp)
    // If exp is even: base^exp = (base^(exp/2))^2
    // If exp is odd:  base^exp = base * base^(exp-1)
    static long fastPower(long base, int exp) {
        if (exp == 0) return 1;
        if (exp % 2 == 0) {
            long half = fastPower(base, exp / 2);
            return half * half;
        } else {
            return base * fastPower(base, exp - 1);
        }
    }

    public static void main(String[] args) {
        System.out.print("Descending 5 to 1: ");
        printDesc(5);
        System.out.println();

        System.out.print("Ascending 1 to 5: ");
        printAsc(5);
        System.out.println();

        System.out.println("5! = " + factorial(5));   // 120
        System.out.println("10! = " + factorial(10)); // 3628800

        System.out.println("sum(10) = " + sum(10));   // 55

        System.out.println("2^10 = " + power(2, 10));          // 1024
        System.out.println("2^10 (fast) = " + fastPower(2, 10)); // 1024
        System.out.println("3^20 (fast) = " + fastPower(3, 20)); // 3486784401
    }
}
