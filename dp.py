import time

# --- DYNAMIC PROGRAMMING ---

def knapsack_01(W, wt, val):
    start_time = time.perf_counter()
    n = len(val)
    dp = [[0 for _ in range(W + 1)] for _ in range(n + 1)]
    for i in range(n + 1):
        for w in range(W + 1):
            if i == 0 or w == 0:
                dp[i][w] = 0
            elif wt[i-1] <= w:
                dp[i][w] = max(val[i-1] + dp[i-1][w-wt[i-1]],  dp[i-1][w])
            else:
                dp[i][w] = dp[i-1][w]
    execution_time = time.perf_counter() - start_time
    return execution_time

def floyd_warshall(graph):
    # graph is a 2D adjacency matrix representation
    start_time = time.perf_counter()
    V = len(graph)
    dist = list(map(lambda i: list(map(lambda j: j, i)), graph))
    for k in range(V):
        for i in range(V):
            for j in range(V):
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
    execution_time = time.perf_counter() - start_time
    return execution_time

def multistage_graph(graph, stages, n):
    # n is number of vertices, graph is adjacency matrix
    start_time = time.perf_counter()
    cost = [0] * n
    dest = [0] * n
    cost[n-1] = 0
    for i in range(n-2, -1, -1):
        cost[i] = float('inf')
        for j in range(n):
            if graph[i][j] == float('inf'):
                continue
            if graph[i][j] + cost[j] < cost[i]:
                cost[i] = graph[i][j] + cost[j]
                dest[i] = j
    execution_time = time.perf_counter() - start_time
    return execution_time

def knapsack_brute(W, wt, val, n):
    start_time = time.perf_counter()
    
    def solve(W, wt, val, n):
        if n == 0 or W == 0:
            return 0
        if wt[n-1] > W:
            return solve(W, wt, val, n-1)
        else:
            return max(val[n-1] + solve(W-wt[n-1], wt, val, n-1), solve(W, wt, val, n-1))
    
    # Ugh, Brute force is O(2^n) and will crash your laptop if size is too big!
    # So we cap the test size at 20 max just for the competitor proof.
    solve(W, wt, val, min(n, 20)) 
    
    return time.perf_counter() - start_time