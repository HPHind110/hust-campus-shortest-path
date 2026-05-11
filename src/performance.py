import time
import random
import statistics
from src.graph import Graph
from src.models import Node
from src.dijkstra import dijkstra

def generate_random_graph(num_nodes, extra_edges, max_weight, seed=42):
    """
    Generates a random connected weighted graph deterministically with a seed.
    To ensure connectivity, it first creates a simple path: 0-1-2-...-(n-1).
    Then it adds 'extra_edges' randomly.
    """
    rng = random.Random(seed)
    graph = Graph()
    
    # Create nodes
    for i in range(num_nodes):
        node_id = str(i)
        node = Node(node_id, f"Node {i}", "Random")
        graph.add_node(node)
        
    # Ensure connectivity: create a path 0-1-2-...-(num_nodes-1)
    for i in range(num_nodes - 1):
        weight = rng.randint(1, max_weight)
        graph.add_edge(str(i), str(i+1), weight)
        
    # Add extra random edges
    edges_count = num_nodes - 1
    attempts = 0
    max_attempts = extra_edges * 5 # Increased attempts for better coverage in dense graphs
    
    while edges_count < (num_nodes - 1 + extra_edges) and attempts < max_attempts:
        u = str(rng.randint(0, num_nodes - 1))
        v = str(rng.randint(0, num_nodes - 1))
        
        if u != v:
            neighbors = [neighbor for neighbor, _ in graph.get_neighbors(u)]
            if v not in neighbors:
                weight = rng.randint(1, max_weight)
                graph.add_edge(u, v, weight)
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
    
    # Count actual undirected edges
    actual_edges = sum(len(adj) for adj in graph.adjacency_list.values()) // 2
    
    print(f"Running benchmark with {runs} runs from {start_node} to {end_node}...")
    
    runtimes = []
    distances = []
    paths = []
    visited_counts = []
    
    for _ in range(runs):
        dist, path, visited, time_ms = dijkstra(graph, start_node, end_node)
        runtimes.append(time_ms)
        distances.append(dist)
        paths.append(path)
        visited_counts.append(visited)
        
    avg_time = statistics.mean(runtimes)
    median_time = statistics.median(runtimes)
    min_time = min(runtimes)
    max_time = max(runtimes)
    
    # Since the graph and start/end are fixed, dist, path, and visited should be same for all runs
    dist = distances[0]
    path = paths[0]
    visited = visited_counts[0]

    print("\n--- Benchmark Results ---")
    print(f"Number of nodes:      {num_nodes}")
    print(f"Total edges:          {actual_edges}")
    print(f"Extra edges (req):    {extra_edges}")
    print(f"Extra edges (added):  {actual_edges - (num_nodes - 1)}")
    print(f"Seed:                 {seed}")
    print(f"Runs:                 {runs}")
    print("-" * 26)
    print(f"Shortest distance:    {dist}")
    print(f"Path length:          {len(path)}")
    print(f"Visited node count:   {visited}")
    print("-" * 26)
    print(f"Avg runtime:          {avg_time:.4f} ms")
    print(f"Median runtime:       {median_time:.4f} ms")
    print(f"Min runtime:          {min_time:.4f} ms")
    print(f"Max runtime:          {max_time:.4f} ms")
    print("--------------------------")

def run_benchmark(graph):
    """
    Runs basic performance metrics on the existing graph (kept for compatibility).
    """
    all_node_ids = list(graph.nodes.keys())
    if len(all_node_ids) < 2:
        print("Not enough nodes to benchmark.")
        return

    print(f"Benchmarking on current graph ({len(graph.nodes)} nodes, {sum(len(adj) for adj in graph.adjacency_list.values()) // 2} edges)")
    
    total_time = 0
    iterations = 10
    
    # Use fixed seed for random choices in this simple benchmark to keep it somewhat stable
    rng = random.Random(42)
    
    for _ in range(iterations):
        start = rng.choice(all_node_ids)
        end = rng.choice(all_node_ids)
        
        _, _, _, elapsed_ms = dijkstra(graph, start, end)
        total_time += elapsed_ms
        
    avg_time = total_time / iterations
    print(f"Average execution time over {iterations} random paths: {avg_time:.4f} ms")
