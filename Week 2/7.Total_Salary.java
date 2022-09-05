/*Total Salary

Write a program to calculate the total salary of a person. The user has to enter the basic salary (an integer) and the grade (an uppercase character), 
and depending upon which the total salary is calculated as -
    
  
  totalSalary = basic + hra + da + allow – pf

where :
hra   = 20% of basic
da    = 50% of basic
allow = 1700 if grade = ‘A’
allow = 1500 if grade = ‘B’
allow = 1300 if grade = ‘C' or any other character
pf    = 11% of basic.
Round off the total salary and then print the integral part only.
Note: Try finding out a function on the internet to do so.
  
  
Input format :
Basic salary & Grade (separated by space)
  
Output Format :
Total Salary

*/
/*
How to Approach?
1. Take basic and grade as input from the user.
2. Calculate hra, da, pf by using basic.
3. Check for the grade and then take the allowance corresponding to it.
4. Calculate total salary by using basic, hra, da, pf and allowance calculated above.
5. Round off the total salary using library function and then print it.
*/


import java.util.Scanner;

public class Solution {
    public static void main(String[] args) {
      Scanner s = new Scanner(System.in);
      int basic = s.nextInt();
      char grade = s.next().charAt(0);
      double hra = 0.2 * basic;
      double da = 0.5 * basic;
      int allowance;
      if(grade == 'A') {
          allowance = 1700;
        }
      else if(grade == 'B') {
          allowance = 1500;
        }
      else {
          allowance = 1300;
      }
      double pf = 0.11 * basic;
      double totalSalary = basic + hra + da + allowance - pf;
      int ans = (int) Math.round(totalSalary); 
      //An internal function implemented in the Math class(no need to import as it is available as default) to round off the decimal values
      System.out.println(ans);
}
}
