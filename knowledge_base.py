"""
knowledge_base.py — Algorithm Knowledge Base grouped by paradigm and category.
"""

# --- SORTING PARADIGMS ---
BRUTE_FORCE_SORT = {
    "Bubble Sort": {
        "paradigm": "Brute Force",
        "time_best": "O(n)", "time_avg": "O(n²)", "time_worst": "O(n²)",
        "space": "O(1)",
        "description": "Simple comparison-based sorting that repeatedly swaps adjacent elements.",
        "pros": ["Simple to implement", "Stable", "In-place"],
        "cons": ["Extremely slow on large lists O(n²)", "High number of swaps"],
        "best_when": ["Small datasets (n < 50)", "Educational use"]
    },
    "Selection Sort": {
        "paradigm": "Brute Force",
        "time_best": "O(n²)", "time_avg": "O(n²)", "time_worst": "O(n²)",
        "space": "O(1)",
        "description": "Selects the smallest element from unsorted part and moves it to sorted part.",
        "pros": ["Minimizes swaps", "In-place", "Simple"],
        "cons": ["Always O(n²)", "Not stable"],
        "best_when": ["Swapping is very expensive", "Small datasets"]
    }
}

DECREASE_CONQUER_SORT = {
    "Insertion Sort": {
        "paradigm": "Decrease and Conquer",
        "time_best": "O(n)", "time_avg": "O(n²)", "time_worst": "O(n²)",
        "space": "O(1)",
        "description": "Builds the sorted list one item at a time by 'inserting' elements into position.",
        "pros": ["Adaptive (fast for sorted data)", "Stable", "In-place", "Very fast for small N"],
        "cons": ["O(n²) average case", "Not efficient for large N"],
        "best_when": ["Nearly sorted data", "Small datasets (n < 200)"]
    }
}

DIVIDE_CONQUER_SORT = {
    "Merge Sort": {
        "paradigm": "Divide and Conquer",
        "time_best": "O(n log n)", "time_avg": "O(n log n)", "time_worst": "O(n log n)",
        "space": "O(n)",
        "description": "Recursively splits array in half, sorts them, and merges them back together.",
        "pros": ["Stable", "Guaranteed O(n log n)", "Parallelizable"],
        "cons": ["Extra space O(n)", "Slower than Quick Sort in practice"],
        "best_when": ["Large datasets", "Stability is required", "Linked lists"]
    },
    "Quick Sort": {
        "paradigm": "Divide and Conquer",
        "time_best": "O(n log n)", "time_avg": "O(n log n)", "time_worst": "O(n²)",
        "space": "O(log n)",
        "description": "Picks a pivot, partitions array around it, and recurses.",
        "pros": ["Extremely fast in practice", "Cache-friendly", "In-place (log n stack)"],
        "cons": ["O(n²) worst case", "Not stable", "Recursive overhead"],
        "best_when": ["General purpose sorting", "Large random datasets"]
    }
}

# --- GREEDY METHOD ---
GREEDY_ALGORITHMS = {
    "Fractional Knapsack (Decimal)": {
        "paradigm": "Greedy Method",
        "time_best": "O(n log n)", "time_avg": "O(n log n)", "time_worst": "O(n log n)",
        "space": "O(1)",
        "description": "Items can be broken into smaller pieces to maximize profit for a given capacity.",
        "pros": ["Efficient calculation", "Guaranteed optimal for fractional case"],
        "cons": ["Only works if items can be divided", "Greedy choice only works here"],
        "best_when": ["Items are divisible (like gold dust, fluids)"]
    },
    "Prim's Algorithm": {
        "paradigm": "Greedy Method",
        "time_best": "O(E log V)", "time_avg": "O(E log V)", "time_worst": "O(E log V)",
        "space": "O(V)",
        "description": "Grows a Minimum Spanning Tree from a starting node by adding nearest neighbor.",
        "pros": ["Efficient for dense graphs", "Guaranteed optimal MST"],
        "cons": ["Requires adjacency matrix/list", "Higher complexity than Kruskal for sparse graphs"],
        "best_when": ["Dense graphs", "Starting from a specific node"]
    },
    "Kruskal's Algorithm": {
        "paradigm": "Greedy Method",
        "time_best": "O(E log E)", "time_avg": "O(E log E)", "time_worst": "O(E log E)",
        "space": "O(E + V)",
        "description": "Finds MST by sorting all edges and adding them if they don't form a cycle.",
        "pros": ["Better for sparse graphs", "Simple edge-based logic"],
        "cons": ["Requires edge sorting", "Cycle detection overhead"],
        "best_when": ["Sparse graphs", "Edges are already sorted"]
    },
    "Dijkstra's Algorithm": {
        "paradigm": "Greedy Method",
        "time_best": "O(V + E log V)", "time_avg": "O(V + E log V)", "time_worst": "O(V²)",
        "space": "O(V)",
        "description": "Finds shortest path from a single source to all other nodes in a weighted graph.",
        "pros": ["Efficient single-source pathfinding", "Widely used in GPS/Maps"],
        "cons": ["Doesn't handle negative weights", "Greedy choice can fail with negative edges"],
        "best_when": ["Single source shortest path", "Positive edge weights"]
    }
}

