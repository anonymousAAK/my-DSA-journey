/*
Sum or Product


Write a program that asks the user for a number N and a choice C. 
And then give them the possibility to choose between computing the sum and computing the product of all integers in the range 1 to N (both inclusive).

  
  If C is equal to -
 1, then print the sum
 2, then print the product
 Any other number, then print '-1' (without the quotes)

  
  Input format :
Line 1 : Integer N
Line 2 : Choice C


Output Format :
 Sum or product according to user's choice
 


How to approach?
1. Take the number N and choice C from the user.
2. Now if C is equal to 1, then run a while loop from number=1 to N to calculate their sum
and print it.
3. If C is equal to 2, then run a while loop from number =1 to N to calculate their product
and print it.
4. If C is any other number then just print -1.
  
  
  
Pseudo Code for this problem:
Input=N, C
If C=1:
 sum=0, num=1
 While num is less than equal to N:
 sum=sum+num
 Increment num by 1
 print(sum)
If C=2:
 product = 1, num = 1
 While num is less than equal to N:
product *= num;
 Increment num by 1
 print(product)
Else:
 print(-1)


*/

import java.util.Scanner;
public class Main {
    public static void main(String[] args) {
        Scanner s = new Scanner(System.in);
        int n = s.nextInt();
        int choice = s.nextInt();
        if(choice == 1) {
            int sum = 0, num = 1;
            while(num <= n) {
                sum += num;
                num++;
              }
        System.out.println(sum);
        }else if(choice == 2) {
             int product = 1, num = 1;
             while(num <= n) {
                  product *= num;
                   num++;
            }
         System.out.println(product);
          } else {
         System.out.println("-1");
      }
    }
}


