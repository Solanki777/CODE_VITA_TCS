from collections import deque

n = int(input())

graph = {}

# Read station connections
for _ in range(n):
    data = input().split()

    source = data[0]

    if source not in graph:
        graph[source] = set()

    for station in data[1:]:
        graph[source].add(station)

        if station not in graph:
            graph[station] = set()

        graph[station].add(source)


q = int(input())

queries = []

for _ in range(q):
    queries.append(input().split())


r = int(input())

restricted = {}

# Read restrictions
for _ in range(r):
    data = input().split()

    source = data[0]
    restricted[source] = set(data[1:])


def can_travel(source, destination):
    # Stations that this source cannot visit
    blocked = restricted.get(source, set())

    if source in blocked or destination in blocked:
        return False

    visited = set()
    queue = deque([source])

    visited.add(source)

    while queue:
        current = queue.popleft()

        if current == destination:
            return True

        for next_station in graph.get(current, set()):

            if next_station in visited:
                continue

            if next_station in blocked:
                continue

            visited.add(next_station)
            queue.append(next_station)

    return False


# Process queries
for query in queries:

    source = query[0]
    operation = query[1]
    destination = query[2]

    if operation == "to":

        if can_travel(source, destination):
            print("yes")
        else:
            print("no")

    elif operation == "connects":

        graph.setdefault(source, set()).add(destination)
        graph.setdefault(destination, set()).add(source)

    elif operation == "disconnects":

        graph.setdefault(source, set()).discard(destination)
        graph.setdefault(destination, set()).discard(source)

        
# This solution uses an adjacency list to manage railway connections. BFS checks whether travel is possible while avoiding source-specific restricted stations. Connections can be dynamically added or removed through queries.
# Time Complexity: O(Q × (V + E))
# Space Complexity: O(V + E)