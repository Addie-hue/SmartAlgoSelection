import time
import heapq

# --- GREEDY METHOD ---

def fractional_knapsack(W, wt, val):
    start_time = time.perf_counter()
    n = len(val)
    # List of (ratio, weight, value)
    items = []
    for i in range(n):
        items.append((val[i] / wt[i], wt[i], val[i]))
    
    # Sort items by value/weight ratio in descending order
    items.sort(key=lambda x: x[0], reverse=True)
    
    cur_weight = 0
    final_value = 0.0
    
    for ratio, weight, value in items:
        if cur_weight + weight <= W:
            cur_weight += weight
            final_value += value
        else:
            remain = W - cur_weight
            final_value += value * (remain / weight)
            break
            
    execution_time = time.perf_counter() - start_time
    return execution_time

def prims_algo(graph):
    # graph is adjacency matrix
    start_time = time.perf_counter()
    V = len(graph)
    key = [float('inf')] * V
    parent = [None] * V
    key[0] = 0
    mst_set = [False] * V
    
    for _ in range(V):
        # Pick the minimum key vertex from the set of vertices not yet included in MST
        min_val = float('inf')
        u = -1
        for v in range(V):
            if key[v] < min_val and not mst_set[v]:
                min_val = key[v]
                u = v
        
        if u == -1: break
        mst_set[u] = True
        
        for v in range(V):
            if 0 < graph[u][v] < float('inf') and not mst_set[v] and graph[u][v] < key[v]:
                key[v] = graph[u][v]
                parent[v] = u
                
    execution_time = time.perf_counter() - start_time
    return execution_time

def kruskals_algo(graph):
    # graph is adjacency matrix
    start_time = time.perf_counter()
    V = len(graph)
    edges = []
    for i in range(V):
        for j in range(V):
            if 0 < graph[i][j] < float('inf'):
                edges.append((graph[i][j], i, j))
    
    edges.sort() # Sort by weight
    
    parent = list(range(V))
    def find(i):
        root = i
        while parent[root] != root:
            root = parent[root]
        # Path compression (optional but good)
        while parent[i] != root:
            next_node = parent[i]
            parent[i] = root
            i = next_node
        return root
    
    def union(i, j):
        root_i = find(i)
        root_j = find(j)
        if root_i != root_j:
            parent[root_i] = root_j
            return True
        return False
        
    mst_edges = 0
    for weight, u, v in edges:
        if union(u, v):
            mst_edges += 1
            if mst_edges == V - 1:
                break
                
    execution_time = time.perf_counter() - start_time
    return execution_time

def dijkstra_algo(graph, src=0):
    # graph is adjacency matrix
    start_time = time.perf_counter()
    V = len(graph)
    dist = [float('inf')] * V
    dist[src] = 0
    pq = [(0, src)]
    
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
            
        for v in range(V):
            weight = graph[u][v]
            if 0 < weight < float('inf'):
                if dist[u] + weight < dist[v]:
                    dist[v] = dist[u] + weight
                    heapq.heappush(pq, (dist[v], v))
                    
    execution_time = time.perf_counter() - start_time
    return execution_time
