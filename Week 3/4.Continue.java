/*
 * WEEK 3 - LOOPS & NUMBER THEORY
 * Topic: Continue Statement
 * File: 4.Continue.java
 *
 * CONCEPT:
 * The continue statement skips the remaining code in the current iteration
 * and jumps to the next iteration of the loop. Unlike break (which exits
 * the loop entirely), continue only skips the current pass.
 *
 * KEY POINTS / ALGORITHM:
 * 1. In a for loop, continue jumps to the update statement, then re-checks condition.
 * 2. In a while loop, continue jumps directly to the condition check.
 * 3. CAUTION in while loops: if the increment is after continue, it will be
 *    skipped, potentially causing an infinite loop. Always update the loop
 *    variable BEFORE the continue statement in while loops.
 * 4. Useful for skipping specific values (e.g., skip multiples, skip invalid data).
 *
 * Time Complexity: O(n) - loop still runs all iterations, just skips some work
 * Space Complexity: O(1)
 */


// Example 1: continue in a for loop - skips printing when i == 3
public static void main(String[] args){
      for (int i=1; i <= 5; i++) {
            if(i==3){
              continue;                  // skips println for i==3, jumps to i++
          }
           System.out.println(i);        // prints 1, 2, 4, 5 (3 is skipped)
        }
    }
/*Output:
1
2
4
5

*/


// Example 2: continue in a while loop - must increment BEFORE continue
public static void main(String[] args){
        int i=1;
        while (i <= 5) {
            if(i==3){
                i++;                     // CRITICAL: increment before continue
// if increment isn't done here then loop will run
// infinite time for i=3
                continue;               // skip to condition check with i=4
          }
        System.out.println(i);          // prints 1, 2, 4, 5 (3 is skipped)
         i++;                           // normal increment for non-skipped iterations
      }
   }
/*
Output:
1
2
4
5

*/
