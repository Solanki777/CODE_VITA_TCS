n, m = map(int, input().split())

graph = [[] for _ in range(n)]

for _ in range(m):
    a, b = map(int, input().split())
    a -= 1
    b -= 1
    graph[a].append(b)
    graph[b].append(a)

s1, s2 = map(int, input().split())
s1 -= 1
s2 -= 1

dest = int(input()) - 1

# Find all possible simple path masks from a starting town
def find_paths(start):
    size = 1 << n

    # dp[mask] contains towns where we can finish
    # after visiting exactly the towns in mask
    dp = [0] * size

    dp[1 << start] = 1 << start

    for mask in range(size):
        if dp[mask] == 0:
            continue

        ends = dp[mask]

        while ends:
            bit = ends & -ends
            u = bit.bit_length() - 1
            ends -= bit

            for v in graph[u]:
                if not (mask & (1 << v)):
                    new_mask = mask | (1 << v)
                    dp[new_mask] |= 1 << v

    paths = []

    for mask in range(size):
        if dp[mask] & (1 << dest):
            paths.append(mask)

    return paths


paths1 = find_paths(s1)
paths2 = find_paths(s2)

# Remove destination from masks because
# destination is allowed to be common.
without_dest = ((1 << n) - 1) ^ (1 << dest)

# best[mask] = minimum number of towns used by
# a path of scout 2 whose non-destination towns
# are a subset of mask.
INF = 999999
best = [INF] * (1 << n)

for path in paths2:
    p = path & without_dest
    count = p.bit_count()

    if count < best[p]:
        best[p] = count

# Make best[mask] also consider all subsets of mask.
for i in range(n):
    for mask in range(1 << n):
        if mask & (1 << i):
            best[mask] = min(best[mask], best[mask ^ (1 << i)])

answer = INF

for path in paths1:
    p1 = path & without_dest

    # Scout 2 must use towns that scout 1 does not use.
    allowed = without_dest ^ p1

    if best[allowed] != INF:
        total = p1.bit_count() + best[allowed] + 1
        answer = min(answer, total)

if answer == INF:
    print("Impossible")
else:
    print(answer)

# How it works
# - 1 << town represents a town using a bit.
# - A mask represents all towns visited by one scout.
# - find_paths() finds every possible simple path from a scout's starting town to the destination.
# - Before comparing paths, we remove the destination because both scouts are allowed to share it.
# - We then find two path masks having no common towns.
# - Finally:
# total = scout1 towns + scout2 towns + destination

# Complexity
# For N <= 15:
# - Time: approximately O(N × 2^N)
# - Space: O(2^N)