# --- DYNAMIC PROGRAMMING ---
DP_ALGORITHMS = {
    "Knapsack 0/1": {
        "paradigm": "Dynamic Programming",
        "time_best": "O(nW)", "time_avg": "O(nW)", "time_worst": "O(nW)",
        "space": "O(nW)",
        "description": "Finds max value of items in a bag with capacity W. Items cannot be broken.",
        "pros": ["Guarantees optimal solution for non-divisible items", "Avoids recomputing subproblems"],
        "cons": ["High memory usage (2D table)", "Pseudo-polynomial time"],
        "best_when": ["Discrete items", "Small weights/capacity"]
    },
    "Floyd Warshall": {
        "paradigm": "Dynamic Programming",
        "time_best": "O(V³)", "time_avg": "O(V³)", "time_worst": "O(V³)",
        "space": "O(V²)",
        "description": "Finds shortest paths between ALL pairs of vertices in a weighted graph.",
        "pros": ["Computes all-pairs shortest paths", "Handles negative weights (no negative cycles)"],
        "cons": ["O(V³) complexity is slow for large V", "O(V²) space for distance matrix"],
        "best_when": ["All-pairs shortest path", "Dense graphs", "Negative weights exist"]
    },
    "Multistage Graph": {
        "paradigm": "Dynamic Programming",
        "time_best": "O(V + E)", "time_avg": "O(V + E)", "time_worst": "O(V + E)",
        "space": "O(V)",
        "description": "Finds shortest path in a graph divided into stages/layers.",
        "pros": ["Very efficient for layered structures", "Optimal substructure property"],
        "cons": ["Only works on DAGs with clear stages", "Limited applicability"],
        "best_when": ["Pipeline processing", "Layered decision networks"]
    }
}

def get_algorithms(domain):
    """Returns a dictionary of all relevant algorithms for a given domain."""
    if domain == "ordering":
        # Return all sorting algorithms across paradigms
        combined = {}
        combined.update(BRUTE_FORCE_SORT)
        combined.update(DECREASE_CONQUER_SORT)
        combined.update(DIVIDE_CONQUER_SORT)
        return combined
    
    elif domain == "optimization":
        # For knapsack-style problems, we show both Greedy and DP variants
        return {
            "Fractional Knapsack (Decimal)": GREEDY_ALGORITHMS["Fractional Knapsack (Decimal)"],
            "Knapsack 0/1": DP_ALGORITHMS["Knapsack 0/1"]
        }
        
    elif domain == "pathfinding":
        # For shortest path problems, we show both Greedy (Dijkstra) and DP (Floyd)
        return {
            "Dijkstra's Algorithm": GREEDY_ALGORITHMS["Dijkstra's Algorithm"],
            "Floyd Warshall": DP_ALGORITHMS["Floyd Warshall"]
        }
        
    elif domain == "mst":
        # Minimum Spanning Tree problems
        return {
            "Prim's Algorithm": GREEDY_ALGORITHMS["Prim's Algorithm"],
            "Kruskal's Algorithm": GREEDY_ALGORITHMS["Kruskal's Algorithm"]
        }
        
    elif domain == "staged":
        # Multistage graph problems
        return {
            "Multistage Graph": DP_ALGORITHMS["Multistage Graph"]
        }
        
    return {}
