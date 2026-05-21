/*
 * Java correctness-check harness for tests/cases/*.json.
 *
 * Each topic in TOPIC_DISPATCH is wired to a class in tests/refs/<Topic>.java
 * via reflection. For every case we coerce the parsed JSON `input` array into
 * the method's parameter types, invoke, then normalise the result for
 * comparison against `expected` (deep-equal via list/array normalisation).
 *
 * The mini JSON parser supports objects, arrays, strings, numbers, booleans,
 * and null — enough for every fixture under tests/cases/.
 *
 * Compile & run a single fixture:
 *     javac -d /tmp/jbuild tests/harness/Harness.java tests/refs/*.java
 *     java -cp /tmp/jbuild Harness tests/cases/kadane_max_subarray.json
 *
 * Run every fixture under tests/cases/:
 *     java -cp /tmp/jbuild Harness --all
 */

import java.io.File;
import java.lang.reflect.Method;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.*;

public class Harness {

    // topic -> [class, method] driver pair
    static final Map<String, String[]> TOPIC_DISPATCH = new LinkedHashMap<>();
    static {
        TOPIC_DISPATCH.put("kadane_max_subarray",            new String[]{"KadaneMaxSubarray", "maxSubarraySum"});
        TOPIC_DISPATCH.put("linear_search",                  new String[]{"LinearSearch", "linearSearch"});
        TOPIC_DISPATCH.put("dutch_national_flag",            new String[]{"DutchNationalFlag", "dutchFlag"});
        TOPIC_DISPATCH.put("palindrome_check",               new String[]{"PalindromeCheck", "isPalindrome"});
        TOPIC_DISPATCH.put("valid_anagram",                  new String[]{"ValidAnagram", "isAnagram"});
        TOPIC_DISPATCH.put("kmp_search",                     new String[]{"KmpSearch", "kmpSearch"});
        TOPIC_DISPATCH.put("binary_search",                  new String[]{"BinarySearch", "binarySearch"});
        TOPIC_DISPATCH.put("binary_search_on_answer",        new String[]{"BinarySearchOnAnswer", "minEatingSpeed"});
        TOPIC_DISPATCH.put("merge_sort",                     new String[]{"MergeSort", "mergeSort"});
        TOPIC_DISPATCH.put("quick_sort",                     new String[]{"QuickSort", "quickSort"});
        TOPIC_DISPATCH.put("spiral_traversal",               new String[]{"SpiralTraversal", "spiralOrder"});
        TOPIC_DISPATCH.put("reverse_linked_list",            new String[]{"ReverseLinkedList", "reverseList"});
        TOPIC_DISPATCH.put("lru_cache",                      new String[]{"LruCache", "lruDriver"});
        TOPIC_DISPATCH.put("balanced_parens",                new String[]{"BalancedParens", "isBalanced"});
        TOPIC_DISPATCH.put("sliding_window_max",             new String[]{"SlidingWindowMax", "slidingWindowMax"});
        TOPIC_DISPATCH.put("bst_validate",                   new String[]{"BstValidate", "isValidBST"});
        TOPIC_DISPATCH.put("kth_largest",                    new String[]{"KthLargest", "kthLargest"});
        TOPIC_DISPATCH.put("two_sum",                        new String[]{"TwoSum", "twoSum"});
        TOPIC_DISPATCH.put("topological_sort",               new String[]{"TopologicalSort", "topologicalSort"});
        TOPIC_DISPATCH.put("coin_change",                    new String[]{"CoinChange", "coinChange"});
        TOPIC_DISPATCH.put("n_queens_count",                 new String[]{"NQueensCount", "nQueensCount"});
        TOPIC_DISPATCH.put("dijkstra_shortest_path",         new String[]{"DijkstraShortestPath", "dijkstra"});
        TOPIC_DISPATCH.put("kruskal_mst_weight",             new String[]{"KruskalMstWeight", "kruskalMST"});
        TOPIC_DISPATCH.put("rabin_karp_search",              new String[]{"RabinKarpSearch", "rabinKarpSearch"});
        TOPIC_DISPATCH.put("sliding_window_longest_substr",  new String[]{"SlidingWindowLongestSubstr", "longestUniqueSubstring"});
    }

