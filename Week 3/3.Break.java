/*
break statement: 

The break statement terminates the loop (for, while and do. while loop) immediately when it is encountered. As soon as break is
encountered inside a loop, the loop terminates immediately. Hence the statement after loop will be executed next.
  

● Example: (using break inside for loop|)

*/


public static void main(String[] args) {
      for(int i = 1; i < 10; i++) {
          System.out.println(i);
          if(i == 5) {
              break;
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


// ● Example: (using break inside while loop)

public static void main(String[] args) {
      int i = 1;
      while (i <= 10) {
          System.out.println(i);
              if(i==5)
            {
               break;
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
● Inner loop break:
When there are two more loops inside one another. Break from innermost loop will just exit that loop.

*/
// Example Code 1:
public static void main(String[] args) {
      for (int i=1; i <=3; i++) {
            System.out.println(i);
            for (int j=1; j<= 5; j++)
                {
                System.out.println(“in”);
                if(j==1)
                 {
                break;
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


// Example Code 2:
public static void main(String[] args) {
      int i=1;
      while (i <=3) {
          System.out.println(i);
          int j=1;
          while (j <= 5)
          {
              System.out.println(“in”);
              if(j==1)
            {
              break;
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
