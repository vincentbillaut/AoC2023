with open("input.txt") as f:
    l = [x.strip() for x in f.readlines()]

digits = [[c for c in x if c in '0123456789'] for x in l]
values = [int(d[0] + d[-1]) for d in digits]

print(sum(values))  # question 1

numbers = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
get_positions = lambda s, ref: [(-1 if n not in s else s.find(n)) for n in ref]

def first_digit_or_spelled_out(s, n_list):
    digits, positions = [(i, int(c)) for i, c in enumerate(s) if c in '0123456789'], [(pos, i + 1) for i, pos in enumerate(get_positions(s, n_list))]
    first_digit = digits[0]
    first_spelled_out = min([(pos, v) for pos, v in positions if pos > -1], key=lambda pair: pair[0], default=(-1, None))
    if first_spelled_out[1] is not None and first_spelled_out[0] < first_digit[0]:
        return first_spelled_out[1]
    return first_digit[1]

print(sum([first_digit_or_spelled_out(s, numbers) * 10 + first_digit_or_spelled_out(s[::-1], [n[::-1] for n in numbers]) for s in l])) # question 2