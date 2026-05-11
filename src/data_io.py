import csv
from src.models import Node
from src.graph import Graph

def load_data(nodes_file, edges_file):
    graph = Graph()
    
    # Load nodes
    try:
        with open(nodes_file, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                node = Node(
                    node_id=row['id'],
                    name=row['name'],
                    node_type=row['type'],
                    x=int(row['x']),
                    y=int(row['y']),
                    description=row['description']
                )
                graph.add_node(node)
    except FileNotFoundError:
        print(f"Error: {nodes_file} not found.")
        return None

    # Load edges
    try:
        with open(edges_file, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                graph.add_edge(
                    start_id=row['from'],
                    end_id=row['to'],
                    weight=float(row['weight']),
                    bidirectional=int(row['bidirectional']) == 1
                )
    except FileNotFoundError:
        print(f"Error: {edges_file} not found.")
        return None
        
    return graph

def save_data(output_file, result_data):
    """
    Saves path results to a file for reporting.
    """
    with open(output_file, mode='w', encoding='utf-8') as f:
        f.write(f"Shortest Path Result\n")
        f.write(f"====================\n")
        f.write(f"Distance: {result_data['distance']}\n")
        f.write(f"Path: {' -> '.join(result_data['path'])}\n")
        f.write(f"Visited Nodes: {result_data['visited_count']}\n")
        f.write(f"Time: {result_data['elapsed_ms']:.4f} ms\n")
