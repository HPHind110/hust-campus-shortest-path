import heapq
import time
from src.models import DijkstraResult

def dijkstra(graph, start_id, end_id):
    """
    Implements Dijkstra's algorithm using a min-priority queue (heapq).
    Returns:
        DijkstraResult object
    """
    start_time = time.perf_counter()
    
    # Priority Queue stores: (distance, current_vertex_id)
    pq = [(0, start_id)]
    
    # Distances dictionary: vertex_id -> shortest distance from start
    distances = {vertex_id: float('inf') for vertex_id in graph.vertices}
    distances[start_id] = 0
    
    # Parent dictionary for path reconstruction: vertex_id -> previous_vertex_id
    parents = {vertex_id: None for vertex_id in graph.vertices}
    
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
        for neighbor_id, weight in graph.getNeighbors(current_id):
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
    
    return DijkstraResult(start_id, end_id, total_distance, path, visited_count, elapsed_ms)

def reconstruct_path(parents, start_id, end_id):
    path = []
    current = end_id
    
    # If end_id has no parent and is not start_id, no path exists
    if parents.get(end_id) is None and start_id != end_id:
        return []
        
    while current is not None:
        path.append(current)
        current = parents[current]
        
    return path[::-1] # Reverse to get start -> end
