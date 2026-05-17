import os
import sys

from flask import Flask, jsonify, render_template, request, send_from_directory

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.navigator import CampusNavigator

NODES_FILE = os.path.join(PROJECT_ROOT, "data", "hust_nodes.csv")
EDGES_FILE = os.path.join(PROJECT_ROOT, "data", "hust_edges.csv")
MAP_IMAGE = os.path.join(PROJECT_ROOT, "map-dhbk.jpg")

app = Flask(__name__)
navigator = CampusNavigator()
if not navigator.loadData(NODES_FILE, EDGES_FILE):
    raise RuntimeError("Failed to load HUST graph data.")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/map-image")
def map_image():
    return send_from_directory(PROJECT_ROOT, "map-dhbk.jpg")


@app.route("/api/nodes")
def api_nodes():
    nodes = [
        {
            "id": v.id,
            "name": v.name,
            "type": v.type,
            "x": v.x,
            "y": v.y,
            "description": v.description,
        }
        for v in navigator.graph.vertices.values()
    ]
    return jsonify({"nodes": nodes})


@app.route("/api/path")
def api_path():
    start = request.args.get("start", "").strip()
    end = request.args.get("end", "").strip()
    if not start or not end:
        return jsonify({"error": "Both 'start' and 'end' query params are required."}), 400
    if start == end:
        return jsonify({"error": "Start and end must be different."}), 400

    result = navigator.findShortestPath(start, end)
    if result is None:
        return jsonify({"error": "Unknown start or end vertex."}), 404
    if not result.found:
        return jsonify({"error": "No path exists between the selected points."}), 404

    return jsonify({
        "source_id": result.source_id,
        "dest_id": result.dest_id,
        "total_distance": result.total_distance,
        "path": result.path,
        "visited_count": result.visited_count,
        "elapsed_ms": result.elapsed_ms,
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
