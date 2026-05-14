"""
WEEK 5 - PYTHON FUNCTIONS & RECURSION
Topic: Tower of Hanoi
File: 5.tower_of_hanoi.py

PROBLEM:
Three rods (Source, Auxiliary, Destination). N disks on Source, largest at
bottom. Move all disks to Destination, ONE at a time, never placing a
larger disk on a smaller one. Find a sequence of moves.

CONCEPT:
Recursive insight:
  Move N from Source to Dest using Aux:
    1. Move (N-1) disks from Source -> Aux (using Dest as helper)
    2. Move disk N from Source -> Dest
    3. Move (N-1) disks from Aux -> Dest (using Source as helper)

Base case: N == 0 -> nothing to do.

KEY POINTS:
 - Minimum number of moves = 2^N - 1.
 - Time complexity O(2^N) -- the answer itself is exponential.
 - Space O(N) for the recursion stack.

DRY RUN (N=2):
 hanoi(2, A, B, C):
   hanoi(1, A, C, B):
     move disk 1: A -> B
   move disk 2: A -> C
   hanoi(1, B, A, C):
     move disk 1: B -> C
 Total: 3 moves (2^2 - 1)

COMPLEXITY: O(2^N) time, O(N) space.
"""


move_count = 0


def hanoi(n: int, source: str, auxiliary: str, destination: str) -> None:
    global move_count
    if n == 0:
        return
    hanoi(n - 1, source, destination, auxiliary)
    move_count += 1
    print(f"Move disk {n}: {source} -> {destination}")
    hanoi(n - 1, auxiliary, source, destination)


def main() -> None:
    global move_count
    print("=== Tower of Hanoi: 3 Disks ===")
    move_count = 0
    hanoi(3, 'A', 'B', 'C')
    print(f"Total moves for 3 disks: {move_count}  (expected {2**3 - 1})")

    print("\n=== Tower of Hanoi: 4 Disks ===")
    move_count = 0
    hanoi(4, 'A', 'B', 'C')
    print(f"Total moves for 4 disks: {move_count}  (expected {2**4 - 1})")

    print("\n=== Move counts by disk count ===")
    print("Disks | Moves  | Formula 2^n - 1")
    print("------+--------+----------------")
    for i in range(1, 21):
        print(f"  {i:>2}  | {2**i - 1:>6} | {2**i - 1}")
    print(f"\n64 disks -> {2**64 - 1:,} moves (~585 years at 1 billion/sec)")


if __name__ == "__main__":
    main()


# NOTES:
# - The number of moves is provably MINIMAL at 2^N - 1.
# - Iterative solutions exist (using bit-twiddling tricks) but recursion is the
#   most readable formulation.
# - Tower of Hanoi is a CANONICAL example of "divide and conquer where the
#   answer itself is exponential" -- there's no polynomial algorithm.
