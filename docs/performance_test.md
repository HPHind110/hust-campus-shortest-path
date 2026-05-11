# Performance Test Report

## Purpose of Benchmark
The benchmark evaluates the scalability and efficiency of the Dijkstra algorithm implementation using large, randomly generated graphs. This helps ensure that the system can handle increased data volume without significant performance degradation.

## Generated Graph Explanation
The benchmark uses a synthetic graph generation process:
1. **Connectivity**: To ensure a path always exists, the generator first creates a Hamiltonian path (0-1-2-...-n).
2. **Randomization**: Additional "extra edges" are added between random pairs of nodes.
3. **Weights**: All edges are assigned a random positive integer weight (default 1 to 100).
4. **Bidirectional**: All edges are treated as bidirectional, simulating two-way paths.

## Result Table Template
When running the benchmark with `python main.py --benchmark --nodes <N> --edges <E>`, record the results here:

| Nodes | Extra Edges | Total Edges | Visited Nodes | Runtime (ms) |
|-------|-------------|-------------|---------------|--------------|
| 1,000 | 3,000       | ~4,000      | ...           | ...          |
| 5,000 | 15,000      | ~20,000     | ...           | ...          |
| 10,000| 30,000      | ~40,000     | ...           | ...          |

## How to Interpret Runtime
- **< 10ms**: Excellent performance, suitable for real-time interactive applications.
- **10ms - 100ms**: Good performance, unnoticeable delay for most users.
- **100ms - 500ms**: Acceptable, but might be noticeable on low-end devices.
- **> 500ms**: May require further optimization or indexing if used in a high-concurrency environment.

## Methodology (HUST Map)
The basic performance test runs Dijkstra's algorithm 10 times between random pairs of nodes in the current HUST campus graph and calculates the average execution time.
