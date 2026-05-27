import os
import sys
import unittest
import tempfile

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from src.data_io import load_data


class TestDataIO(unittest.TestCase):
    def write_file(self, path, content):
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

    def test_load_valid_data(self):
        with tempfile.TemporaryDirectory() as tmp:
            nodes_file = os.path.join(tmp, "nodes.csv")
            edges_file = os.path.join(tmp, "edges.csv")

            self.write_file(
                nodes_file,
                "id,name,type,x,y,description,visible\n"
                "A,Gate,gate,10,20,,1\n"
                "B,Library,library,30,40,,1\n"
                "C,Canteen,canteen,50,60,,1\n"
            )

            self.write_file(
                edges_file,
                "from,to,weight,bidirectional,waypoints\n"
                "A,B,15,1,\n"
                "B,C,20,1,\n"
            )

            graph = load_data(nodes_file, edges_file)

            self.assertIsNotNone(graph)
            self.assertEqual(graph.getVertexCount(), 3)
            self.assertEqual(graph.getEdgeCount(), 2)

    def test_missing_nodes_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            nodes_file = os.path.join(tmp, "missing_nodes.csv")
            edges_file = os.path.join(tmp, "edges.csv")

            self.write_file(
                edges_file,
                "from,to,weight,bidirectional,waypoints\n"
            )

            graph = load_data(nodes_file, edges_file)

            self.assertIsNone(graph)

    def test_edge_with_missing_vertex(self):
        with tempfile.TemporaryDirectory() as tmp:
            nodes_file = os.path.join(tmp, "nodes.csv")
            edges_file = os.path.join(tmp, "edges.csv")

            self.write_file(
                nodes_file,
                "id,name,type,x,y,description,visible\n"
                "A,Gate,gate,10,20,,1\n"
                "B,Library,library,30,40,,1\n"
            )

            self.write_file(
                edges_file,
                "from,to,weight,bidirectional,waypoints\n"
                "A,X,15,1,\n"
            )

            graph = load_data(nodes_file, edges_file)

            self.assertIsNone(graph)

    def test_negative_weight_in_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            nodes_file = os.path.join(tmp, "nodes.csv")
            edges_file = os.path.join(tmp, "edges.csv")

            self.write_file(
                nodes_file,
                "id,name,type,x,y,description,visible\n"
                "A,Gate,gate,10,20,,1\n"
                "B,Library,library,30,40,,1\n"
            )

            self.write_file(
                edges_file,
                "from,to,weight,bidirectional,waypoints\n"
                "A,B,-10,1,\n"
            )

            graph = load_data(nodes_file, edges_file)

            self.assertIsNone(graph)


if __name__ == "__main__":
    unittest.main()