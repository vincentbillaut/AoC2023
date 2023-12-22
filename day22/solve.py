data = [(tuple(map(int, x.strip().split('~')[0].split(','))), 
         tuple(map(int, x.strip().split('~')[1].split(',')))) for x in open("input.txt")]

xy_footprint = lambda brick, fun: set((x, y, fun(brick[0][2], brick[1][2])) 
    for x in range(brick[0][0], brick[1][0] + 1)
    for y in range(brick[0][1], brick[1][1] + 1))

lower_brick = lambda brick, n: ((brick[0][0], brick[0][1], brick[0][2] - n), 
                                (brick[1][0], brick[1][1], brick[1][2] - n))

def get_support_list(l):
    to_process, base = sorted([(i, b) for i, b in enumerate(l) if 1 not in (b[0][2], b[1][2])], key=lambda x: min(x[1][0][2], x[1][1][2])), {}
    ordered_bricks, supported_by = [(i, b) for i, b in enumerate(l) if 1 in (b[0][2], b[1][2])], [set() for _ in range(len(l))]
    for i, brick in ordered_bricks:
        base.update({(x, y): (z, i) for x, y, z in xy_footprint(brick, max)})
    for brick_i, brick in to_process:
        footprint = xy_footprint(brick, min)
        relevant_base = {v for pt, v in base.items() if pt in {(i, j) for i, j, _ in footprint}}
        if relevant_base:
            max_relevant_z = max(z for z, _ in relevant_base)
            supported_by[brick_i] = {i for z, i in relevant_base if z == max_relevant_z}
        else:
            max_relevant_z = 0
        new_brick = lower_brick(brick, list(footprint)[0][2] - max_relevant_z - 1)
        ordered_bricks.append((brick_i, new_brick))
        base.update({(x, y): (z, brick_i) for x, y, z in xy_footprint(new_brick, max)})
    return supported_by

def count_removable(l):
    supported_by = get_support_list(l)
    necessary = set()
    for x in supported_by:
        if len(x) == 1:
            necessary.add(list(x)[0])
    return len(supported_by) - len(necessary)

def number_falling(index_to_remove, supported_by):
    removed, supported, changed = {index_to_remove}, [s.copy() for s in supported_by], True
    for i in range(len(supported)):
        if len(supported[i]) == 0:
            supported[i].add(-1)
    while changed:
        changed = False
        for i in range(len(supported)):
            if supported[i] & removed:
                supported[i] = supported[i] - removed
                changed = True
        removed = {index_to_remove}.union(set(i for i in range(len(supported)) if len(supported[i]) == 0))
    return len(removed) - 1

def chainreaction(l):
    supported_by = get_support_list(l)
    return sum(number_falling(i, supported_by) for i in range(len(l)))

print(count_removable(data))
print(chainreaction(data))