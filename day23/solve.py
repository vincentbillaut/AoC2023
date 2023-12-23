data = [x.strip() for x in open("input.txt")]
start, end = (0, data[0].index('.')), (len(data) - 1, data[-1].index('.'))

def neighbors(i, j, l):
    n, m, coords = len(l), len(l[0]), set()
    if i > 0: coords.add((i - 1, j))
    if j > 0: coords.add((i, j - 1))
    if i < n - 1: coords.add((i + 1, j))
    if j < m - 1: coords.add((i, j + 1))
    return {(a, b) for a, b in coords if l[a][b] != '#'}

slope = lambda i, j, dir: {{'>':(i, j + 1), '<':(i, j - 1), '^':(i - 1, j), 'v':(i + 1, j)}[dir]}

def build_graph(l, no_slopes=False):
    adjacency = {}
    for i, x in enumerate(l):
        for j, c in enumerate(x):
            if c == '.':
                adjacency[(i, j)] = neighbors(i, j, l)
            elif c != '#':
                adjacency[(i, j)] = neighbors(i, j, l) if no_slopes else (neighbors(i, j, l) & slope(i, j, c))
    return adjacency

def continue_path(source, first_node, g):
    seen, node, length = {source}, first_node, 1
    next_nodes = g[node] - seen
    while len(next_nodes) == 1:
        length += 1
        seen.add(node)
        node = list(next_nodes)[0]
        next_nodes = g[node] - seen
    return node, length, seen  # destination, length, marked

def compress_ugraph(start, graph):
    new_graph, marked = {}, {start}
    node_after_start = list(graph[start])[0]
    vects = [(start, node_after_start)]
    while vects:
        source, first_node = vects.pop()
        destination, weight, seen_nodes = continue_path(source, first_node, graph)
        new_graph[source] = new_graph.get(source, set()) | {(destination, weight)}
        new_graph[destination] = new_graph.get(destination, set()) | {(source, weight)}
        marked |= seen_nodes | {destination}
        next_options = graph[destination] - marked
        for next_node in next_options:
            vects.append((destination, next_node))
    return new_graph

def explore_graph(source, target, graph, compressed=False):
    paths, lengths = [(source, {source}, 0)], []
    while paths:
        node, marked, length_so_far = paths.pop()
        if compressed: next_nodes = {(n, l) for n, l in graph[node] if n not in marked}
        else: next_nodes = {(n, 1) for n in graph[node] if n not in marked}
        for next_node, length in next_nodes:
            if next_node == target:
                lengths.append(length_so_far + length)
            else:
                paths.append((next_node, (marked | {next_node}), length_so_far + length))
    return lengths

print(max(explore_graph(start, end, build_graph(data))))

graph_part2 = build_graph(data, True)
graph_part2_compressed = compress_ugraph(start, graph_part2)

print(max(explore_graph(start, end, graph_part2_compressed, compressed=True)))