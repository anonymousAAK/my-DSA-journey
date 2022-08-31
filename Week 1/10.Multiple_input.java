package fundamentals;
import java.util.Scanner;
public class ArithematicOperators {
    public static void main(String args[]) {

  
        Scanner s = new Scanner(System.in);
        int a = s.nextInt();
        String str = s.next();
        System.out.print(a);
        System.out.println(str);
    }
}

/*


Other scanner options


Some commonly used Scanner class methods are as follows:
METHOD                                            DESCRIPTION
public String next()                    It returns the next token from the Scanner.
public String nextLine()                It moves the Scanner position to the next line and returns the value as a string.
public byte nextByte()                  It scans the next token as a byte.
public short nextShort()                It scans the next token as a short value.
public int nextInt()                    It scans the next token as an int value.
public long nextLong()                  It scans the next token as a long value.
public float nextFloat()                It scans the next token as a float value.
public double nextDouble()              It scans the next token as a double value.



*/
