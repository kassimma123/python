def is_prime(x):
    if x < 2: return False
    return all(x % i != 0 for i in range(2, int((x ** 0.5)+1)))


def filter_sequence(A: list[int], B: list[int]):
    b_counts = {}
    for x in B:
        b_counts[x] = b_counts.get(x, 0) + 1

    exclude = {x for x, freq in b_counts.items() if is_prime(freq) }

    return [x for x in A if x not in exclude]

if __name__ == "__main__":
    A = [2, 3, 9, 2, 5, 1, 3, 7, 10]
    B = [2, 1, 3, 4, 3, 10, 6, 6, 1, 7, 10, 10, 10]
    C = filter_sequence(A, B)
    print(C)
