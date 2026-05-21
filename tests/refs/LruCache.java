/*
 * Reference Java implementation for tests/cases/lru_cache.json.
 *
 * Driver consumes a list of ops [["put", k, v], ["get", k], ...] over a
 * cache of given capacity and returns the ordered list of get results.
 */
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public class LruCache {
    private static class LRU {
        private final int capacity;
        private final LinkedHashMap<Long, Long> map;
        LRU(int capacity) {
            this.capacity = capacity;
            this.map = new LinkedHashMap<>(16, 0.75f, true);
        }
        long get(long key) {
            Long v = map.get(key);
            return v == null ? -1L : v;
        }
        void put(long key, long value) {
            map.put(key, value);
            if (map.size() > capacity) {
                map.remove(map.entrySet().iterator().next().getKey());
            }
        }
    }

    public static List<Long> lruDriver(long capacity, List<List<Object>> ops) {
        LRU cache = new LRU((int) capacity);
        List<Long> out = new ArrayList<>();
        for (List<Object> op : ops) {
            String name = (String) op.get(0);
            if (name.equals("put")) {
                cache.put(((Number) op.get(1)).longValue(),
                          ((Number) op.get(2)).longValue());
            } else if (name.equals("get")) {
                out.add(cache.get(((Number) op.get(1)).longValue()));
            } else {
                throw new IllegalArgumentException("unknown op: " + name);
            }
        }
        return out;
    }
}
