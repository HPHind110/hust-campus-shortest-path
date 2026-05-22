import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

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


# --- Dev-only CSV hot-reload (remove after calibration is done) ---
_csv_mtimes = {
    NODES_FILE: os.path.getmtime(NODES_FILE),
    EDGES_FILE: os.path.getmtime(EDGES_FILE),
}

def _ensure_graph_fresh():
    changed = False
    for path in (NODES_FILE, EDGES_FILE):
        m = os.path.getmtime(path)
        if m != _csv_mtimes[path]:
            _csv_mtimes[path] = m
            changed = True
    if changed:
        navigator.loadData(NODES_FILE, EDGES_FILE)
        print(f"[reload] CSV changed → graph reloaded ({len(navigator.graph.vertices)} nodes)")
# --- end dev-only block ---


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/map-image")
def map_image():
    return send_from_directory(PROJECT_ROOT, "map-dhbk.jpg")


@app.route("/api/nodes")
def api_nodes():
    _ensure_graph_fresh()
    nodes = [
        {
            "id": v.id,
            "name": v.name,
            "type": v.type,
            "x": v.x,
            "y": v.y,
            "description": v.description,
            "visible": v.visible,
        }
        for v in navigator.graph.vertices.values()
    ]
    return jsonify({"nodes": nodes})


def _expand_polyline(path):
    """Expand a node-id path into [[x, y], ...] including any edge waypoints."""
    graph = navigator.graph
    coords = []
    for i, node_id in enumerate(path):
        v = graph.vertices[node_id]
        coords.append([v.x, v.y])
        if i + 1 < len(path):
            for wx, wy in graph.getEdgeWaypoints(node_id, path[i + 1]):
                coords.append([wx, wy])
    return coords


@app.route("/api/path")
def api_path():
    _ensure_graph_fresh()
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
        "polyline": _expand_polyline(result.path),
        "visited_count": result.visited_count,
        "elapsed_ms": result.elapsed_ms,
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
