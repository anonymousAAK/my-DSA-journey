/*
 * WEEK 1 - JAVA FUNDAMENTALS
 * Topic: Hello World - First Java Program
 * File: 2.hello_world.java
 *
 * CONCEPT:
 * The classic "Hello World" program introduces the basic structure of every
 * Java application. Every Java program must have at least one class and a
 * main() method which serves as the entry point for execution.
 *
 * KEY POINTS:
 * - Every Java file must contain a class definition
 * - The main() method is the entry point: public static void main(String args[])
 * - System.out.println() prints text to the console followed by a newline
 * - Java is case-sensitive: 'System' is not the same as 'system'
 * - Every statement ends with a semicolon (;)
 * - Code blocks are enclosed in curly braces {}
 *
 * SYNTAX:
 * System.out.println("text"); // prints text with newline
 */

//After creating a class .
// Here's the first code
package fundamentals;
public class HelloWorld {
    public static void main(String args[]) {
      System.out.println("Hello World");
    }
}

/* Consider the following line of code:
public static void main(String[] args)
1. This is the line at which the program will begin executing. This statement
is similar to start block in flowcharts. All Java programs begin execution
by calling main()
2. We will understand what public, static, void mean in subsequent
lectures. For now we should assume that we have to write main as it is.
3. The curly braces {} indicate start and end of mai                       */
