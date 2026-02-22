"""
Sorting Assignment Starter Code
Implement five sorting algorithms and benchmark their performance.
"""

import json
import time
import random
import tracemalloc


# ============================================================================
# PART 1: SORTING IMPLEMENTATIONS
# ============================================================================

def bubble_sort(arr, key=None):
    """Sort a sequence using the bubble sort algorithm.

    The implementation mimics Python's built-in ``sorted`` behaviour by
    accepting an optional ``key`` function.  If ``arr`` is a dictionary it is
    converted to a list of its keys before sorting (just like ``sorted``).

    Args:
        arr (list|dict): Sequence to sort.  If a dict is passed the sorted list of
            keys is returned.
        key (callable, optional): Function that extracts a comparison key from
            each element.  Defaults to ``None`` (identity).

    Returns:
        list: Sorted list.  The original input is not modified.

    Example:
        bubble_sort([64, 34, 25, 12, 22, 11, 90])
            returns [11, 12, 22, 25, 34, 64, 90]
        bubble_sort(products, key=lambda p: p['price'])
            works when ``products`` is a list of dictionaries.
    """
    # make a working copy and normalise dictionary inputs
    is_dict = isinstance(arr, dict)
    if is_dict:
        arr = list(arr)
    else:
        arr = list(arr)

    # helper to get key value
    def _k(x):
        return key(x) if key else x

    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if _k(arr[j]) > _k(arr[j + 1]):
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

    # return same type as sorted would
    return arr

def selection_sort(arr, key=None):
    """Sort a sequence using the selection sort algorithm.

    Supports an optional ``key`` function and will gracefully convert a
    dictionary input into a list of keys before sorting.

    Args:
        arr (list|dict): Sequence to sort.
        key (callable, optional): Key extraction function.

    Returns:
        list: Sorted sequence.
    """
    is_dict = isinstance(arr, dict)
    if is_dict:
        arr = list(arr)
    else:
        arr = list(arr)

    def _k(x):
        return key(x) if key else x

    for step in range(len(arr)):
        min_idx = step
        for i in range(step + 1, len(arr)):
            if _k(arr[i]) < _k(arr[min_idx]):
                min_idx = i
        arr[step], arr[min_idx] = arr[min_idx], arr[step]
    return arr
def insertion_sort(arr, key=None):
    """Sort a sequence using the insertion sort algorithm.

    Optional ``key`` parameter is applied to elements for comparison.  Dictionary
    inputs are converted to a list of keys.
    """
    is_dict = isinstance(arr, dict)
    if is_dict:
        arr = list(arr)
    else:
        arr = list(arr)

    def _k(x):
        return key(x) if key else x

    for step in range(1, len(arr)):
        current = arr[step]
        j = step - 1
        while j >= 0 and _k(current) < _k(arr[j]):
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = current
    return arr
def merge_sort(arr, key=None):
    """Sort a sequence using merge sort (divide and conquer).

    Accepts a ``key`` function and will treat a dictionary input as a list of
    its keys.  The function is implemented recursively and returns a new sorted
    list; the argument is not modified.
    """
    is_dict = isinstance(arr, dict)
    if is_dict:
        arr = list(arr)
    else:
        arr = list(arr)

    def _k(x):
        return key(x) if key else x

    # recursive helper that works on lists
    def _merge_sort(lst):
        if len(lst) <= 1:
            return lst
        mid = len(lst) // 2
        left = _merge_sort(lst[:mid])
        right = _merge_sort(lst[mid:])
        merged = []
        i = j = 0
        while i < len(left) and j < len(right):
            if _k(left[i]) <= _k(right[j]):
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged

    sorted_list = _merge_sort(arr)
    return sorted_list
# ============================================================================
# PART 2: STABILITY DEMONSTRATION
# ============================================================================

def demonstrate_stability():
    """Demonstrate which sorting algorithms are stable.

    We create a small list of product dictionaries where multiple items share the
    same ``price``.  A stable sort will preserve the relative ``original_position``
    of products that have identical prices.

    The four sorting functions are exercised with the ``key`` parameter so they
    can operate on the ``price`` field of each product dictionary.  If an
    algorithm raises an exception during the sort it is recorded as "Error".

    Returns:
        dict: Mapping from algorithm name to one of "Stable", "Unstable" or
        "Error".
    """

    products = [
        {"name": "Widget A", "price": 1999, "original_position": 0},
        {"name": "Gadget B", "price": 999, "original_position": 1},
        {"name": "Widget C", "price": 1999, "original_position": 2},
        {"name": "Tool D", "price": 999, "original_position": 3},
        {"name": "Widget E", "price": 1999, "original_position": 4},
    ]

    def check_stable(sorted_list):
        last_seen = {}
        for prod in sorted_list:
            price = prod["price"]
            pos = prod["original_position"]
            if price in last_seen and pos < last_seen[price]:
                return False
            last_seen[price] = pos
        return True

    algorithms = {
        "bubble_sort": bubble_sort,
        "selection_sort": selection_sort,
        "insertion_sort": insertion_sort,
        "merge_sort": merge_sort,
    }

    results = {}
    for name, func in algorithms.items():
        try:
            copy_list = [p.copy() for p in products]
            sorted_products = func(copy_list, key=lambda x: x["price"])
            stable = check_stable(sorted_products)
            results[name] = "Stable" if stable else "Unstable"
        except Exception as e:
            results[name] = f"Error: {e}"

    return results


