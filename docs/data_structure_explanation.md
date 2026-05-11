# Data Structure Explanation

This document explains the choices of data structures used in the HUST Shortest Path project.

## 1. Graph: Adjacency List
We represent the HUST campus map using an **Adjacency List**.
- **Structure**: A dictionary mapping `node_id` to a list of tuples `(neighbor_id, weight)`.
- **Reasoning**: Campus maps are generally sparse (each building only connects to a few neighbors). An Adjacency List is more memory-efficient \( $O(V+E)$ \) than an Adjacency Matrix \($O(V^2)$\).

## 2. Priority Queue: Min-Heap
For Dijkstra's algorithm, we need to efficiently extract the node with the minimum tentative distance.
- **Structure**: Python's built-in `heapq` module.
- **Reasoning**: Min-Heap allows extraction in $O(\log V)$ time. This is the standard optimization for Dijkstra's algorithm.

## 3. Node Mapping
- **Structure**: Dictionaries.
    - `graph.nodes`: `id -> Node Object` for $O(1)$ metadata retrieval.
    - `parents`: `id -> previous_id` for path reconstruction.
    - `distances`: `id -> float` for tracking shortest paths found so far.
- **Reasoning**: Dictionaries (Hash Maps) provide $O(1)$ average time complexity for lookups, which is crucial during the relaxation step.
