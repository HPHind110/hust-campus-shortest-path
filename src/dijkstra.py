import heapq
import time

def dijkstra(graph, start_id, end_id):
    """
    Implements Dijkstra's algorithm using a min-priority queue (heapq).
    Returns:
        total_distance, path, visited_count, elapsed_ms
    """
    start_time = time.perf_counter()
    
    # Priority Queue stores: (distance, current_node_id)
    pq = [(0, start_id)]
    
    # Distances dictionary: node_id -> shortest distance from start
    distances = {node_id: float('inf') for node_id in graph.nodes}
    distances[start_id] = 0
    
    # Parent dictionary for path reconstruction: node_id -> previous_node_id
    parents = {node_id: None for node_id in graph.nodes}
    
    visited_nodes = set()
    
    while pq:
        current_distance, current_id = heapq.heappop(pq)
        
        # Standard Dijkstra: if we found a longer path, skip it
        if current_distance > distances[current_id]:
            continue

        visited_nodes.add(current_id)
        
        # If we reached the target, we can stop early
        if current_id == end_id:
            break
            
        # Explore neighbors
        for neighbor_id, weight in graph.get_neighbors(current_id):
            distance = current_distance + weight
            
            # If found a shorter path to neighbor
            if distance < distances[neighbor_id]:
                distances[neighbor_id] = distance
                parents[neighbor_id] = current_id
                heapq.heappush(pq, (distance, neighbor_id))
                
    end_time = time.perf_counter()
    elapsed_ms = (end_time - start_time) * 1000
    
    # Reconstruct path
    path = reconstruct_path(parents, start_id, end_id)
    
    total_distance = distances[end_id]
    visited_count = len(visited_nodes)
    if total_distance == float('inf'):
        return float('inf'), [], visited_count, elapsed_ms
        
    return total_distance, path, visited_count, elapsed_ms

def reconstruct_path(parents, start_id, end_id):
    path = []
    current = end_id
    
    # If end_id has no parent and is not start_id, no path exists
    if parents[end_id] is None and start_id != end_id:
        return []
        
    while current is not None:
        path.append(current)
        current = parents[current]
        
    return path[::-1] # Reverse to get start -> end
