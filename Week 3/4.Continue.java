/*
❖Continue


The continue keyword can be used in any of the loop control structures. It causes the loop to immediately jump to the next iteration of the loop.

  ● Example: (using for loop)
*/


public static void main(String[] args){
      for (int i=1; i <= 5; i++) {
            if(i==3){
              continue;
          }
           System.out.println(i);
        }
    }
/*Output:
1
2
4
5

*/


// ● Example: (using while loop)


public static void main(String[] args){
        int i=1;
        while (i <= 5) {
            if(i==3){
                i++;
// if increment isn’t done here then loop will run
// infinite time for i=3
                continue;
          }
        System.out.println(i);
         i++;
      }
   }
/*
Output:
1
2
4
5

*/
