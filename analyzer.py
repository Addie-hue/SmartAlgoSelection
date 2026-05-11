"""
analyzer.py - Smart Natural Language Problem Analyzer
Detects problem domain, paradigm, and extracts input data from text.
"""
import re

DOMAIN_KEYWORDS = {
    "ordering": [
        "arrange", "order", "ascending", "descending", "smallest to largest",
        "largest to smallest", "organize", "rank", "position", "sequence",
        "increasing", "decreasing", "rearrange", "list in order", "put in order",
        "low to high", "high to low", "sort", "sorted", "sorting", "marks", "scores",
    ],
    "optimization": [
        "maximize", "minimize", "optimal", "best combination", "select items",
        "capacity", "budget", "weight limit", "profit", "pack", "fill",
        "choose items", "pick items", "constraint", "limited space",
        "maximum value", "minimum cost", "best subset", "combination",
        "knapsack", "bag", "container", "load", "weight", "value", "decimal", "fractional",
        "optimization", "greedy", "dynamic programming", "dp",
    ],
    "pathfinding": [
        "shortest", "minimum distance", "route", "path between", "travel",
        "navigate", "cities", "locations", "network", "roads", "connections",
        "distance between", "all pairs", "every pair", "cost between",
        "floyd", "warshall", "dijkstra", "shortest path", "adjacency", "single source",
        "pathfinding", "graph traversal", "map", "gps", "fastest way",
    ],
    "mst": [
        "spanning tree", "minimum spanning", "connect all nodes", "least cost network",
        "prims", "kruskal", "mst", "minimum cost to connect", "wiring cost", "fiber optic layout",
        "electrical grid", "minimum connections",
    ],
    "staged": [
        "stages", "pipeline", "levels", "phases", "sequential",
        "multi-step", "multistage", "stage", "layered", "step by step",
        "process through", "resource allocation", "layered graph",
    ],
}

ORDERING_THRESHOLDS = {
    "Brute Force": (1, 50),
    "Decrease and Conquer": (51, 200),
    "Divide and Conquer": (201, 1000000),
}


def _normalize(text):
    return re.sub(r"\s+", " ", text.lower().strip())


def detect_domain(text):
    text = _normalize(text)
    
    # Priority Overrides
    if any(k in text for k in ["prims", "kruskal", "mst", "spanning tree", "connect all"]):
        return "mst", ["mst-override"], None
    if any(k in text for k in ["multistage", "layered graph", "stages"]):
        return "staged", ["staged-override"], None
    if any(k in text for k in ["knapsack", "weights", "values", "capacity"]):
        if any(k in text for k in ["fractional", "decimal", "break", "divide"]):
             return "optimization", ["knapsack-greedy"], None
        return "optimization", ["knapsack-dp"], None

    scores = {}
    matched = {}
    for domain, keywords in DOMAIN_KEYWORDS.items():
        hits = [k for k in keywords if k in text]
        scores[domain] = len(hits)
        matched[domain] = hits
    
    if not any(scores.values()):
        return None, [], "Please describe the problem clearly (e.g., sort these numbers, find the shortest route between cities)."
        
    best = max(scores, key=scores.get)
    return best, matched[best], None


def extract_input_size(text):
    text = _normalize(text)
    patterns = [
        r"n\s*[=:]\s*(\d+)",
        r"(\d+)\s+(?:elements?|numbers?|integers?|items?|values?|nodes?|vertices|cities|locations|rooms|scores|students|records|data)",
        r"(?:size|capacity|limit|total)\s*(?:of|is|=|:)?\s*(\d+)",
        r"(?:array|list|set|collection|group)\s+(?:of|with|containing)\s+(\d+)",
    ]
    for p in patterns:
        m = re.search(p, text)
        if m:
            size = int(m.group(1))
            if 1 <= size <= 1000000:
                return size, m.group(0)
    return None, None


def conclude_paradigm(domain, input_size, text):
    text_lower = _normalize(text)
    
    if domain == "ordering":
        for paradigm, (lo, hi) in ORDERING_THRESHOLDS.items():
            if lo <= input_size <= hi:
                reasons = {
                    "Brute Force": f"Input size {input_size} is small, making Brute Force (Bubble/Selection) efficient enough.",
                    "Decrease and Conquer": f"Input size {input_size} is moderate; Decrease and Conquer (Insertion) works well here.",
                    "Divide and Conquer": f"Input size {input_size} is large; log-linear Divide and Conquer is required.",
                }
                return paradigm, reasons[paradigm]
        return "Divide and Conquer", "Large input size defaults to Divide and Conquer for optimal performance."
    
    if domain == "optimization":
        if any(k in text_lower for k in ["decimal", "fractional", "greedy"]):
            return "Greedy Method", "Fractional selection allows for a Greedy approach to reach optimality."
        return "Dynamic Programming", "Discrete decisions (0/1 Knapsack) require Dynamic Programming for global optimality."
            
    if domain == "pathfinding":
        if any(k in text_lower for k in ["floyd", "warshall", "all pairs", "every pair", "reachability"]):
            return "Dynamic Programming", "All-pairs shortest path analysis requires Dynamic Programming (Floyd-Warshall)."
        return "Greedy Method", "Single-source shortest path is best solved using a Greedy approach (Dijkstra)."
            
    if domain == "mst":
        return "Greedy Method", "Minimum Spanning Tree construction is a classic Greedy problem (Prim/Kruskal)."
        
    if domain == "staged":
        return "Dynamic Programming", "Multistage graphs are solved optimally using Dynamic Programming layers."
        
    return "Dynamic Programming", "Complex constraints detected; applying Dynamic Programming logic."


