/*
Code : Interesting Alphabets


Print the following pattern for the given number of rows.
Pattern for N = 5

E
DE
CDE
BCDE
ABCDE


Input format :
N (Total no. of rows)


Output format :
Pattern in N lines


How to approach?
1. Take N as input from the user.
2. Figure out the number of rows, (which is N here) and run a loop for that.
3. Now, figure out the number of columns in the ith row (which is equal to row number i.e i
here) and run a loop for that within this.
4. Now, figure out “What to print?” in a particular row, column number. It can depend on
the column number, row number or N which depends on all of them here. As each row
starts from ‘A’+n-i and an increment of 1 is done for each column.


*/
import java.util.Scanner;

public class Solution {

  public static void main(String[] args) {
    Scanner s = new Scanner(System.in);
    int n = s.nextInt();
    int currRow = 1;
    while (currRow <= n) {
      int currCol = 1;
      char ch = (char) ('A' + n - currRow);
      while (currCol <= currRow) {
        System.out.print((char) (ch + currCol - 1));
        currCol += 1;
      }
      System.out.println();
      currRow += 1;
    }
  }
}
