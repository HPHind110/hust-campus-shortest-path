import os

def visualize_path(graph, path=None, output_path="output/hust_shortest_path.png"):
    """
    Visualizes the graph and optionally the shortest path.
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("\nError: matplotlib is not installed.")
        print("Please install matplotlib with: pip install matplotlib")
        return

    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    plt.figure(figsize=(12, 10))

    # 1. Draw all edges
    for start_id, neighbors in graph.adjacency_list.items():
        start_vertex = graph.vertices[start_id]
        for end_id, weight in neighbors:
            end_vertex = graph.vertices[end_id]
            plt.plot([start_vertex.x, end_vertex.x], [start_vertex.y, end_vertex.y], 
                     color='gray', linestyle='-', linewidth=0.5, alpha=0.5, zorder=1)

    # 2. Draw the shortest path if provided
    if path and len(path) > 1:
        path_x = []
        path_y = []
        for vertex_id in path:
            vertex = graph.vertices[vertex_id]
            path_x.append(vertex.x)
            path_y.append(vertex.y)
        
        plt.plot(path_x, path_y, color='red', linestyle='-', linewidth=3, marker='o', 
                 markersize=6, label='Shortest Path', zorder=3)

    # 3. Draw vertices
    for vertex_id, vertex in graph.vertices.items():
        color = 'blue'
        size = 20
        zorder = 2
        
        # Highlight start and end if path exists
        if path:
            if vertex_id == path[0]:
                color = 'green'
                size = 100
                zorder = 4
                plt.scatter(vertex.x, vertex.y, c=color, s=size, label='Start', zorder=zorder)
                plt.annotate(vertex.name, (vertex.x, vertex.y), textcoords="offset points", 
                             xytext=(0,10), ha='center', fontsize=9, fontweight='bold')
                continue
            elif vertex_id == path[-1]:
                color = 'darkred'
                size = 100
                zorder = 4
                plt.scatter(vertex.x, vertex.y, c=color, s=size, label='End', zorder=zorder)
                plt.annotate(vertex.name, (vertex.x, vertex.y), textcoords="offset points", 
                             xytext=(0,10), ha='center', fontsize=9, fontweight='bold')
                continue

        plt.scatter(vertex.x, vertex.y, c=color, s=size, zorder=zorder)
        
        # Label important nodes (gates, landmarks, etc.)
        important_types = ['gate', 'library', 'sport', 'lake']
        if vertex.type in important_types:
            plt.annotate(vertex.name, (vertex.x, vertex.y), textcoords="offset points", 
                         xytext=(0,5), ha='center', fontsize=8)

    plt.title("HUST Campus Shortest Path Visualization")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.3)
    
    plt.savefig(output_path)
    print(f"\nVisualization saved to: {output_path}")
    plt.close()