def extract_array(text):
    # Match [1, 2, 3] or similar
    match = re.search(r"\[([\d\s,.]+)\]", text)
    if match:
        try:
            return [float(x.strip()) for x in match.group(1).split(",") if x.strip()]
        except: pass
    
    # Match strings of numbers like "marks: 10, 20, 30"
    num_list_match = re.search(r"(?:marks|scores|numbers|values|array|list|is|are)[:\s]+([\d\s,.]+)", text, re.I)
    if num_list_match:
        try:
            raw = num_list_match.group(1)
            nums = re.findall(r"\d+(?:\.\d+)?", raw)
            if len(nums) > 2:
                return [float(x) for x in nums]
        except: pass

    return None

def extract_knapsack_data(text):
    data = {}
    cap_match = re.search(r"(?:capacity|limit|bag|weight limit)\s*(?:is|=|:)?\s*(\d+)", text, re.I)
    if cap_match: data['capacity'] = int(cap_match.group(1))
    
    # "weights = [2, 3, 4]" or "weights: 2, 3, 4"
    w_match = re.search(r"weights?\s*[=:]?\s*\[?([\d\s,.]+)\]?", text, re.I)
    if w_match:
        nums = re.findall(r"\d+(?:\.\d+)?", w_match.group(1))
        if nums: data['weights'] = [float(x) for x in nums]
    
    v_match = re.search(r"values?\s*[=:]?\s*\[?([\d\s,.]+)\]?", text, re.I)
    if v_match:
        nums = re.findall(r"\d+(?:\.\d+)?", v_match.group(1))
        if nums: data['values'] = [float(x) for x in nums]
    
    return data if 'weights' in data or 'values' in data or 'capacity' in data else None

def extract_graph_data(text):
    # Try to find edges like "A-B: 5", "A to B = 10", "(A, B, 5)"
    edge_patterns = [
        r"([a-zA-Z\d]+)\s*(?:-|->|to)\s*([a-zA-Z\d]+)\s*(?:[:=]|\s+is\s+|\s+cost\s+)\s*(\d+(?:\.\d+)?)",
        r"[\(\[]\s*([a-zA-Z\d]+)\s*[,: ]\s*([a-zA-Z\d]+)\s*[,: ]\s*(\d+(?:\.\d+)?)\s*[\)\]]",
    ]
    
    edges = []
    seen = set()
    for p in edge_patterns:
        matches = re.findall(p, text)
        for u, v, w in matches:
            u, v, w = u.upper(), v.upper(), float(w)
            if (u, v, w) not in seen:
                edges.append((u, v, w))
                seen.add((u, v, w))
    
    if not edges: return None
    
    # Convert to matrix
    nodes = sorted(list(set([e[0] for e in edges] + [e[1] for e in edges])))
    node_map = {node: i for i, node in enumerate(nodes)}
    n = len(nodes)
    matrix = [[None] * n for _ in range(n)]
    for i in range(n): matrix[i][i] = 0
    
    for u, v, w in edges:
        ui, vi = node_map[u], node_map[v]
        matrix[ui][vi] = w
        # Assume undirected unless specified
        if "directed" not in text.lower():
            matrix[vi][ui] = w
            
    return {"matrix": matrix, "nodes": nodes}

def analyze_problem(statement):
    domain, keywords, error = detect_domain(statement)
    if error:
        return {"error": error}
    
    extracted_data = {
        "array": extract_array(statement),
        "knapsack": extract_knapsack_data(statement),
        "graph": extract_graph_data(statement)
    }

    input_size, size_source = extract_input_size(statement)
    if not input_size:
        if extracted_data["array"]:
            input_size = len(extracted_data["array"])
            size_source = "length of detected array"
        elif extracted_data["knapsack"] and "weights" in extracted_data["knapsack"]:
            input_size = len(extracted_data["knapsack"]["weights"])
            size_source = "count of knapsack items"
        elif extracted_data["graph"] and "nodes" in extracted_data["graph"]:
            input_size = len(extracted_data["graph"]["nodes"])
            size_source = "count of graph nodes"
        else:
            defaults = {"ordering": 100, "optimization": 20, "pathfinding": 30, "mst": 25, "staged": 15}
            input_size = defaults.get(domain, 50)
            size_source = "estimated based on problem type"
        
    paradigm, reasoning = conclude_paradigm(domain, input_size, statement)
    
    is_all_pairs = any(k in statement.lower() for k in ["all pairs", "every pair", "floyd", "warshall", "reachability"])
    
    justifications = {
        "ordering": "Analysis focuses on data arrangement efficiency. We compare various sorting paradigms based on your input size.",
        "optimization": "This is a resource allocation/selection problem. We compare Greedy vs Dynamic Programming based on constraint types.",
        "pathfinding": "This is a network routing problem. We apply the best pathfinding algorithms for the detected network scale.",
        "mst": "This problem seeks the minimum cost to connect a network. We apply Greedy algorithms like Prim's and Kruskal's.",
        "staged": "This problem involves sequential decision stages, best solved using Dynamic Programming."
    }
    
    return {
        "original_statement": statement,
        "domain": domain,
        "paradigm": paradigm,
        "paradigm_reasoning": reasoning,
        "selection_justification": justifications.get(domain, "AI analyzed the text and selected the best algorithm group."),
        "input_size": input_size,
        "size_source": size_source,
        "matched_keywords": keywords,
        "is_all_pairs": is_all_pairs,
        "extracted_data": extracted_data,
        "error": None,
    }
