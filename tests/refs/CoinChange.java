/*
 * Reference Java implementation for tests/cases/coin_change.json.
 * Minimum coins to make `amount`, or -1 if impossible (LC 322).
 */
import java.util.Arrays;

public class CoinChange {
    public static long coinChange(long[] coins, long amount) {
        int amt = (int) amount;
        int INF = Integer.MAX_VALUE;
        int[] dp = new int[amt + 1];
        Arrays.fill(dp, INF);
        dp[0] = 0;
        for (int a = 1; a <= amt; ++a) {
            for (long c : coins) {
                if (c <= a && dp[a - (int) c] != INF && dp[a - (int) c] + 1 < dp[a]) {
                    dp[a] = dp[a - (int) c] + 1;
                }
            }
        }
        return dp[amt] == INF ? -1 : dp[amt];
    }
}
