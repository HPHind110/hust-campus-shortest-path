import os
import sys
import unittest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from src.graph import Graph
from src.models import Vertex
from src.dijkstra import dijkstra

print("DANG CHAY FILE CO 3 TEST")
class TestDijkstraBasic(unittest.TestCase):
    def setUp(self):
        self.graph = Graph()

        self.graph.addVertex(Vertex("A", "Node A", "test"))
        self.graph.addVertex(Vertex("B", "Node B", "test"))
        self.graph.addVertex(Vertex("C", "Node C", "test"))
        self.graph.addVertex(Vertex("D", "Node D", "test"))

        self.graph.addEdge("A", "B", 10)
        self.graph.addEdge("B", "C", 20)
        self.graph.addEdge("A", "C", 50)

    def test_shortest_path_normal_case(self):
        result = dijkstra(self.graph, "A", "C")

        self.assertTrue(result.found)
        self.assertEqual(result.total_distance, 30)
        self.assertEqual(result.path, ["A", "B", "C"])

    def test_direct_path_not_always_best(self):
        result = dijkstra(self.graph, "A", "C")

        self.assertNotEqual(result.path, ["A", "C"])
        self.assertLess(result.total_distance, 50)

    def test_multiple_valid_shortest_paths(self):
        graph = Graph()

        for node in ["A", "B", "C", "D"]:
            graph.addVertex(Vertex(node, f"Node {node}", "test"))

        graph.addEdge("A", "B", 1)
        graph.addEdge("B", "D", 1)
        graph.addEdge("A", "C", 1)
        graph.addEdge("C", "D", 1)

        result = dijkstra(graph, "A", "D")

        self.assertTrue(result.found)
        self.assertEqual(result.total_distance, 2)
        self.assertIn(result.path, [["A", "B", "D"], ["A", "C", "D"]])


if __name__ == "__main__":
    unittest.main()