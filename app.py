"""
app.py - SmartAlgoSelection Backend
Analyzes problem statements, handles image OCR, benchmarks algorithms.
Uses extracted data from questions when available.
"""
from flask import Flask, render_template, request, jsonify
import random, time, warnings

import sort as sa
import dp
from analyzer import analyze_problem
from knowledge_base import get_algorithms

warnings.filterwarnings("ignore")
app = Flask(__name__)


# ═══ SAMPLE QUESTIONS ═════════════════════════════════════════════════════

SAMPLE_QUESTIONS = {
    "Sorting (Brute Force)": [
        "Arrange the numbers [34, 12, 5, 78, 23] from smallest to largest",
        "Put these 15 student marks in ascending order",
        "Order the elements [9, 1, 4, 7, 2, 8, 3, 6, 5] from low to high",
        "I have 25 random values, organize them in increasing sequence",
    ],
    "Sorting (Decrease & Conquer)": [
        "Organize these 120 employee IDs in ascending sequence",
        "Arrange 75 temperature readings from lowest to highest",
        "Put 150 exam scores in increasing order for the department",
        "Order 100 product prices from cheapest to most expensive",
    ],
    "Sorting (Divide & Conquer)": [
        "Arrange 5000 numbers from smallest to largest",
        "I need to organize 10000 records in ascending order efficiently",
        "Put 2500 sensor readings in sequence from low to high",
        "Order 8000 transaction amounts from smallest to largest",
    ],
    "Knapsack (DP)": [
        "Given items with weights = [2, 3, 4, 5] and values = [3, 4, 5, 6], capacity = 8, maximize value",
        "I have 20 items with different weights and profits, find the best combination within weight limit 150",
        "Pack a bag with capacity = 50 using items: weights = [10, 20, 30] values = [60, 100, 120]",
        "Select the best subset of 30 products to maximize profit without exceeding budget constraint of 500",
    ],
    "Shortest Path (DP)": [
        "Find minimum travel distance between every pair of 40 cities connected by roads",
        "Given a network of 25 locations, find the shortest route between all pairs",
        "Calculate minimum cost paths between all 15 nodes in this weighted network",
        "Find shortest distance between every pair of 50 vertices in a weighted graph",
    ],
    "Multistage Graph (DP)": [
        "Process 60 tasks through 4 pipeline stages to minimize total cost",
        "Find optimal path through a 5-stage network with 30 nodes",
        "Route data through a 3-level layered network of 45 nodes minimizing latency",
        "Allocate resources across 4 sequential phases with 20 decision points",
    ],
}


# ═══ BENCHMARK RUNNERS ════════════════════════════════════════════════════

def benchmark_sorting(size, extracted_array=None):
    if extracted_array:
        arr = extracted_array
        size = len(arr)
    else:
        arr = [random.randint(1, 10000) for _ in range(size)]

    preview_n = min(size, 20)
    preview = f"[{', '.join(str(x) for x in arr[:preview_n])}{'...' if size > preview_n else ''}]  ({size} elements)"
    using = "User-provided array" if extracted_array else "Randomly generated array"

    times = {
        "Bubble Sort":     sa.bubble_sort(arr),
        "Selection Sort":  sa.selection_sort(arr),
        "Insertion Sort":  sa.insertion_sort(arr),
        "Merge Sort":      sa.merge_sort(arr),
        "Quick Sort":      sa.quick_sort(arr),
    }
    return {"times": times, "preview": preview, "data_desc": f"{using} of size {size}"}


