# HUST Campus Shortest Path

A Python application for finding the shortest path between buildings and landmarks on the HUST campus using Dijkstra's algorithm.

## Features
- Manual implementation of Dijkstra's algorithm using `heapq`.
- Adjacency list graph representation.
- Search by location ID (e.g., `NORTH_GATE`) or Name (e.g., `North Gate`).
- Performance benchmarking and complexity analysis.

## Project Structure
- `src/`: Core logic (models, graph, dijkstra, data IO).
- `data/`: CSV files containing nodes and edges for HUST.
- `docs/`: Algorithm pseudocode, Big-O complexity, and performance reports.
- `tests/`: Unit tests for the algorithm.
- `main.py`: CLI entry point.

## Usage

### 1. List all locations
```bash
python main.py --list
```

### 2. Find shortest path by ID
```bash
python main.py --start NORTH_GATE --end TQB_LIBRARY
```

### 3. Find shortest path by Name
```bash
python main.py --start "North Gate" --end "Thư viện Tạ Quang Bửu"
```

### 4. Run performance benchmark
On actual HUST map:
```bash
python main.py --test
```

On generated random graphs:
```bash
python main.py --benchmark --nodes 1000 --edges 4000
```

## Documentation
Detailed documentation is available in the `docs/` folder:
- [Pseudocode](docs/pseudocode.md)
- [Complexity Analysis](docs/complexity.md)
- [Data Structures](docs/data_structure_explanation.md)
- [Performance Test Results](docs/performance_test.md) (Updated with actual benchmark data)
