data = [x.strip() for x in open("input.txt")]

CONNECTIONS = {'|': ('N', 'S'), '-': ('E', 'W'), 'L': ('S', 'W'), 'J': ('S', 'E'), '7': ('E', 'N'), 'F': ('N', 'W'), '.': [], 'S': ['N', 'S', 'W', 'E']}
reverse_dir = {'N': 'S', 'E': 'W', 'S': 'N', 'W': 'E'}

def neighbors(i, j, l):
    h, w, neighbors = len(l), len(l[0]), {}
    if i > 0: neighbors["N"] = (i - 1, j)
    if j > 0: neighbors["W"] = (i, j - 1)
    if i < h - 1: neighbors["S"] = (i + 1, j)
    if j < w - 1: neighbors["E"] = (i, j + 1)
    return neighbors

def find_loop(l):
    i, loop = 0, []
    while 'S' not in l[i]: i += 1
    start = i, l[i].find('S')  # starting position
    loop.append(start)
    next_dir, next_pipe = [(dir, coords) for dir, coords in neighbors(start[0], start[1], l).items() if dir in CONNECTIONS[l[coords[0]][coords[1]]]][0]
    while next_pipe != start:
        loop.append(next_pipe)
        pipe_type = l[next_pipe[0]][next_pipe[1]]
        next_dir = reverse_dir[list(set(CONNECTIONS[pipe_type]) - {next_dir})[0]]
        next_pipe = neighbors(next_pipe[0], next_pipe[1], l)[next_dir]
    directions_from_start = tuple([dir for dir, coords in neighbors(start[0], start[1], l).items() if dir in CONNECTIONS[l[coords[0]][coords[1]]]])
    start_type = [tile_type for tile_type, dirs in CONNECTIONS.items() if set(dirs) == set(reverse_dir[d] for d in directions_from_start)][0]
    return loop, start_type

def count_loop_interior(loop, l, start_type):
    h, count = len(l), 0
    for i in range(h):
        offset, previous_wall = 0, None  # keep a count of walls crossed + the last wall pipe encountered
        for j, c in enumerate(l[i].replace('S', start_type)):
            if (i, j) not in loop and offset % 2:  # loop interior
                count, previous_wall = count + 1, None
            elif (i, j) in loop and c in 'F|LJ7':  # encountering a vertical pipe
                if (previous_wall, c) in [('F', 'J'), ('L', '7')]: offset -= 1  # special case where the 2 vertical pipes correspond to just one wall
                offset, previous_wall = offset + 1, c
    return count

loop, s_type = find_loop(data)

print(len(loop) // 2)
print(count_loop_interior(set(loop), data, s_type))