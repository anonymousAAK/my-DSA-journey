/*
Check Number sequence

You are given S, a sequence of n integers i.e. S = s1, s2, ..., sn. Compute if it is possible to split S into two parts : s1, s2, ..., si and si+1, si+2, ….., sn (0 <= i <= n) in such a way that the first part is strictly decreasing while the second is strictly increasing one.
Note : We say that x is strictly larger than y when x > y.
So, a strictly increasing sequence can be 1 4 8. However, 1 4 4 is NOT a strictly increasing sequence.


That is, in the sequence if numbers are decreasing, they can start increasing at one point. And once the sequence of numbers starts increasing, they cannot decrease at any point further.
Sequence made up of only increasing numbers or only decreasing numbers is a valid sequence. So, in both the cases, print true.


You just need to print true/false. No need to split the sequence.


Input format :
Line 1 : Integer 'n'
Line 2 and Onwards : 'n' integers on 'n' lines(single integer on each line)


Output Format :
"true" or "false" (without quotes)


Problem Description: You are given a sequence of numbers and you have to check whether it
is possible to split the sequence into 2 parts such that 1st part is strictly decreasing while the
other part is strictly increasing.


That is, in the sequence if the numbers are decreasing, they can start to increase at one point.
And once the numbers start increasing, they cannot decrease at any point further.
How to approach?


In this problem, we have these valid sequences:
So, we need to traverse the whole array once, so for this we need to maintain a count variable
and run a loop until this count becomes equal to the number n. In each iteration of this loop, take
the current number as input and check whether it is equal to the previous number. If this is true,
then we should directly print false, as the sequence is neither strictly increasing or decreasing in
that case.


Now, if the current number is less than the previous one, then we will check whether the
previous sequence was decreasing or not with the help of a flag isDec. If this flag is true that
means the previous sequence was decreasing, then we will move to the next number, but if this
flag is false that means we found a decrease after a previously increasing sequence, so we should
directly print false.


But if the current number is greater than the previous number we will say that if the previous
sequence was decreasing i.e. if isDec is true, now we have found an increase in the sequence so
we will make isDec as false. And, if the previous sequence was increasing we will do nothing
and continue.


Step by step implementation:
1. Take the number of integers N as input from the user, and then take the 1st number as
input from the user, in variable previous.
2. Initialize the number count by 2, and an isDec by true.
3. Run a loop until count becomes equal to N, increment it in each iteration.
4. In each iteration, take the current number as input from the user. Check whether the
current number is equal to the previous number, if yes then we print false directly.
5. If the current number is less than the previous number, then we will check if isDec is
false, then we will directly print false. If isDec is true, then we will continue.
6. But if the current number is greater than the previous number, then we will check if isDec
is true. If isDec is true then make it as false, as we have found an increase in the sequence
here. If isDec is false, then we will continue.
7. Make previous number=current number.


Pseudo Code for this problem:
Input=N, prev
Count=2, isDec=true
while count is less than or equal to N:
 Input=curr
 If(curr=prev):
 print(false)
 Return
 If(curr<prev):
 If isDec=false:
 print(false)
 Return
 else:
 If isDec = true:
 isDec = false
 prev = current
 Increment count by 1.
print (true)


*/



import java.util.Scanner;
public class Main {
     public static void main(String[] args) {
          Scanner s = new Scanner(System.in);
          int n = s.nextInt();
          int prev = s.nextInt();
          int count = 2, current;
          boolean isDec = true;
          while(count <= n) {
              current = s.nextInt();
              count++;
              if(current == prev) {
                  System.out.println("false");
                    return;
                  }
              if(current < prev) {
                    if(isDec == false) {
                        System.out.println("false");
                        return;
             }
              }
                     else {
                        if(isDec == true) {
                            isDec = false;
                }
           }
                 prev = current;
       }
          System.out.println("true");
}
}
