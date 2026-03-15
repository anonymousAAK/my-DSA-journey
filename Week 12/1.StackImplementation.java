/*
 * WEEK 12 - STACKS
 * Topic: Stack Implementation + Classic Problems
 *
 * STACK: LIFO (Last In, First Out) data structure.
 * Think of a stack of plates — you always add/remove from the top.
 *
 * CORE OPERATIONS (all O(1)):
 * - push(x): add element to top
 * - pop():   remove and return top element
 * - peek()/top(): view top element without removing
 * - isEmpty(): check if stack is empty
 *
 * IMPLEMENTATIONS: Array-based (fast) or LinkedList-based (dynamic).
 *
 * CLASSIC APPLICATIONS:
 * 1. Balanced parentheses: (){}[] matching
 * 2. Next Greater Element
 * 3. Min Stack: O(1) min retrieval
 * 4. Expression evaluation
 *
 * In Java: use Deque<Integer> (ArrayDeque) instead of legacy Stack class.
 * ArrayDeque is faster and more complete.
 */

import java.util.ArrayDeque;
import java.util.Deque;
import java.util.Stack;

public class StackImplementation {

    // Array-based stack implementation
    static class ArrayStack {
        private int[] data;
        private int top;

        ArrayStack(int capacity) {
            data = new int[capacity];
            top = -1;
        }

        void push(int x) {
            if (top == data.length - 1) throw new RuntimeException("Stack overflow");
            data[++top] = x;
        }

        int pop() {
            if (isEmpty()) throw new RuntimeException("Stack underflow");
            return data[top--];
        }

        int peek() {
            if (isEmpty()) throw new RuntimeException("Stack is empty");
            return data[top];
        }

        boolean isEmpty() { return top == -1; }
        int size() { return top + 1; }
    }

    // Min Stack: supports push, pop, peek, AND getMin() in O(1)
    // Trick: maintain a second stack that tracks minimums.
    static class MinStack {
        Deque<Integer> stack = new ArrayDeque<>();
        Deque<Integer> minStack = new ArrayDeque<>(); // top = current minimum

        void push(int x) {
            stack.push(x);
            int min = minStack.isEmpty() ? x : Math.min(x, minStack.peek());
            minStack.push(min);
        }

        void pop() {
            stack.pop();
            minStack.pop();
        }

        int peek() { return stack.peek(); }
        int getMin() { return minStack.peek(); }
    }

    // --- CLASSIC PROBLEMS ---

    // 1. Balanced Parentheses
    static boolean isBalanced(String s) {
        Deque<Character> stack = new ArrayDeque<>();
        for (char c : s.toCharArray()) {
            if (c == '(' || c == '{' || c == '[') {
                stack.push(c);
            } else {
                if (stack.isEmpty()) return false;
                char top = stack.pop();
                if (c == ')' && top != '(') return false;
                if (c == '}' && top != '{') return false;
                if (c == ']' && top != '[') return false;
            }
        }
        return stack.isEmpty();
    }

    // 2. Next Greater Element for each element in array
    // For each element, find the next element that is greater than it.
    // Use monotonic stack (decreasing): O(n) time
    static int[] nextGreaterElement(int[] arr) {
        int n = arr.length;
        int[] result = new int[n];
        java.util.Arrays.fill(result, -1); // default: no greater element
        Deque<Integer> stack = new ArrayDeque<>(); // stores INDICES

        for (int i = 0; i < n; i++) {
            // While stack is not empty AND current element > element at stack's top index
            while (!stack.isEmpty() && arr[i] > arr[stack.peek()]) {
                int idx = stack.pop();
                result[idx] = arr[i]; // arr[i] is the next greater for arr[idx]
            }
            stack.push(i);
        }
        return result;
    }

    // 3. Evaluate Postfix expression (e.g., "3 4 + 2 *" = 14)
    static int evalPostfix(String expr) {
        Deque<Integer> stack = new ArrayDeque<>();
        for (String token : expr.split("\\s+")) {
            switch (token) {
                case "+": stack.push(stack.pop() + (int)stack.pop()); break; // order doesn't matter for +
                case "*": stack.push(stack.pop() * (int)stack.pop()); break;
                case "-": { int b = stack.pop(), a = stack.pop(); stack.push(a - b); break; }
                case "/": { int b = stack.pop(), a = stack.pop(); stack.push(a / b); break; }
                default:  stack.push(Integer.parseInt(token));
            }
        }
        return stack.pop();
    }

    public static void main(String[] args) {
        // Array stack
        ArrayStack as = new ArrayStack(10);
        as.push(1); as.push(2); as.push(3);
        System.out.println("peek: " + as.peek()); // 3
        System.out.println("pop: " + as.pop());   // 3
        System.out.println("pop: " + as.pop());   // 2
        System.out.println("size: " + as.size()); // 1

        // Min stack
        System.out.println("\n=== Min Stack ===");
        MinStack ms = new MinStack();
        ms.push(5); ms.push(3); ms.push(7); ms.push(2);
        System.out.println("peek: " + ms.peek() + ", min: " + ms.getMin()); // 2, 2
        ms.pop();
        System.out.println("After pop — peek: " + ms.peek() + ", min: " + ms.getMin()); // 7, 3

        // Balanced parentheses
        System.out.println("\n=== Balanced Parentheses ===");
        String[] tests = {"([]{})", "(])", "((()))", "{[}]", ""};
        for (String t : tests) System.out.println("\"" + t + "\": " + isBalanced(t));

        // Next Greater Element
        System.out.println("\n=== Next Greater Element ===");
        int[] arr = {4, 5, 2, 10, 8};
        System.out.println("Array: " + java.util.Arrays.toString(arr));
        System.out.println("NGE:   " + java.util.Arrays.toString(nextGreaterElement(arr)));
        // [5, 10, 10, -1, -1]

        // Postfix evaluation
        System.out.println("\n=== Postfix Evaluation ===");
        System.out.println("\"3 4 +\" = " + evalPostfix("3 4 +"));           // 7
        System.out.println("\"3 4 + 2 *\" = " + evalPostfix("3 4 + 2 *"));  // 14
        System.out.println("\"15 7 1 1 + - / 3 * 2 1 1 + + -\" = " +
            evalPostfix("15 7 1 1 + - / 3 * 2 1 1 + + -")); // 5
    }
}
