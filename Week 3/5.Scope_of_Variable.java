/*
Scope of variables


Scope of variables is the curly brackets {} inside which they are defined. Outside 
which they aren’t known to the compiler. Same is for all loops and conditional


statement (if).
  
 
❖Scope of variable - for loop

*/
for (initializationStatement; test_expression; updateStatement) {
// Scope of variable defined in loop
}


// Example:
public static void main(String[] args) {
        for (int i=0; i<5; i++) {
              int j=2; // Scope of i and j are both inside the loop they can’t be used outside
          }
//   ❖Scope of variable for while loop
        while(test_expression) {
// Scope of variable defined in loop
              }
  
public static void main(String[] args) {
          int i=0;
          while(i<5){
              int j=2; // Scope of i is main and scope of j is only the loop
               i++;
          }
      }
// ❖ Scope of variable for conditional statements

  if(test_expression) {
// Scope of variable defined in the conditional statement
}
  
  
public static void main(String[] args) {
      int i=0;
       if (i<5){
          int j=5; // Scope of j is only in this block
}
// cout<<j; 
