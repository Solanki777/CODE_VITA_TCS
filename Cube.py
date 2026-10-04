# MisCube - TCS CodeVita

data = input().split()

# Face order:
# Top, Front, Down, Back, Left, Right

F = [
    (0,1,0, 1,0,0, 0,0,1),     # Top
    (0,0,1, 1,0,0, 0,-1,0),    # Front
    (0,-1,0, 1,0,0, 0,0,-1),   # Down
    (0,0,-1, 1,0,0, 0,1,0),    # Back
    (-1,0,0, 0,0,1, 0,-1,0),   # Left
    (1,0,0, 0,0,-1, 0,-1,0)    # Right
]

corners = [
    (0,15,16),
    (1,14,21),
    (2,4,17),
    (3,5,20),
    (6,8,19),
    (7,9,22),
    (10,13,18),
    (11,12,23)
]


def rotate(v, axis, sign):
    r = list(v)

    a = (axis + 1) % 3
    b = (axis + 2) % 3

    r[a] = sign * v[b]
    r[b] = -sign * v[a]

    return tuple(r)


# Position and normal of every sticker
pos = []
normal = []

for f in range(6):

    n = F[f][0:3]
    right = F[f][3:6]
    down = F[f][6:9]

    for row in range(2):
        for col in range(2):

            p = (
                n[0] + right[0] * (2 * col - 1) + down[0] * (2 * row - 1),
                n[1] + right[1] * (2 * col - 1) + down[1] * (2 * row - 1),
                n[2] + right[2] * (2 * col - 1) + down[2] * (2 * row - 1)
            )

            pos.append(p)
            normal.append(n)


# Create all 18 cube moves
moves = []

for f in range(6):

    face = F[f]

    if face[0] != 0:
        axis = 0
    elif face[1] != 0:
        axis = 1
    else:
        axis = 2

    direction = face[axis]

    for move_type in range(3):

        if move_type == 0:
            sign = 1
        elif move_type == 1:
            sign = -1
        else:
            sign = 2

        move = list(range(24))

        for i in range(24):

            if pos[i][axis] != direction:
                continue

            if move_type == 2:
                new_pos = rotate(pos[i], axis, direction)
                new_pos = rotate(new_pos, axis, direction)

                new_normal = rotate(normal[i], axis, direction)
                new_normal = rotate(new_normal, axis, direction)
            else:
                new_pos = rotate(pos[i], axis, direction * sign)
                new_normal = rotate(normal[i], axis, direction * sign)

            for j in range(24):

                if pos[j] == new_pos and normal[j] == new_normal:
                    move[i] = j
                    break

        moves.append(move)


def apply(state, move):
    new_state = [''] * 24

    for i in range(24):
        new_state[move[i]] = state[i]

    return tuple(new_state)


def twist(state, corner, direction):

    new_state = list(state)

    a, b, c = corner

    if direction == 0:
        new_state[a] = state[c]
        new_state[b] = state[a]
        new_state[c] = state[b]
    else:
        new_state[a] = state[b]
        new_state[b] = state[c]
        new_state[c] = state[a]

    return tuple(new_state)


# Standard solved cube
colors = ['y', 'r', 'w', 'o', 'b', 'g']

solved = []

for color in colors:
    solved += [color] * 4

solved = tuple(solved)


# Store every possible twisted-corner state
possible = {}

for corner in corners:

    for direction in [0, 1]:

        state = twist(solved, corner, direction)

        answer = ''.join(sorted(solved[i] for i in corner))

        possible[state] = answer


# Search at most 4 moves
def dfs(state, depth):

    if state in possible:
        return possible[state]

    if depth == 4:
        return None

    for move in moves:

        new_state = apply(state, move)

        result = dfs(new_state, depth + 1)

        if result:
            return result

    return None


answer = dfs(tuple(data), 0)

if answer:
    print(answer)
else:
    print("Not enough clues")



# This solution models the 24 cube stickers and generates all 18 possible cube moves. It creates every possible twisted-corner state from a solved cube and uses DFS to check whether the given cube can reach one within four moves. The colors of the matching corner are sorted alphabetically.
# Time: O(18^4 × 24)
# Space: O(24 × 18^4)