# Algorithm
# 1. Read the number of commands.
# 2. Store all cube placement commands.
# 3. Read the target cube.
# 4. Sort the commands using the existing cube and new cube.
# 5. Place the first cube at coordinate (0, 0).
# 6. Process every command.
# 7. Calculate the new cube's coordinate using the direction.
# 8. Store the cube and its coordinate.
# 9. Find the target cube's coordinate.
# 10. Check the four neighbouring coordinates.
# 11. Print the cubes in:
#     - Up
#     - Down
#     - Left
#     - Right


# Direction vectors:
# top   -> increase y
# down  -> decrease y
# left  -> decrease x
# right -> increase x
directions = {
    'top': (0, 1),
    'down': (0, -1),
    'left': (-1, 0),
    'right': (1, 0)
}

# Read the number of cube placement commands
n = int(input().strip())

commands = []

# Read all commands
for _ in range(n):
    existing, new, direction = input().strip().split()

    existing = int(existing)
    new = int(new)

    commands.append((existing, new, direction))

# Read the cube for which neighbours are required
target = int(input().strip())

# Sort commands by existing cube and then new cube
commands.sort(key=lambda x: (x[0], x[1]))

# pos stores:
# cube -> (x, y)
pos = {}

# cube_at stores:
# (x, y) -> cube
cube_at = {}

# Place the first cube at the origin
if commands:
    first_cube = commands[0][0]

    pos[first_cube] = (0, 0)
    cube_at[(0, 0)] = first_cube

# Process every cube placement command
for existing, new, direction in commands:

    # If the existing cube has not been positioned,
    # we cannot determine the position of the new cube.
    if existing not in pos:
        continue

    # Get the coordinates of the existing cube
    x, y = pos[existing]

    # Get the coordinate change for the direction
    dx, dy = directions[direction]

    # Calculate the position of the new cube
    new_pos = (x + dx, y + dy)

    # If another cube already occupies this position,
    # remove its old position mapping.
    if new_pos in cube_at:
        replaced_cube = cube_at[new_pos]
        del pos[replaced_cube]

    # Store the new cube's position
    pos[new] = new_pos

    # Store which cube occupies this coordinate
    cube_at[new_pos] = new

# If the requested cube does not exist
if target not in pos:
    print("-1 -1 -1 -1")

else:
    # Get the target cube's coordinates
    x, y = pos[target]

    # Check the four neighbouring positions
    up = cube_at.get((x, y + 1), -1)
    down = cube_at.get((x, y - 1), -1)
    left = cube_at.get((x - 1, y), -1)
    right = cube_at.get((x + 1, y), -1)

    # Output in required order:
    # Up Down Left Right
    print(up, down, left, right)





# Space Complexity : O(N)
#     The program stores:
#     - commands → O(N)
#     - pos → O(N)
#     - cube_at → O(N)

# Time Complexity:  O(N log N)