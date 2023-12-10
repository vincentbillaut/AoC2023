data = [(x.strip().split()[0], int(x.strip().split()[1])) for x in open("input.txt")]

card_order = {card: i for i, card in enumerate(['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2'])}
card_order2 = {card: i for i, card in enumerate(['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J'])}

def counter(l):
    d = {}
    for x in l:
        d[x] = d.get(x, 0) + 1
    return d

def hand_type(hand):
    counts = counter(hand)
    if 5 in counts.values():
        return 5
    if 4 in counts.values():
        return 4
    if 3 in counts.values() and 2 in counts.values():
        return 3.5
    if 3 in counts.values():
        return 3
    if 2 in counts.values() and counter(counts.values())[2] == 2:
        return 2.5
    if 2 in counts.values():
        return 2
    return 1

def hand_type2(hand):
    if 'J' not in hand:
        return hand_type(hand)
    counts = counter(hand)
    del counts['J']
    if len(counts) == 0:
        return 5
    max_count = max(counts.values())
    for c in counts:
        if counts[c] == max_count:
            return hand_type(hand.replace('J', c))

def comparison_function(hand_type_func, order_dict):
    def greater(hand1, hand2):
        type1, type2 = hand_type_func(hand1), hand_type_func(hand2)
        order1, order2 = tuple(order_dict[c] for c in hand1), tuple(order_dict[c] for c in hand2)
        return type1 > type2 or (type1 == type2 and order1 < order2)
    return greater

def sort_by_first_element(l_input, compare_func):
    n, l = len(l_input), l_input.copy()
    for i in range(n):
        for j in range(1, n - i):
            if compare_func(l[j-1][0], l[j][0]):
                temp = l[j]
                l[j] = l[j-1]
                l[j-1] = temp
    return l

print(sum(bet * (i + 1) for i, (_, bet) in enumerate(sort_by_first_element(data, comparison_function(hand_type, card_order)))))
print(sum(bet * (i + 1) for i, (_, bet) in enumerate(sort_by_first_element(data, comparison_function(hand_type2, card_order2)))))