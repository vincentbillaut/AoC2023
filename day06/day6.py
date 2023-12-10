l = [x.strip() for x in open("input.txt")]

times, distances = list(map(int, l[0].split(':')[1].split())), list(map(int, l[1].split(':')[1].split()))
single_time, single_distance = int(''.join(c for c in l[0] if c.isdigit())), int(''.join(c for c in l[1] if c.isdigit()))

delta = lambda t, record: (t ** 2 - 4 * record) ** .5

def solve(t, record):
    x1, x2 = (t - delta(t, record)) / 2, (t + delta(t, record)) / 2
    x1, x2 = int(x1 + 1), int(x2) if x2 != int(x2) else x2 - 1
    return x2 - x1 + 1

product = lambda lst: (solve(*lst[0])) * product(lst[1:]) if len(lst) else 1

print(product(list(zip(times, distances))))
print(solve(single_time, single_distance))