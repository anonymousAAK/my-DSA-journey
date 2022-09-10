/*
Terms of AP 

Write a program to print first x terms of the series 3N + 2 which are not multiples of 4. 

 

Input format: 

Integer x 
 

Output format: 

Terms of series (separated by space) 

 

How to approach?  

1. Take the number x as input from the user.  

2. Initialize the count of numbers from 1 and N from 1.  

3. Run a loop while count is less than or equal to x.  

4. Calculate the number to printed as 3*N+2  

5. If number is not divisible by 4 print it and increment the count.  

 

Pseudo Code for this problem:  

Input=N  

count=1, N=1  

While count is less than or equal to x:  

num=3*N+2  

If num is not divisible by 4:  

print(num)  

Increment the count by 1  

Increment N by 1 

 
*/
import java.util.Scanner;  

public class Main {  

    public static void main(String[] args) {  

          Scanner s = new Scanner(System.in);  

          int n = s.nextInt();  

          int count = 1, current = 1; 

          while(count <= n) { 

              int num = 3 * current + 2; 

              if(num % 4 != 0) {  

                    System.out.print(num + " ");  

                    count++;  

                  }  

               current++;  

          } 

        } 

 } 

 
