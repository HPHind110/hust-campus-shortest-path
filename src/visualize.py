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
        start_node = graph.nodes[start_id]
        for end_id, weight in neighbors:
            end_node = graph.nodes[end_id]
            plt.plot([start_node.x, end_node.x], [start_node.y, end_node.y], 
                     color='gray', linestyle='-', linewidth=0.5, alpha=0.5, zorder=1)

    # 2. Draw the shortest path if provided
    if path and len(path) > 1:
        path_x = []
        path_y = []
        for node_id in path:
            node = graph.nodes[node_id]
            path_x.append(node.x)
            path_y.append(node.y)
        
        plt.plot(path_x, path_y, color='red', linestyle='-', linewidth=3, marker='o', 
                 markersize=6, label='Shortest Path', zorder=3)

    # 3. Draw nodes
    for node_id, node in graph.nodes.items():
        color = 'blue'
        size = 20
        zorder = 2
        
        # Highlight start and end if path exists
        if path:
            if node_id == path[0]:
                color = 'green'
                size = 100
                zorder = 4
                plt.scatter(node.x, node.y, c=color, s=size, label='Start', zorder=zorder)
                plt.annotate(node.name, (node.x, node.y), textcoords="offset points", 
                             xytext=(0,10), ha='center', fontsize=9, fontweight='bold')
                continue
            elif node_id == path[-1]:
                color = 'darkred'
                size = 100
                zorder = 4
                plt.scatter(node.x, node.y, c=color, s=size, label='End', zorder=zorder)
                plt.annotate(node.name, (node.x, node.y), textcoords="offset points", 
                             xytext=(0,10), ha='center', fontsize=9, fontweight='bold')
                continue

        plt.scatter(node.x, node.y, c=color, s=size, zorder=zorder)
        
        # Label important nodes (gates, landmarks, etc.)
        important_types = ['gate', 'library', 'sport', 'lake']
        if node.type in important_types:
            plt.annotate(node.name, (node.x, node.y), textcoords="offset points", 
                         xytext=(0,5), ha='center', fontsize=8)

    plt.title("HUST Campus Shortest Path Visualization")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.3)
    
    # Invert Y axis if necessary (often map coordinates have Y increasing downwards)
    # But based on the data, it seems standard. Let's keep it as is or auto-scale.
    # Actually, we can just let matplotlib handle it.
    
    plt.savefig(output_path)
    print(f"\nVisualization saved to: {output_path}")
    plt.close()
