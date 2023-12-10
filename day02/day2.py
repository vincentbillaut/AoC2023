with open("input.txt") as f:
    l = [x.strip() for x in f.readlines()]

def parse_game(s):
    split = s.split(': ')
    game_id, samples = int(split[0][5:]), split[1].split('; ')
    all_sample_dicts = []
    for sample in samples:
        colors = sample.split(', ')
        sample_dict = {}
        for color in colors:
            n_color = color.split(' ')
            n, color = int(n_color[0]), n_color[1]
            sample_dict[color] = n
        all_sample_dicts.append(sample_dict)
    return game_id, all_sample_dicts

satisfies_constraint = lambda sample_dicts, const_dict: all(not any([sample_dict[color] > const_dict.get(color, 0) for color in sample_dict]) for sample_dict in sample_dicts)
print(sum(game_id for game_id, sample_dicts in [parse_game(game) for game in l] if satisfies_constraint(sample_dicts, {'red': 12, 'green': 13, 'blue': 14})))

def power(sample_dicts):
    max_dict, p = {}, 1
    for sample_dict in sample_dicts:
        for color in sample_dict:
            max_dict[color] = max(max_dict.get(color, 0), sample_dict[color])
    for v in max_dict.values():
        p *= v
    return p

print(sum(power(parse_game(game)[1]) for game in l))