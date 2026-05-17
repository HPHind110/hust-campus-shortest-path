import argparse
import sys
from src.navigator import CampusNavigator

# Ensure Vietnamese (and any non-ASCII) output works on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def main():
    parser = argparse.ArgumentParser(description="HUST Campus Shortest Path Finder")
    parser.add_argument("--list", action="store_true", help="List all campus locations")
    parser.add_argument("--start", type=str, help="Start location ID or Name")
    parser.add_argument("--end", type=str, help="End location ID or Name")
    parser.add_argument("--visualize", action="store_true", help="Visualize the shortest path")
    parser.add_argument("--save", type=str, help="Save the path result to a text file (requires --start/--end)")
    parser.add_argument("--test", action="store_true", help="Run performance test on existing HUST map")
    parser.add_argument("--benchmark", action="store_true", help="Run benchmark on a generated random graph")
    parser.add_argument("--nodes", type=int, default=1000, help="Number of nodes for benchmark")
    parser.add_argument("--edges", type=int, default=3000, help="Number of extra edges for benchmark")
    parser.add_argument("--seed", type=int, default=42, help="Seed for random graph generation")
    parser.add_argument("--runs", type=int, default=5, help="Number of benchmark runs")

    args = parser.parse_args()

    # Validate flag combinations
    if (args.start and not args.end) or (args.end and not args.start):
        parser.error("--start and --end must be used together.")

    selected_actions = []
    if args.list:
        selected_actions.append("--list")
    if args.benchmark:
        selected_actions.append("--benchmark")
    if args.test:
        selected_actions.append("--test")
    if args.start and args.end:
        selected_actions.append("--start/--end")

    if len(selected_actions) > 1:
        parser.error(
            f"Conflicting actions: {', '.join(selected_actions)}. Pick exactly one."
        )

    if args.visualize and not (args.start and args.end):
        parser.error("--visualize requires --start and --end.")
    if args.save and not (args.start and args.end):
        parser.error("--save requires --start and --end.")

    if not selected_actions:
        parser.print_help()
        return

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
            if args.save:
                navigator.saveData(args.save, result)
                print(f"Result saved to: {args.save}")
        else:
            print(f"Error: One or both locations ('{args.start}', '{args.end}') not found.")
        return

    if args.test:
        print("Running performance test on HUST map...")
        navigator.runHustBenchmark()
        return

if __name__ == "__main__":
    main()
