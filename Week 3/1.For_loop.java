/*
for loop

Loop statements allows us to execute a block of statements several number of
times depending on certain condition. for loop is kind of loop in which we give
initialization statement, test expression and update statement can be written in
one line.


Inside for, three statements are written –
a. Initialization – used to initialize your loop control variables. This statement is
executed first and only once.
b. Test condition – this condition is checked everytime we enter the loop.
Statements inside the loop are executed till this condition evaluates to true. As
soon as condition evaluates to false, loop terminates and then first statement
after for loop will be executed next.
c. Updation – this statement updates the loop control variable after every
execution of statements inside loop. After updation, again test conditon is
checked. If that comes true, the loop executes and process repeats. And if
condition is false, the loop terminates.


*/


for (initializationStatement; test_expression; updateStatement) {
// Statements to be executed till test_expression is true
}


// Example Code :
public static void main(String[] args) {
        for(int i = 0; i < 3; i++) {
            System.out.print("Inside for loop : ");
            System.out.println(i);
            }
         System.out.println("Done");
      }

/*
Output:
Inside for Loop : 0
Inside for Loop : 1
Inside for Loop : 2
Done

*/


/*
In for loop its not compulsory to write all three statements i.e.
initializationStatement, test_expression and updateStatement. We can skip one
or more of them (even all three)
Above code can be written as:

*/
public static void main(String[] args) {
      int i = 1; //initialization is done outside the for loop
      for(; i < =5; i++) {
          System.out.println(i);
        }
      }
OR
public static void main(String[] args) {
      int i = 1; //initialization is done outside the for loop
      for(; i < =5; ) {
          System.out.println(i);
           i++; // update Statement written here
          }
        }
