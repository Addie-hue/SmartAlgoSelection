import time

# --- BRUTE FORCE ---
def bubble_sort(arr):
    data = arr.copy() # Copy so we don't modify the original array for other tests
    start_time = time.perf_counter()
    n = len(data)
    for i in range(n):
        for j in range(0, n-i-1):
            if data[j] > data[j+1]:
                data[j], data[j+1] = data[j+1], data[j]
    return time.perf_counter() - start_time

def selection_sort(arr):
    data = arr.copy()
    start_time = time.perf_counter()
    n = len(data)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if data[j] < data[min_idx]:
                min_idx = j
        data[i], data[min_idx] = data[min_idx], data[i]
    return time.perf_counter() - start_time

# --- DECREASE AND CONQUER ---
def insertion_sort(arr):
    data = arr.copy()
    start_time = time.perf_counter()
    for i in range(1, len(data)):
        key = data[i]
        j = i-1
        while j >= 0 and key < data[j]:
            data[j + 1] = data[j]
            j -= 1
        data[j + 1] = key
    return time.perf_counter() - start_time

# --- DIVIDE AND CONQUER ---
def _merge_sort_logic(arr):
    if len(arr) > 1:
        mid = len(arr)//2
        L = arr[:mid]
        R = arr[mid:]
        _merge_sort_logic(L)
        _merge_sort_logic(R)
        i = j = k = 0
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

def merge_sort(arr):
    data = arr.copy()
    start_time = time.perf_counter()
    _merge_sort_logic(data)
    return time.perf_counter() - start_time

def _quick_sort_logic(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return _quick_sort_logic(left) + middle + _quick_sort_logic(right)

def quick_sort(arr):
    data = arr.copy()
    start_time = time.perf_counter()
    _quick_sort_logic(data)
    return time.perf_counter() - start_time