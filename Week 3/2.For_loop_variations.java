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

//Example code 2: Updation part removed

public static void main(String[] args) {
      for(int i = 0; i < 3; ) {
          System.out.println(i);
          i++;
      }
    }

/*
Output:
0
1
2
*/


// Example code 3: Condition expression removed , thus making our loop infinite –

public static void main(String[] args) {
      for(int i = 0; ; i++) {
          System.out.println(i);
      }
  }


//Example code 4:
//We can remove all the three expression, thus forming an infinite loop

public static void main(String[] args) {
for( ; ; ) {
      System.out.print("Inside for loop");
    }
}

/*
● Multiple statements inside for loop
We can initialize multiple variables, have multiple conditions and multiple update
statements inside a for loop. We can separate multiple statements using
comma, but not for conditions. They need to be combined using logical
operators.


Example code:

*/
public static void main(String[] args) {
      for(int i = 0, j = 4; i < 5 && j >= 0; i++, j--) {
          System.out.println(i + " " + j);
      }
    }
/*Output:
0 4
1 3
2 2
3 1
4 0
*/
