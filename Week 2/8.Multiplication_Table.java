/*
Multiplication Table

Write a program to print multiplication table of n


Input Format :
A single integer, n



Output Format :
First 10 multiples of n each printed in new line

*/

import java.util.Scanner;
public class Main {
	
	public static void main(String[] args) {
        int n;
		Scanner s = new Scanner(System.in);
		n = s.nextInt();
		int i = 1;
		while(i<=10) {
			int j = i*n;
			System.out.println(j);
			i = i+1;
		}

	}
}
