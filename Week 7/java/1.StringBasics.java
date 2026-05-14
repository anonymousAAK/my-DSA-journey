/*
 * WEEK 7 - STRINGS
 * Topic: String Basics in Java
 *
 * KEY CONCEPTS:
 * - String in Java is IMMUTABLE — every modification creates a new object.
 * - StringBuilder is MUTABLE — efficient for repeated modifications.
 * - String pool: Java caches string literals for memory efficiency.
 *
 * IMPORTANT METHODS:
 * length(), charAt(), substring(), indexOf(), contains(), replace(),
 * toLowerCase(), toUpperCase(), trim(), split(), toCharArray()
 *
 * Time Complexity of common operations:
 * - charAt(i):      O(1)
 * - substring(l,r): O(r-l)  — creates a new string
 * - indexOf:        O(n*m) naive, O(n) with KMP
 * - concat (+):     O(n) — creates new string each time!
 * - StringBuilder append: O(1) amortized
 *
 * GOLDEN RULE: Never concatenate strings inside a loop with +.
 *              Use StringBuilder instead → O(n) vs O(n²)
 */

public class StringBasics {

    public static void main(String[] args) {
        // --- Basic Operations ---
        String s = "Hello, World!";
        System.out.println("String: " + s);
        System.out.println("Length: " + s.length());
        System.out.println("charAt(7): " + s.charAt(7));
        System.out.println("substring(7, 12): " + s.substring(7, 12));
        System.out.println("indexOf('o'): " + s.indexOf('o'));
        System.out.println("lastIndexOf('o'): " + s.lastIndexOf('o'));
        System.out.println("contains(\"World\"): " + s.contains("World"));
        System.out.println("toLowerCase: " + s.toLowerCase());
        System.out.println("toUpperCase: " + s.toUpperCase());
        System.out.println("replace('l', 'r'): " + s.replace('l', 'r'));
        System.out.println("trim: \"  hello  \".trim() = \"" + "  hello  ".trim() + "\"");

        // --- Comparison ---
        String a = "apple";
        String b = "apple";
        String c = new String("apple");
        System.out.println("\n\"apple\" == \"apple\": " + (a == b));       // true (same pool ref)
        System.out.println("\"apple\" == new String(\"apple\"): " + (a == c)); // false! different object
        System.out.println("\"apple\".equals(new String(\"apple\")): " + a.equals(c)); // true (content)
        System.out.println("compareTo: " + "apple".compareTo("banana")); // negative (a < b)

        // --- String to char array and back ---
        char[] chars = s.toCharArray();
        System.out.println("\ntoCharArray: " + chars.length + " chars");
        System.out.println("new String(chars): " + new String(chars));

        // --- Split ---
        String csv = "one,two,three,four";
        String[] parts = csv.split(",");
        System.out.println("\nSplit by ',': ");
        for (String p : parts) System.out.println("  " + p);

        // --- StringBuilder: efficient string building ---
        StringBuilder sb = new StringBuilder();
        for (int i = 1; i <= 5; i++) {
            sb.append(i);
            if (i < 5) sb.append("-");
        }
        System.out.println("\nBuilt with StringBuilder: " + sb.toString());

        // Reverse with StringBuilder
        StringBuilder sb2 = new StringBuilder("hello");
        System.out.println("Reversed: " + sb2.reverse().toString());

        // --- BAD vs GOOD string concatenation in loops ---
        // BAD:  O(n²) — creates n new strings
        // String result = "";
        // for (int i = 0; i < n; i++) result += chars[i];

        // GOOD: O(n) — amortized O(1) per append
        StringBuilder good = new StringBuilder();
        for (char ch : chars) good.append(ch);
        System.out.println("\nRebuilt string: " + good.toString());
    }
}
