/*
Code : Reverse Number Pattern

Print the following pattern for the given N number of rows.
Pattern for N = 4
1
21
321
4321



Input format :
Integer N (Total no. of rows)


Output format :
Pattern in N lines

How to approach?
1. Take N as input from the user.
2. Figure out the number of rows, (which is N here) and run a loop for that.
3. Now, figure out how many columns are to be printed in ith row and run a loop for that
within this.
4. Now, figure out “What to print?” in a particular (row, column). It can depend on the
column number, row number or N.

*/

import java.util.Scanner;

public class Solution {

  public static void main(String[] args) {
    Scanner s = new Scanner(System.in);
    int n = s.nextInt();
    int currRow = 1;
    while (currRow <= n) {
      int currCol = currRow;
      while (currCol >= 1) {
        System.out.print(currCol);
        currCol -= 1;
      }
      System.out.println();
      currRow += 1;
    }
  }
}