# ============================================================================
# PART 3: PERFORMANCE BENCHMARKING
# ============================================================================

def load_dataset(filename):
    """Load a dataset from JSON file."""
    with open(f"datasets/{filename}", "r") as f:
        return json.load(f)


def load_test_cases():
    """Load test cases for validation."""
    with open("datasets/test_cases.json", "r") as f:
        return json.load(f)


def test_sorting_correctness():
    """Test that sorting functions work correctly on small test cases."""
    print("="*70)
    print("TESTING SORTING CORRECTNESS")
    print("="*70 + "\n")
    
    test_cases = load_test_cases()
    
    test_names = ["small_random", "small_sorted", "small_reverse", "small_duplicates"]
    algorithms = {
        "Bubble Sort": bubble_sort,
        "Selection Sort": selection_sort,
        "Insertion Sort": insertion_sort,
        "Merge Sort": merge_sort
    }
    
    for test_name in test_names:
        print(f"Test: {test_name}")
        print(f"  Input:    {test_cases[test_name]}")
        print(f"  Expected: {test_cases['expected_sorted'][test_name]}")
        print()
        
        for algo_name, algo_func in algorithms.items():
            try:
                result = algo_func(test_cases[test_name].copy())
                expected = test_cases['expected_sorted'][test_name]
                status = "✓ PASS" if result == expected else "✗ FAIL"
                print(f"    {algo_name:20s}: {result} {status}")
            except Exception as e:
                print(f"    {algo_name:20s}: ERROR - {str(e)}")
        
        print()


def benchmark_algorithm(sort_func, data):

    """
    Benchmark a sorting algorithm on given data.
    
    Args:
        sort_func: The sorting function to test
        data: The dataset to sort (will be copied so original isn't modified)
    
    Returns:
        tuple: (execution_time_ms, peak_memory_kb)
    """
    # Copy data so we don't modify original
    data_copy = data.copy()
    
    # Start memory tracking
    tracemalloc.start()
    
    # Measure execution time
    start_time = time.perf_counter()
    sort_func(data_copy)
    end_time = time.perf_counter()
    
    # Get peak memory usage
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    execution_time_ms = (end_time - start_time) * 1000
    peak_memory_kb = peak / 1024
    
    return execution_time_ms, peak_memory_kb


def benchmark_all_datasets():
    """Benchmark all sorting algorithms on all datasets."""
    print("\n" + "="*70)
    print("BENCHMARKING SORTING ALGORITHMS")
    print("="*70 + "\n")
    
    datasets = {
        "orders.json": ("Order Processing Queue", 50000, 5000),
        "products.json": ("Product Catalog", 100000, 5000),
        "inventory.json": ("Inventory Reconciliation", 25000, 5000),
        "activity_log.json": ("Customer Activity Log", 75000, 5000)
    }
    
    algorithms = {
        "Bubble Sort": bubble_sort,
        "Selection Sort": selection_sort,
        "Insertion Sort": insertion_sort,
        "Merge Sort": merge_sort
    }
    
    for filename, (description, full_size, sample_size) in datasets.items():
        print(f"Dataset: {description} ({sample_size:,} element sample)")
        print("-" * 70)
        
        data = load_dataset(filename)
        # Use first sample_size elements for fair comparison
        data_sample = data[:sample_size]
        
        for algo_name, algo_func in algorithms.items():
            try:
                exec_time, memory = benchmark_algorithm(algo_func, data_sample)
                print(f"  {algo_name:20s}: {exec_time:8.2f} ms | {memory:8.2f} KB")
            except Exception as e:
                print(f"  {algo_name:20s}: ERROR - {str(e)}")
        
        print()


def analyze_stability():
    """Test and display which algorithms are stable."""
    print("="*70)
    print("STABILITY ANALYSIS")
    print("="*70 + "\n")
    
    print("Testing which algorithms preserve order of equal elements...\n")
    
    results = demonstrate_stability()
    
    for algo_name, stability in results.items():
        print(f"  {algo_name:20s}: {stability}")
    
    print()


if __name__ == "__main__":
    print("SORTING ASSIGNMENT - STARTER CODE")
    print("Implement the sorting functions above, then run tests.\n")
    
    # Uncomment these as you complete each part:
    
    # test_sorting_correctness()
    benchmark_all_datasets()
    # analyze_stability()
    
    print("\n⚠ Uncomment the test functions in the main block to run benchmarks!")