    public static void main(String[] args) throws Exception {
        if (args.length < 1) {
            System.err.println("Usage: java Harness <fixture.json>|--all");
            System.exit(2);
        }
        if (args[0].equals("--all")) {
            runAll();
        } else {
            int[] pf = runFixture(Paths.get(args[0]));
            System.out.println();
            System.out.println(Paths.get(args[0]).getFileName() + ": " + pf[0] + " passed, " + pf[1] + " failed");
            System.exit(pf[1] == 0 ? 0 : 1);
        }
    }

    static void runAll() throws Exception {
        // Discover fixtures next to this harness file.
        Path casesDir = findCasesDir();
        File[] files = casesDir.toFile().listFiles((d, name) -> name.endsWith(".json"));
        if (files == null || files.length == 0) {
            System.err.println("No fixtures found in " + casesDir);
            System.exit(1);
        }
        Arrays.sort(files);
        int totalP = 0, totalF = 0;
        List<String[]> summary = new ArrayList<>();
        for (File f : files) {
            int[] pf = runFixture(f.toPath());
            totalP += pf[0];
            totalF += pf[1];
            String stem = f.getName().replaceFirst("\\.json$", "");
            summary.add(new String[]{stem, String.valueOf(pf[0]), String.valueOf(pf[1])});
        }
        System.out.println();
        System.out.println("============================================================");
        System.out.println("Per-topic summary:");
        for (String[] row : summary) {
            int p = Integer.parseInt(row[1]);
            int fl = Integer.parseInt(row[2]);
            String flag = (fl == 0 && p > 0) ? "OK" : (fl > 0 ? "FAIL" : "SKIP");
            System.out.printf("  [%-4s] %-35s %3d passed, %3d failed%n", flag, row[0], p, fl);
        }
        System.out.println("============================================================");
        System.out.println("TOTAL: " + totalP + " passed, " + totalF + " failed across " + files.length + " fixtures");
        System.exit(totalF == 0 ? 0 : 1);
    }

    private static Path findCasesDir() {
        // Try a few likely locations: cwd, ./tests/cases, ../cases.
        Path[] candidates = {
            Paths.get("tests/cases"),
            Paths.get("cases"),
            Paths.get("../cases"),
            Paths.get("../../tests/cases"),
        };
        for (Path c : candidates) {
            if (Files.isDirectory(c)) return c;
        }
        throw new RuntimeException("could not locate tests/cases directory");
    }

    static int[] runFixture(Path fixturePath) throws Exception {
        String text = new String(Files.readAllBytes(fixturePath));
        MiniJson js = new MiniJson(text);
        @SuppressWarnings("unchecked")
        Map<String, Object> root = (Map<String, Object>) js.parse();

        String topic = (String) root.get("topic");
        String[] cm = TOPIC_DISPATCH.get(topic);
        if (cm == null) {
            System.out.println("SKIP " + topic + " :: no Java driver");
            return new int[]{0, 0};
        }
        Class<?> klass = Class.forName(cm[0]);
        Method method = findMethod(klass, cm[1]);
        if (method == null) {
            System.out.println("FAIL " + topic + " :: no method " + cm[1] + " on " + cm[0]);
            return new int[]{0, 1};
        }

        @SuppressWarnings("unchecked")
        List<Map<String, Object>> cases = (List<Map<String, Object>>) root.get("cases");
        int passed = 0, failed = 0;
        for (Map<String, Object> c : cases) {
            if (Boolean.TRUE.equals(c.get("skip"))) continue;
            String name = (String) c.get("name");
            @SuppressWarnings("unchecked")
            List<Object> input = (List<Object>) c.get("input");
            Object expected = c.get("expected");

            Object[] callArgs;
            try {
                callArgs = coerceArgs(method, input);
            } catch (Exception ex) {
                System.out.println("FAIL " + topic + " :: " + name);
                System.out.println("  arg coercion error: " + ex.getMessage());
                failed++;
                continue;
            }
            Object got;
            try {
                got = method.invoke(null, callArgs);
            } catch (Throwable t) {
                System.out.println("FAIL " + topic + " :: " + name);
                System.out.println("  exception: " + (t.getCause() != null ? t.getCause() : t));
                failed++;
                continue;
            }
            Object gotN = normalise(got);
            Object expN = normalise(expected);
            if (deepEquals(gotN, expN)) {
                System.out.println("PASS " + topic + " :: " + name);
                passed++;
            } else {
                System.out.println("FAIL " + topic + " :: " + name);
                System.out.println("  expected: " + expN);
                System.out.println("  got: " + gotN);
                failed++;
            }
        }
        return new int[]{passed, failed};
    }

