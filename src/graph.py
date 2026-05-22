from src.models import Vertex

class Graph:
    def __init__(self):
        # Adjacency list: vertex_id -> list of (neighbor_id, weight)
        self.adjacency_list = {}
        # Vertex metadata: vertex_id -> Vertex object
        self.vertices = {}
        # Optional polyline geometry for an edge: (source_id, dest_id) -> [(x, y), ...]
        # Only used for rendering — Dijkstra ignores it.
        self.edge_waypoints = {}
        self.vertex_count = 0
        self.edge_count = 0

    def addVertex(self, vertex):
        if vertex.id not in self.vertices:
            self.vertices[vertex.id] = vertex
            self.vertex_count += 1
            if vertex.id not in self.adjacency_list:
                self.adjacency_list[vertex.id] = []

    def addEdge(self, source_id, dest_id, weight, bidirectional=True, waypoints=None):
        if weight < 0:
            raise ValueError(
                f"Edge weight cannot be negative (got {weight} for '{source_id}' -> '{dest_id}')."
            )
        if source_id not in self.vertices:
            raise ValueError(f"Cannot add edge: source vertex '{source_id}' does not exist.")
        if dest_id not in self.vertices:
            raise ValueError(f"Cannot add edge: destination vertex '{dest_id}' does not exist.")

        self.adjacency_list[source_id].append((dest_id, weight))
        if bidirectional:
            self.adjacency_list[dest_id].append((source_id, weight))
        if waypoints:
            self.edge_waypoints[(source_id, dest_id)] = list(waypoints)
            if bidirectional:
                self.edge_waypoints[(dest_id, source_id)] = list(reversed(waypoints))
        self.edge_count += 1

    def getEdgeWaypoints(self, source_id, dest_id):
        return self.edge_waypoints.get((source_id, dest_id), [])

    def removeVertex(self, vertex_id):
        """Removes a vertex and every logical edge touching it."""
        if vertex_id not in self.vertices:
            return

        outgoing = {n for n, _ in self.adjacency_list.get(vertex_id, [])}
        incoming = {
            vid for vid, edges in self.adjacency_list.items()
            if vid != vertex_id and any(e[0] == vertex_id for e in edges)
        }
        self.edge_count -= len(outgoing | incoming)

        del self.vertices[vertex_id]
        self.vertex_count -= 1
        self.adjacency_list.pop(vertex_id, None)
        for vid in self.adjacency_list:
            self.adjacency_list[vid] = [e for e in self.adjacency_list[vid] if e[0] != vertex_id]

    def removeEdge(self, source_id, dest_id):
        """Removes the logical edge between source_id and dest_id (clears both directions)."""
        removed = False
        for u, v in ((source_id, dest_id), (dest_id, source_id)):
            if u in self.adjacency_list:
                before = len(self.adjacency_list[u])
                self.adjacency_list[u] = [e for e in self.adjacency_list[u] if e[0] != v]
                if len(self.adjacency_list[u]) != before:
                    removed = True
        if removed:
            self.edge_count -= 1

    def getNeighbors(self, vertex_id):
        return self.adjacency_list.get(vertex_id, [])

    def getVertex(self, vertex_id):
        return self.vertices.get(vertex_id)

    def getVertexCount(self):
        return self.vertex_count

    def getEdgeCount(self):
        return self.edge_count

    def getVertexByName(self, name):
        for vertex in self.vertices.values():
            if vertex.name.lower() == name.lower():
                return vertex
        return None
