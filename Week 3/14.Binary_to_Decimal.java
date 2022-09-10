/*
Binary to decimal 

  

  

Given a binary number as an integer N, convert it into decimal and print. 

  

  

Input format : 

An integer N in the Binary Format 

  

  

Output format : 

Corresponding Decimal number (as integer) 

  

How to approach? 

A binary number can be converted into a decimal number by picking up the last digit and then 

multiplying each digit with 2 raised to the power of its place value and then adding them in a 

continuous manner. 

For example, in the case of 1100, start picking up the last digit multiplied by 2’s respective 

powers and add them up.So, 

1100=0*2^(0)+0*2^(1)+1*2^(2)+1*2^(3)=0+0+4+8=12 

1. Take the number as input from the user. 

2. Now, initialize the decimal number (this will be our running sum) by 0 and take another 

variable pow for powers of 2 and initialize it with 1. 

3. Now, run a loop until the number is greater than 0. 

4. In each iteration, take the last digit by taking modulo 10 of the number. Find the decimal 

number by maintaining a running sum of multiplication of last digit and pow. 

5. In each iteration multiply pow by 2 and divide num by 10 

  

Pseudo Code for this problem: 

Input = number 

decimal=0, pow=1 

While number is greater than 0: 

last = number % 10 

decimal += last * pow 

pow *= 2 

number = number / 10 

print(decimal) 

  

  

  */

import java.util.Scanner; 

public class Main { 

    public static void main(String[] args) { 

          Scanner s = new Scanner(System.in); 

          int num = s.nextInt(); 

          int decimal = 0, pow = 1; 

          while(num > 0) { 

              int last = num % 10; 

              decimal += last * pow; 

              pow *= 2; 

              num = num / 10; 

            } 

          System.out.println(decimal); 

        } 

} 

 

 
