data = [x.strip() for x in open("input.txt")]
start_i = [i for i, x in enumerate(data) if 'S' in x][0]
start = start_i, data[start_i].index('S')

def neighbors(i, j, l):
    n, m, coords = len(l), len(l[0]), set()
    if i > 0: coords.add((i - 1, j))
    if j > 0: coords.add((i, j - 1))
    if i < n - 1: coords.add((i + 1, j))
    if j < m - 1: coords.add((i, j + 1))
    return {(a, b) for a, b in coords if l[a][b] != '#'}

def neighbors_infinite(i, j, l):
    n, m = len(l), len(l[0])
    coords = [(i - 1, j), (i, j - 1), (i + 1, j), (i, j + 1)]
    return {(a, b) for a, b in coords if l[a % n][b % m] != '#'}

def steps(l, start, n, neighbor_func):
    previous_positions, positions, added_cells = set(), {start}, {start}
    for _ in range(n):
        new_cells = set()
        for i, j in added_cells:
            new_cells |= neighbor_func(i, j, l)
        new_positions = previous_positions | new_cells
        previous_positions = positions
        added_cells = new_cells
        positions = new_positions
    return len(positions)

def count_positions(m, refs, n):
    return [
        len({(i, j) for i, j in m if i // n == ref[0] and j // n == ref[1]})
        for ref in refs
    ]

def steps_math(l, start, n_steps):
    n, counts_base = len(l), [0]
    previous_positions, positions, added_cells = set(), {start}, {start}
    for _ in range(2 * n + n // 2):
        new_cells = set()
        for i, j in added_cells:
            new_cells |= neighbors_infinite(i, j, l)
        new_positions = previous_positions | new_cells
        previous_positions = positions
        added_cells = new_cells
        positions = new_positions
        counts_base.append(len({(i, j) for i, j in positions if 0 <= i < n and 0 <= j < n}))
    # state of filled up squares
    loop0, loop1 = counts_base[len(counts_base) - 1 - (len(counts_base) % 2)], counts_base[len(counts_base) - 2 - (len(counts_base) % 2)]
    # state of other particular squares
    big_diagonals = count_positions(positions, [(-1, -1), (-1, 1), (1, -1), (1, 1)], n)
    small_diagonals = count_positions(positions, [(-2, -1), (-1, 2), (1, -2), (1, 2)], n)
    sides = count_positions(positions, [(-2, 0), (0, 2), (0, -2), (2, 0)], n)
    # compute total
    k = n_steps // n
    n_full, n_even = 1 + 2 * k * (k - 1), 1 + 4 * ((k + 1) // 2) * ((k + 1) // 2 - 1)
    n_odd = n_full - n_even
    return n_even * loop0 + n_odd * loop1 + sum(sides) + (k - 1) * sum(big_diagonals) + k * sum(small_diagonals)
    
print(steps(data, start, 64, neighbors))
print(steps_math(data, start, 26501365))