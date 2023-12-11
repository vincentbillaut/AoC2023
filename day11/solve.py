data = []
for i, x in enumerate(open("input.txt")):
    data.extend([(i, j) for j, c in enumerate(x) if c == '#'])
n, m = i + 1, len(x)

def compute_sum_shortest_distances(l, multiple=2):
    rows, columns = set(i for i, _ in l), set(j for _, j in l)
    missing_rows, missing_columns = set(range(n)) - rows, set(range(m)) - columns
    s = 0
    for i in range(len(l)):
        for j in range(i + 1, len(l)):
            dist = abs(l[i][0] - l[j][0]) + abs(l[i][1] - l[j][1])
            dist += (multiple - 1) * len([r for r in missing_rows if min(l[i][0], l[j][0]) < r < max(l[i][0], l[j][0])])
            dist += (multiple - 1) * len([c for c in missing_columns if min(l[i][1], l[j][1]) < c < max(l[i][1], l[j][1])])
            s += dist
    return s

print(compute_sum_shortest_distances(data))
print(compute_sum_shortest_distances(data, 1000000))
