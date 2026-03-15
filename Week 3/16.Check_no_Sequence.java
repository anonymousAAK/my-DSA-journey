/*
 * WEEK 3 - LOOPS & NUMBER THEORY
 * Topic: Check Number Sequence (Decreasing then Increasing)
 * File: 16.Check_no_Sequence.java
 *
 * CONCEPT:
 * Given a sequence of N integers, determine if it can be split into two parts:
 * - First part: strictly decreasing
 * - Second part: strictly increasing
 * The transition from decreasing to increasing can happen at most once.
 * A fully increasing or fully decreasing sequence is also valid.
 * Equal consecutive elements make the sequence invalid.
 *
 * KEY POINTS / ALGORITHM:
 * 1. Read N and the first number as 'prev'.
 * 2. Set isDec = true (assume sequence starts in decreasing phase).
 * 3. For each subsequent number:
 *    a. If current == prev: print "false" (not strictly monotonic).
 *    b. If current < prev (decreasing):
 *       - If isDec is false (was already increasing), print "false" (can't decrease again).
 *       - Otherwise, continue (still in decreasing phase).
 *    c. If current > prev (increasing):
 *       - If isDec is true, set isDec = false (transition to increasing phase).
 *       - Otherwise, continue (still in increasing phase).
 *    d. Update prev = current.
 * 4. If loop completes without returning false, print "true".
 *
 * Time Complexity: O(n) - single pass through the sequence
 * Space Complexity: O(1) - only stores previous value and a boolean flag
 *
 * Input Format:
 *   Line 1: Integer N (number of elements)
 *   Lines 2..N+1: One integer per line
 * Output Format: "true" or "false"
 *
 * Examples:
 *   [5, 3, 1, 2, 4] -> true (decreasing 5,3,1 then increasing 1,2,4)
 *   [1, 2, 3, 4, 5] -> true (fully increasing, decreasing part is empty)
 *   [5, 4, 3, 2, 1] -> true (fully decreasing, increasing part is empty)
 *   [1, 2, 3, 2, 1] -> false (increases then decreases - invalid)
 *   [1, 2, 2, 3]    -> false (equal elements - not strictly increasing)
 */



import java.util.Scanner;
public class Main {
     public static void main(String[] args) {
          Scanner s = new Scanner(System.in);
          int n = s.nextInt();           // number of elements in the sequence
          int prev = s.nextInt();        // read first element
          int count = 2, current;
          boolean isDec = true;          // flag: true = in decreasing phase

          // Process remaining elements one by one
          while(count <= n) {
              current = s.nextInt();     // read next element
              count++;

              // Equal consecutive elements -> not strictly monotonic
              if(current == prev) {
                  System.out.println("false");
                    return;
                  }

              // Current is less than previous -> sequence is decreasing here
              if(current < prev) {
                    if(isDec == false) {  // was in increasing phase, can't decrease again
                        System.out.println("false");
                        return;
             }
              }
              // Current is greater than previous -> sequence is increasing here
                     else {
                        if(isDec == true) {  // transition from decreasing to increasing
                            isDec = false;   // mark that we've entered increasing phase
                }
           }
                 prev = current;         // update prev for next comparison
       }

          // If we made it through the entire sequence, it's valid
          System.out.println("true");
}
}
