data = [x.strip() for x in open("input.txt")]

load = lambda l: sum((len(l) - i) * x.count('O') for i, x in enumerate(l))
hash_data = lambda data: '\n'.join(data)

def slide_north(l):
    new_field = [list(x.replace('O', '.')) for x in l]
    for j in range(len(l[0])):
        column = ''.join([l[i][j] for i in range(len(l))])
        free_sections = column.split('#')
        new_column = '#'.join([''.join(sorted(sect, reverse=True)) for sect in free_sections])
        for i in range(len(l)):
            new_field[i][j] = new_column[i]
    return [''.join(x) for x in new_field]

def cycle(l_input):
    l = l_input.copy()
    for _ in range(4):
        l = slide_north(l)
        l = [''.join(l[len(l) - 1 - i][j] for i in range(len(l))) for j in range(len(l[0]))]
    return l

def cycle_n(l_input, n):
    memory, loads = {hash_data(l_input)}, [load(l_input)]
    l = cycle(l_input)
    while hash_data(l) not in memory:
        memory.add(hash_data(l))
        loads.append(load(l))
        l = cycle(l)
    period = len(memory)
    return loads[n % period]

print(load(slide_north(data)))
print(cycle_n(data, 1000000000))