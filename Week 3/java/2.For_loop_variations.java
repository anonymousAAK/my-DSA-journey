/*
 * WEEK 3 - LOOPS & NUMBER THEORY
 * Topic: Variations of For Loop
 * File: 2.For_loop_variations.java
 *
 * CONCEPT:
 * The three expressions inside a for loop (initialization, condition, update)
 * are all optional. This file demonstrates various combinations of omitting
 * one or more parts, including infinite loops and multi-variable loops.
 *
 * KEY POINTS / ALGORITHM:
 * 1. Initialization can be moved before the loop.
 * 2. Update can be placed inside the loop body.
 * 3. Omitting the condition creates an infinite loop.
 * 4. Omitting all three parts also creates an infinite loop: for(;;).
 * 5. Multiple variables can be initialized, tested, and updated using commas.
 * 6. Multiple conditions must be combined with logical operators (&&, ||).
 *
 * Time Complexity: O(n) for finite loops, infinite for loops without termination
 * Space Complexity: O(1) - only loop control variables used
 */


// Example code 1: Initialization part removed - declared before the loop
public static void main(String[] args) {
      int i = 0;                        // initialization done outside for(...)
      for( ; i < 3; i++) {              // only condition and update remain
          System.out.println(i);
      }
    }

/*
Output:
0
1
2

*/

// Example code 2: Update part removed from for(...) - placed inside loop body
public static void main(String[] args) {
      for(int i = 0; i < 3; ) {         // no update in for(...) header
          System.out.println(i);
          i++;                           // update done manually inside the body
      }
    }

/*
Output:
0
1
2
*/


// Example code 3: Condition removed - creates an INFINITE loop (runs forever)
public static void main(String[] args) {
      for(int i = 0; ; i++) {           // no condition means always true
          System.out.println(i);         // prints 0, 1, 2, 3, ... indefinitely
      }
  }


// Example code 4: All three expressions removed - another form of INFINITE loop
public static void main(String[] args) {
for( ; ; ) {                            // equivalent to while(true)
      System.out.print("Inside for loop"); // runs forever with no way to exit
    }
}

/*
 * MULTIPLE VARIABLES IN A FOR LOOP:
 * - Multiple initializations and updates are separated by commas.
 * - Multiple conditions must be combined using logical operators (&&, ||).
 */

// Example code 5: Two loop variables (i counts up, j counts down)
public static void main(String[] args) {
      for(int i = 0, j = 4; i < 5 && j >= 0; i++, j--) {  // two vars, two updates
          System.out.println(i + " " + j);                  // prints pairs until either condition fails
      }
    }
/*Output:
0 4
1 3
2 2
3 1
4 0
*/
