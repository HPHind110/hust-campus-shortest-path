# Complexity Analysis

Analysis of the Dijkstra implementation for the HUST Campus Shortest Path project.

## 1. Time Complexity

The implementation uses an **Adjacency List** and a **Min-Priority Queue (Binary Heap)**.

- **Initialization**: $O(V)$ to set initial distances to infinity.
- **Main Loop**: Executes at most $V$ times (once per node).
- **Edge Relaxation**: Total number of relaxations is $E$.
- **Heap Operations**:
    - `heappop`: $O(\log V)$
    - `heappush`: $O(\log V)$

Total Time Complexity: **$O((V + E) \log V)$**

In a dense graph, this is significantly better than the $O(V^2)$ approach using a simple array. Empirical validation of this complexity can be found in the [Performance Test Report](performance_test.md).

## 2. Space Complexity

- **Adjacency List**: $O(V + E)$ to store nodes and edges.
- **Distances Map**: $O(V)$
- **Parents Map**: $O(V)$
- **Priority Queue**: $O(V)$ in the worst case.

Total Space Complexity: **$O(V + E)$**

## 3. Data Structure Choices

| Component | Choice | Reason |
| :--- | :--- | :--- |
| Graph | Adjacency List | Memory efficient for sparse campus maps. |
| Priority Queue | `heapq` (Min-Heap) | Provides efficient $O(\log V)$ extraction of the minimum distance node. |
| Path Tracking | Dictionary (Parent Map) | $O(1)$ lookup and easy path reconstruction. |
