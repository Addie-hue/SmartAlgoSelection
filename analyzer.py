"""
analyzer.py - NLP Problem Statement Analyzer
Detects problem domain, paradigm, AND extracts specific inputs from the question.
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
        "knapsack", "bag", "container", "load", "weight", "value",
    ],
    "pathfinding": [
        "shortest", "minimum distance", "route", "path between", "travel",
        "navigate", "cities", "locations", "network", "roads", "connections",
        "distance between", "all pairs", "every pair", "cost between",
        "floyd", "warshall", "dijkstra", "shortest path", "adjacency",
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
    scores = {}
    matched = {}
    for domain, keywords in DOMAIN_KEYWORDS.items():
        hits = [k for k in keywords if k in text]
        scores[domain] = len(hits)
        matched[domain] = hits
    best = max(scores, key=scores.get) if scores else None
    if not best or scores[best] == 0:
        return None, [], "Could not detect problem domain. Describe the problem more clearly (e.g., arrange numbers, find shortest path, maximize value with weight limit)."
    return best, matched[best], None


def extract_input_size(text):
    text = _normalize(text)
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


def extract_array(text):
    """Extract an explicit array from the question, e.g. [5, 3, 8, 1] or {5,3,8,1}."""
    # Match [1, 2, 3] or {1, 2, 3} or (1, 2, 3)
    m = re.search(r'[\[({]([\d\s,]+)[\])}]', text)
    if m:
        nums = re.findall(r'\d+', m.group(1))
        if len(nums) >= 2:
            return [int(n) for n in nums]
    # Match comma-separated: "numbers: 5, 3, 8, 1, 9"
    m = re.search(r'(?:numbers|elements|array|list|data|values)[:\s]+((?:\d+[\s,]+){2,}\d+)', _normalize(text))
    if m:
        nums = re.findall(r'\d+', m.group(1))
        if len(nums) >= 2:
            return [int(n) for n in nums]
    return None


def extract_knapsack_data(text):
    """Extract weights, values, and capacity from knapsack problem descriptions."""
    text_lower = _normalize(text)
    data = {}

    # Extract weights: weights = [10, 20, 30] or w = [10, 20, 30]
    w_match = re.search(r'(?:weights?|w)\s*[=:]\s*[\[({]([\d\s,]+)[\])}]', text_lower)
    if w_match:
        data['weights'] = [int(n) for n in re.findall(r'\d+', w_match.group(1))]

    # Extract values/profits: values = [60, 100, 120] or v = [60, 100, 120] or profits = [...]
    v_match = re.search(r'(?:values?|profits?|v|p)\s*[=:]\s*[\[({]([\d\s,]+)[\])}]', text_lower)
    if v_match:
        data['values'] = [int(n) for n in re.findall(r'\d+', v_match.group(1))]

    # Extract capacity: capacity = 50 or W = 50 or cap = 50 or weight limit 50
    c_match = re.search(r'(?:capacity|cap|weight\s*limit|w|max\s*weight)\s*[=:]\s*(\d+)', text_lower)
    if c_match:
        data['capacity'] = int(c_match.group(1))

    return data if data else None


def extract_graph_data(text):
    """Extract graph edges or adjacency matrix from the question."""
    text_lower = _normalize(text)
    data = {}

    # Extract number of nodes/vertices
    n_match = re.search(r'(\d+)\s+(?:nodes?|vertices|vertex|cities|locations)', text_lower)
    if n_match:
        data['nodes'] = int(n_match.group(1))

    # Extract edges: (1,2,5), (2,3,3) or 1->2:5, 2->3:3
    edges = re.findall(r'[\(]([\d]+)\s*[,\s]\s*([\d]+)\s*[,\s]\s*([\d]+)[\)]', text)
    if edges:
        data['edges'] = [(int(a), int(b), int(w)) for a, b, w in edges]

    # Extract adjacency matrix rows: [0, 5, inf, 10]
    matrix_rows = re.findall(r'[\[({]([\d\s,infinf]+)[\])}]', text_lower)
    if len(matrix_rows) >= 2:
        matrix = []
        for row in matrix_rows:
            vals = []
            for v in re.split(r'[,\s]+', row.strip()):
                if v in ('inf', 'infinity', '∞', '-'):
                    vals.append(float('inf'))
                elif v.isdigit():
                    vals.append(int(v))
            if vals:
                matrix.append(vals)
        if len(matrix) >= 2 and all(len(r) == len(matrix[0]) for r in matrix):
            data['matrix'] = matrix

    return data if data else None


def conclude_paradigm(domain, input_size):
    if domain in ("optimization", "pathfinding", "staged"):
        labels = {"optimization": "optimal selection under constraints",
                  "pathfinding": "shortest paths", "staged": "staged/layered decisions"}
        return "Dynamic Programming", f"Problems involving {labels[domain]} require Dynamic Programming for efficient solutions."
    if domain == "ordering":
        for paradigm, (lo, hi) in ORDERING_THRESHOLDS.items():
            if lo <= input_size <= hi:
                reasons = {
                    "Brute Force": f"Input size {input_size} is small (<=50), making simple Brute Force approaches efficient enough.",
                    "Decrease and Conquer": f"Input size {input_size} is moderate (51-200), where Decrease and Conquer provides a good balance.",
                    "Divide and Conquer": f"Input size {input_size} is large (>200), requiring efficient Divide and Conquer strategies.",
                }
                return paradigm, reasons[paradigm]
        return "Divide and Conquer", "Large input size defaults to Divide and Conquer."
    return None, "Could not determine paradigm."


def analyze_problem(statement):
    domain, keywords, error = detect_domain(statement)
    if error:
        return {"error": error}

    # Extract specific data from the question
    arr = extract_array(statement)
    knapsack_data = extract_knapsack_data(statement)
    graph_data = extract_graph_data(statement)

    # Determine input size: from extracted data first, then from text, then default
    input_size = None
    size_source = None

    if arr:
        input_size = len(arr)
        size_source = f"extracted array of {len(arr)} elements"
    elif knapsack_data and 'weights' in knapsack_data:
        input_size = len(knapsack_data['weights'])
        size_source = f"extracted {len(knapsack_data['weights'])} items from weights"
    elif graph_data and 'nodes' in graph_data:
        input_size = graph_data['nodes']
        size_source = f"extracted {graph_data['nodes']} nodes"
    elif graph_data and 'matrix' in graph_data:
        input_size = len(graph_data['matrix'])
        size_source = f"extracted {len(graph_data['matrix'])}x{len(graph_data['matrix'])} matrix"

    if not input_size:
        input_size, size_source = extract_input_size(statement)
    if not input_size:
        input_size = 100
        size_source = "default (100)"

    paradigm, reasoning = conclude_paradigm(domain, input_size)
    if not paradigm:
        return {"error": reasoning}

    return {
        "original_statement": statement,
        "domain": domain,
        "paradigm": paradigm,
        "paradigm_reasoning": reasoning,
        "input_size": input_size,
        "size_source": size_source,
        "matched_keywords": keywords,
        "extracted_data": {
            "array": arr,
            "knapsack": knapsack_data,
            "graph": graph_data,
        },
        "error": None,
    }
