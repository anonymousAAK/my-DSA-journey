 package fundamentals;
import java.util.Scanner;
public class ArithematicOperators {
    public static void main(String args[]) {
      int a,b;
      Scanner s=new Scanner(System.in);
      a=s.nextInt();
      b=s.nextInt();
      int c=a+b;
      
      String str=s.nextLine();
      char ch=str.charAt(0);
      System.out.println(ch);
      s.nextDouble();
      s.nextLong();
    }
}

/*

The Java Scanner class breaks the input into tokens using a delimiter that is
whitespace by default. It provides many ways to read and parse various
primitive values.
In order to use scanner you have to write this import statement at the top –
import java.util.Scanner;


Sample Input:
10 5

Here, s.nextInt() scans and returns the next token as int. A token is part of entered
line that is separated from other tokens by space, tab or newline. So when input
line is: “10 5” then s.nextInt() returns the first token i.e. “10” as int and s.nextInt()
again returns the next token i.e. “5” as int  
  */
