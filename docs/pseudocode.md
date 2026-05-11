# Dijkstra's Algorithm Pseudocode

This document describes the manual implementation of Dijkstra's algorithm used in this project.

```text
FUNCTION Dijkstra(Graph, StartNode, EndNode):
    # Initialization
    CREATE a Priority Queue (PQ)
    CREATE a Map 'Distances' with all nodes set to Infinity
    CREATE a Map 'Parents' to track the path
    
    SET Distances[StartNode] = 0
    PUSH (0, StartNode) into PQ
    
    WHILE PQ is not empty:
        POP (current_distance, current_node) with smallest distance
        
        IF current_node == EndNode:
            BREAK (Target reached)
            
        IF current_distance > Distances[current_node]:
            CONTINUE (Already found a shorter path)
            
        FOR each neighbor of current_node:
            weight = edge weight between current_node and neighbor
            new_distance = current_distance + weight
            
            IF new_distance < Distances[neighbor]:
                Distances[neighbor] = new_distance
                Parents[neighbor] = current_node
                PUSH (new_distance, neighbor) into PQ
                
    RETURN Distances[EndNode] and RECONSTRUCT_PATH(Parents, EndNode)

FUNCTION ReconstructPath(Parents, EndNode):
    path = []
    current = EndNode
    WHILE current is not NULL:
        APPEND current to path
        current = Parents[current]
    REVERSE path
    RETURN path
```
