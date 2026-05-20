from collections import defaultdict, deque

bajtocja = {
    0: [2], 
    1: [], 
    2: [0, 3], 
    3: [2]
}


def liczba_aglomeracji():
    n = len(bajtocja)
    
    visited = set()
    queue = deque()
    counter = 0

    for i in bajtocja:
        if i not in visited:
            counter += 1
            queue.append(i)
            print(queue)
            while queue:
                x = queue.popleft()
                visited.add(x)
                for j in bajtocja[x]:
                    if j not in visited:
                        queue.append(j)
                        visited.add(j)
    return counter
                
    

            

    
for i in bajtocja:
    print(i, bajtocja[i])
print(liczba_aglomeracji())                


