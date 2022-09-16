/*
Code : Character Pattern


Print the following pattern for the given N number of rows.
Pattern for N = 4
A
BC
CDE
DEFG


Input format :
Integer N (Total no. of rows)


Output format :
Pattern in N lines


How to approach?
1. Take N as input from the user.
2. Figure out the number of rows, (which is N here) and run a loop for that.
3. Now, figure out how many columns are to be printed for ith row (which is equal to row
number i.e i here) and run a loop for that within this.
4. Now, figure out “What to print?” in a particular row, column number. It can depend on
the column number, row number or N which depends on both column number and row
number here. As each row starts from ‘A’+i-1 and increases with 1 for each column.

*/

import java.util.Scanner;

public class Solution {

  public static void main(String[] args) {
    Scanner s = new Scanner(System.in);
    int n = s.nextInt();
    int currRow = 1;
    while (currRow <= n) {
      int currCol = 1;
      char ch = (char) ('A' + currRow - 1);
      while (currCol <= currRow) {
        System.out.print((char) (ch + currCol - 1));
        currCol += 1;
      }
      System.out.println();
      currRow += 1;
    }
  }
}
