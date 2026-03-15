/*
 * WEEK 2 - CONTROL FLOW
 * Topic: Fahrenheit to Celsius Conversion Table
 * File: 6.Fahrenheit_to_Celsius_Table.java
 *
 * CONCEPT:
 * This file demonstrates using a while loop to generate a temperature
 * conversion table. It converts a range of Fahrenheit values to Celsius
 * using the formula: C = (F - 32) * 5 / 9.
 *
 * KEY POINTS:
 * - The conversion formula is Celsius = (Fahrenheit - 32) * 5 / 9
 * - A while loop iterates from Start to End value with a given step size
 * - Integer arithmetic is used, so Celsius values are truncated (not rounded)
 * - The loop increments the current Fahrenheit value by the step size W each iteration
 *
 * APPROACH:
 * 1. Read three integers: Start (S), End (E), and Step (W)
 * 2. Loop while S <= E
 * 3. In each iteration, compute Celsius using the formula
 * 4. Print the Fahrenheit and Celsius pair
 * 5. Increment S by W
 *
 * Time Complexity: O((E - S) / W) - depends on range and step size
 * Space Complexity: O(1)
 */

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
public class F_C_Table {


	public static void main(String[] args) {
		
	
		int S , E , W;        // S=Start, E=End, W=Step size (in Fahrenheit)
		int a = 0;            // Variable to store the Celsius result
		Scanner p = new Scanner(System.in);
		S = p.nextInt();      // Read start Fahrenheit value
		E = p.nextInt();      // Read end Fahrenheit value
		W = p.nextInt();      // Read step size

		// Loop from Start to End, incrementing by step size W
		while(E>=S) {
			a = ((S-32)*5)/9 ;         // Convert current Fahrenheit to Celsius (integer arithmetic)
			System.out.println(S +" " + a);  // Print Fahrenheit and Celsius pair
			S=S+W;                     // Move to next Fahrenheit value
		}
		
		
	}

}
