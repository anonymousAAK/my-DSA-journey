// Week 27: Computational Geometry
// Convex Hull O(n log n), Line Intersection O(1), Closest Pair O(n log n)

import java.util.*;

public class geometry {
    static long cross(int[] o, int[] a, int[] b) {
        return (long)(a[0]-o[0])*(b[1]-o[1]) - (long)(a[1]-o[1])*(b[0]-o[0]);
    }

    // === Convex Hull (Andrew's Monotone Chain) ===
    static List<int[]> convexHull(int[][] points) {
        int n = points.length;
        if (n < 2) return Arrays.asList(points);
        Arrays.sort(points, (a, b) -> a[0] != b[0] ? a[0]-b[0] : a[1]-b[1]);
        int[] hull = new int[2*n];
        int k = 0;
        for (int i = 0; i < n; i++) {
            while (k >= 2 && cross(points[hull[k-2]], points[hull[k-1]], points[i]) <= 0) k--;
            hull[k++] = i;
        }
        int lower = k + 1;
        for (int i = n-2; i >= 0; i--) {
            while (k >= lower && cross(points[hull[k-2]], points[hull[k-1]], points[i]) <= 0) k--;
            hull[k++] = i;
        }
        List<int[]> result = new ArrayList<>();
        for (int i = 0; i < k-1; i++) result.add(points[hull[i]]);
        return result;
    }

    // === Closest Pair of Points ===
    static double closestPair(int[][] points) {
        Arrays.sort(points, (a, b) -> a[0]-b[0]);
        return solve(points, 0, points.length-1);
    }

    static double dist(int[] a, int[] b) {
        return Math.sqrt(Math.pow(a[0]-b[0],2) + Math.pow(a[1]-b[1],2));
    }

    static double solve(int[][] pts, int l, int r) {
        if (r - l < 3) {
            double best = Double.MAX_VALUE;
            for (int i = l; i <= r; i++)
                for (int j = i+1; j <= r; j++)
                    best = Math.min(best, dist(pts[i], pts[j]));
            return best;
        }
        int mid = (l+r)/2;
        int midX = pts[mid][0];
        double d = Math.min(solve(pts, l, mid), solve(pts, mid+1, r));
        List<int[]> strip = new ArrayList<>();
        for (int i = l; i <= r; i++)
            if (Math.abs(pts[i][0]-midX) < d) strip.add(pts[i]);
        strip.sort((a,b) -> a[1]-b[1]);
        for (int i = 0; i < strip.size(); i++)
            for (int j = i+1; j < strip.size() && strip.get(j)[1]-strip.get(i)[1] < d; j++)
                d = Math.min(d, dist(strip.get(i), strip.get(j)));
        return d;
    }

    public static void main(String[] args) {
        int[][] pts = {{0,0},{1,1},{2,2},{3,1},{0,3},{2,4}};
        List<int[]> hull = convexHull(pts);
        System.out.print("Convex Hull: ");
        for (int[] p : hull) System.out.print(Arrays.toString(p) + " ");
        System.out.println();

        int[][] pts2 = {{2,3},{12,30},{40,50},{5,1},{12,10},{3,4}};
        System.out.printf("Closest pair: %.4f%n", closestPair(pts2));
    }
}
