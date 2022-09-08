/*
Increment Decrement operator

Explanation


Pre-increment and pre-decrement operators’ increments or decrements the value of the object and returns a reference to the result.

Post-increment and post-decrement creates a copy of the object, increments or decrements the value of the object and returns the copy from before the
increment or decrement.
  
  
Post-increment(a++):

This increases value by 1, but uses old value of a in any statement.

  
Pre-increment(++a):

This increases value by 1, and uses increased value of a in any statement.
  
  
Post-decrement(a--):

This decreases value by 1, but uses old value of a in any statement.

  
Pre-decrement(++a):


This decreases value by 1, and uses decreased value of a in any statement.
  
*/
public static void main(String[] args) {
      int I=1, J=1, K=1, L=1;
      cout<<I++<<' '<<J-- <<' '<<++K<<' '<< --L<<endl;
      cout<<I<<' '<<J<<' '<<K<<' '<<L<<endl;
        }
/*
Output:
1 1 2 0
2 0 2 0
*/
