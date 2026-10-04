directions = {
    'top': (0, 1),
    'down': (0, -1),
    'left': (-1, 0),
    'right': (1, 0)
}

n = int(input().strip())

commands = []

for _ in range(n):
    existing, new, direction = input().strip().split()
    existing = int(existing)
    new = int(new)

    commands.append((existing, new, direction))

target = int(input().strip())

commands.sort(key=lambda x: (x[0], x[1]))

pos = {}
cube_at = {}

if commands:
    first_cube = commands[0][0]
    pos[first_cube] = (0, 0)
    cube_at[(0, 0)] = first_cube

for existing, new, direction in commands:

    if existing not in pos:
        continue

    x, y = pos[existing]

    dx, dy = directions[direction]

    new_pos = (x + dx, y + dy)

    if new_pos in cube_at:
        replaced_cube = cube_at[new_pos]
        del pos[replaced_cube]

    pos[new] = new_pos
    cube_at[new_pos] = new

if target not in pos:
    print("-1 -1 -1 -1")

else:
    x, y = pos[target]

    up = cube_at.get((x, y + 1), -1)
    down = cube_at.get((x, y - 1), -1)
    left = cube_at.get((x - 1, y), -1)
    right = cube_at.get((x + 1, y), -1)

    print(up, down, left, right)