n, m = map(int, input().split())

grid = []

for _ in range(n):
    grid.append(input().split())

t = int(input())
I = int(input())

# Initially every cell is possible for every time
possible = []

for k in range(t):
    cells = set()

    for i in range(n):
        for j in range(m):
            cells.add((i, j))

    possible.append(cells)


# Apply clues
for _ in range(I):
    time = int(input())
    x1, y1, x2, y2 = map(int, input().split())

    time -= 1

    for i in range(x1 - 1, x2):
        for j in range(y1 - 1, y2):
            possible[time].discard((i, j))


# If any time has no possible cell
for k in range(t):
    if len(possible[k]) == 0:
        print("Not enough clues")
        exit()


# Find all possible paths
answer = set()


def dfs(r, c, time, word, visited):
    if time == t:
        answer.add(word)
        return

    directions = [
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1)
    ]

    for dr, dc in directions:
        nr = r + dr
        nc = c + dc

        if nr < 0 or nr >= n or nc < 0 or nc >= m:
            continue

        if (nr, nc) not in possible[time]:
            continue

        if (nr, nc) in visited:
            continue

        visited.add((nr, nc))

        dfs(
            nr,
            nc,
            time + 1,
            word + grid[nr][nc],
            visited
        )

        visited.remove((nr, nc))


# Try every possible starting cell
for r, c in possible[0]:
    visited = {(r, c)}

    dfs(
        r,
        c,
        1,
        grid[r][c],
        visited
    )

    # More than one possible word means answer is not unique
    if len(answer) > 1:
        print("Not enough clues")
        exit()


if len(answer) == 1:
    print(next(iter(answer)))
else:
    print("Not enough clues")


# This solution first removes cells excluded by each clue. DFS then explores all valid paths using only up, down, left, and right movements while preventing cell reuse. Every possible secret word is stored. If exactly one word is found, it is printed; otherwise, Not enough clues is printed.
# Time: O(N×M×4^T)
# Space: O(N×M + T)