def benchmark_dp(size, knapsack_data=None, graph_data=None):
    results = {}

    # Knapsack
    if knapsack_data and 'weights' in knapsack_data and 'values' in knapsack_data:
        weights = knapsack_data['weights']
        values = knapsack_data['values']
        capacity = knapsack_data.get('capacity', sum(weights) // 2)
        cap_n = len(weights)
        ks_desc = f"User-provided: {cap_n} items, capacity={capacity}"
    else:
        cap_n = min(size, 500)
        weights = [random.randint(1, 50) for _ in range(cap_n)]
        values = [random.randint(10, 100) for _ in range(cap_n)]
        capacity = cap_n * 10
        ks_desc = f"Random: {cap_n} items, capacity={capacity}"
    results["Knapsack 0/1 (DP)"] = dp.knapsack_01(capacity, weights, values)

    # Floyd-Warshall
    if graph_data and 'matrix' in graph_data:
        graph = graph_data['matrix']
        v = len(graph)
        fw_desc = f"User-provided {v}x{v} matrix"
    else:
        v = min(size, 80)
        graph = [[random.randint(1, 100) if i != j else 0 for j in range(v)] for i in range(v)]
        fw_desc = f"Random {v}x{v} matrix"
    results["Floyd-Warshall"] = dp.floyd_warshall(graph)

    # Multistage Graph
    if graph_data and 'matrix' in graph_data:
        ms_graph = graph_data['matrix']
        ms = len(ms_graph)
    else:
        ms = min(size, 80)
        ms_graph = [[random.randint(1, 100) if i != j else float('inf') for j in range(ms)] for i in range(ms)]
    results["Multistage Graph (DP)"] = dp.multistage_graph(ms_graph, 4, ms)

    preview = f"Knapsack: {ks_desc} | Floyd: {fw_desc} | Multistage: {ms} nodes"
    return {"times": results, "preview": preview, "data_desc": f"DP problems benchmarked with size ~{size}"}


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
    paradigm = analysis["paradigm"]
    input_size = analysis["input_size"]
    extracted = analysis.get("extracted_data", {})

    algos = get_algorithms(domain)
    if not algos:
        return jsonify({"error": f"No algorithms found for domain: {domain}"}), 400

    # Benchmark using extracted data when available
    if domain == "ordering":
        bench = benchmark_sorting(input_size, extracted_array=extracted.get("array"))
    else:
        bench = benchmark_dp(input_size, knapsack_data=extracted.get("knapsack"), graph_data=extracted.get("graph"))

    times = bench["times"]
    best_name = min(times, key=times.get)
    best_time = times[best_name]

    algo_list = []
    for name, info in algos.items():
        is_best = (name == best_name)
        t = times.get(name)
        speedup = round(t / best_time, 2) if t and best_time and not is_best and best_time > 0 else None
        algo_list.append({
            "name": name, "paradigm": info["paradigm"],
            "time_best": info["time_best"], "time_avg": info["time_avg"],
            "time_worst": info["time_worst"], "space": info["space"],
            "description": info["description"], "pros": info["pros"],
            "cons": info["cons"], "best_when": info["best_when"],
            "actual_time": round(t, 8) if t else None,
            "is_best": is_best, "speedup_vs_best": speedup,
        })
    algo_list.sort(key=lambda x: (not x["is_best"], x["actual_time"] or float("inf")))

    best_info = algos[best_name]

    # Build extracted data summary for frontend
    extracted_summary = {}
    if extracted.get("array"):
        extracted_summary["array"] = extracted["array"]
    if extracted.get("knapsack"):
        extracted_summary["knapsack"] = extracted["knapsack"]
    if extracted.get("graph"):
        g = extracted["graph"]
        extracted_summary["graph"] = {k: v for k, v in g.items() if k != "matrix"}
        if "matrix" in g:
            extracted_summary["graph"]["matrix_size"] = f"{len(g['matrix'])}x{len(g['matrix'])}"

    return jsonify({
        "analysis": {
            "original_statement": analysis["original_statement"],
            "domain": domain, "paradigm": paradigm,
            "paradigm_reasoning": analysis["paradigm_reasoning"],
            "input_size": input_size, "size_source": analysis["size_source"],
            "matched_keywords": analysis["matched_keywords"],
            "extracted_data": extracted_summary,
        },
        "best_algorithm": {
            "name": best_name, "time": round(best_time, 8),
            "paradigm": best_info["paradigm"], "info": best_info,
        },
        "all_algorithms": algo_list,
        "benchmark": {"preview": bench["preview"], "data_desc": bench["data_desc"]},
    })


if __name__ == "__main__":
    app.run(debug=True)