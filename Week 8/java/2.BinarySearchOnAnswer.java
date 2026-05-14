/*
 * WEEK 8 - SEARCHING ALGORITHMS
 * Topic: Binary Search on the Answer
 *
 * KEY INSIGHT: Binary search isn't just for finding an element in an array.
 * It can be applied to ANY monotonic function over a range.
 *
 * PATTERN: "Find the minimum/maximum value X such that condition(X) is true/false."
 *
 * TEMPLATE:
 *   lo = minimum possible answer
 *   hi = maximum possible answer
 *   while (lo < hi) {
 *       mid = lo + (hi - lo) / 2
 *       if (condition(mid)) hi = mid       // mid might be the answer, go left
 *       else lo = mid + 1                   // mid is too small, go right
 *   }
 *   return lo // lo == hi is the answer
 *
 * PROBLEMS COVERED:
 * 1. Square root (integer) of a number
 * 2. Koko eating bananas (minimize maximum speed)
 * 3. Capacity to ship packages in D days (minimize maximum load)
 */

import java.util.Arrays;

public class BinarySearchOnAnswer {

    // PROBLEM 1: Integer Square Root
    // Find largest x such that x*x <= n
    static int sqrtInt(int n) {
        if (n < 2) return n;
        int lo = 1, hi = n / 2;
        while (lo < hi) {
            int mid = lo + (hi - lo + 1) / 2; // +1 to avoid infinite loop when hi = lo+1
            if ((long) mid * mid <= n) lo = mid;
            else hi = mid - 1;
        }
        return lo;
    }

    // PROBLEM 2: Koko Eating Bananas
    // Piles of bananas, H hours, find minimum speed k (bananas/hour) to eat all in H hours
    // Condition: canFinish(k) = sum of ceil(pile/k) for all piles <= H
    static boolean canFinish(int[] piles, int h, int speed) {
        long hours = 0;
        for (int pile : piles) {
            hours += (pile + speed - 1) / speed; // = ceil(pile / speed)
        }
        return hours <= h;
    }

    static int minEatingSpeed(int[] piles, int h) {
        int lo = 1;
        int hi = Arrays.stream(piles).max().getAsInt(); // max pile size is upper bound
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (canFinish(piles, h, mid)) hi = mid; // can finish, try slower
            else lo = mid + 1;                       // too slow, speed up
        }
        return lo;
    }

    // PROBLEM 3: Ship Packages in D Days
    // Find minimum capacity W such that all packages can be shipped in D days
    // Greedily assign packages to current day; start new day when adding next package exceeds W
    static boolean canShip(int[] weights, int days, int capacity) {
        int currentLoad = 0, daysNeeded = 1;
        for (int w : weights) {
            if (w > capacity) return false; // single package exceeds capacity
            if (currentLoad + w > capacity) {
                daysNeeded++;
                currentLoad = 0;
            }
            currentLoad += w;
        }
        return daysNeeded <= days;
    }

    static int minShipCapacity(int[] weights, int days) {
        int lo = Arrays.stream(weights).max().getAsInt(); // min = heaviest package
        int hi = Arrays.stream(weights).sum();            // max = ship all in one day
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (canShip(weights, days, mid)) hi = mid;
            else lo = mid + 1;
        }
        return lo;
    }

    public static void main(String[] args) {
        // Square root
        System.out.println("=== Integer Square Root ===");
        int[] nums = {0, 1, 4, 8, 9, 16, 17, 100};
        for (int n : nums) {
            System.out.printf("sqrt(%3d) = %d%n", n, sqrtInt(n));
        }

        // Koko
        System.out.println("\n=== Koko Eating Bananas ===");
        int[] piles = {3, 6, 7, 11};
        System.out.println("Piles: " + Arrays.toString(piles));
        System.out.println("Min speed for H=8: " + minEatingSpeed(piles, 8)); // 4

        int[] piles2 = {30, 11, 23, 4, 20};
        System.out.println("Piles: " + Arrays.toString(piles2));
        System.out.println("Min speed for H=5: " + minEatingSpeed(piles2, 5));  // 30
        System.out.println("Min speed for H=6: " + minEatingSpeed(piles2, 6));  // 23

        // Ship packages
        System.out.println("\n=== Ship Packages ===");
        int[] weights = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
        System.out.println("Weights: " + Arrays.toString(weights));
        System.out.println("Min capacity for D=5 days: " + minShipCapacity(weights, 5));  // 15
        System.out.println("Min capacity for D=10 days: " + minShipCapacity(weights, 10)); // 10
    }
}
