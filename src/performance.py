import time
import random
import statistics
from src.graph import Graph
from src.models import Vertex
from src.dijkstra import dijkstra

def generate_random_graph(num_nodes, extra_edges, max_weight, seed=42):
    """
    Generates a random connected weighted graph deterministically with a seed.
    """
    rng = random.Random(seed)
    graph = Graph()
    
    # Create vertices
    for i in range(num_nodes):
        v_id = str(i)
        vertex = Vertex(v_id, f"Vertex {i}", "Random")
        graph.addVertex(vertex)
        
    # Ensure connectivity: create a path 0-1-2-...-(num_nodes-1)
    existing_pairs = set()
    for i in range(num_nodes - 1):
        weight = rng.randint(1, max_weight)
        u, v = str(i), str(i + 1)
        graph.addEdge(u, v, weight)
        existing_pairs.add(frozenset((u, v)))

    # Add extra random edges (O(1) duplicate check via set)
    edges_count = num_nodes - 1
    attempts = 0
    max_attempts = extra_edges * 5

    while edges_count < (num_nodes - 1 + extra_edges) and attempts < max_attempts:
        u = str(rng.randint(0, num_nodes - 1))
        v = str(rng.randint(0, num_nodes - 1))

        if u != v:
            key = frozenset((u, v))
            if key not in existing_pairs:
                weight = rng.randint(1, max_weight)
                graph.addEdge(u, v, weight)
                existing_pairs.add(key)
                edges_count += 1
        attempts += 1

    return graph

def run_performance_test(num_nodes, extra_edges, seed=42, runs=5, max_weight=100):
    """
    Runs Dijkstra multiple times on a generated random graph and prints detailed metrics.
    """
    print(f"Generating random graph with {num_nodes} nodes, {extra_edges} extra edges (Seed: {seed})...")
    graph = generate_random_graph(num_nodes, extra_edges, max_weight, seed)
    
    start_node = "0"
    end_node = str(num_nodes - 1)
    
    actual_edges = graph.getEdgeCount()
    
    print(f"Running benchmark with {runs} runs from {start_node} to {end_node}...")
    
    results = []
    for _ in range(runs):
        result = dijkstra(graph, start_node, end_node)
        results.append(result)
        
    runtimes = [r.elapsed_ms for r in results]
    
    avg_time = statistics.mean(runtimes)
    median_time = statistics.median(runtimes)
    min_time = min(runtimes)
    max_time = max(runtimes)
    
    # All runs on same graph should yield same path
    res = results[0]

    print("\n--- Benchmark Results ---")
    print(f"Number of nodes:      {num_nodes}")
    print(f"Total edges:          {actual_edges}")
    print(f"Extra edges (req):    {extra_edges}")
    print(f"Extra edges (added):  {actual_edges - (num_nodes - 1)}")
    print(f"Seed:                 {seed}")
    print(f"Runs:                 {runs}")
    print("-" * 26)
    print(f"Shortest distance:    {res.total_distance}")
    print(f"Path length:          {len(res.path)}")
    print(f"Visited node count:   {res.visited_count}")
    print("-" * 26)
    print(f"Avg runtime:          {avg_time:.4f} ms")
    print(f"Median runtime:       {median_time:.4f} ms")
    print(f"Min runtime:          {min_time:.4f} ms")
    print(f"Max runtime:          {max_time:.4f} ms")
    print("--------------------------")

def run_benchmark(graph):
    """
    Runs basic performance metrics on the existing graph.
    """
    all_node_ids = list(graph.vertices.keys())
    if len(all_node_ids) < 2:
        print("Not enough nodes to benchmark.")
        return

    print(f"Benchmarking on current graph ({graph.getVertexCount()} nodes, {graph.getEdgeCount()} edges)")
    
    total_time = 0
    iterations = 10
    rng = random.Random(42)
    
    for _ in range(iterations):
        start = rng.choice(all_node_ids)
        end = rng.choice(all_node_ids)
        while end == start:
            end = rng.choice(all_node_ids)

        result = dijkstra(graph, start, end)
        total_time += result.elapsed_ms
        
    avg_time = total_time / iterations
    print(f"Average execution time over {iterations} random paths: {avg_time:.4f} ms")
