class Node:
    def __init__(self, node_id, name, node_type, x=0, y=0, description=""):
        self.id = node_id
        self.name = name
        self.type = node_type
        self.x = x
        self.y = y
        self.description = description

    def __repr__(self):
        return f"Node({self.id}, {self.name})"

class Edge:
    def __init__(self, start_node, end_node, weight, bidirectional=True):
        self.start_node = start_node
        self.end_node = end_node
        self.weight = weight
        self.bidirectional = bidirectional
