/*
 * WEEK 11 - LINKED LISTS
 * Topic: Merge Sorted Lists + LRU Cache
 *
 * ==========================================
 * PART A: MERGE TWO SORTED LINKED LISTS
 * ==========================================
 * Given two sorted linked lists, merge them into one sorted list.
 * Approach: Compare heads, attach smaller, recurse/iterate.
 * Time: O(m + n), Space: O(1) iterative / O(m+n) recursive
 *
 * ==========================================
 * PART B: LRU CACHE
 * ==========================================
 * Least Recently Used Cache: evict the least recently used item when full.
 *
 * REQUIREMENTS:
 * - get(key): return value if exists, else -1. Mark as most recently used.
 * - put(key, value): insert or update. If over capacity, evict LRU item.
 * - Both operations: O(1)
 *
 * DATA STRUCTURE: Doubly Linked List + HashMap
 * - HashMap: key → node (for O(1) lookup)
 * - Doubly Linked List: maintains access order (head = most recent, tail = least recent)
 * - On get/put: move node to head of list
 * - On eviction: remove tail node
 *
 * This is a CLASSIC system design + data structures problem!
 * Used in: CPU caches, browser history, Redis, database buffer pools.
 */

import java.util.HashMap;
import java.util.Map;

public class MergeSortedListsAndLRU {

    // Simple Node for linked list
    static class ListNode {
        int val;
        ListNode next;
        ListNode(int val) { this.val = val; }
    }

    // PART A: Merge Two Sorted Linked Lists
    static ListNode mergeSortedLists(ListNode l1, ListNode l2) {
        ListNode dummy = new ListNode(0); // sentinel head
        ListNode curr = dummy;
        while (l1 != null && l2 != null) {
            if (l1.val <= l2.val) { curr.next = l1; l1 = l1.next; }
            else { curr.next = l2; l2 = l2.next; }
            curr = curr.next;
        }
        curr.next = (l1 != null) ? l1 : l2;
        return dummy.next;
    }

    static ListNode buildList(int... vals) {
        ListNode dummy = new ListNode(0), curr = dummy;
        for (int v : vals) { curr.next = new ListNode(v); curr = curr.next; }
        return dummy.next;
    }

    static void printList(ListNode head) {
        StringBuilder sb = new StringBuilder();
        while (head != null) { sb.append(head.val); if (head.next != null) sb.append(" -> "); head = head.next; }
        System.out.println(sb);
    }

    // PART B: LRU Cache using Doubly Linked List + HashMap
    static class LRUCache {
        // Doubly linked list node
        static class DLNode {
            int key, val;
            DLNode prev, next;
            DLNode(int k, int v) { key = k; val = v; }
        }

        private final int capacity;
        private final Map<Integer, DLNode> map;
        private final DLNode head, tail; // dummy head and tail

        LRUCache(int capacity) {
            this.capacity = capacity;
            this.map = new HashMap<>();
            head = new DLNode(0, 0); // most recent side
            tail = new DLNode(0, 0); // least recent side
            head.next = tail;
            tail.prev = head;
        }

        // Remove a node from the doubly linked list
        private void remove(DLNode node) {
            node.prev.next = node.next;
            node.next.prev = node.prev;
        }

        // Insert node right after head (most recently used position)
        private void insertAfterHead(DLNode node) {
            node.next = head.next;
            node.prev = head;
            head.next.prev = node;
            head.next = node;
        }

        int get(int key) {
            if (!map.containsKey(key)) return -1;
            DLNode node = map.get(key);
            remove(node);           // move to front
            insertAfterHead(node);
            return node.val;
        }

        void put(int key, int value) {
            if (map.containsKey(key)) {
                DLNode node = map.get(key);
                node.val = value;
                remove(node);
                insertAfterHead(node);
            } else {
                if (map.size() == capacity) {
                    // Evict least recently used (node before tail)
                    DLNode lru = tail.prev;
                    remove(lru);
                    map.remove(lru.key);
                }
                DLNode newNode = new DLNode(key, value);
                insertAfterHead(newNode);
                map.put(key, newNode);
            }
        }

        void printState() {
            System.out.print("Cache (MRU→LRU): ");
            DLNode curr = head.next;
            while (curr != tail) {
                System.out.print("[" + curr.key + "=" + curr.val + "]");
                if (curr.next != tail) System.out.print(" → ");
                curr = curr.next;
            }
            System.out.println();
        }
    }

    public static void main(String[] args) {
        // --- Merge Sorted Lists ---
        System.out.println("=== Merge Sorted Lists ===");
        ListNode l1 = buildList(1, 2, 4);
        ListNode l2 = buildList(1, 3, 4);
        System.out.print("L1: "); printList(l1);
        System.out.print("L2: "); printList(l2);
        System.out.print("Merged: "); printList(mergeSortedLists(l1, l2));

        ListNode l3 = buildList(1, 3, 5, 7);
        ListNode l4 = buildList(2, 4, 6, 8, 10);
        System.out.print("L3: "); printList(l3);
        System.out.print("L4: "); printList(l4);
        System.out.print("Merged: "); printList(mergeSortedLists(l3, l4));

        // --- LRU Cache ---
        System.out.println("\n=== LRU Cache (capacity=3) ===");
        LRUCache cache = new LRUCache(3);
        cache.put(1, 1); cache.printState();
        cache.put(2, 2); cache.printState();
        cache.put(3, 3); cache.printState();
        System.out.println("get(1) = " + cache.get(1)); // returns 1, moves 1 to front
        cache.printState();
        cache.put(4, 4); // evicts 2 (least recently used)
        cache.printState();
        System.out.println("get(2) = " + cache.get(2)); // returns -1 (evicted)
        System.out.println("get(3) = " + cache.get(3)); // returns 3
        System.out.println("get(4) = " + cache.get(4)); // returns 4
        cache.printState();
    }
}
