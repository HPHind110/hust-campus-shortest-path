from src.models import Vertex

class Graph:
    def __init__(self):
        # Adjacency list: vertex_id -> list of (neighbor_id, weight)
        self.adjacency_list = {}
        # Vertex metadata: vertex_id -> Vertex object
        self.vertices = {}
        self.vertex_count = 0
        self.edge_count = 0

    def addVertex(self, vertex):
        if vertex.id not in self.vertices:
            self.vertices[vertex.id] = vertex
            self.vertex_count += 1
            if vertex.id not in self.adjacency_list:
                self.adjacency_list[vertex.id] = []

    def addEdge(self, source_id, dest_id, weight, bidirectional=True):
        if weight < 0:
            raise ValueError("Edge weight cannot be negative.")
        
        if source_id not in self.adjacency_list:
            self.adjacency_list[source_id] = []
        self.adjacency_list[source_id].append((dest_id, weight))
        self.edge_count += 1
        
        if bidirectional:
            if dest_id not in self.adjacency_list:
                self.adjacency_list[dest_id] = []
            self.adjacency_list[dest_id].append((source_id, weight))
            self.edge_count += 1

    def removeVertex(self, vertex_id):
        """Optional: Removes a vertex and its associated edges."""
        if vertex_id in self.vertices:
            del self.vertices[vertex_id]
            self.vertex_count -= 1
            # Remove from adjacency list and all references in other lists
            if vertex_id in self.adjacency_list:
                # Decrease edge count for outgoing edges
                self.edge_count -= len(self.adjacency_list[vertex_id])
                del self.adjacency_list[vertex_id]
            
            for vid in self.adjacency_list:
                original_len = len(self.adjacency_list[vid])
                self.adjacency_list[vid] = [edge for edge in self.adjacency_list[vid] if edge[0] != vertex_id]
                self.edge_count -= (original_len - len(self.adjacency_list[vid]))

    def removeEdge(self, source_id, dest_id):
        """Optional: Removes an edge."""
        if source_id in self.adjacency_list:
            original_len = len(self.adjacency_list[source_id])
            self.adjacency_list[source_id] = [edge for edge in self.adjacency_list[source_id] if edge[0] != dest_id]
            self.edge_count -= (original_len - len(self.adjacency_list[source_id]))

    def getNeighbors(self, vertex_id):
        return self.adjacency_list.get(vertex_id, [])

    def getVertex(self, vertex_id):
        return self.vertices.get(vertex_id)

    def getVertexCount(self):
        return self.vertex_count

    def getEdgeCount(self):
        return self.edge_count

    def get_vertex_by_name(self, name):
        for vertex in self.vertices.values():
            if vertex.name.lower() == name.lower():
                return vertex
        return None
