/*
 * Reference Java implementation for tests/cases/topological_sort.json.
 *
 * Kahn's algorithm with a min-heap tiebreaker for deterministic order.
 * Returns null on cycle.
 */
import java.util.ArrayList;
import java.util.List;
import java.util.PriorityQueue;

public class TopologicalSort {
    public static List<Long> topologicalSort(long V, long[][] edges) {
        int n = (int) V;
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < n; ++i) adj.add(new ArrayList<>());
        int[] indeg = new int[n];
        for (long[] e : edges) {
            int u = (int) e[0], v = (int) e[1];
            adj.get(u).add(v);
            indeg[v]++;
        }
        PriorityQueue<Integer> heap = new PriorityQueue<>();
        for (int i = 0; i < n; ++i) if (indeg[i] == 0) heap.offer(i);
        List<Long> result = new ArrayList<>();
        while (!heap.isEmpty()) {
            int u = heap.poll();
            result.add((long) u);
            for (int v : adj.get(u)) {
                if (--indeg[v] == 0) heap.offer(v);
            }
        }
        return result.size() == n ? result : null;
    }
}
