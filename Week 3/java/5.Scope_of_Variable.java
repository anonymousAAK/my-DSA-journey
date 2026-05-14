/*
 * WEEK 3 - LOOPS & NUMBER THEORY
 * Topic: Scope of Variables
 * File: 5.Scope_of_Variable.java
 *
 * CONCEPT:
 * The scope of a variable is defined by the curly brackets {} inside which
 * it is declared. A variable is only accessible within its scope and is
 * unknown to the compiler outside of it. This applies to all blocks:
 * loops, conditionals, methods, and classes.
 *
 * KEY POINTS / ALGORITHM:
 * 1. Variables declared inside a for loop header (e.g., int i) are scoped to that loop.
 * 2. Variables declared inside a loop body are scoped to that body block.
 * 3. Variables declared in main() are accessible throughout main but not outside.
 * 4. Variables declared inside if/else blocks are scoped to those blocks.
 * 5. Inner scopes can access variables from outer scopes, but not vice versa.
 *
 * Time Complexity: N/A (conceptual topic, not an algorithm)
 * Space Complexity: N/A
 */

/* --- Scope of variable in a for loop --- */
for (initializationStatement; test_expression; updateStatement) {
// Scope of variable defined in loop - only accessible here
}


// Example: for loop scope
public static void main(String[] args) {
        for (int i=0; i<5; i++) {
              int j=2; // Scope of i and j are both inside the loop they can't be used outside
          }
          // i and j are NOT accessible here - they are out of scope

/* --- Scope of variable in a while loop --- */
        while(test_expression) {
// Scope of variable defined in loop - only accessible inside this block
              }

// Example: while loop scope
public static void main(String[] args) {
          int i=0;                       // i is declared in main - accessible throughout main
          while(i<5){
              int j=2; // Scope of i is main and scope of j is only the loop
               i++;
          }
          // j is NOT accessible here, but i still is
      }

/* --- Scope of variable in conditional statements --- */
  if(test_expression) {
// Scope of variable defined in the conditional statement - only accessible here
}


// Example: if-block scope
public static void main(String[] args) {
      int i=0;                           // i is scoped to main
       if (i<5){
          int j=5; // Scope of j is only in this if-block
}
// cout<<j;                              // j is NOT accessible here - would cause error
