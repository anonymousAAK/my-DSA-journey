/*
 * WEEK 3 - LOOPS & NUMBER THEORY
 * Topic: Sum or Product of First N Natural Numbers
 * File: 11.Sum-Or-Product.java
 *
 * CONCEPT:
 * Given an integer N and a choice C, compute either the sum (C=1) or
 * product (C=2) of all integers from 1 to N. If C is any other value,
 * output -1. Demonstrates conditional logic combined with while loops.
 *
 * KEY POINTS / ALGORITHM:
 * 1. Read N (upper bound) and C (choice: 1=sum, 2=product).
 * 2. If C == 1: initialize sum=0, loop from 1 to N adding each number.
 * 3. If C == 2: initialize product=1, loop from 1 to N multiplying each number.
 * 4. Otherwise: print -1 (invalid choice).
 * 5. Note: product uses 1 as identity (not 0), since 0 * anything = 0.
 *
 * Time Complexity: O(n) - single pass from 1 to N
 * Space Complexity: O(1)
 *
 * Input Format:
 *   Line 1: Integer N
 *   Line 2: Choice C (1 for sum, 2 for product)
 * Output Format: Sum or product, or -1 for invalid choice
 */

import java.util.Scanner;
public class Main {
    public static void main(String[] args) {
        Scanner s = new Scanner(System.in);
        int n = s.nextInt();             // upper bound
        int choice = s.nextInt();        // 1 = sum, 2 = product

        if(choice == 1) {
            // Calculate sum of 1 to N
            int sum = 0, num = 1;        // sum starts at 0 (additive identity)
            while(num <= n) {
                sum += num;              // accumulate running sum
                num++;
              }
        System.out.println(sum);
        }else if(choice == 2) {
             // Calculate product of 1 to N (i.e., N factorial)
             int product = 1, num = 1;   // product starts at 1 (multiplicative identity)
             while(num <= n) {
                  product *= num;         // accumulate running product
                   num++;
            }
         System.out.println(product);
          } else {
         System.out.println("-1");       // invalid choice
      }
    }
}


