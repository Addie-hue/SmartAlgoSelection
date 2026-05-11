import random
import csv
from pathlib import Path
import sort as sa
import dp as dp

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / 'algorithm_data.csv'

def generate_data():
    print("Generating AI training data... this might take a few seconds...")
    sizes = [10, 50, 100, 200, 500, 800, 1000] 
    results = []

    for size in sizes:
        # 1. Sorting
        arr = [random.randint(1, 1000) for _ in range(size)]
        times = {
            "Bubble Sort": sa.bubble_sort(arr),
            "Selection Sort": sa.selection_sort(arr),
            "Insertion Sort": sa.insertion_sort(arr),
            "Merge Sort": sa.merge_sort(arr),
            "Quick Sort": sa.quick_sort(arr)
        }
        best_sort = min(times, key=times.get)
        results.append({"Problem_Type": "Sorting", "Input_Size": size, "Best_Algorithm": best_sort})

        # 2. Knapsack
        weights = [random.randint(1, 50) for _ in range(size)]
        values = [random.randint(10, 100) for _ in range(size)]
        capacity = size * 10
        dp.knapsack_01(capacity, weights, values)
        results.append({"Problem_Type": "Knapsack", "Input_Size": size, "Best_Algorithm": "Knapsack_01 (DP)"})

        # 3. Floyd-Warshall (Shortest Path)
        # Capping graph size at 50 so data generation doesn't take 5 hours
        v_size = min(size, 50)
        graph = [[random.randint(1, 100) if i != j else 0 for j in range(v_size)] for i in range(v_size)]
        dp.floyd_warshall(graph)
        results.append({"Problem_Type": "Shortest Path", "Input_Size": size, "Best_Algorithm": "Floyd-Warshall (DP)"})

        # 4. Multistage Graph
        dp.multistage_graph(graph, 4, v_size)
        results.append({"Problem_Type": "Multistage Graph", "Input_Size": size, "Best_Algorithm": "Multistage (DP)"})

    with open(DATA_FILE, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["Problem_Type", "Input_Size", "Best_Algorithm"])
        writer.writeheader()
        writer.writerows(results)

    print("Done! Dataset saved as 'algorithm_data.csv'.")

if __name__ == "__main__":
    generate_data()