data = [x.strip() for x in open("input.txt")]

def get_beam_map(l, starting_beam=(0, -1, 0, 1)):
    beam_visited, beam_heads = set(), {starting_beam}  # i, j, vi, vj
    n, m = len(l), len(l[0])
    while beam_heads:
        new_beam_heads = set()
        for i, j, vi, vj in beam_heads:
            if (i, j, vi, vj) not in beam_visited:
                beam_visited.add((i, j, vi, vj))
                new_i, new_j = i + vi, j + vj
                if 0 <= new_i < n and 0 <= new_j < m:
                    tile = l[new_i][new_j]
                    if tile == '.' or (tile == '|' and vi != 0) or (tile == '-' and vj != 0):
                        new_beam_heads.add((new_i, new_j, vi, vj))
                    elif tile == '/':
                        new_beam_heads.add((new_i, new_j, -vj, -vi))
                    elif tile == '\\':
                        new_beam_heads.add((new_i, new_j, vj, vi))
                    elif tile == '|':
                        new_beam_heads.add((new_i, new_j, 1, 0))
                        new_beam_heads.add((new_i, new_j, -1, 0))
                    elif tile == '-':
                        new_beam_heads.add((new_i, new_j, 0, 1))
                        new_beam_heads.add((new_i, new_j, 0, -1))
        new_beam_heads = {(i, j, vi, vj) for i, j, vi, vj in new_beam_heads if 0 <= i < n and 0 <= j < m}   
        beam_heads = new_beam_heads
    return beam_visited - {starting_beam}

count_energized = lambda l, starting_beam=(0, -1, 0, 1): len(set((i, j) for i, j, _, _ in get_beam_map(l, starting_beam)))

def best_energization(l):
    n, m, energizations = len(l), len(l[0]), []
    for i in range(n):
        energizations.append(count_energized(l, (i, -1, 0, 1)))
        energizations.append(count_energized(l, (i, m, 0, -1)))
    for j in range(m):
        energizations.append(count_energized(l, (-1, j, 1, 0)))
        energizations.append(count_energized(l, (n, j, -1, 0)))
    return max(energizations)

print(count_energized(data))
print(best_energization(data))