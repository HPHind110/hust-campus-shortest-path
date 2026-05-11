import time
import random
from src.graph import Graph
from src.models import Node
from src.dijkstra import dijkstra

def generate_random_graph(num_nodes, extra_edges, max_weight):
    """
    Generates a random connected weighted graph.
    To ensure connectivity, it first creates a simple path: 0-1-2-...-(n-1).
    Then it adds 'extra_edges' randomly.
    """
    graph = Graph()
    
    # Create nodes
    for i in range(num_nodes):
        node_id = str(i)
        node = Node(node_id, f"Node {i}", "Random")
        graph.add_node(node)
        
    # Ensure connectivity: create a path 0-1-2-...-(num_nodes-1)
    for i in range(num_nodes - 1):
        weight = random.randint(1, max_weight)
        graph.add_edge(str(i), str(i+1), weight)
        
    # Add extra random edges
    edges_count = num_nodes - 1
    attempts = 0
    max_attempts = extra_edges * 2 # To avoid infinite loop if graph is dense
    
    while edges_count < (num_nodes - 1 + extra_edges) and attempts < max_attempts:
        u = str(random.randint(0, num_nodes - 1))
        v = str(random.randint(0, num_nodes - 1))
        
        if u != v:
            # Check if edge already exists to avoid redundant edges (optional but cleaner)
            neighbors = [neighbor for neighbor, _ in graph.get_neighbors(u)]
            if v not in neighbors:
                weight = random.randint(1, max_weight)
                graph.add_edge(u, v, weight)
                edges_count += 1
        attempts += 1
        
    return graph

def run_performance_test(num_nodes, extra_edges, max_weight=100):
    """
    Runs Dijkstra on a generated random graph and prints metrics.
    """
    print(f"Generating random graph with {num_nodes} nodes and {extra_edges} extra edges...")
    graph = generate_random_graph(num_nodes, extra_edges, max_weight)
    
    start_node = "0"
    end_node = str(num_nodes - 1)
    
    # We count actual edges. Since graph.add_edge is bidirectional by default:
    # Each call adds 2 directed edges.
    actual_edges = sum(len(adj) for adj in graph.adjacency_list.values()) // 2
    
    print(f"Running Dijkstra from {start_node} to {end_node}...")
    dist, path, visited, time_ms = dijkstra(graph, start_node, end_node)
    
    print("\n--- Benchmark Results ---")
    print(f"Number of nodes:      {num_nodes}")
    print(f"Number of edges:      {actual_edges}")
    print(f"Shortest distance:    {dist}")
    print(f"Path length:          {len(path)}")
    print(f"Visited node count:   {visited}")
    print(f"Runtime:              {time_ms:.4f} ms")
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
    
    for _ in range(iterations):
        start = random.choice(all_node_ids)
        end = random.choice(all_node_ids)
        
        _, _, _, elapsed_ms = dijkstra(graph, start, end)
        total_time += elapsed_ms
        
    avg_time = total_time / iterations
    print(f"Average execution time over {iterations} random paths: {avg_time:.4f} ms")
