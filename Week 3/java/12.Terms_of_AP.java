/*
 * WEEK 3 - LOOPS & NUMBER THEORY
 * Topic: Terms of Arithmetic Progression (AP)
 * File: 12.Terms_of_AP.java
 *
 * CONCEPT:
 * Print the first X terms of the series 3N + 2 that are NOT multiples of 4.
 * The series 3N + 2 generates: 5, 8, 11, 14, 17, 20, 23, ...
 * After filtering out multiples of 4 (8, 20, ...): 5, 11, 14, 17, 23, ...
 *
 * KEY POINTS / ALGORITHM:
 * 1. Read x (number of terms to print).
 * 2. Use two counters: 'count' for how many valid terms printed, 'current' for N.
 * 3. For each N, compute num = 3*N + 2.
 * 4. If num is NOT divisible by 4, print it and increment count.
 * 5. Always increment current (N) regardless of whether we printed.
 * 6. Stop when count reaches x.
 *
 * Time Complexity: O(x) in the best case, O(x * k) where k depends on how
 *                  many multiples of 4 are skipped; effectively linear.
 * Space Complexity: O(1)
 *
 * Input Format: Integer x (number of terms to print)
 * Output Format: Terms separated by spaces
 */
import java.util.Scanner;

public class Main {

    public static void main(String[] args) {

          Scanner s = new Scanner(System.in);

          int n = s.nextInt();           // number of terms to print

          int count = 1, current = 1;    // count tracks printed terms, current is N

          while(count <= n) {            // loop until we've printed n valid terms

              int num = 3 * current + 2; // compute the series term: 3N + 2

              if(num % 4 != 0) {         // only print if NOT a multiple of 4

                    System.out.print(num + " ");  // print valid term

                    count++;             // increment count of printed terms

                  }

               current++;               // always move to next N

          }

        }

 }


