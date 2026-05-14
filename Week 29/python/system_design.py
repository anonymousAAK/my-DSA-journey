# Week 29: System Design for Engineers
# Consistent Hashing, LRU Cache, Token Bucket, Trie Autocomplete, Merkle Tree

import hashlib, time, heapq
from bisect import bisect_right

# === Consistent Hashing ===
class ConsistentHash:
    def __init__(self, nodes=None, replicas=150):
        self.replicas = replicas
        self.ring = {}
        self.sorted_keys = []
        for node in (nodes or []):
            self.add_node(node)

    def _hash(self, key):
        return int(hashlib.md5(key.encode()).hexdigest(), 16)

    def add_node(self, node):
        for i in range(self.replicas):
            h = self._hash(f"{node}#vn{i}")
            self.ring[h] = node
            self.sorted_keys.append(h)
        self.sorted_keys.sort()

    def get_node(self, key):
        if not self.ring: return None
        h = self._hash(key)
        idx = bisect_right(self.sorted_keys, h) % len(self.sorted_keys)
        return self.ring[self.sorted_keys[idx]]

# === LRU Cache ===
class LRUNode:
    def __init__(self, key=0, val=0):
        self.key, self.val, self.prev, self.next = key, val, None, None

class LRUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.cache = {}
        self.head, self.tail = LRUNode(), LRUNode()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        node.prev.next, node.next.prev = node.next, node.prev

    def _add_front(self, node):
        node.next, node.prev = self.head.next, self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        if key not in self.cache: return -1
        node = self.cache[key]
        self._remove(node); self._add_front(node)
        return node.val

    def put(self, key, value):
        if key in self.cache: self._remove(self.cache[key])
        node = LRUNode(key, value)
        self._add_front(node); self.cache[key] = node
        if len(self.cache) > self.cap:
            lru = self.tail.prev
            self._remove(lru); del self.cache[lru.key]

# === Token Bucket Rate Limiter ===
class TokenBucket:
    def __init__(self, capacity, refill_rate):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate
        self.last_refill = time.time()

    def allow_request(self):
        now = time.time()
        self.tokens = min(self.capacity, self.tokens + (now - self.last_refill) * self.refill_rate)
        self.last_refill = now
        if self.tokens >= 1:
            self.tokens -= 1; return True
        return False

# === Trie Autocomplete ===
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.freq = 0

class AutoComplete:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, freq=1):
        node = self.root
        for ch in word:
            if ch not in node.children: node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True; node.freq += freq

    def suggest(self, prefix, k=5):
        node = self.root
        for ch in prefix:
            if ch not in node.children: return []
            node = node.children[ch]
        results = []
        def dfs(n, path):
            if n.is_end: results.append((n.freq, path))
            for ch, child in n.children.items(): dfs(child, path + ch)
        dfs(node, prefix)
        return [w for _, w in heapq.nlargest(k, results)]

# === Merkle Tree ===
class MerkleTree:
    def __init__(self, blocks):
        self.leaves = [hashlib.sha256(b.encode()).hexdigest() for b in blocks]
        while len(self.leaves) & (len(self.leaves) - 1):
            self.leaves.append(hashlib.sha256(b"").hexdigest())
        n = len(self.leaves)
        self.tree = [None] * (2 * n)
        for i in range(n): self.tree[n + i] = self.leaves[i]
        for i in range(n - 1, 0, -1):
            self.tree[i] = hashlib.sha256((self.tree[2*i] + self.tree[2*i+1]).encode()).hexdigest()

    @property
    def root(self): return self.tree[1]

if __name__ == "__main__":
    ch = ConsistentHash(["A", "B", "C"])
    print(f"Node for 'key1': {ch.get_node('key1')}")
    cache = LRUCache(2)
    cache.put(1, 1); cache.put(2, 2)
    print(f"LRU get(1): {cache.get(1)}")
    ac = AutoComplete()
    for w in ["cat","car","card","care"]: ac.insert(w)
    print(f"Autocomplete 'car': {ac.suggest('car')}")
    mt = MerkleTree(["a","b","c","d"])
    print(f"Merkle root: {mt.root[:16]}...")