    private static Method findMethod(Class<?> klass, String name) {
        for (Method m : klass.getMethods()) {
            if (m.getName().equals(name)) return m;
        }
        return null;
    }

    // ---- Coerce parsed JSON values to the parameter types of the target method ----
    @SuppressWarnings("unchecked")
    private static Object[] coerceArgs(Method m, List<Object> input) {
        Class<?>[] pt = m.getParameterTypes();
        if (pt.length != input.size()) {
            throw new RuntimeException("arity mismatch: method wants " + pt.length + ", fixture has " + input.size());
        }
        Object[] out = new Object[pt.length];
        for (int i = 0; i < pt.length; ++i) {
            out[i] = coerce(input.get(i), pt[i]);
        }
        return out;
    }

    @SuppressWarnings("unchecked")
    private static Object coerce(Object val, Class<?> target) {
        if (val == null) return null;
        if (target == long.class || target == Long.class) {
            return ((Number) val).longValue();
        }
        if (target == int.class || target == Integer.class) {
            return ((Number) val).intValue();
        }
        if (target == double.class || target == Double.class) {
            return ((Number) val).doubleValue();
        }
        if (target == boolean.class || target == Boolean.class) {
            return val;
        }
        if (target == String.class) {
            return val;
        }
        if (target == long[].class) {
            List<Object> arr = (List<Object>) val;
            long[] r = new long[arr.size()];
            for (int i = 0; i < arr.size(); ++i) r[i] = ((Number) arr.get(i)).longValue();
            return r;
        }
        if (target == int[].class) {
            List<Object> arr = (List<Object>) val;
            int[] r = new int[arr.size()];
            for (int i = 0; i < arr.size(); ++i) r[i] = ((Number) arr.get(i)).intValue();
            return r;
        }
        if (target == long[][].class) {
            List<Object> rows = (List<Object>) val;
            long[][] r = new long[rows.size()][];
            for (int i = 0; i < rows.size(); ++i) {
                List<Object> row = (List<Object>) rows.get(i);
                long[] inner = new long[row.size()];
                for (int j = 0; j < row.size(); ++j) inner[j] = ((Number) row.get(j)).longValue();
                r[i] = inner;
            }
            return r;
        }
        if (target == List.class) {
            // Used by lru_cache (List<List<Object>>) and bst_validate (List<Long> possibly with nulls).
            List<Object> arr = (List<Object>) val;
            // Heuristic: if elements are themselves lists, keep them as List<Object>.
            // Otherwise normalise numbers to Long, preserving nulls.
            List<Object> out = new ArrayList<>(arr.size());
            for (Object e : arr) {
                if (e == null) out.add(null);
                else if (e instanceof Number) out.add(((Number) e).longValue());
                else if (e instanceof List) out.add(e);
                else out.add(e);
            }
            return out;
        }
        throw new RuntimeException("unsupported parameter type: " + target);
    }

