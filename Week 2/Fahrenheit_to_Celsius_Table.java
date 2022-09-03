/*
Given three values - Start Fahrenheit Value (S), End Fahrenheit value (E) and Step Size (W), 
you need to convert all Fahrenheit values from Start to End at the gap of W, into their corresponding Celsius values and print the table.


Input Format :
3 integers - S, E and W respectively 

*/
/*
How to approach?
1. Take the start value, end value and the step as input from the user.
2. Take a current value equal to start value.
3. Then, run a loop until current value becomes equal to end value with a step increment of
W
4. In each iteration convert into corresponding celsius value. And print both fahrenheit and
celsius value.
*/

import java.util.Scanner;
public class Solution {


	public static void main(String[] args) {
		
	
		int S , E , W;
		int a = 0;
		Scanner p = new Scanner(System.in);
		S = p.nextInt();
		E = p.nextInt();
		W = p.nextInt();
		
		while(E>=S) {
			a = ((S-32)*5)/9 ;
			System.out.println(S +" " + a);
			S=S+W;
		}
		
		
	}

}
