l = [x.strip() for x in open("input.txt")]

directions, map = l[0], {x.split(' = ')[0]: tuple(x.split(' = ')[1][1:-1].split(', ')) for x in l[2:]}

def n_steps(directions, map):
    curr, target, n = "AAA", "ZZZ", 0
    while curr != target:
        n += 1
        curr = map[curr][{'L': 0, 'R':1}[directions[(n - 1) % len(directions)]]]
    return n

def gcd(a, b):
    while b:
        t = b
        b = a % b
        a = t
    return a

lcm = lambda a, b: a // gcd(a, b) * b

def n_ghost_steps(directions, map):
    curr, n = [x for x in map if x[-1] == 'A'], 0, 
    periods, final_n = [-1] * len(curr), 1
    while -1 in periods:
        n += 1
        curr = [map[node][{'L': 0, 'R':1}[directions[(n - 1) % len(directions)]]] for node in curr]
        for i, node in enumerate(curr):
            if node[-1] == 'Z' and periods[i] == -1:
                periods[i] = n
    for p in periods:
        final_n = lcm(final_n, p)
    return final_n

print(n_steps(directions, map))
print(n_ghost_steps(directions, map))