    // ---- Normalise results for deep comparison: arrays -> List<Object>, numbers -> Long ----
    @SuppressWarnings("unchecked")
    private static Object normalise(Object v) {
        if (v == null) return null;
        if (v instanceof Number) return ((Number) v).longValue();
        if (v instanceof Boolean || v instanceof String) return v;
        if (v instanceof long[]) {
            long[] a = (long[]) v;
            List<Object> out = new ArrayList<>(a.length);
            for (long x : a) out.add(x);
            return out;
        }
        if (v instanceof int[]) {
            int[] a = (int[]) v;
            List<Object> out = new ArrayList<>(a.length);
            for (int x : a) out.add((long) x);
            return out;
        }
        if (v instanceof Object[]) {
            Object[] a = (Object[]) v;
            List<Object> out = new ArrayList<>(a.length);
            for (Object x : a) out.add(normalise(x));
            return out;
        }
        if (v instanceof List) {
            List<Object> arr = (List<Object>) v;
            List<Object> out = new ArrayList<>(arr.size());
            for (Object x : arr) out.add(normalise(x));
            return out;
        }
        if (v instanceof Map) {
            Map<Object, Object> m = (Map<Object, Object>) v;
            LinkedHashMap<Object, Object> out = new LinkedHashMap<>();
            for (Map.Entry<Object, Object> e : m.entrySet()) out.put(e.getKey(), normalise(e.getValue()));
            return out;
        }
        return v;
    }

    private static boolean deepEquals(Object a, Object b) {
        if (a == null || b == null) return a == b;
        return Objects.equals(a, b);
    }

    // ----- Minimal JSON parser (objects/arrays/strings/numbers/bools/null) -----
    static class MiniJson {
        private final String s;
        private int i;

        MiniJson(String s) { this.s = s; this.i = 0; }

        Object parse() { skipWs(); return readValue(); }

        private Object readValue() {
            skipWs();
            char c = s.charAt(i);
            if (c == '{') return readObject();
            if (c == '[') return readArray();
            if (c == '"') return readString();
            if (c == 't' || c == 'f') return readBool();
            if (c == 'n') { i += 4; return null; }
            return readNumber();
        }

        private Map<String, Object> readObject() {
            Map<String, Object> m = new LinkedHashMap<>();
            i++; skipWs();
            if (s.charAt(i) == '}') { i++; return m; }
            while (true) {
                skipWs();
                String k = readString();
                skipWs();
                i++; // ':'
                Object v = readValue();
                m.put(k, v);
                skipWs();
                if (s.charAt(i) == ',') { i++; continue; }
                if (s.charAt(i) == '}') { i++; return m; }
                throw new RuntimeException("expected , or } at " + i);
            }
        }

        private List<Object> readArray() {
            List<Object> a = new ArrayList<>();
            i++; skipWs();
            if (s.charAt(i) == ']') { i++; return a; }
            while (true) {
                a.add(readValue());
                skipWs();
                if (s.charAt(i) == ',') { i++; continue; }
                if (s.charAt(i) == ']') { i++; return a; }
                throw new RuntimeException("expected , or ] at " + i);
            }
        }

        private String readString() {
            StringBuilder sb = new StringBuilder();
            i++; // '"'
            while (s.charAt(i) != '"') {
                char c = s.charAt(i);
                if (c == '\\') { sb.append(s.charAt(i + 1)); i += 2; }
                else { sb.append(c); i++; }
            }
            i++; return sb.toString();
        }

        private Number readNumber() {
            int start = i;
            if (s.charAt(i) == '-' || s.charAt(i) == '+') i++;
            while (i < s.length() && (Character.isDigit(s.charAt(i)) || s.charAt(i) == '.'
                    || s.charAt(i) == 'e' || s.charAt(i) == 'E' || s.charAt(i) == '-' || s.charAt(i) == '+')) {
                i++;
            }
            String tok = s.substring(start, i);
            if (tok.contains(".") || tok.contains("e") || tok.contains("E")) {
                return Double.parseDouble(tok);
            }
            return Long.parseLong(tok);
        }

        private Boolean readBool() {
            if (s.charAt(i) == 't') { i += 4; return Boolean.TRUE; }
            i += 5; return Boolean.FALSE;
        }

        private void skipWs() {
            while (i < s.length() && Character.isWhitespace(s.charAt(i))) i++;
        }
    }
}
