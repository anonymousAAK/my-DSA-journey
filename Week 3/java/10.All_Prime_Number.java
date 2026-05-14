/*
 * WEEK 3 - LOOPS & NUMBER THEORY
 * Topic: All Prime Numbers up to N
 * File: 10.All_Prime_Number.java
 *
 * CONCEPT:
 * A prime number is a natural number greater than 1 that has no positive
 * divisors other than 1 and itself. This program finds and prints all
 * prime numbers from 2 to N using trial division.
 *
 * KEY POINTS / ALGORITHM:
 * 1. Loop through each number i from 2 to N.
 * 2. For each i, assume it is prime (isPrime = true).
 * 3. Check divisibility by all numbers j from 2 to i-1.
 * 4. If any j divides i evenly (i % j == 0), mark isPrime as false and break.
 * 5. If isPrime remains true after the inner loop, print i as a prime.
 * 6. Optimization possible: only check up to sqrt(i) instead of i-1.
 *
 * Time Complexity: O(n^2) - nested loops; could be O(n*sqrt(n)) with optimization
 * Space Complexity: O(1) - only boolean flag and loop variables
 *
 * Input Format: Integer N
 * Output Format: All prime numbers from 2 to N, each on a new line
 */



import java.util.Scanner;
public class Solution{
      public static void main(String[] args) {
            Scanner s = new Scanner(System.in);
            int n = s.nextInt();         // read upper bound N

            // Outer loop: check each number from 2 to N
            for(int i = 2; i <= n; i++) {
                   boolean isPrime = true;  // assume i is prime initially

                    // Inner loop: test divisibility by all numbers from 2 to i-1
                    for(int j = 2; j < i; j++) {
                            if(i % j == 0) {      // i is divisible by j, so not prime
                                 isPrime = false;
                                 break;            // no need to check further divisors
                                  }
                            }

                    // If no divisor was found, i is prime
                    if(isPrime) {
                            System.out.println(i);
              }
          }
      }
}
