l = [x.strip() for x in open("input.txt")]
n, m = len(l), len(l[0])

def get_numbers(row):
    res, s, start = [], "", None
    for i, c in enumerate(row):
        if c.isdigit():
            s += c
            start = start if start is not None else i
        elif s != "":
            res.append((start, i, int(s)))
            start, s = None, ""
    if s != "":
        res.append((start, i, int(s)))
    return res

def adjacent_nondigit_nonperiod_chars(i, a, b):
    bounds_i = max(0, i-1), min(n-1, i+1) + 1
    bounds_j = max(0, a-1), min(m-1, b+1)
    s = ""
    for row_i in l[bounds_i[0]:bounds_i[1]]:
        s += row_i[bounds_j[0]:bounds_j[1]]
    return set(s) - set('1234567890.')

def stars_touching(i, a, b):
    bounds_i = max(0, i-1), min(n-1, i+1) + 1
    bounds_j = max(0, a-1), min(m-1, b+1)
    stars = []
    for i in range(*bounds_i):
        for j in range(*bounds_j):
            if l[i][j] == '*':
                stars.append((i, j))
    return stars

print(sum(sum(number for a, b, number in get_numbers(row) if adjacent_nondigit_nonperiod_chars(i, a, b)) for i, row in enumerate(l))) # question 1

stars = {}
for i, row in enumerate(l):
    for a, b, number in get_numbers(row):
        for star in stars_touching(i, a, b):
            stars[star] = stars.get(star, []) + [number]
gear_ratii = 0
for star in stars:
    if len(stars[star]) == 2:
        gear_ratii += stars[star][0] * stars[star][1]

print(gear_ratii) # question 2