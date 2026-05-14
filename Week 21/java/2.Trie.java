/*
 * WEEK 21 - ADVANCED TREES
 * Topic: Trie (Prefix Tree)
 *
 * TRIE: A tree where each node represents a character.
 * A path from root to a marked node spells a word.
 *
 * STRUCTURE:
 * - Each node has up to 26 children (for lowercase letters)
 * - 'isEnd' flag marks end of a word
 *
 * OPERATIONS:
 * - insert(word):       O(m) where m = word length
 * - search(word):       O(m)
 * - startsWith(prefix): O(m) — prefix search
 * - delete(word):       O(m)
 *
 * Space: O(N * m * 26) worst case where N = number of words
 *
 * APPLICATIONS:
 * - Autocomplete / search suggestions
 * - Spell checkers
 * - IP routing (longest prefix match)
 * - XOR maximum / minimum (using binary trie)
 *
 * BONUS: Maximum XOR of two numbers using binary Trie
 * XOR maximum: O(n log(max_val))
 */

import java.util.*;

public class Trie {

    static class TrieNode {
        TrieNode[] children = new TrieNode[26];
        boolean isEnd = false;
        int wordCount = 0; // number of words passing through this node
    }

    static class TrieImpl {
        TrieNode root = new TrieNode();

        void insert(String word) {
            TrieNode curr = root;
            for (char c : word.toCharArray()) {
                int idx = c - 'a';
                if (curr.children[idx] == null) curr.children[idx] = new TrieNode();
                curr = curr.children[idx];
                curr.wordCount++;
            }
            curr.isEnd = true;
        }

        boolean search(String word) {
            TrieNode curr = root;
            for (char c : word.toCharArray()) {
                int idx = c - 'a';
                if (curr.children[idx] == null) return false;
                curr = curr.children[idx];
            }
            return curr.isEnd;
        }

        boolean startsWith(String prefix) {
            TrieNode curr = root;
            for (char c : prefix.toCharArray()) {
                int idx = c - 'a';
                if (curr.children[idx] == null) return false;
                curr = curr.children[idx];
            }
            return true;
        }

        // Count words with given prefix
        int countWithPrefix(String prefix) {
            TrieNode curr = root;
            for (char c : prefix.toCharArray()) {
                int idx = c - 'a';
                if (curr.children[idx] == null) return 0;
                curr = curr.children[idx];
            }
            return curr.wordCount; // this counts how many words share this path
        }

        // Get all words with given prefix (autocomplete)
        List<String> autocomplete(String prefix) {
            List<String> result = new ArrayList<>();
            TrieNode curr = root;
            for (char c : prefix.toCharArray()) {
                int idx = c - 'a';
                if (curr.children[idx] == null) return result;
                curr = curr.children[idx];
            }
            dfsCollect(curr, new StringBuilder(prefix), result);
            return result;
        }
        void dfsCollect(TrieNode node, StringBuilder current, List<String> result) {
            if (node.isEnd) result.add(current.toString());
            for (int i = 0; i < 26; i++) {
                if (node.children[i] != null) {
                    current.append((char)('a' + i));
                    dfsCollect(node.children[i], current, result);
                    current.deleteCharAt(current.length() - 1);
                }
            }
        }

        // Delete a word (mark isEnd = false; clean up dead branches)
        boolean delete(String word) {
            return deleteHelper(root, word, 0);
        }
        boolean deleteHelper(TrieNode node, String word, int idx) {
            if (idx == word.length()) {
                if (!node.isEnd) return false;
                node.isEnd = false;
                return true; // node is now deletable if no children
            }
            int i = word.charAt(idx) - 'a';
            if (node.children[i] == null) return false;
            boolean deleted = deleteHelper(node.children[i], word, idx + 1);
            if (deleted) {
                node.children[i].wordCount--;
                // Clean up node if no longer useful
                if (!isLeaf(node.children[i]) && node.children[i].wordCount == 0) {
                    node.children[i] = null;
                }
            }
            return deleted;
        }
        boolean isLeaf(TrieNode node) {
            for (TrieNode child : node.children) if (child != null) return false;
            return true;
        }
    }

    // BONUS: Maximum XOR of two elements in array using binary Trie
    // For each bit from MSB to LSB, try to pick the opposite bit (to maximize XOR)
    static int maxXOR(int[] nums) {
        int max = Arrays.stream(nums).max().getAsInt();
        int bits = 32 - Integer.numberOfLeadingZeros(max);
        // Build binary trie
        int[][] trie = new int[32 * nums.length][2];
        int size = 1;
        for (int x : nums) {
            int node = 0;
            for (int b = bits - 1; b >= 0; b--) {
                int bit = (x >> b) & 1;
                if (trie[node][bit] == 0) trie[node][bit] = size++;
                node = trie[node][bit];
            }
        }
        int result = 0;
        for (int x : nums) {
            int node = 0, cur = 0;
            for (int b = bits - 1; b >= 0; b--) {
                int bit = (x >> b) & 1;
                int want = 1 - bit; // try opposite bit
                if (trie[node][want] != 0) { cur |= (1 << b); node = trie[node][want]; }
                else node = trie[node][bit];
            }
            result = Math.max(result, cur);
        }
        return result;
    }

    public static void main(String[] args) {
        TrieImpl trie = new TrieImpl();
        String[] words = {"apple", "app", "application", "apply", "apt", "banana", "band"};
        for (String w : words) trie.insert(w);

        System.out.println("=== Trie ===");
        System.out.println("search(\"apple\"):       " + trie.search("apple"));       // true
        System.out.println("search(\"app\"):         " + trie.search("app"));         // true
        System.out.println("search(\"ap\"):          " + trie.search("ap"));          // false
        System.out.println("startsWith(\"app\"):     " + trie.startsWith("app"));     // true
        System.out.println("startsWith(\"xyz\"):     " + trie.startsWith("xyz"));     // false

        System.out.println("\nAutocomplete 'app': " + trie.autocomplete("app"));
        System.out.println("Autocomplete 'ban': " + trie.autocomplete("ban"));
        System.out.println("Autocomplete 'z':   " + trie.autocomplete("z"));

        trie.delete("app");
        System.out.println("\nAfter deleting 'app':");
        System.out.println("search(\"app\"):   " + trie.search("app"));    // false
        System.out.println("search(\"apple\"): " + trie.search("apple"));  // still true

        // Max XOR
        System.out.println("\n=== Maximum XOR ===");
        System.out.println("maxXOR([3,10,5,25,2,8]) = " + maxXOR(new int[]{3,10,5,25,2,8})); // 28
        System.out.println("maxXOR([0,1,2]) = " + maxXOR(new int[]{0, 1, 2})); // 3
    }
}
