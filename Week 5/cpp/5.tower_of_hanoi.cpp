/*
 * WEEK 5 - C++ FUNCTIONS & RECURSION
 * Topic: Tower of Hanoi
 * File: 5.tower_of_hanoi.cpp
 *
 * RECURSIVE INSIGHT:
 *  hanoi(n, src, aux, dst):
 *    1. hanoi(n-1, src, dst, aux)
 *    2. move disk n: src -> dst
 *    3. hanoi(n-1, aux, src, dst)
 *
 * COMPLEXITY: O(2^n) -- minimum number of moves is 2^n - 1.
 */

#include <iostream>
#include <cmath>

int move_count = 0;

void hanoi(int n, char source, char auxiliary, char destination) {
    if (n == 0) return;
    hanoi(n - 1, source, destination, auxiliary);
    ++move_count;
    std::cout << "Move disk " << n << ": " << source << " -> " << destination << '\n';
    hanoi(n - 1, auxiliary, source, destination);
}

int main() {
    std::cout << "=== Tower of Hanoi: 3 Disks ===\n";
    move_count = 0;
    hanoi(3, 'A', 'B', 'C');
    std::cout << "Total moves: " << move_count << " (expected " << ((1<<3) - 1) << ")\n";

    std::cout << "\n=== Tower of Hanoi: 4 Disks ===\n";
    move_count = 0;
    hanoi(4, 'A', 'B', 'C');
    std::cout << "Total moves: " << move_count << " (expected " << ((1<<4) - 1) << ")\n";

    std::cout << "\nDisks | Moves\n------+------\n";
    for (int i = 1; i <= 20; ++i) {
        long long expected = (1LL << i) - 1;
        std::cout << "  " << i << "  | " << expected << '\n';
    }
    std::cout << "\n64 disks -> " << ((1ULL << 63) | ((1ULL << 63) - 1)) << " moves\n";
    return 0;
}

/*
 * NOTES:
 *  - The recursion tree grows exponentially -- printing all 2^N - 1 moves
 *    becomes impractical for N >= 30.
 *  - Iterative variants exist (using bit tricks) but recursion remains the
 *    clearest formulation.
 */
