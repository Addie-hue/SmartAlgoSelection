"""
app.py — SmartAlgoSelection Backend
Updated to handle Greedy Method and specific algorithm mappings.
"""
from flask import Flask, render_template, request, jsonify
import random
import time
import warnings

import sort as sa
import dp
import greedy as gr
from analyzer import analyze_problem
from knowledge_base import get_algorithms

warnings.filterwarnings("ignore")
app = Flask(__name__)


# ═══ BENCHMARK RUNNERS ═══════════════════════════════════════════════════

def benchmark_sorting(size, data=None):
    if data and data.get('array'):
        arr = data['array']
        size = len(arr)
        preview_desc = "User-provided array"
    else:
        arr = [random.randint(1, 10000) for _ in range(size)]
        preview_desc = f"Random integer array of size {size}"
        
    preview_n = min(size, 15)
    preview = f"[{', '.join(str(x) for x in arr[:preview_n])}{'...' if size > preview_n else ''}]  ({size} elements)"
    times = {
        "Bubble Sort":     sa.bubble_sort(arr),
        "Selection Sort":  sa.selection_sort(arr),
        "Insertion Sort":  sa.insertion_sort(arr),
        "Merge Sort":      sa.merge_sort(arr),
        "Quick Sort":      sa.quick_sort(arr),
    }
    return {"times": times, "preview": preview, "data_desc": preview_desc}


def benchmark_knapsack(size, data=None):
    ks = data.get('knapsack') if data else None
    if ks and ks.get('weights') and ks.get('values'):
        wt = ks['weights']
        val = ks['values']
        W = ks.get('capacity', int(sum(wt) * 0.6))
        size = len(wt)
        preview_desc = "User-provided knapsack items"
    else:
        wt = [random.randint(1, 50) for _ in range(size)]
        val = [random.randint(10, 100) for _ in range(size)]
        W = size * 10
        preview_desc = f"Knapsack problem with {size} random items"
    
    # Convert weights/capacity to int for 0/1 DP (required for table indexing)
    wt_int = [int(w) for w in wt]
    W_int = int(W)
    
    times = {
        "Fractional Knapsack (Decimal)": gr.fractional_knapsack(W, wt, val),
        "Knapsack 0/1": dp.knapsack_01(W_int, wt_int, val)
    }
    preview = f"Weights: {wt[:5]}..., Values: {val[:5]}..., Capacity: {W}"
    return {"times": times, "preview": preview, "data_desc": preview_desc}


def benchmark_shortest_path(size, is_all_pairs=False, data=None):
    gr_data = data.get('graph') if data else None
    if gr_data and gr_data.get('matrix'):
        graph = gr_data['matrix']
        V = len(graph)
        preview_desc = "User-provided adjacency matrix"
    else:
        V = min(size, 100)
        graph = [[random.randint(1, 100) if i != j else 0 for j in range(V)] for i in range(V)]
        preview_desc = f"Weighted graph with {V} random vertices"
    
    if is_all_pairs:
        start = time.perf_counter()
        for i in range(V):
            gr.dijkstra_algo(graph, i)
        dijkstra_time = time.perf_counter() - start
    else:
        dijkstra_time = gr.dijkstra_algo(graph, 0)

    times = {
        "Dijkstra's Algorithm": dijkstra_time,
        "Floyd Warshall": dp.floyd_warshall(graph)
    }
    preview = f"Adjacency Matrix ({V}x{V}) for {'All-Pairs' if is_all_pairs else 'Single-Source'} shortest path"
    return {"times": times, "preview": preview, "data_desc": preview_desc}


def benchmark_mst(size, data=None):
    gr_data = data.get('graph') if data else None
    if gr_data and gr_data.get('matrix'):
        graph = gr_data['matrix']
        V = len(graph)
        preview_desc = "User-provided adjacency matrix"
    else:
        V = min(size, 100)
        graph = [[random.randint(1, 100) if i != j else 0 for j in range(V)] for i in range(V)]
        preview_desc = f"Graph with {V} random vertices"
    
    times = {
        "Prim's Algorithm": gr.prims_algo(graph),
        "Kruskal's Algorithm": gr.kruskals_algo(graph)
    }
    preview = f"Adjacency Matrix ({V}x{V}) for Minimum Spanning Tree"
    return {"times": times, "preview": preview, "data_desc": preview_desc}


def benchmark_staged(size, data=None):
    gr_data = data.get('graph') if data else None
    if gr_data and gr_data.get('matrix'):
        graph = gr_data['matrix']
        V = len(graph)
        preview_desc = "User-provided layered graph"
    else:
        V = min(size, 80)
        graph = [[random.randint(1, 100) if i != j else float('inf') for j in range(V)] for i in range(V)]
        preview_desc = f"Layered graph with {V} random nodes"
    
    times = {
        "Multistage Graph": dp.multistage_graph(graph, 4, V)
    }
    preview = f"Multistage decision layers with {V} total nodes"
    return {"times": times, "preview": preview, "data_desc": preview_desc}


