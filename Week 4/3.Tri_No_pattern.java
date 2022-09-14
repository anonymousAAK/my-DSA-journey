/*
Triangle Number Pattern

Print the following pattern for the given N number of rows.
Pattern for N = 4
1
22
333
4444
  
  
Input format :
Integer N (Total no. of rows)
  
  
Output format :
Pattern in N lines

How to approach?
1. Take N as input from the user.
2. Figure out the number of rows, (which is N here) and run a loop for that.
3. Now, figure out how many columns are to be printed in ith row and run a loop for that
within this.
4. Now, figure out “What to print?” in a (row, column) number. It can depend on the
column number, row number or N.
  
  
Pseudo code for the given problem:
input=N
i=1
While i is less than or equal to N:
 j=1
 While j is less than or equal to i:
 print(i)
 Increment j by 1
 Increment i by 1
 Add a new line here
 
 */

import java.util.Scanner;

public class Solution {

	public static void main(String[] args) {
		
		int n;
		Scanner s = new Scanner(System.in);
		n = s.nextInt();
		
		for(int i = 1; i <=n ; i++){
            for(int j = 1; j <= i ; j++){
                System.out.print(i);
            }
            System.out.println();
        }
        
        
	}

}
