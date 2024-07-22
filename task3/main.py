import timeit
from pathlib import Path

def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps

def kmp_search(text, pattern):
    M = len(pattern)
    N = len(text)

    lps = compute_lps(pattern)

    i = j = 0
    found_indices = []

    while i < N:
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == M:
            found_indices.append(i - j)
            j = lps[j - 1]

        elif i < N and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return found_indices

def build_shift_table(pattern):
    table = {}
    length = len(pattern)
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    table.setdefault(pattern[-1], length)
    return table

def boyer_moore_search(text, pattern):
    shift_table = build_shift_table(pattern)
    i = 0
    found_indices = []

    while i <= len(text) - len(pattern):
        j = len(pattern) - 1

        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1

        if j < 0:
            found_indices.append(i)
            i += (shift_table.get(text[i + len(pattern) - 1], len(pattern))
                  if i + len(pattern) < len(text) else 1)
        else:
            i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

    return found_indices

def rabin_karp_search(text, pattern):
    d = 256
    q = 101
    M = len(pattern)
    N = len(text)
    p = 0
    t = 0
    h = 1
    found_indices = []

    for i in range(M - 1):
        h = (h * d) % q

    for i in range(M):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q

    for i in range(N - M + 1):
        if p == t:
            if text[i:i + M] == pattern:
                found_indices.append(i)
        if i < N - M:
            t = (d * (t - ord(text[i]) * h) + ord(text[i + M])) % q
            if t < 0:
                t = t + q

    return found_indices

def load_text(file_path):
    with open(file_path, "r", encoding="cp1251") as file:
        return file.read()

def measure_time(search_func, text, pattern):
    start_time = timeit.default_timer()
    search_func(text, pattern)
    end_time = timeit.default_timer()
    return end_time - start_time

# Завантаження текстів
text1 = load_text(Path("task3/text1.txt"))
text2 = load_text(Path("task3/text2.txt"))

# Підрядки для тестування
existing_pattern = "Висновки"
non_existing_pattern = "тайтаке"

# Вимірювання часу
results = {
    "KMP": {"text1": {}, "text2": {}},
    "Boyer-Moore": {"text1": {}, "text2": {}},
    "Rabin-Karp": {"text1": {}, "text2": {}}
}

# Вимірювання часу для існуючого підрядка
results["KMP"]["text1"]["existing"] = measure_time(kmp_search, text1, existing_pattern)
results["KMP"]["text2"]["existing"] = measure_time(kmp_search, text2, existing_pattern)
results["Boyer-Moore"]["text1"]["existing"] = measure_time(boyer_moore_search, text1, existing_pattern)
results["Boyer-Moore"]["text2"]["existing"] = measure_time(boyer_moore_search, text2, existing_pattern)
results["Rabin-Karp"]["text1"]["existing"] = measure_time(rabin_karp_search, text1, existing_pattern)
results["Rabin-Karp"]["text2"]["existing"] = measure_time(rabin_karp_search, text2, existing_pattern)

# Вимірювання часу для вигаданого підрядка
results["KMP"]["text1"]["non_existing"] = measure_time(kmp_search, text1, non_existing_pattern)
results["KMP"]["text2"]["non_existing"] = measure_time(kmp_search, text2, non_existing_pattern)
results["Boyer-Moore"]["text1"]["non_existing"] = measure_time(boyer_moore_search, text1, non_existing_pattern)
results["Boyer-Moore"]["text2"]["non_existing"] = measure_time(boyer_moore_search, text2, non_existing_pattern)
results["Rabin-Karp"]["text1"]["non_existing"] = measure_time(rabin_karp_search, text1, non_existing_pattern)
results["Rabin-Karp"]["text2"]["non_existing"] = measure_time(rabin_karp_search, text2, non_existing_pattern)

# Виведення результатів
for algo, texts in results.items():
    print(f"\n{algo} algorithm:")
    for text_name, patterns in texts.items():
        for pattern_type, time in patterns.items():
            print(f"  {text_name} - {pattern_type} pattern: {time:.6f} seconds")
