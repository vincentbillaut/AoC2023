import sys
input_n = "" if len(sys.argv) == 1 else sys.argv[1]

data = [(s[0], int(s[1]), s[2][1:-1]) for x in open(f"input{input_n}.txt") if (s := x.strip().split())]
instructions = [(x[0], x[1]) for x in data]
instructions2 = [(['R','D','L','U'][int(x[2][-1])], int(x[2][1:-1], base=16)) for x in data]

class FactorizedWeightMap:
    def __init__(self, i_weights, j_weights, offsets=(0, 0)) -> None:
        self.i_weights = i_weights
        self.j_weights = j_weights
        self.set_offsets(offsets)

    def set_offsets(self, offsets):
        self.i_offset = offsets[0]
        self.j_offset = offsets[1]
    
    def get(self, pair, default=0):
        if pair[0]  + self.i_offset == -1 or pair[1]  + self.j_offset == -1:
            return 0
        if pair[0]  + self.i_offset == len(self.i_weights) or pair[1]  + self.j_offset == len(self.j_weights):
            return 0
        if 0 <= pair[0]  + self.i_offset < len(self.i_weights) and 0 <= pair[1]  + self.j_offset < len(self.j_weights):
            return self.i_weights[pair[0] + self.i_offset] * self.j_weights[pair[1] + self.j_offset]
        raise KeyError

def move(i, j, dir, n_steps=1):
    d = {
        'U': (i - n_steps, j),
        'D': (i + n_steps, j),
        'R': (i, j + n_steps),
        'L': (i, j - n_steps),
    }
    return d[dir]

def count_interior_row(r, i, weight_map={}):
    count, wall_count, prev_wall = 0, 0, None
    for j, c in enumerate(r):
        if c == '.':
            try:
                count += (wall_count % 2) * weight_map.get((i, j - 1), 1)
            except Exception as e:
                print(r, j, len(r))
                raise e
            prev_wall = None
        elif c in ('U', 'D'):
            if prev_wall is None:
                wall_count += 1
                prev_wall = c
            else:
                wall_count += int(prev_wall != c)
                prev_wall = None
    return count

def lagoon_contour(l):
    i, j, visited = 0, 0, {}
    for inst_i, (dir, n) in enumerate(l):
        for k in range(n):
            if dir in ('U', 'D'):
                character = dir
            elif k == 0:
                character = l[(inst_i - 1) % len(l)][0]
            else:
                character = dir
            visited[(i, j)] = character
            i, j = move(i, j, dir)
    return visited

def dict_interior(d, weight_map={}):
    mini, maxi = min(i for i, _ in d), max(i for i, _ in d)
    minj, maxj = min(j for _, j in d), max(j for _, j in d)
    count = 0
    for i in range(mini - 1, maxi + 1):
        row_string = ''.join(['.' if (i, j) not in d else d[(i, j)] for j in range(minj - 1, maxj + 1)])
        count += count_interior_row(row_string, i, weight_map)
    return count

def full_dig_size(l, weight_map={}):
    s = lagoon_contour(l)
    mini, minj = min(i for i, _ in s), min(j for _, j in s)
    if weight_map != {}: weight_map.set_offsets((-mini, 0))
    return sum(weight_map.get((x[0], x[1] - minj), 1) for x in s) + dict_interior(s, weight_map)

def compute_edges(l):
    i, j, edges = 0, 0, []
    for dir, n in l:
        edges.append((i, j, dir, n))
        i, j = move(i, j, dir, n)
    return edges

def full_dig_size_opti(l):
    edges = compute_edges(l)
    i_vals, j_vals = list(sorted(set(i for i, _, _, _ in edges))), list(sorted(set(j for _, j, _, _ in edges)))
    new_instructions = []
    for i, j, dir, n in edges:
        ni, nj = move(i, j, dir, n)
        start_loc = (i_vals.index(i)) if dir in ('U', 'D') else (j_vals.index(j))
        end_loc = (i_vals.index(ni)) if dir in ('U', 'D') else (j_vals.index(nj))
        new_instructions.append((dir, abs(end_loc - start_loc) * 2))  # operational version
    # make weight_map
    i_weights, j_weights = [1] * (len(i_vals) * 2 - 1), [1] * (len(j_vals) * 2 - 1)
    for i_rank in range(len(i_vals) - 1):
        i_weights[1 + 2*i_rank] = i_vals[i_rank + 1] - i_vals[i_rank] - 1
    for j_rank in range(len(j_vals) - 1):
        j_weights[1 + 2*j_rank] = j_vals[j_rank + 1] - j_vals[j_rank] - 1
    weight_map = FactorizedWeightMap(i_weights, j_weights)
    return full_dig_size(new_instructions, weight_map)


print(full_dig_size(instructions))
# print(full_dig_size_opti(instructions))
print(full_dig_size_opti(instructions2))
