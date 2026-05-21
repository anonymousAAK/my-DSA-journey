/*
 * Reference Java implementation for tests/cases/kruskal_mst_weight.json.
 * Kruskal MST total weight using union-find with path compression.
 */
import java.util.Arrays;
import java.util.Comparator;

public class KruskalMstWeight {
    private static int[] parent;
    private static int[] rank_;

    private static int find(int x) {
        int root = x;
        while (parent[root] != root) root = parent[root];
        while (parent[x] != root) {
            int nxt = parent[x];
            parent[x] = root;
            x = nxt;
        }
        return root;
    }

    private static boolean union(int x, int y) {
        int px = find(x), py = find(y);
        if (px == py) return false;
        if (rank_[px] < rank_[py]) { int t = px; px = py; py = t; }
        parent[py] = px;
        if (rank_[px] == rank_[py]) rank_[px]++;
        return true;
    }

    public static long kruskalMST(long V, long[][] edges) {
        int n = (int) V;
        parent = new int[n];
        rank_ = new int[n];
        for (int i = 0; i < n; ++i) parent[i] = i;
        long[][] sorted = edges.clone();
        Arrays.sort(sorted, Comparator.comparingLong(e -> e[2]));
        long total = 0;
        int used = 0;
        for (long[] e : sorted) {
            if (union((int) e[0], (int) e[1])) {
                total += e[2];
                if (++used == n - 1) break;
            }
        }
        return total;
    }
}
