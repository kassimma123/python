def find_peak_element(arr: list[int]) -> int:
    left = 0
    right = len(arr) - 1

    while left < right:
        mid = (left + right) //2 

        if arr[mid] < arr[mid + 1]:
            left = mid + 1
        else:
            right = mid 
    return left

gory = [1, 3, 4, 5, 7, 4, 2, 0]
print(f"Indeks szczytu to: {find_peak_element(gory)}")

from collections import defaultdict, deque

def count_graphs_in_forest(n: int, edges: list[list[int]]) -> int:
    graph = defaultdict(list)

    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    visited = set()
    count = 0 

    for i in range(n):
        if i not in visited:
            count += 1

            queue = deque([i])
            visited.add(i)

            while queue:
                current = queue.popleft()

                for neighbour in graph[current]:
                    if neighbour not in visited:
                        visited.add(neighbour)
                        queue.append(neighbour)
    return count

        
