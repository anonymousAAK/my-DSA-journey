/*
 * WEEK 3 - LOOPS & NUMBER THEORY
 * Topic: For Loop Basics
 * File: 1.For_loop.java
 *
 * CONCEPT:
 * The for loop is a control flow statement that allows code to be executed
 * repeatedly based on a given condition. It combines initialization, condition
 * checking, and update in a single line, making it ideal for counted iterations.
 *
 * KEY POINTS / ALGORITHM:
 * 1. Initialization - Executed once at the start; sets up loop control variable.
 * 2. Test Condition - Evaluated before each iteration; loop runs while true.
 * 3. Update Statement - Executed after each iteration; modifies loop variable.
 * 4. Any of the three parts can be omitted (even all three for an infinite loop).
 * 5. Initialization can be done outside the loop; update can be inside the body.
 *
 * Time Complexity: O(n) - where n is the number of iterations
 * Space Complexity: O(1) - only loop control variables used
 */


/* --- FOR LOOP SYNTAX --- */
for (initializationStatement; test_expression; updateStatement) {
// Statements to be executed till test_expression is true
}


// Example Code 1: Basic for loop with all three parts
public static void main(String[] args) {
        for(int i = 0; i < 3; i++) {       // i starts at 0, runs while i < 3, increments each time
            System.out.print("Inside for loop : ");
            System.out.println(i);          // prints current value of i
            }
         System.out.println("Done");        // executes after loop finishes
      }

/*
Output:
Inside for Loop : 0
Inside for Loop : 1
Inside for Loop : 2
Done

*/


/*
 * OPTIONAL PARTS IN FOR LOOP:
 * In a for loop, it is not compulsory to write all three statements i.e.
 * initializationStatement, test_expression and updateStatement. We can skip one
 * or more of them (even all three).
 * Above code can be written as:
 */

// Example Code 2: Initialization moved outside the for loop
public static void main(String[] args) {
      int i = 1; // initialization is done outside the for loop
      for(; i < =5; i++) {              // no initialization part inside for(...)
          System.out.println(i);
        }
      }

// OR

// Example Code 3: Both initialization and update moved outside for(...)
public static void main(String[] args) {
      int i = 1; // initialization is done outside the for loop
      for(; i < =5; ) {                 // only condition remains inside for(...)
          System.out.println(i);
           i++; // update statement written inside the loop body
          }
        }
