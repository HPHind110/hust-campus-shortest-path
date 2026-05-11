import argparse
import sys
from src.data_io import load_data
from src.dijkstra import dijkstra
from src.performance import run_performance_test, run_benchmark
from src.visualize import visualize_path

def main():
    parser = argparse.ArgumentParser(description="HUST Campus Shortest Path Finder")
    parser.add_argument("--list", action="store_true", help="List all campus locations")
    parser.add_argument("--start", type=str, help="Start location ID or Name")
    parser.add_argument("--end", type=str, help="End location ID or Name")
    parser.add_argument("--visualize", action="store_true", help="Visualize the shortest path")
    parser.add_argument("--test", action="store_true", help="Run performance test on existing HUST map")
    parser.add_argument("--benchmark", action="store_true", help="Run benchmark on a generated random graph")
    parser.add_argument("--nodes", type=int, default=1000, help="Number of nodes for benchmark")
    parser.add_argument("--edges", type=int, default=3000, help="Number of extra edges for benchmark")

    args = parser.parse_args()

    if args.benchmark:
        run_performance_test(args.nodes, args.edges)
        return

    # Load data for other commands
    graph = load_data("data/hust_nodes.csv", "data/hust_edges.csv")
    if not graph:
        sys.exit(1)

    if args.list:
        print("\n--- HUST Campus Locations ---")
        print(f"{'ID':<15} | {'Name':<20} | {'Type':<10}")
        print("-" * 50)
        for node in graph.nodes.values():
            print(f"{node.id:<15} | {node.name:<20} | {node.type:<10}")
        return

    if args.start and args.end:
        # Resolve IDs if names were provided
        start_node = graph.nodes.get(args.start) or graph.get_node_by_name(args.start)
        end_node = graph.nodes.get(args.end) or graph.get_node_by_name(args.end)

        if not start_node:
            print(f"Error: Start location '{args.start}' not found.")
            return
        if not end_node:
            print(f"Error: End location '{args.end}' not found.")
            return

        print(f"\nFinding path from {start_node.name} to {end_node.name}...")
        dist, path, visited, time_ms = dijkstra(graph, start_node.id, end_node.id)

        if dist == float('inf'):
            print("No path found between these locations.")
        else:
            print(f"\nResults:")
            print(f"- Total Distance: {dist} meters")
            print(f"- Path: {' -> '.join(path)}")
            print(f"- Visited Nodes: {visited}")
            print(f"- Execution Time: {time_ms:.4f} ms")
            
            if args.visualize:
                visualize_path(graph, path)
        return

    if args.test:
        print("Running performance test on HUST map...")
        run_benchmark(graph)
        return

    parser.print_help()

if __name__ == "__main__":
    main()
