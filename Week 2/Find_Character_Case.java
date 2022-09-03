/*

Problem Statement:- 

Write a program that takes a character as input and prints either 1, 0 or -1 according to the following rules.
1, if the character is an uppercase alphabet (A - Z)
0, if the character is a lowercase alphabet (a - z)
-1, if the character is not an alphabet

*/

// Input Format :- Single Character

import java.util.Scanner;

public class Solution {
    
    public static void main(String[] args) {
        Scanner s = new Scanner(System.in);
		    String str = s.next();
		    char ch = str.charAt(0); 
		    int i = ch;   // Since characters are stored as their ASCII value 
        int a= 1 ,b = 0, c  =-1;
	    
          if(i>= 97 && i<= 122) {
			        System.out.println(0); 
		          }
		      else if(i>=65 && i<=90) {
			        System.out.println(1);
		        }
		      else {
			        System.out.println(-1);
		    }
    }
}
