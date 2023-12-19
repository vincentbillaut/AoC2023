data = [x.strip() for x in open("input.txt")]

def parse_data(l):
    workflows, parts = {}, []
    for x in l:
        if x != '' and not x.startswith('{'):
            name = x.split('{')[0]
            rules = list(x.split('{')[1][:-1].split(','))
            workflows[name] = rules
        elif x != '' and x.startswith('{'):
            parts.append(eval(f"dict({x[1:-1]})"))
    return workflows, parts

def check_part(part, workflows):
    current_name = 'in'
    x, m, a, s = part['x'], part['m'], part['a'], part['s']
    while True:
        rules = workflows[current_name]
        for rule in rules:
            if ':' not in rule and rule in workflows:
                current_name = rule
                break
            elif ':' not in rule and rule not in workflows:
                return rule == 'A'
            elif eval(rule.split(':')[0]) and rule.split(':')[1] in workflows:
                current_name = rule.split(':')[1]
                break
            elif eval(rule.split(':')[0]) and rule.split(':')[1] not in workflows:
                return rule.split(':')[1] == 'A'

range_size = lambda ranges, acc=1: acc if len(ranges) == 0 else range_size(ranges[1:], acc=(ranges[0][1] - ranges[0][0]) * acc)

def do_split(ranges, var, sgn, crt):
    range_true, range_false = ranges.copy(), ranges.copy()
    bounds_var = ranges[var]
    if (sgn == '<' and crt >= bounds_var[1] - 1) or (sgn == '>' and crt <= bounds_var[0] - 1):
        return ranges.copy(), None
    elif (sgn == '<' and crt <= bounds_var[0]) or (sgn == '>' and crt >= bounds_var[1] - 1):
        return None, ranges.copy()
    elif sgn == '<':
        range_true[var] = (bounds_var[0], crt)
        range_false[var] = (crt, bounds_var[1])
    elif sgn == '>':
        range_true[var] = (crt + 1, bounds_var[1])
        range_false[var] = (bounds_var[0], crt + 1)
    return range_true, range_false


def propagate_ranges(workflows):
    ranges_list, total = [({'x': (1, 4001), 'a': (1, 4001), 'm': (1, 4001), 's': (1, 4001)}, 'in')], 0
    while ranges_list:
        ranges, wf_name = ranges_list.pop()
        if ranges is None:
            continue
        elif wf_name not in workflows:
            total += (wf_name == 'A') * range_size(list(ranges.values()))
        else:
            new_ranges = []
            rules = workflows[wf_name]
            for rule in rules:
                if ':' not in rule and rule in workflows:
                    new_ranges.append((ranges, rule))
                elif ':' not in rule and rule not in workflows:
                    total += (rule == 'A') * range_size(list(ranges.values()))
                else:  # recurrence
                    variable, sign, next_step_if_conf = rule[0], rule[1], rule.split(':')[1]
                    crit = int(rule.split(':')[0].split(sign)[1])
                    split_ranges, ranges = do_split(ranges, variable, sign, crit)
                    new_ranges.append((split_ranges, next_step_if_conf))
            ranges_list.extend(new_ranges)
    return total

workflows, parts = parse_data(data)

print(sum(sum(part.values()) for part in parts if check_part(part, workflows)))
print(propagate_ranges(workflows))