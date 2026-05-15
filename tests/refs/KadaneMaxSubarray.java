/*
 * Reference Java implementation for tests/cases/kadane_max_subarray.json.
 *
 * The shared harness (tests/harness/harness.java) loads the cases.json
 * fixture, reflects on this class to find a method called
 * maxSubarraySum(long[]) -> long, invokes it per case, and prints PASS/FAIL.
 *
 * Compile alongside the harness:
 *     javac -d /tmp/java-out tests/harness/harness.java tests/refs/KadaneMaxSubarray.java
 *     java -cp /tmp/java-out Harness tests/cases/kadane_max_subarray.json
 */
public class KadaneMaxSubarray {
    public static long maxSubarraySum(long[] arr) {
        if (arr.length == 0) return 0;
        long best = arr[0], current = arr[0];
        for (int i = 1; i < arr.length; ++i) {
            current = Math.max(arr[i], current + arr[i]);
            best = Math.max(best, current);
        }
        return best;
    }
}
