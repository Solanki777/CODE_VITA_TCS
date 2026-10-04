from collections import deque
import re

n = int(input())

grid = []
brick_id = 0
start = None
end = None

for r in range(n):
    line = input().strip()
    row = []
    i = 0

    while i < len(line):
        match = re.match(r'(\d+)([RGSD])', line[i:])
        length = int(match.group(1))
        kind = match.group(2)

        brick_id += 1

        for _ in range(length):
            row.append((kind, brick_id))

            if kind == 'S':
                start = (r, len(row) - 1)

            if kind == 'D':
                end = (r, len(row) - 1)

        i += len(match.group(0))

    grid.append(row)

dist = [[10**9] * n for _ in range(n)]
dist[start[0]][start[1]] = 0

q = deque([start])

directions = [
    (1, 0),
    (-1, 0),
    (0, 1),
    (0, -1)
]

while q:
    r, c = q.popleft()

    for dr, dc in directions:
        nr = r + dr
        nc = c + dc

        if nr < 0 or nr >= n or nc < 0 or nc >= n:
            continue

        kind, bid = grid[nr][nc]

        if kind == 'R':
            continue

        # Same brick costs 0.
        # Entering a new Green brick costs 1.
        current_bid = grid[r][c][1]

        if bid == current_bid:
            cost = 0
        elif kind == 'G':
            cost = 1
        else:
            cost = 0

        new_dist = dist[r][c] + cost

        if new_dist < dist[nr][nc]:
            dist[nr][nc] = new_dist

            if cost == 0:
                q.appendleft((nr, nc))
            else:
                q.append((nr, nc))

print(dist[end[0]][end[1]])


# Complexity
# Time: O(N²) approximately, because each cell has only 4 neighbours.
# Space: O(N²) for the expanded grid and distance array.