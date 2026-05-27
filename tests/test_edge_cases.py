import os
import sys
import unittest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from src.graph import Graph
from src.models import Vertex
from src.dijkstra import dijkstra
from src.navigator import CampusNavigator


class TestEdgeCases(unittest.TestCase):
    def setUp(self):
        self.graph = Graph()

        self.graph.addVertex(Vertex("A", "Node A", "test"))
        self.graph.addVertex(Vertex("B", "Node B", "test"))
        self.graph.addVertex(Vertex("C", "Node C", "test"))
        self.graph.addVertex(Vertex("D", "Node D", "test"))

        self.graph.addEdge("A", "B", 10)
        self.graph.addEdge("B", "C", 20)

        # D là đỉnh cô lập, không nối với ai

    def test_same_start_and_end(self):
        result = dijkstra(self.graph, "A", "A")

        self.assertTrue(result.found)
        self.assertEqual(result.total_distance, 0)
        self.assertEqual(result.path, ["A"])

    def test_no_path_between_two_vertices(self):
        result = dijkstra(self.graph, "A", "D")

        self.assertFalse(result.found)
        self.assertEqual(result.total_distance, float("inf"))
        self.assertEqual(result.path, [])

    def test_negative_weight_is_rejected(self):
        with self.assertRaises(ValueError):
            self.graph.addEdge("A", "C", -5)

    def test_edge_to_missing_vertex_is_rejected(self):
        with self.assertRaises(ValueError):
            self.graph.addEdge("A", "X", 10)

    def test_navigator_returns_none_when_vertex_not_found(self):
        navigator = CampusNavigator()
        navigator.graph = self.graph

        result = navigator.findShortestPath("A", "X")

        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()