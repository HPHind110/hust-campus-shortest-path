class Graph:
    def __init__(self):
        # Adjacency list: node_id -> list of (neighbor_id, weight)
        self.adjacency_list = {}
        # Node metadata: node_id -> Node object
        self.nodes = {}

    def add_node(self, node):
        self.nodes[node.id] = node
        if node.id not in self.adjacency_list:
            self.adjacency_list[node.id] = []

    def add_edge(self, start_id, end_id, weight, bidirectional=True):
        if weight < 0:
            raise ValueError("Edge weight cannot be negative.")
        
        if start_id not in self.adjacency_list:
            self.adjacency_list[start_id] = []
        self.adjacency_list[start_id].append((end_id, weight))
        
        if bidirectional:
            if end_id not in self.adjacency_list:
                self.adjacency_list[end_id] = []
            self.adjacency_list[end_id].append((start_id, weight))

    def get_neighbors(self, node_id):
        return self.adjacency_list.get(node_id, [])

    def get_node_by_name(self, name):
        for node in self.nodes.values():
            if node.name.lower() == name.lower():
                return node
        return None
