l = [x.strip() for x in open("input.txt")]

seeds = list(map(int, l[0].split(': ')[1].split()))
maps, buf = [], None
for row in l[1:]:
    if row == '' and buf is not None:
        maps.append(buf)
        buf = []
    elif 'map' in row:
        buf = []
    elif row != '':
        buf.append(tuple(map(int, row.split())))
maps.append(buf)

def find_location(seed):
    loc = seed
    for map in maps:
        triplet = 0
        d, s, l = map[triplet]
        while (not s <= loc <= s + l) and triplet < len(map) - 1:
            triplet += 1
            d, s, l = map[triplet]
        if s <= loc <= s + l:
            loc = d + loc - s
    return loc

print(min(find_location(seed) for seed in seeds)) # question 1

ranges = [(seeds[2*i], seeds[2*i+1]) for i in range(len(seeds)//2)]

def next_ranges(ranges, map):
    if len(ranges) == 0:
        return []
    start, length = ranges.pop()
    sorted_triplets = sorted(map, key=lambda x:x[1])
    for d, s, l in sorted_triplets:
        if s > start:
            if s - start > length:
                return [(start, length)] + next_ranges(ranges, map)
            else:
                return [(start, s - start)] + next_ranges([(s, length - s + start)] + ranges, map)
        elif s <= start < s + l:
            if length < l - start + s:
                return [(d + start - s, length)] + next_ranges(ranges, map)
            else:
                return [(d + start - s, l - start + s)] + next_ranges([(s + l, length - l + start - s)] + ranges, map)
    return [(start, length)] + next_ranges(ranges, map)

def run_all(ranges, maps):
    for map in maps:
        ranges = next_ranges(ranges, map)
    return min(range[0] for range in ranges)

print(run_all(ranges, maps)) # question 2