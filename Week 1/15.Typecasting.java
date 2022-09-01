/*
Typecasting


1. Widening or Automatic type conversion: 

In Java, automatic type conversion takes place when the two types are compatible and size of destination type is larger than source type.
  
  
2. Narrowing or Explicit type conversion:
When we are assigning a larger type value to a variable of smaller type, then we need to perform explicit type casting.
Example code:

*/
public static void main(String[] args) {
    int i = 100;
    long l1 = i; //automatic type casting
    double d = 100.04;
    long l2 = (long)d; //explicit type casting
    System.out.println(i);
    System.out.println(l1);
    System.out.println(d);
    System.out.println(l2);
}

/*
Output:
100
100
100.04
100

*/
