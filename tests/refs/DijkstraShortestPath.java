/*
 * Reference Java implementation for tests/cases/dijkstra_shortest_path.json.
 *
 * Dijkstra on an undirected non-negative weighted graph. Unreachable nodes
 * are reported as -1 to keep results JSON-friendly.
 */
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.PriorityQueue;

public class DijkstraShortestPath {
    public static List<Long> dijkstra(long V, long[][] edges, long src) {
        int n = (int) V;
        List<long[]>[] adj = new List[n];
        for (int i = 0; i < n; ++i) adj[i] = new ArrayList<>();
        for (long[] e : edges) {
            int u = (int) e[0], v = (int) e[1];
            long w = e[2];
            adj[u].add(new long[]{v, w});
            adj[v].add(new long[]{u, w});
        }
        long INF = Long.MAX_VALUE;
        long[] dist = new long[n];
        Arrays.fill(dist, INF);
        dist[(int) src] = 0;
        PriorityQueue<long[]> pq = new PriorityQueue<>((a, b) -> Long.compare(a[0], b[0]));
        pq.offer(new long[]{0, src});
        while (!pq.isEmpty()) {
            long[] cur = pq.poll();
            long d = cur[0];
            int u = (int) cur[1];
            if (d > dist[u]) continue;
            for (long[] nb : adj[u]) {
                int v = (int) nb[0];
                long nd = d + nb[1];
                if (nd < dist[v]) {
                    dist[v] = nd;
                    pq.offer(new long[]{nd, v});
                }
            }
        }
        List<Long> out = new ArrayList<>(n);
        for (long d : dist) out.add(d == INF ? -1L : d);
        return out;
    }
}
