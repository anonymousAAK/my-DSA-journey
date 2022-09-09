/*
All Prime Numbers


Given an integer N, print all the prime numbers that lie in the range 2 to N (both inclusive).
  
Print the prime numbers in different lines.
  
  
Input Format :
Integer N


Output Format :
Prime numbers in different lines



How to approach?
1. Take the number as input from the user.
2. Now, initialize a loop from i=2 to n, and for each i check whether it is prime or not,
initially take isPrime (to denote whether a number is prime or not) as true which means
we are assuming that the number is prime, initially.
3. Now, for each i we create another loop in this to check if that number is prime or not. If it
is not prime then make isPrime as false and continue to next i otherwise if isPrime
remains true, then print it.



Pseudo Code for this problem:
Input = N
For i=2 to i less than equal to N:
 isPrime=true
 For j=2 to i less than i:
 If i%j=0:
 isPrime=false
 Break (to move out of inner loop)
 If (isPrime= true):
 Print (i) in new line


*/



import java.util.Scanner;
public class Solution{
      public static void main(String[] args) {
            Scanner s = new Scanner(System.in);
            int n = s.nextInt();
            for(int i = 2; i <= n; i++) {
                   boolean isPrime = true;
                    for(int j = 2; j < i; j++) {
                            if(i % j == 0) {
                                 isPrime = false;
                                 break;
                                  }
                            }
                    if(isPrime) {
                            System.out.println(i);
              }
          }
      }
}
