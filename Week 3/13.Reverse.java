/*
Reverse of a number 

 

Write a program to generate the reverse of a given number N.  

Print the corresponding reverse number. 

Note: If a number has trailing zeros, then its reverse will not include them. For e.g., reverse of 10400 will be 401 instead of 00401. 

 

Input format: 

Integer N 
 

Output format: 

Corresponding reverse number 


How to approach? 

 1. Take the number N as input from the user.  

2. Initialize the reverse number from 0, and a variable temp equal to N.  

3. Run a while loop until temp becomes 0 and in each iteration pick up the last digit of the number by taking modulo 10 and make it as the first digit of reverse number by multiplying the already existing reverse number by 10 and then adding the last digit obtained to it and pass temp as temp/10 to the next iteration.  

4. Print the reverse number.  


Pseudo Code for this problem:  

Input=N temp=N, rev_num=0  

While temp is greater than 0:  

Last_digit=temp modulo 10  

temp=temp/10  

rev_num=rev_num*10+last_digit  

print(rev_num) 

 */

import java.util.Scanner;  

public class Main {  

    public static void main(String[] args) { 

        Scanner s = new Scanner(System.in); 

        int n = s.nextInt();  

        int temp = n, revNum = 0;  

        while(temp > 0) {  

            int lastDigit = temp % 10;  

            temp = temp / 10;  

            revNum = revNum * 10 + lastDigit; 

          }  

 

          System.out.println(revNum); 

      }  

} 
