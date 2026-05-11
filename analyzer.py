"""
analyzer.py - NLP Problem Statement Analyzer
Detects problem domain, paradigm, and provides justification.
"""
import re

DOMAIN_KEYWORDS = {
    "ordering": [
        "arrange", "order", "ascending", "descending", "smallest to largest",
        "largest to smallest", "organize", "rank", "position", "sequence",
        "increasing", "decreasing", "rearrange", "list in order", "put in order",
        "low to high", "high to low", "sort", "sorted", "sorting",
    ],
    "optimization": [
        "maximize", "minimize", "optimal", "best combination", "select items",
        "capacity", "budget", "weight limit", "profit", "pack", "fill",
        "choose items", "pick items", "constraint", "limited space",
        "maximum value", "minimum cost", "best subset", "combination",
        "knapsack", "bag", "container", "load", "weight", "value", "decimal", "fractional",
        "optimization", "optimization problem", "greedy", "dynamic programming", "dp",
    ],
    "pathfinding": [
        "shortest", "minimum distance", "route", "path between", "travel",
        "navigate", "cities", "locations", "network", "roads", "connections",
        "distance between", "all pairs", "every pair", "cost between",
        "floyd", "warshall", "dijkstra", "shortest path", "adjacency", "single source",
        "pathfinding", "graph traversal",
    ],
    "mst": [
        "spanning tree", "minimum spanning", "connect all nodes", "least cost network",
        "prims", "kruskal", "mst", "minimum cost to connect", "wiring cost", "fiber optic layout",
    ],
    "staged": [
        "stages", "pipeline", "levels", "phases", "sequential",
        "multi-step", "multistage", "stage", "layered", "step by step",
        "process through", "resource allocation",
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
    
    # Priority 0: Explicit Architect Data
    if "graph connections:" in text or "(source, destination, weight)" in text:
        if any(k in text for k in ["mst", "spanning", "connect", "kruskal", "prim", "roads", "cities"]):
            return "mst", ["graph", "mst"], None
        if any(k in text for k in ["staged", "multistage"]):
            return "staged", ["graph", "multistage"], None
        return "pathfinding", ["graph", "pathfinding"], None
        
    # Priority 1: Overrides
    if any(k in text for k in ["prims", "kruskal", "mst", "spanning tree", "connect all"]):
        return "mst", ["mst-override"], None
    if any(k in text for k in ["multistage", "layered graph", "stages"]):
        return "staged", ["staged-override"], None

    scores = {}
    matched = {}
    for domain, keywords in DOMAIN_KEYWORDS.items():
        hits = [k for k in keywords if k in text]
        scores[domain] = len(hits)
        matched[domain] = hits
    
    if not any(scores.values()):
        return None, [], "Please describe the problem (e.g., sort numbers, find MST, knapsack)."
        
    best = max(scores, key=scores.get)
    return best, matched[best], None


def extract_input_size(text):
    text = _normalize(text)
    # Improved size extraction
    patterns = [
        r"n\s*[=:]\s*(\d+)",
        r"(\d+)\s+(?:elements?|numbers?|integers?|items?|values?|nodes?|vertices|cities|locations|rooms|scores|students|data)",
        r"(?:size|capacity|limit)\s*(?:of|is|=|:)?\s*(\d+)",
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
                    "Brute Force": f"Input size {input_size} is small, allowing simple Brute Force comparisons.",
                    "Decrease and Conquer": f"Input size {input_size} is moderate; Decrease and Conquer (Insertion) is efficient here.",
                    "Divide and Conquer": f"Input size {input_size} is large; Divide and Conquer is necessary for log-linear efficiency.",
                }
                return paradigm, reasons[paradigm]
        return "Divide and Conquer", "Large input size defaults to Divide and Conquer."
    
    if domain == "optimization":
        if "decimal" in text_lower or "fractional" in text_lower or "greedy" in text_lower:
            return "Greedy Method", "Problem involves fractional selection or greedy optimization heuristics."
        else:
            return "Dynamic Programming", "Discrete decisions (Knapsack 0/1) require Dynamic Programming for global optimality."
            
    if domain == "pathfinding":
        if any(k in text_lower for k in ["floyd", "warshall", "all pairs", "every pair"]):
            return "Dynamic Programming", "All-pairs shortest path requirement identified. Floyd-Warshall (DP) is the standard solution."
        else:
            return "Greedy Method", "Single-source shortest path identified. Dijkstra (Greedy) is optimal for this scenario."
            
    if domain == "mst":
        return "Greedy Method", "Minimum Spanning Tree construction identified. Prim and Kruskal (Greedy) are the primary solutions."
        
    if domain == "staged":
        return "Dynamic Programming", "Multistage graph detected. This problem exhibits optimal substructure solved via DP."
        
    return "Dynamic Programming", "Complex constraints detected; applying Dynamic Programming."


def extract_array(text):
    # Look for [1, 2, 3] or 1, 2, 3
    match = re.search(r"\[([\d\s,.]+)\]", text)
    if match:
        try:
            return [float(x.strip()) for x in match.group(1).split(",") if x.strip()]
        except: pass
    
    # Try comma separated numbers if no brackets
    nums = re.findall(r"\b\d+(?:\.\d+)?\b", text)
    if len(nums) > 3: # Avoid catching lone numbers like 'size 10'
        return [float(x) for x in nums]
    return None

def extract_knapsack_data(text):
    data = {}
    # Capacity
    cap_match = re.search(r"(?:capacity|limit|bag|weight limit)\s*(?:is|=|:)?\s*(\d+)", text, re.I)
    if cap_match: data['capacity'] = int(cap_match.group(1))
    
    # Weights/Values usually in pairs or arrays
    # "weights = [2, 3, 4]"
    w_match = re.search(r"weights?\s*[=:]\s*\[([\d\s,.]+)\]", text, re.I)
    if w_match: data['weights'] = [float(x.strip()) for x in w_match.group(1).split(",") if x.strip()]
    
    v_match = re.search(r"values?\s*[=:]\s*\[([\d\s,.]+)\]", text, re.I)
    if v_match: data['values'] = [float(x.strip()) for x in v_match.group(1).split(",") if x.strip()]
    
    return data if data else None

def extract_edges(text):
    # Strip out UI headers and noise
    clean_text = re.sub(r"-{3,}.*?-{3,}", "", text, flags=re.DOTALL)
    
    # Standard Architect Format: (A, B, 5)
    matches = re.findall(r"[\(\[]\s*([a-zA-Z\d]+)\s*[,: ]\s*([a-zA-Z\d]+)\s*[,: ]\s*(\d+(?:\.\d+)?)\s*[\)\]]", clean_text)
    
    # Fallback Format: A-B: 5 or A->B=5
    matches2 = re.findall(r"\b([a-zA-Z\d]+)\s*(?:-|->|to)\s*([a-zA-Z\d]+)\s*(?:[:=]|\s+is\s+|\s*\(?)\s*(\d+(?:\.\d+)?)\)?", clean_text)
    
    edges = []
    seen = set()
    for u, v, w in (matches + matches2):
        pair = tuple(sorted([u.upper(), v.upper()]))
        if (u.upper(), v.upper(), float(w)) not in seen:
            edges.append((u.upper(), v.upper(), float(w)))
            seen.add((u.upper(), v.upper(), float(w)))
            
    return edges

def edges_to_matrix(edges):
    if not edges: return None
    # Find all unique nodes
    nodes = set()
    for u, v, w in edges:
        nodes.add(u); nodes.add(v)
    
    sorted_nodes = sorted(list(nodes))
    node_map = {node: i for i, node in enumerate(sorted_nodes)}
    n = len(sorted_nodes)
    
    matrix = [[float('inf')] * n for _ in range(n)]
    for i in range(n): matrix[i][i] = 0
    
    for u, v, w in edges:
        ui, vi = node_map[u], node_map[v]
        matrix[ui][vi] = w
        matrix[vi][ui] = w # Assuming undirected for MST/general
        
    return {"matrix": matrix, "nodes": sorted_nodes}

def extract_graph_data(text):
    # 1. Check for existing matrix structure
    matrix_match = re.search(r"\[\s*(\[[\d\s,.]+\](?:\s*,\s*\[[\d\s,.]+\])*)\s*\]", text)
    if matrix_match:
        try:
            rows = re.findall(r"\[([\d\s,.]+)\]", matrix_match.group(1))
            matrix = []
            for r in rows:
                matrix.append([float(x.strip()) for x in r.split(",") if x.strip()])
            return {"matrix": matrix}
        except: pass
    
    # 2. Try inferring from edges
    edges = extract_edges(text)
    if edges:
        return edges_to_matrix(edges)
        
    return None

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
        # If we have an array, its length is the size
        if extracted_data["array"]:
            input_size = len(extracted_data["array"])
            size_source = "extracted array length"
        elif extracted_data["knapsack"] and "weights" in extracted_data["knapsack"]:
            input_size = len(extracted_data["knapsack"]["weights"])
            size_source = "extracted knapsack items count"
        else:
            # Defaults based on domain if not found
            defaults = {"ordering": 100, "optimization": 20, "pathfinding": 30, "mst": 25, "staged": 15}
            input_size = defaults.get(domain, 50)
            size_source = f"estimated from domain: {domain}"
        
    paradigm, reasoning = conclude_paradigm(domain, input_size, statement)
    
    # Justification for why these algorithms were chosen
    text_lower = statement.lower()
    is_all_pairs = any(k in text_lower for k in ["all pairs", "every pair", "floyd", "warshall", "transitive closure", "reachability"])
    
    justifications = {
        "ordering": "This problem involves sorting or arranging data. We apply Brute Force, Decrease & Conquer, and Divide & Conquer to compare efficiency across different input sizes.",
        "optimization": "This is a resource allocation problem (Knapsack). We compare the Greedy Method (Fractional) vs Dynamic Programming (0/1) based on item divisibility.",
        "pathfinding": f"This is a network routing problem ({'All-Pairs' if is_all_pairs else 'Single-Source'}). We apply Dijkstra (Greedy) and Floyd-Warshall (DP) to compare their efficiency for this specific graph scale.",
        "mst": "This problem seeks the minimum cost to connect all nodes. We apply Greedy algorithms (Prim's and Kruskal's) to find the Minimum Spanning Tree.",
        "staged": "This problem has sequential decision stages. Dynamic Programming is chosen to solve the shortest path through layered nodes."
    }
    
    return {
        "original_statement": statement,
        "domain": domain,
        "paradigm": paradigm,
        "paradigm_reasoning": reasoning,
        "selection_justification": justifications.get(domain, "AI analyzed the problem constraints and selected the best algorithm group."),
        "input_size": input_size,
        "size_source": size_source,
        "matched_keywords": keywords,
        "is_all_pairs": is_all_pairs,
        "extracted_data": extracted_data,
        "error": None,
    }
