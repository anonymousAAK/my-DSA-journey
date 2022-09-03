//Some Codes for practice:

byte b = 50;
b = b * 50; 

//This will convert b to int since bytes store in the range of [-128,127].


public class  Solution{
    public static void main(String [] args)  {
        double a = 6 / 4;
        int b  = 6 / 4;
        double c = a + b;
        System.out.println(c);
      
      /*
When 6 / 4 is performed, both the operands of / are integer. Hence answer will be an int i.e. 1.
When we store it in a (which is double), value of a will be 1.0 and value of b will be 1. Thus a + b will be 2.0.

*/
    }
}

public class  Solution{
    public static void main(String [] args)  {
        double a = 55.5;
        int b = 55;
        a = a % 10;
        b = b % 10;
        System.out.println(a + " "  + b);
      /* 
      % operator gives remainder. So a % 10 will give us 5.5 and b % 10 will give us 5. Hence output is : 5.5 5
        */
      
      }
 }

 public class  Solution {
    public static void main(String [] args)  {
        int var1 = 5;
        int var2 = 6;
        System.out.print(var1 > var2);
     /*
     > is a relational operator. So it will give the result as true or false only. var1 is not greater than var2, hence result is false. */
    }
}
