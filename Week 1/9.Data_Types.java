package fundamentals;
import java.util.Scanner;
public class ArithematicOperators {
    public static void main(String args[]) {
        Scanner s = new Scanner(System.in);
        String str;
        str = s.next();
        System.out.print(str);
    }
}

/*

Based on the data type of a variable, the operating system allocates memory and
decides what can be stored in the reserved memory. Therefore, by assigning
different data types to variables, we can store integers, decimals, or characters in
these variables.



DATA TYPE        DEFAULT VALUE         DEFAULT SIZE
   char       '\0' (nullcharacter)      2 bytes
   byte              0                  1 byte
   short             0                  2 bytes
    int              0                  4 bytes
    long             0L                 8 bytes
   Float             0.0f               4 bytes
   Double            0.0d               8 bytes
   Boolean           false              Not specified
