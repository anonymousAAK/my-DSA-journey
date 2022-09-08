Bitwise Operators
Bitwise operators are used to perform operations at bit level. Following is the
summary of various bitwise operations:
    Operator    Name          Example       Result        Description
      a & b     and             4 & 6          4            1 if both bits are 1.
      a | b      or             4 | 6          6            1 if either bit is 1.
      a ^ b     xor             4 ^ 6          2            1 if both bits are different.
        ~a      not               ~4          -5            Inverts the bits. (Unary bitwise compliment)
      n << p    left shift     3 << 2         12            Shifts the bits of n left p positions. Zero bits are shifted into the low-order positions.
      n >> p    right shift    5 >> 2          1            Shifts the bits of n right p positions. If n is a 2's complement signed number, 
                                                            the sign bit is shifted into the high-order positions.
      n >>> p   right shift   -4 >>> 28       15            Shifts the bits of n right p positions. Zeros are shifted into the high-order positions.


Example Code:


public static void main(String args[]) {
          int a = 19; // 19 = 10011
          int b = 28; // 28 = 11100
          int c = 0;
          c = a & b; // 16 = 10000
          System.out.println("a & b = " + c );
          c = a | b; // 31 = 11111
          System.out.println("a | b = " + c );
          c = a ^ b; // 15 = 01111
          System.out.println("a ^ b = " + c );
          c = ~a; // -20 = 01100
          System.out.println("~a = " + c );
          c = a << 2; // 76 = 1001100
          System.out.println("a << 2 = " + c );
          c = a >> 2; // 4 = 00100
          System.out.println("a >> 2 = " + c );
          c = a >>> 2; // 4 = 00100
          System.out.println("a >>> 2 = " + c );
    }


Output
a & b = 16
a | b = 31
a ^ b = 15
~a = -20
a << 2 = 76
a >> 2 = 4
a >>> 2 = 4
