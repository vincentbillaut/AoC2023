import sys
input_n = "" if len(sys.argv) == 1 else sys.argv[1]

data = [x.strip() for x in open(f"input{input_n}.txt")]

def parse_node(r):
    node = r.split(' -> ')[0]
    type = {'b': 'broadcaster', '%': 'flipflop', '&': 'conjunction'}[node[0]]
    name = 'broadcaster' if type == 'broadcaster' else node[1:]
    destination_nodes = r.split(' -> ')[1].split(', ')
    return type, name, destination_nodes

class Node:
    def __init__(self, name, destin_nodes) -> None:
        self.destination_nodes = destin_nodes
        self.name = name

    def receive(self, pulse, input_node=None):
        raise NotImplementedError

class Flipflop(Node):
    def __init__(self, name, destin_nodes) -> None:
        super().__init__(name, destin_nodes)
        self.state = 0  # off

    def receive(self, pulse, input_node):
        if not pulse:
            self.state = 1 - self.state
            return [(self.state, node, self.name) for node in self.destination_nodes]
        return []
    
    def __repr__(self) -> str:
        return f"{self.name}: Flipflop(state = {self.state}, dest = {self.destination_nodes})"
    
class Conjunction(Node):
    def __init__(self, name, destin_nodes, input_nodes) -> None:
        super().__init__(name, destin_nodes)
        self.input_nodes = input_nodes
        self.input_states = {node: 0 for node in self.input_nodes}

    def receive(self, pulse, input_node):
        self.input_states[input_node] = pulse
        out_pulse = 1 - int(all(state for state in self.input_states.values()))
        return [(out_pulse, node, self.name) for node in self.destination_nodes]
    
    def __repr__(self) -> str:
        return f"{self.name}: Conjunction(states = {self.input_states}, dest = {self.destination_nodes})"
    
class Broadcaster(Node):
    def __init__(self, name, destin_nodes) -> None:
        super().__init__(name, destin_nodes)

    def receive(self, pulse, input_node):
        return [(pulse, node, self.name) for node in self.destination_nodes]
    
    def __repr__(self) -> str:
        return f"{self.name}: Broadcaster(dest = {self.destination_nodes})"

def process_nodes(l):
    nodes = {name: (type, name, destination_nodes) for type, name, destination_nodes in [parse_node(r) for r in l]}
    input_nodes = {}
    for name in nodes:
        for node in nodes[name][2]:
            input_nodes[node] = input_nodes.get(node, []) + [name]
    node_objects = {}
    for name in nodes:
        if nodes[name][0] == 'flipflop':
            node_objects[name] = Flipflop(name, nodes[name][2])
        elif nodes[name][0] == 'conjunction':
            node_objects[name] = Conjunction(name, nodes[name][2], input_nodes[name])
        elif nodes[name][0] == 'broadcaster':
            node_objects[name] = Broadcaster(name, nodes[name][2])
        else:
            raise NameError
    return node_objects

def run_simulation(l, n=1):
    counts = [0, 0]
    nodes = process_nodes(l)
    for _ in range(n):
        orders = [(0, 'broadcaster', None)]
        while orders:
            pulse, to_node, from_node = orders[0]
            counts[pulse] += 1
            if to_node in nodes:
                orders = orders[1:] + nodes[to_node].receive(pulse, from_node)
            else:
                orders = orders[1:]
    return counts[0] * counts[1]

def gcd(a, b):
    while b:
        t = b
        b = a % b
        a = t
    return a

lcm = lambda a, b: a // gcd(a, b) * b

def start_machine(l):
    nodes = process_nodes(l)
    lg_sources = nodes['lg'].input_nodes
    iterations = {source: set() for source in lg_sources}
    for i in range(40000):
        orders = [(0, 'broadcaster', None)]
        while orders:
            for node, v in nodes['lg'].input_states.items():
                if v:
                    iterations[node].add(i + 1)
            pulse, to_node, from_node = orders[0]
            if to_node in nodes:
                orders = orders[1:] + nodes[to_node].receive(pulse, from_node)
            else:
                orders = orders[1:]
    res = 1
    for source in lg_sources:
        res = lcm(res, min(iterations[source]))
    return res


print(run_simulation(data, 1000))
print(start_machine(data))