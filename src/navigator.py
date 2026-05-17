from src.data_io import load_data, save_data
from src.dijkstra import dijkstra
from src.performance import run_performance_test, run_benchmark
from src.visualize import visualize_path

class CampusNavigator:
    def __init__(self):
        self.graph = None

    def loadData(self, nodes_file, edges_file):
        self.graph = load_data(nodes_file, edges_file)
        return self.graph is not None

    def saveData(self, output_file, result):
        save_data(output_file, result)

    def findShortestPath(self, start_id_or_name, end_id_or_name):
        if not self.graph:
            return None
        
        # Resolve IDs if names were provided
        start_vertex = self.graph.getVertex(start_id_or_name) or self.graph.getVertexByName(start_id_or_name)
        end_vertex = self.graph.getVertex(end_id_or_name) or self.graph.getVertexByName(end_id_or_name)

        if not start_vertex or not end_vertex:
            return None

        return dijkstra(self.graph, start_vertex.id, end_vertex.id)

    def listLocations(self):
        if not self.graph:
            return
            
        print("\n--- HUST Campus Locations ---")
        
        # Define the categories and their order
        categories = {
            "gate": "Gate",
            "library": "Library",
            "lake": "Lake",
            "building": "Building",
            "canteen": "Canteen",
            "dormitory": "Dormitory",
            "sport": "Sport"
        }
        order = ["gate", "library", "lake", "building", "canteen", "dormitory", "sport"]
        
        # Group vertices by type
        grouped = {cat: [] for cat in order}
        for vertex in self.graph.vertices.values():
            if vertex.type in grouped:
                grouped[vertex.type].append(vertex)
        
        for cat_key in order:
            vertices_in_cat = grouped[cat_key]
            if not vertices_in_cat:
                continue

            print(f"\n[{categories[cat_key]}]")

            max_id_len = max(
                (len(v.id) for v in vertices_in_cat if v.id != v.name), default=0
            )

            for vertex in vertices_in_cat:
                if vertex.id == vertex.name:
                    print(f"  - {vertex.id}")
                else:
                    print(f"  - {vertex.id:<{max_id_len}} : {vertex.name}")

    def performanceTest(self, num_nodes, extra_edges, seed=42, runs=5):
        run_performance_test(num_nodes, extra_edges, seed, runs)

    def runHustBenchmark(self):
        if self.graph:
            run_benchmark(self.graph)

    def visualize(self, result):
        if self.graph and result and result.found:
            visualize_path(self.graph, result.path)
