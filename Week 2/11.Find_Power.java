/*
Find power of a number


Write a program to find x to the power n (i.e. x^n). Take x and n from the user. You need to print the answer.
Note : For this question, you can assume that 0 raised to the power of 0 is 1.
  


Input format :
Two integers x and n (separated by space)
  
  
Output Format :
x^n (i.e. x raise to the power n)



How to approach?
1. Take x and n as input from the user.
2. x^n basically means, multiplying x, n times. So, initialize an ans with 1.
3. Now, run a loop until n becomes 0, and multiply x with ans each time.
4. Print the final ans obtained.



*/




import java.util.Scanner;
public class Solution {
    public static void main(String[] args) {
        Scanner s = new Scanner(System.in);
        int n = s.nextInt();
        int i = 2;
        while(i <= n / 2) {
            if(n % i == 0) {
              System.out.print(i + " ");
              }
            i += 1;
          }
      }
}
