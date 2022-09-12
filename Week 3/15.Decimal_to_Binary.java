/*
Decimal to Binary

Given a decimal number (integer N), convert it into binary and print.
The binary number should be in the form of an integer.

Input format :
Integer N


Output format :
Corresponding Binary number (long)
  
  
A decimal number can be converted into a binary number by picking up the number and then
taking its remainder, after dividing it by 2, then start adding up the remainder by multiplying it
by its place value to convert the binary representation into an integer.
For example in case of 12, start picking up the remainder when 12 is divided by 2 and then
adding it by multiplying by its place value.
12 = 12%2 = 0*1 = 0
12/2 = 6%2 = 0*10 = 0
6/2 = 3%2 = 1*100 = 100
3/2 = 1%2 = 1*1000 = 1000
1/2 = 0. We will terminate the algorithm, when number becomes 0.
So, decimal number = 1000+100+0+0 = 1100
Step by step implementation:
1. Take the number as input from the user.
2. Now, initialize binary number by 0, and place value by 1.
3. Run a while loop until the number is greater than 0.
4. In each iteration of this loop, find the remainder when divided by 2, multiply it by its
place value and then add it to the binary number.
5. After this, in each iteration, multiply the place value by 10 and divide the number by 2.



Pseudo Code for this problem:
Input = number
binary_number=0, pv=1
While number is greater than 0:
 rem = number % 2
binary_number += rem* pv
pv *= 10;
number = number / 2
print(binary_number)

*/



import java.util.Scanner;
  public class Main {
      public static void main(String[] args) {
          Scanner s = new Scanner(System.in);
          int n = s.nextInt();
          long binary = 0, pow = 1;
          while(n > 0) {
             int lastBit = n % 2;
             binary += lastBit * pow;
              pow *= 10;
              n = n / 2;
          }
          System.out.println(binary);
      }
}
