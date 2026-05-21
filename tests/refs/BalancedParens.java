/*
 * Reference Java implementation for tests/cases/balanced_parens.json.
 * Classic stack-based bracket validator for (), [], {}.
 */
import java.util.ArrayDeque;
import java.util.Deque;

public class BalancedParens {
    public static boolean isBalanced(String s) {
        Deque<Character> stack = new ArrayDeque<>();
        for (int i = 0; i < s.length(); ++i) {
            char c = s.charAt(i);
            if (c == '(' || c == '[' || c == '{') {
                stack.push(c);
            } else if (c == ')' || c == ']' || c == '}') {
                char want = c == ')' ? '(' : (c == ']' ? '[' : '{');
                if (stack.isEmpty() || stack.pop() != want) return false;
            }
        }
        return stack.isEmpty();
    }
}
