/*
Loops can execute a block of code as long as a specified condition is reached.

Loops are handy because they save time, reduce errors, and they make code more readable.
  
Java While Loop

The while loop loops through a block of code as long as a specified condition is true:

Syntax

while (condition) {
  // code block to be executed
}

*/

//Q.The number of Hello printed on the screen for the following code will be:


public static void main (String[] args) {
    int x=5;
    int y=5;
    while((x=5)==y)
    {
        System.out.println("Hello");
        x++;
        y++;
    }
}

// The loop is executed only once when y=5.

// The condition is false when y=6.