# ═══ SAMPLE QUESTIONS ═════════════════════════════════════════════════════

SAMPLE_QUESTIONS = {
    "BRUTE FORCE (Sorting)": [
        "OVERALL: Compare all sorting algorithms on a list of 25 numbers",
        "BUBBLE SORT: Arrange the numbers [34, 12, 5, 78, 23, 45, 11] in increasing order",
        "SELECTION SORT: Put these 15 student marks [85, 92, 70, 65, 88, 95...] in ascending order"
    ],
    "DECREASE AND CONQUER": [
        "INSERTION SORT: Order 100 employee records from lowest to highest salary"
    ],
    "DIVIDE AND CONQUER": [
        "OVERALL: Benchmark large-scale sorting on 5000 random values",
        "MERGE SORT: Organize 2000 sensor readings efficiently",
        "QUICK SORT: Arrange a list of 1500 coordinates by their X-value"
    ],
    "GREEDY METHOD (Optimization & Paths)": [
        "OVERALL (Shortest Path): Compare Single-Source pathfinding algorithms for 50 nodes",
        "OVERALL (MST): Compare Prim's vs Kruskal's for a 30-node computer network",
        "KNAPSACK (DECIMAL): Optimize a bag with capacity 50 using fractional selection",
        "PRIMS ALGO: Find the minimum cost wiring for a new office layout with 15 nodes",
        "KRUSKAL ALGO: Connect 20 cities into a single network with minimum total distance",
        "DIJKSTRA'S: Find the fastest single-source route through 40 intersections"
    ],
    "DYNAMIC PROGRAMMING": [
        "OVERALL: Compare DP vs Greedy for optimization problems",
        "KNAPSACK 0/1: Best subset of 20 items (cannot be broken). Weights=[2,5,10...], Values=[3,6,12...], Cap=50",
        "FLOYD WARSHALL: Calculate all-pairs shortest paths for every city in a 20-node network",
        "MULTISTAGE GRAPH: Find the shortest path through 5 stages of a 40-node pipeline network"
    ]
}

# ═══ ROUTES ═══════════════════════════════════════════════════════════════

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/sample-questions")
def sample_questions():
    return jsonify(SAMPLE_QUESTIONS)


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    statement = data.get("statement", "").strip()
    if not statement:
        return jsonify({"error": "Please enter a problem statement."}), 400

    analysis = analyze_problem(statement)
    if analysis.get("error"):
        return jsonify({"error": analysis["error"]}), 400

    domain = analysis["domain"]
    input_size = analysis["input_size"]

    # Dispatch to relevant benchmark group
    ex_data = analysis.get("extracted_data")
    if domain == "ordering":
        bench = benchmark_sorting(input_size, ex_data)
    elif domain == "optimization":
        bench = benchmark_knapsack(input_size, ex_data)
    elif domain == "pathfinding":
        bench = benchmark_shortest_path(input_size, analysis.get("is_all_pairs", False), ex_data)
    elif domain == "mst":
        bench = benchmark_mst(input_size, ex_data)
    elif domain == "staged":
        bench = benchmark_staged(input_size, ex_data)
    else:
        return jsonify({"error": "No benchmark available for this domain."}), 400

    algos_data = get_algorithms(domain)
    times = bench["times"]
    
    # Identify the best (fastest) algorithm in the group
    best_name = min(times, key=times.get)
    best_time = times[best_name]

    # Build algorithm details for display
    algo_list = []
    for name, info in algos_data.items():
        t = times.get(name)
        if t is None: continue
        
        is_best = (name == best_name)
        speedup = round(t / best_time, 2) if t and best_time and not is_best and best_time > 0 else None
        
        algo_list.append({
            "name": name,
            "paradigm": info["paradigm"],
            "time_best": info["time_best"],
            "time_avg": info["time_avg"],
            "time_worst": info["time_worst"],
            "space": info["space"],
            "description": info["description"],
            "pros": info["pros"],
            "cons": info["cons"],
            "best_when": info["best_when"],
            "actual_time": round(t, 8),
            "is_best": is_best,
            "speedup_vs_best": speedup,
        })

    # Sort so best is at top
    algo_list.sort(key=lambda x: (not x["is_best"], x["actual_time"]))

    best_info = algos_data[best_name]
    
    return jsonify({
        "analysis": {
            "original_statement": analysis["original_statement"],
            "domain": domain,
            "paradigm": analysis["paradigm"],
            "paradigm_reasoning": analysis["paradigm_reasoning"],
            "selection_justification": analysis["selection_justification"], # Justification for choosing these algos
            "input_size": input_size,
            "size_source": analysis["size_source"],
            "matched_keywords": analysis["matched_keywords"],
            "extracted_data": ex_data
        },
        "best_algorithm": {
            "name": best_name,
            "time": round(best_time, 8),
            "paradigm": best_info["paradigm"],
            "info": best_info,
        },
        "all_algorithms": algo_list,
        "benchmark": {
            "preview": bench["preview"],
            "data_desc": bench["data_desc"],
        },
    })


if __name__ == "__main__":
    app.run(debug=True)