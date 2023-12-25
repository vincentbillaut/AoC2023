import networkx as nx

data = [(s.split(':')[0], s.split(':')[1].split()) for x in open("input.txt") if (s := x.strip())]

def build_graph_nx(l):
    G = nx.Graph()
    for source, dests in l:
        G.add_edges_from((source, dest) for dest in dests)
    return G

def solve_nx(l):
    graph = build_graph_nx(l)
    betweenness_centrality = nx.edge_betweenness_centrality(graph)
    edges_to_remove = sorted(betweenness_centrality, key=lambda e: betweenness_centrality[e], reverse=True)[:3]
    graph.remove_edges_from(edges_to_remove)
    components_lengths = [len(component) for component in nx.connected_components(graph)]
    return components_lengths[0] * components_lengths[1]

print(solve_nx(data))