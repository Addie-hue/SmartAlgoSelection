"""
knowledge_base.py — Algorithm Knowledge Base grouped by paradigm.
For sorting: all 5 algorithms across 3 paradigms are shown together.
For DP: all 3 DP algorithms are shown together.
"""

SORTING_ALGORITHMS = {
    "Bubble Sort": {
        "paradigm": "Brute Force",
        "time_best": "O(n)", "time_avg": "O(n²)", "time_worst": "O(n²)",
        "space": "O(1)",
        "description": "Repeatedly swaps adjacent elements if they are in wrong order.",
        "pros": [
            "Very simple to implement and understand",
            "Stable sort (preserves relative order of equal elements)",
            "Best case O(n) when array is already sorted",
            "In-place — no extra memory needed",
        ],
        "cons": [
            "O(n²) average & worst — extremely slow for large inputs",
            "Too many swap operations compared to other algorithms",
            "Not suitable for large datasets",
            "Outperformed by Insertion Sort even on small inputs",
        ],
        "best_when": ["n < 50", "educational purposes", "data is already nearly sorted"],
    },
    "Selection Sort": {
        "paradigm": "Brute Force",
        "time_best": "O(n²)", "time_avg": "O(n²)", "time_worst": "O(n²)",
        "space": "O(1)",
        "description": "Finds the minimum element from unsorted part and puts it at the beginning.",
        "pros": [
            "Simple to implement",
            "In-place — no extra memory",
            "Minimizes number of swaps (O(n) swaps)",
            "Performs well with small lists",
        ],
        "cons": [
            "Always O(n²) — no best case improvement",
            "Not stable",
            "Slower than Insertion Sort on nearly sorted data",
            "No adaptivity — doesn't improve with partially sorted data",
        ],
        "best_when": ["n < 30", "memory writes are expensive", "educational purposes"],
    },
    "Insertion Sort": {
        "paradigm": "Decrease and Conquer",
        "time_best": "O(n)", "time_avg": "O(n²)", "time_worst": "O(n²)",
        "space": "O(1)",
        "description": "Builds sorted array one element at a time by inserting each into its correct position.",
        "pros": [
            "Best case O(n) for nearly sorted data",
            "Stable sort",
            "In-place — O(1) extra space",
            "Very efficient for small arrays",
            "Adaptive — fast when data is partially sorted",
        ],
        "cons": [
            "O(n²) worst case — poor for large random datasets",
            "Requires shifting elements, costly for arrays",
            "Not suitable when n > ~1000",
        ],
        "best_when": ["n < 100", "data is nearly sorted", "real-time streaming data"],
    },
    "Merge Sort": {
        "paradigm": "Divide and Conquer",
        "time_best": "O(n log n)", "time_avg": "O(n log n)", "time_worst": "O(n log n)",
        "space": "O(n)",
        "description": "Divides array in half, recursively sorts each half, then merges the sorted halves.",
        "pros": [
            "Guaranteed O(n log n) in ALL cases — very predictable",
            "Stable sort",
            "Excellent for linked lists",
            "Parallelizable — subarrays sorted independently",
        ],
        "cons": [
            "O(n) extra space — not in-place",
            "Slower than Quick Sort in practice due to overhead",
            "Not adaptive — doesn't benefit from partially sorted data",
            "Higher constant factors than Quick Sort",
        ],
        "best_when": ["stability required", "worst-case guarantee needed", "n > 1000"],
    },
    "Quick Sort": {
        "paradigm": "Divide and Conquer",
        "time_best": "O(n log n)", "time_avg": "O(n log n)", "time_worst": "O(n²)",
        "space": "O(log n)",
        "description": "Picks a pivot, partitions array so smaller elements are left and larger are right, recurses.",
        "pros": [
            "Fastest in practice — low constant factors",
            "In-place (O(log n) stack space)",
            "Cache-friendly due to sequential access",
            "Average case O(n log n) with good pivot",
        ],
        "cons": [
            "O(n²) worst case with bad pivot",
            "Not stable",
            "Recursive — can cause stack overflow",
            "Degrades on data with many duplicates",
        ],
        "best_when": ["general purpose sorting", "large random datasets", "n > 100"],
    },
}

DP_ALGORITHMS = {
    "Knapsack 0/1 (DP)": {
        "paradigm": "Dynamic Programming",
        "time_best": "O(nW)", "time_avg": "O(nW)", "time_worst": "O(nW)",
        "space": "O(nW)",
        "description": "Uses a 2D DP table to find max value achievable without exceeding weight capacity. Each item taken or not.",
        "pros": [
            "Guarantees optimal solution",
            "Pseudo-polynomial time in n and W",
            "Efficient for moderate n and W",
            "Can reconstruct which items to pick",
        ],
        "cons": [
            "O(nW) space can be huge if W is very large",
            "Pseudo-polynomial — not truly polynomial",
            "Cannot handle fractional items",
            "Slower than greedy for fractional variant",
        ],
        "best_when": ["items cannot be divided", "optimal solution required", "n × W fits in memory"],
    },
    "Floyd-Warshall": {
        "paradigm": "Dynamic Programming",
        "time_best": "O(V³)", "time_avg": "O(V³)", "time_worst": "O(V³)",
        "space": "O(V²)",
        "description": "Finds shortest paths between ALL pairs of vertices using 3 nested loops DP.",
        "pros": [
            "Finds shortest path between ALL pairs in one run",
            "Handles negative edge weights (no negative cycles)",
            "Very simple implementation — just 3 nested loops",
            "Can detect negative cycles",
        ],
        "cons": [
            "O(V³) time — very slow for large graphs",
            "O(V²) space for distance matrix",
            "Overkill for single-source shortest path",
            "Not suitable for V > 500",
        ],
        "best_when": ["all-pairs shortest path", "dense graphs", "negative weights", "V ≤ 500"],
    },
    "Multistage Graph (DP)": {
        "paradigm": "Dynamic Programming",
        "time_best": "O(V × E)", "time_avg": "O(V × E)", "time_worst": "O(V × E)",
        "space": "O(V)",
        "description": "Solves shortest path in a multistage graph using backward DP on stages.",
        "pros": [
            "Efficient for multistage/layered structures",
            "Guaranteed optimal source-to-sink path",
            "O(V) space — memory efficient",
            "Works well for pipeline/stage problems",
        ],
        "cons": [
            "Only works on multistage (DAG-like layered) graphs",
            "Cannot handle general graphs with cycles",
            "Requires knowing stage structure in advance",
            "Very specific — limited applicability",
        ],
        "best_when": ["graph has clear stages", "resource allocation", "pipeline optimization"],
    },
}


def get_algorithms(problem_domain):
    if problem_domain == "ordering":
        return SORTING_ALGORITHMS
    else:
        return DP_ALGORITHMS
