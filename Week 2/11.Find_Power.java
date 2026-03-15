/*
 * Find power of a number: x^n
 *
 * PROBLEM:
 * Given integers x and n, compute x raised to the power n.
 * Note: 0^0 is defined as 1 for this problem.
 *
 * APPROACH:
 * 1. Take x and n as input.
 * 2. Initialize ans = 1.
 * 3. Multiply x with ans, n times.
 * 4. Print the final result.
 *
 * Time Complexity: O(n) — we multiply n times
 * Space Complexity: O(1)
 *
 * NOTE: See Week 5 for O(log n) fast exponentiation.
 */

import java.util.Scanner;

public class FindPower {
    public static void main(String[] args) {
        Scanner s = new Scanner(System.in);
        System.out.print("Enter base x and exponent n: ");
        int x = s.nextInt();
        int n = s.nextInt();

        long ans = 1;
        for (int i = 0; i < n; i++) {
            ans *= x;
        }
        System.out.println(x + "^" + n + " = " + ans);
        s.close();
    }
}
