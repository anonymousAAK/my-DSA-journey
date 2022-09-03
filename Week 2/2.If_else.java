/*
Java supports the usual logical conditions from mathematics:
    Less than: a < b
    Less than or equal to: a <= b
    Greater than: a > b
    Greater than or equal to: a >= b
    Equal to a == b
    Not Equal to: a != b

Java has the following conditional statements:

    Use if to specify a block of code to be executed, if a specified condition is true
    Use else to specify a block of code to be executed, if the same condition is false
    Use else if to specify a new condition to test, if the first condition is false
    Use switch to specify many alternative blocks of code to be executed
    
    
    Various Operators are discussed in Week 1 :-  " https://github.com/anonymousAAK/my-DSA-journey/blob/main/Week%201/16.Operators_in_java "
    */

public static void main(String args[])
{
    int a=10,b=15;
    if(a>b)
    {
        System.out.print("a ");
    }
    else
    {
        System.out.print("b ");
    }
    System.out.print("is greater");
}

// "is greater" is written outside if-else so it would always print
