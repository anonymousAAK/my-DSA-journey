/*
Nth Fibonacci Number


Nth term of Fibonacci series F(n), where F(n) is a function, is calculated using the following formula -
    F(n) = F(n-1) + F(n-2), 
    Where, F(1) =  0, 
           F(2) = 1
Provided N you have to find out the Nth Fibonacci Number.


Input Format :
The first line of each test case contains a real number ‘N’.


Output Format :
For each test case, return its equivalent Fibonacci number.

*/

/*
How to approach?
The Fibonacci numbers are the numbers in the sequence such that the current number will be the
sum of the previous two numbers i.e. F(n) = F(n-1) + F(n-2)
And given that F(1)=F(2)=1
1. Take the number as input from the user.
2. Initialize 1st and second number with 1.
3. Now, start moving iteratively till the Nth number is calculated. To calculate the current
number, equate it as sum of the previous two numbers. And continue to move further.

*/

import java.util.Scanner;
public class Solution {
      public static void main(String[] args) {
          Scanner s = new Scanner(System.in);
          int n = s.nextInt();
          int a = 0;
          int b = 1;
          int c;
          for(int i = 0; i < n; i++){
              c = a + b;
              a = b;
              b = c;
          }
          System.out.println(a);
      }
}
