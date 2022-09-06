/*

Variations of for loop


● The three expressions inside for loop are optional. That means, they can be
omitted as per requirement.

*/


//Example code 1: Initialization part removed –


public static void main(String[] args) {
      int i = 0;
      for( ; i < 3; i++) {
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
