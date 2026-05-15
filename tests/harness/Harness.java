/*
 * Java correctness-check harness — proof-of-concept (kadane pilot).
 *
 * Loads a cases.json fixture, reflects on the corresponding ref class, and
 * runs each case. To minimise scope we DO NOT bring in a third-party JSON
 * library; instead we use a tiny home-rolled parser sufficient for the
 * kadane schema (input = [[ints...]], expected = int).
 *
 * Topic -> class mapping lives in TOPIC_CLASSES below. Currently only
 * kadane_max_subarray is wired end-to-end; extending to additional topics
 * is mechanical: add a class in tests/refs/<TopicName>.java exposing the
 * right static method, wire it here, and (if the input shape differs) add
 * a parser branch.
 *
 * Compile:
 *     javac -d /tmp/java-out tests/harness/harness.java tests/refs/KadaneMaxSubarray.java
 * Run:
 *     java -cp /tmp/java-out Harness tests/cases/kadane_max_subarray.json
 */

import java.lang.reflect.Method;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.*;

public class Harness {

    // --- topic -> (class name, method name) ---
    static final Map<String, String[]> TOPIC_CLASSES = new HashMap<>();
    static {
        TOPIC_CLASSES.put("kadane_max_subarray",
                new String[]{"KadaneMaxSubarray", "maxSubarraySum"});
        // TODO: add more topics here, e.g.:
        // TOPIC_CLASSES.put("binary_search", new String[]{"BinarySearch", "binarySearch"});
    }

    public static void main(String[] args) throws Exception {
        if (args.length < 1) {
            System.err.println("Usage: java Harness <fixture.json>");
            System.exit(2);
        }
        String text = new String(Files.readAllBytes(Path.of(args[0])));
        MiniJson js = new MiniJson(text);
        Map<String, Object> root = (Map<String, Object>) js.parse();

        String topic = (String) root.get("topic");
        String[] classMethod = TOPIC_CLASSES.get(topic);
        if (classMethod == null) {
            System.out.println("SKIP " + topic + " :: no Java driver yet (see tests/README.md)");
            return;
        }

        Class<?> klass = Class.forName(classMethod[0]);
        // For kadane: one-argument method taking long[]
        Method m = klass.getMethod(classMethod[1], long[].class);

        List<Map<String, Object>> cases = (List<Map<String, Object>>) root.get("cases");
        int passed = 0, failed = 0;
        for (Map<String, Object> c : cases) {
            if (Boolean.TRUE.equals(c.get("skip"))) continue;
            String name = (String) c.get("name");
            List<Object> input = (List<Object>) c.get("input");
            List<Object> arr = (List<Object>) input.get(0);
            long[] primArr = new long[arr.size()];
            for (int i = 0; i < arr.size(); ++i) primArr[i] = ((Number) arr.get(i)).longValue();

            long expected = ((Number) c.get("expected")).longValue();
            long got = (Long) m.invoke(null, (Object) primArr);
            if (got == expected) {
                System.out.println("PASS " + topic + " :: " + name);
                ++passed;
            } else {
                System.out.println("FAIL " + topic + " :: " + name);
                System.out.println("  expected: " + expected);
                System.out.println("  got: " + got);
                ++failed;
            }
        }
        System.out.println("TOTAL: " + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }

    // ----- Minimal JSON parser (no external dependency) -----
    //
    // Supports: objects, arrays, strings, numbers, booleans, null. No escapes
    // beyond \" and \\. Good enough for the test fixtures.

    static class MiniJson {
        private final String s;
        private int i;

        MiniJson(String s) { this.s = s; this.i = 0; }

        Object parse() {
            skipWs();
            Object v = readValue();
            return v;
        }

        private Object readValue() {
            skipWs();
            char c = s.charAt(i);
            if (c == '{') return readObject();
            if (c == '[') return readArray();
            if (c == '"') return readString();
            if (c == 't' || c == 'f') return readBool();
            if (c == 'n') { i += 4; return null; } // null
            return readNumber();
        }

        private Map<String, Object> readObject() {
            Map<String, Object> m = new LinkedHashMap<>();
            i++; // '{'
            skipWs();
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
            i++; // '['
            skipWs();
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
            i++; // closing '"'
            return sb.toString();
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
