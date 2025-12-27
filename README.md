# Weighted Interval Shortest Path

This repository contains an optimized Python implementation of the shortest path algorithm for weighted interval graphs. The implementation follows an efficient approach using interval ordering, disjoint-set union (Union-Find), and stack-based processing to achieve near-linear performance.

The project is based on the idea of computing shortest paths over intervals sorted by their right endpoints, avoiding explicit graph construction.

---

## Problem Description

Each interval is defined as:

(a, b, w)


Where:
- `a` is the start point
- `b` is the end point
- `w` is the weight of the interval

An edge exists from interval *i* to interval *j* if the two intervals overlap. The goal is to compute the shortest path from a source interval to every other interval.

---

## Algorithm Overview

The algorithm works as follows:

1. Sort intervals by their right endpoints.
2. For each interval, compute its successor using binary search.
3. Process intervals in sorted order while maintaining:
   - Active intervals
   - Special inactive intervals
   - Disjoint-set union (DSU) for merging interval components
4. Use representative intervals to propagate shortest path labels efficiently.

This avoids building the full interval graph and significantly improves performance.

---

## Features

- Optimized union-find with path compression
- Efficient successor computation using binary search
- Works with large inputs
- Supports both interactive input and redirected file input
- Outputs results in the original input order

---

## Input Format

n
a1 b1 w1
a2 b2 w2
...
an bn wn


Where `n` is the number of intervals.

---

## Output Format

For each interval, the program outputs:

index shortest_path_value

Indices are 1-based and correspond to the original input order.

---

## Example

### Input
3
0 4 3
2 6 1
5 9 4


### Output
1 3
2 4
3 8



---

## How to Run

### Using a file
python DS.py < input.txt


### Interactive mode
python DS.py

yaml
Copy code

Enter the input and finish with:
- `Ctrl + Z` then Enter (Windows)
- `Ctrl + D` (Linux / macOS)

---

## Notes

- The first interval in sorted order by right endpoint is treated as the source.
- The implementation prioritizes clarity and correctness while maintaining high performance.
- Designed for academic and algorithmic experimentation.

---

## License

This project is provided for educational and research purposes.





