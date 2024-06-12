import timeit

def brute_force_search(pattern, text):
    m = len(pattern)
    n = len(text)
    comparisons = 0
    for i in range(n - m + 1):
        j = 0
        while j < m and text[i + j] == pattern[j]:
            comparisons += 1
            j += 1
        if j == m:
            return i, comparisons  # Pattern found
        comparisons += 1  # For the final comparison that fails
    return -1, comparisons  # Pattern not found

def boyer_moore_search(pattern, text):
    m = len(pattern)
    n = len(text)
    skip = [m] * 256
    comparisons = 0
    
    # Preprocess the pattern
    for k in range(m - 1):
        skip[ord(pattern[k])] = m - k - 1
    
    k = m - 1
    while k < n:
        j = m - 1
        i = k
        while j >= 0 and text[i] == pattern[j]:
            comparisons += 1
            j -= 1
            i -= 1
        if j == -1:
            return i + 1, comparisons  # Pattern found 
        comparisons += 1  # For the final comparison that fails
        k += skip[ord(text[k])]
    return -1, comparisons  # Pattern not found

def kmp_preprocess(pattern):
    m = len(pattern)
    border = [0] * m
    length = 0
    i = 1
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            border[i] = length
            i += 1
        else:
            if length != 0:
                length = border[length - 1]
            else:
                border[i] = 0
                i += 1
    return border

def kmp_search(pattern, text):
    m = len(pattern)
    n = len(text)
    border = kmp_preprocess(pattern)
    i = 0  # index for text
    j = 0  # index for pattern
    comparisons = 0
    while i < n:
        if pattern[j] == text[i]:
            comparisons += 1
            i += 1
            j += 1
        if j == m:
            return i - j, comparisons  # Pattern found
        elif i < n and pattern[j] != text[i]:
            comparisons += 1
            if j != 0:
                j = border[j - 1]
            else:
                i += 1
    return -1, comparisons  # Pattern not found

def measure_time(func, *args):
    start_time = timeit.default_timer()
    result = func(*args)
    end_time = timeit.default_timer()
    elapsed_time = (end_time - start_time) * 1000  # Convert to milliseconds
    return result, elapsed_time

def search_disorder(text):
    # Define normal and mutated patterns
    mutations = {
        "ΔF508": ("LTVLFGLGLILF", "LTVLGLGLILF"),
        "G542X": ("TGTLGIFTTQAL", "TGTLXIFTTQAL"),
        "G551D": ("TTTGIGMQC", "TTTGDMQC"),
        "N1303K": ("TATNDKDVL", "TATKDKDVL"),
        "W1282X": ("RVIVTIWVEV", "RVIVTIXVEV")
    }
    # Search for patterns
    results = {"Brute Force": {}, "KMP": {}, "Boyer-Moore": {}}
    
    for mutation, (normal_pattern, mutated_pattern) in mutations.items():
        # Brute Force
        (normal_position_bf, comparisons_bf_normal), time_bf_normal = measure_time(brute_force_search, normal_pattern, text)
        (mutated_position_bf, comparisons_bf_mutated), time_bf_mutated = measure_time(brute_force_search, mutated_pattern, text)
        results["Brute Force"][mutation] = (normal_position_bf, mutated_position_bf, comparisons_bf_normal, comparisons_bf_mutated, time_bf_normal, time_bf_mutated)
        
        # KMP
        (normal_position_kmp, comparisons_kmp_normal), time_kmp_normal = measure_time(kmp_search, normal_pattern, text)
        (mutated_position_kmp, comparisons_kmp_mutated), time_kmp_mutated = measure_time(kmp_search, mutated_pattern, text)
        results["KMP"][mutation] = (normal_position_kmp, mutated_position_kmp, comparisons_kmp_normal, comparisons_kmp_mutated, time_kmp_normal, time_kmp_mutated)
        
        # Boyer-Moore
        (normal_position_bm, comparisons_bm_normal), time_bm_normal = measure_time(boyer_moore_search, normal_pattern, text)
        (mutated_position_bm, comparisons_bm_mutated), time_bm_mutated = measure_time(boyer_moore_search, mutated_pattern, text)
        results["Boyer-Moore"][mutation] = (normal_position_bm, mutated_position_bm, comparisons_bm_normal, comparisons_bm_mutated, time_bm_normal, time_bm_mutated)

    # Print results
    for algorithm, data in results.items():
        print(f"\nResults using {algorithm}:")
        for mutation, (normal_position, mutated_position, comp_normal, comp_mutated, time_normal, time_mutated) in data.items():
            print(f"{mutation}:")
            print(f"  Normal pattern found at position: {normal_position} with {comp_normal} comparisons in {time_normal:.6f} ms")
            print(f"  Mutated pattern found at position: {mutated_position} with {comp_mutated} comparisons in {time_mutated:.6f} ms")
