data = [list(map(int, x.strip())) for x in open("input.txt")]

MAX_INT = 1e9
MARGIN = 9

def next_nodes(i, j, l):
    res, n, m = {}, len(l), len(l[0])
    if i > 0: res["N"] = (i - 1, j)
    if j > 0: res["W"] = (i, j - 1)
    if i < n - 1: res["S"] = (i + 1, j)
    if j < m - 1: res["E"] = (i, j + 1)
    return res

def ultra_options(i, j, dir, l, mini):
    res, n, m = {}, len(l), len(l[0])
    if i > mini - 1: res["N"] = (i - mini, j, sum(l[i - offset][j] for offset in range(1, mini + 1)))
    if j > mini - 1: res["W"] = (i, j - mini, sum(l[i][j - offset] for offset in range(1, mini + 1)))
    if i < n - mini: res["S"] = (i + mini, j, sum(l[i + offset][j] for offset in range(1, mini + 1)))
    if j < m - mini: res["E"] = (i, j + mini, sum(l[i][j + offset] for offset in range(1, mini + 1)))
    if opposite_dir(dir) in res: del res[opposite_dir(dir)]
    one_step_options = next_nodes(i, j, l)
    if dir in one_step_options:
        ni, nj = one_step_options[dir]
        res[dir] = (ni, nj, l[ni][nj])
    return res

opposite_dir = lambda dir: {'N': 'S', 'W': 'E', 'S': 'N', 'E': 'W'}.get(dir)

def shortest_path(l, debug=False):
    nodes = {(i, j): dict() for i in range(len(l)) for j in range(len(l[0]))}
    nodes[(0, 0)] = {(None, 0): 0}
    stack, current_shortest_path, count = [(0, 0, 0, 0, None)], MAX_INT, 0  # i, j, dist, last_turn, dir
    while stack:
        if count % 50000 == 0:
            print(len(stack))
        count += 1
        i, j, dist, last_turn, dir = stack.pop()
        # go to next node
        if (i, j) == (len(l) - 1, len(l[0]) - 1):
            current_shortest_path = min(current_shortest_path, dist)
        else:
            next_step = next_nodes(i, j, l)
            if opposite_dir(dir) in next_step: del next_step[opposite_dir(dir)]
            if last_turn == 2 and dir in next_step: del next_step[dir]
            for ndir, (ni, nj) in next_step.items():
                new_dist, new_last_turn = dist + l[ni][nj], (last_turn + 1) * int(ndir == dir)
                if debug: print(f"{(ni, nj, ndir)} from: orig {(i, j, dir, last_turn)} w/ new dist={new_dist}")
                current_bests = nodes[(ni, nj)]
                relevant_keys = {(dr, l_t) for dr, l_t in current_bests if ndir == dr and l_t <= new_last_turn}
                relevant_best = min((current_bests[(dr, l_t)] for dr, l_t in relevant_keys), default=MAX_INT)
                lower_bound_on_path = new_dist + (len(l) - 1 - ni) + (len(l[0]) - 1 - nj)
                if (new_dist < relevant_best 
                    and new_dist < min(current_bests.values(), default=MAX_INT) + MARGIN
                    and lower_bound_on_path < current_shortest_path):
                    nodes[(ni, nj)] = {(dr, l_t): d for (dr, l_t), d in nodes[(ni, nj)].items() if (dr, l_t) not in relevant_keys}
                    nodes[(ni, nj)][(ndir, new_last_turn)] = new_dist
                    stack.append((ni, nj, new_dist, new_last_turn, ndir))
    return min(nodes[(len(l) - 1, len(l[0]) - 1)].values())

def shortest_path_ultra(l, mini=4, maxi=10, debug=False):
    nodes = {(i, j): dict() for i in range(len(l)) for j in range(len(l[0]))}
    nodes[(0, 0)] = {(None, 0): 0}
    stack, current_shortest_path, count = [(0, 0, 0, 0, None)], MAX_INT, 0  # i, j, dist, last_turn, dir
    while stack:
        if count % 50000 == 0:
            print(len(stack))
        count += 1
        i, j, dist, last_turn, dir = stack.pop()
        # go to next node
        if (i, j) == (len(l) - 1, len(l[0]) - 1):
            current_shortest_path = min(current_shortest_path, dist)
        else:
            next_options = ultra_options(i, j, dir, l, mini)
            if last_turn == maxi - 1 and dir in next_options: del next_options[dir]
            for ndir, (ni, nj, dist_incr) in next_options.items():
                new_dist, new_last_turn = dist + dist_incr, (last_turn + 1) if ndir == dir else (mini - 1)
                if debug: print(f"{(ni, nj, ndir)} from: orig {(i, j, dir, last_turn)} w/ new dist={new_dist}")
                current_bests = nodes[(ni, nj)]
                relevant_keys = {(dr, l_t) for dr, l_t in current_bests if ndir == dr and l_t <= new_last_turn}
                relevant_best = min((current_bests[(dr, l_t)] for dr, l_t in relevant_keys), default=MAX_INT)
                lower_bound_on_path = new_dist + (len(l) - 1 - ni) + (len(l[0]) - 1 - nj)
                if (new_dist < relevant_best
                    and lower_bound_on_path < current_shortest_path):
                    nodes[(ni, nj)] = {(dr, l_t): d for (dr, l_t), d in nodes[(ni, nj)].items() if (dr, l_t) not in relevant_keys}
                    nodes[(ni, nj)][(ndir, new_last_turn)] = new_dist
                    stack.append((ni, nj, new_dist, new_last_turn, ndir))
    return min(nodes[(len(l) - 1, len(l[0]) - 1)].values())

print(shortest_path(data, False))
print(shortest_path_ultra(data, debug=False))