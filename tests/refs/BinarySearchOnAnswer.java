/*
 * Reference Java implementation for tests/cases/binary_search_on_answer.json.
 * Koko eating bananas: binary search on the minimum speed.
 */
public class BinarySearchOnAnswer {
    private static boolean canFinish(long[] piles, long h, long speed) {
        long hours = 0;
        for (long pile : piles) {
            hours += (pile + speed - 1) / speed;
        }
        return hours <= h;
    }

    public static long minEatingSpeed(long[] piles, long h) {
        long lo = 1, hi = 0;
        for (long p : piles) if (p > hi) hi = p;
        while (lo < hi) {
            long mid = lo + (hi - lo) / 2;
            if (canFinish(piles, h, mid)) hi = mid;
            else lo = mid + 1;
        }
        return lo;
    }
}
