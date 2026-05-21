/*
 * Reference Java implementation for tests/cases/two_sum.json.
 * Returns ascending indices summing to target, or [-1, -1] if none.
 */
import java.util.HashMap;
import java.util.Map;

public class TwoSum {
    public static long[] twoSum(long[] nums, long target) {
        Map<Long, Integer> seen = new HashMap<>();
        for (int i = 0; i < nums.length; ++i) {
            long complement = target - nums[i];
            Integer j = seen.get(complement);
            if (j != null) return new long[]{j, i};
            seen.put(nums[i], i);
        }
        return new long[]{-1, -1};
    }
}
