data = open("input.txt").read().strip()
hash = lambda s, acc=0: acc if s == '' else hash(s[1:], ((acc + ord(s[0])) * 17) % 256)

def process_instruction(inst, state):
    new_state = {k: v.copy() for k, v in state.items()}
    label = inst[:-2] if '=' in inst else inst[:-1]
    box_i, op = hash(label), '=' if '=' in inst else '-'
    if op == '-':
        if box_i in new_state:
            new_state[box_i] = [lens for lens in new_state[box_i] if lens[0] != label]
    else:
        focal = int(inst[-1])
        if box_i not in new_state:
            new_state[box_i] = [(label, focal)]
        else:
            labels_present = [lens[0] for lens in new_state[box_i]]
            if label in labels_present:
                new_state[box_i][labels_present.index(label)] = (label, focal)
            else:
                new_state[box_i].append((label, focal))
    return new_state

def process(inst_l):
    state = {}
    for inst in inst_l.split(','):
        state = process_instruction(inst, state)
    return state

total_focusing_power = lambda state: sum((i+1) * sum((k+1) * lens[1] for k, lens in enumerate(l)) for i, l in state.items())

print(sum(hash(inst) for inst in data.split(',')))
print(total_focusing_power(process(data)))