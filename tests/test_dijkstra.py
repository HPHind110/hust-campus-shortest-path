import unittest
from src.graph import Graph
from src.models import Node
from src.dijkstra import dijkstra

class TestDijkstra(unittest.TestCase):
    def setUp(self):
        self.graph = Graph()
        # Create a simple triangle graph
        # A --(10)--> B --(20)--> C
        # A --(50)--> C
        self.graph.add_node(Node("A", "Node A", "type"))
        self.graph.add_node(Node("B", "Node B", "type"))
        self.graph.add_node(Node("C", "Node C", "type"))
        self.graph.add_node(Node("D", "Node D", "type")) # Isolated node
        
        self.graph.add_edge("A", "B", 10)
        self.graph.add_edge("B", "C", 20)
        self.graph.add_edge("A", "C", 50)

    def test_shortest_path(self):
        dist, path, visited, _ = dijkstra(self.graph, "A", "C")
        self.assertEqual(dist, 30)
        self.assertEqual(path, ["A", "B", "C"])

    def test_no_path(self):
        dist, path, _, _ = dijkstra(self.graph, "A", "D")
        self.assertEqual(dist, float('inf'))
        self.assertEqual(path, [])

    def test_same_node(self):
        dist, path, _, _ = dijkstra(self.graph, "A", "A")
        self.assertEqual(dist, 0)
        self.assertEqual(path, ["A"])

    def test_negative_weight_rejection(self):
        with self.assertRaises(ValueError):
            self.graph.add_edge("C", "A", -5)

if __name__ == "__main__":
    unittest.main()
