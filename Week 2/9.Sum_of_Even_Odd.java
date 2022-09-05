/*
Sum of even & odd


Write a program to input an integer N and print the sum of all its even digits and sum of all its odd digits separately.
  
Digits mean numbers, not the places! That is, if the given integer is "13245", even digits are 2 & 4 and odd digits are 1, 3 & 5.
  
  
Input format :
 Integer N
 
 
Output format :
Sum_of_Even_Digits Sum_of_Odd_Digits (Print first even sum and then odd sum separated by space)
*/
/*
How to approach?
1. Take the number as input from the user.
2. Initialize both even sum and odd sum from 0.
3. Now, start picking up the last digit by taking modulo 10 while number is greater than 0
and check whether the last digit is odd or even.
4. If the last digit is odd then, add it to then odd sum otherwise add it to the even sum and
pass the number by dividing it to 10 to the next iteration.
5. Print even sum and odd sum.

*/

import java.util.Scanner;
public class Main {
    public static void main(String[] args) {
        Scanner s = new Scanner(System.in);
        int num = s.nextInt();
        int evenSum = 0, oddSum = 0;
        while(num > 0) {
            int last = num % 10;
            if(last % 2 == 0) {
                evenSum += last;
          } else {
                oddSum += last;
          }
            num = num / 10;
          }
        System.out.println(evenSum + " " + oddSum);
    }
}
