class Vertex:
    def __init__(self, vertex_id, name, vertex_type, x=0, y=0, description=""):
        self.id = vertex_id
        self.name = name
        self.type = vertex_type
        self.x = x
        self.y = y
        self.description = description

    def __repr__(self):
        return f"Vertex({self.id}, {self.name})"

class Edge:
    def __init__(self, source, destination, weight, label=""):
        self.source = source
        self.destination = destination
        self.weight = weight
        self.label = label

    def __repr__(self):
        return f"Edge({self.source} -> {self.destination}, weight={self.weight})"

class DijkstraResult:
    def __init__(self, source_id, dest_id, total_distance, path, visited_count, elapsed_ms):
        self.source_id = source_id
        self.dest_id = dest_id
        self.total_distance = total_distance
        self.path = path
        self.found = total_distance != float('inf')
        self.visited_count = visited_count
        self.elapsed_ms = elapsed_ms

    def print_path(self):
        if not self.found:
            print(f"No path found from {self.source_id} to {self.dest_id}.")
        else:
            print(f"\nResults:")
            print(f"- Total Distance: {self.total_distance} meters")
            print(f"- Path: {' -> '.join(self.path)}")
            print(f"- Visited Nodes: {self.visited_count}")
            print(f"- Execution Time: {self.elapsed_ms:.4f} ms")
