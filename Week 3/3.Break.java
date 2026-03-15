/*
 * WEEK 3 - LOOPS & NUMBER THEORY
 * Topic: Break Statement
 * File: 3.Break.java
 *
 * CONCEPT:
 * The break statement terminates the innermost enclosing loop (for, while,
 * do-while) immediately when encountered. Execution continues with the
 * first statement after the terminated loop.
 *
 * KEY POINTS / ALGORITHM:
 * 1. break exits only the innermost loop it is placed in.
 * 2. Works with for, while, and do-while loops.
 * 3. In nested loops, break only exits the inner loop; outer loop continues.
 * 4. Commonly used with if-conditions to exit early when a goal is met.
 * 5. Also used in switch-case statements to prevent fall-through.
 *
 * Time Complexity: O(k) where k <= n; loop may exit before completing all iterations
 * Space Complexity: O(1)
 */


// Example 1: break inside a for loop - exits when i reaches 5
public static void main(String[] args) {
      for(int i = 1; i < 10; i++) {
          System.out.println(i);
          if(i == 5) {
              break;                     // loop terminates here when i == 5
          }
        }
      }

/*
Output:
1
2
3
4
5

*/


// Example 2: break inside a while loop - same behavior, exits at i == 5
public static void main(String[] args) {
      int i = 1;
      while (i <= 10) {
          System.out.println(i);
              if(i==5)
            {
               break;                   // exits the while loop immediately
              }
          i++;
      }
  }

/*
Output:
1
2
3
4
5

*/

/*
 * INNER LOOP BREAK:
 * When loops are nested, break only exits the innermost loop.
 * The outer loop continues its iterations normally.
 */

// Example Code 1: break in inner for loop - outer loop still runs 3 times
public static void main(String[] args) {
      for (int i=1; i <=3; i++) {        // outer loop: runs 3 times
            System.out.println(i);
            for (int j=1; j<= 5; j++)    // inner loop: would run 5 times
                {
                System.out.println("in");
                if(j==1)
                 {
                break;                   // breaks only inner loop at j==1
            }
          }
      }
}
/*
Output:
1
in…
2
in…
3
in…

*/


// Example Code 2: break in inner while loop - same concept with while loops
public static void main(String[] args) {
      int i=1;
      while (i <=3) {                    // outer while loop
          System.out.println(i);
          int j=1;
          while (j <= 5)                 // inner while loop
          {
              System.out.println("in");
              if(j==1)
            {
              break;                     // breaks only the inner while loop
            }
            j++;
          }
          i++;
        }
    }

/*
Output:
1
in…
2
in…
3
in…
