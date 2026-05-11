import argparse
import sys
from src.navigator import CampusNavigator

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
    parser.add_argument("--seed", type=int, default=42, help="Seed for random graph generation")
    parser.add_argument("--runs", type=int, default=5, help="Number of benchmark runs")

    args = parser.parse_args()

    navigator = CampusNavigator()

    if args.benchmark:
        navigator.performanceTest(args.nodes, args.edges, args.seed, args.runs)
        return

    # Load data for other commands
    if not navigator.loadData("data/hust_nodes.csv", "data/hust_edges.csv"):
        sys.exit(1)

    if args.list:
        navigator.listLocations()
        return

    if args.start and args.end:
        result = navigator.findShortestPath(args.start, args.end)
        if result:
            result.print_path()
            if args.visualize:
                navigator.visualize(result)
        else:
            print(f"Error: One or both locations ('{args.start}', '{args.end}') not found.")
        return

    if args.test:
        print("Running performance test on HUST map...")
        navigator.runHustBenchmark()
        return

    parser.print_help()

if __name__ == "__main__":
    main()
