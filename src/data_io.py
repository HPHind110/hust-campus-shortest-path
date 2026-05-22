import csv
from src.models import Vertex
from src.graph import Graph


def _parse_waypoints(raw):
    """Parse `"x1,y1;x2,y2;..."` into [(x1, y1), (x2, y2), ...]. Empty string -> []."""
    if not raw:
        return []
    points = []
    for chunk in raw.split(';'):
        chunk = chunk.strip()
        if not chunk:
            continue
        try:
            xs, ys = chunk.split(',')
            points.append((int(xs.strip()), int(ys.strip())))
        except ValueError:
            raise ValueError(f"Invalid waypoint segment '{chunk}', expected 'x,y'.")
    return points


def load_data(nodes_file, edges_file):
    graph = Graph()

    # Load nodes
    try:
        with open(nodes_file, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                visible_raw = row.get('visible', '1')
                visible = str(visible_raw).strip() not in ('0', 'false', 'False', '')
                vertex = Vertex(
                    vertex_id=row['id'],
                    name=row['name'],
                    vertex_type=row['type'],
                    x=int(row['x']),
                    y=int(row['y']),
                    description=row.get('description', ''),
                    visible=visible,
                )
                graph.addVertex(vertex)
    except FileNotFoundError:
        print(f"Error: {nodes_file} not found.")
        return None

    # Load edges
    try:
        with open(edges_file, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for line_num, row in enumerate(reader, start=2):
                try:
                    waypoints = _parse_waypoints(row.get('waypoints', ''))
                    graph.addEdge(
                        source_id=row['from'],
                        dest_id=row['to'],
                        weight=float(row['weight']),
                        bidirectional=int(row['bidirectional']) == 1,
                        waypoints=waypoints,
                    )
                except ValueError as e:
                    print(f"Error in {edges_file} (line {line_num}): {e}")
                    return None
                except KeyError as e:
                    print(f"Error in {edges_file} (line {line_num}): missing column {e}.")
                    return None
    except FileNotFoundError:
        print(f"Error: {edges_file} not found.")
        return None

    return graph

def save_data(output_file, result):
    """
    Saves path results to a file for reporting.
    """
    with open(output_file, mode='w', encoding='utf-8') as f:
        f.write(f"Shortest Path Result\n")
        f.write(f"====================\n")
        f.write(f"Source: {result.source_id}\n")
        f.write(f"Destination: {result.dest_id}\n")
        f.write(f"Distance: {result.total_distance}\n")
        f.write(f"Path: {' -> '.join(result.path)}\n")
        f.write(f"Visited Nodes: {result.visited_count}\n")
        f.write(f"Time: {result.elapsed_ms:.4f} ms\n")
