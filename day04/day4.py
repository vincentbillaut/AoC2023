l = [x.strip() for x in open("input.txt")]

def parse_card(s):
    content = s.split(': ')[1]
    ref = list(map(int, content.split(' | ')[0].split()))
    ticket = list(map(int, content.split(' | ')[1].split()))
    return ref, ticket

print(sum(2 ** (len(set(ref) & set(ticket)) - 1) for ref, ticket in [parse_card(card) for card in l] if (set(ref) & set(ticket))))

counts = [1] * len(l)
for i in range(len(l)):
    ref, ticket = parse_card(l[i])
    matches = len(set(ref) & set(ticket))
    for k in range(1, matches + 1):
        if i + k < len(l):
            counts[i + k] += counts[i]

print(sum(counts))