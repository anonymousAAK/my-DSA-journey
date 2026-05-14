/*
 * WEEK 2 - CONTROL FLOW
 * Topic: Total Salary Calculation using If-Else
 * File: 7.Total_Salary.java
 *
 * CONCEPT:
 * This file demonstrates using if-else-if chains to compute a total salary
 * based on a basic salary and a grade. Different grades determine different
 * allowance values. The program also uses Math.round() for rounding.
 *
 * KEY POINTS:
 * - HRA, DA, and PF are calculated as percentages of basic salary
 * - Allowance depends on grade: A=1700, B=1500, C or others=1300
 * - totalSalary = basic + hra + da + allowance - pf
 * - Math.round() rounds a double to the nearest long integer
 * - Casting with (int) truncates the long to int after rounding
 *
 * APPROACH:
 * 1. Read basic salary and grade from input
 * 2. Calculate HRA (20%), DA (50%), and PF (11%) from basic
 * 3. Use if-else-if to determine allowance based on grade
 * 4. Compute total salary from all components
 * 5. Round off and print the integer result
 *
 * Time Complexity: O(1)
 * Space Complexity: O(1)
 */

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
      int basic = s.nextInt();           // Read basic salary
      char grade = s.next().charAt(0);   // Read grade character (A, B, or C)
      double hra = 0.2 * basic;          // House Rent Allowance = 20% of basic
      double da = 0.5 * basic;           // Dearness Allowance = 50% of basic
      int allowance;
      // Determine allowance based on grade
      if(grade == 'A') {
          allowance = 1700;
        }
      else if(grade == 'B') {
          allowance = 1500;
        }
      else {
          allowance = 1300;
      }
      double pf = 0.11 * basic;            // Provident Fund = 11% of basic
      // Total = basic + hra + da + allowance - pf
      double totalSalary = basic + hra + da + allowance - pf;
      int ans = (int) Math.round(totalSalary); 
      //An internal function implemented in the Math class(no need to import as it is available as default) to round off the decimal values
      System.out.println(ans);
}
}
