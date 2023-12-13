patterns = [[x.strip() for x in patt.split('\n')] for patt in open("input.txt").read().split('\n\n')]

def compare_two_rows_max_2(row1, row2):
    c = 0
    for c1, c2 in zip(row1, row2):
        if c > 1: return 2
        if c1 != c2: c += 1
    return c

def find_row_reflection(patt, target):
    starting_points = [i for i in range(len(patt) - 1) if compare_two_rows_max_2(patt[i], patt[i+1]) < 2]
    for i in starting_points:
        cum_diff, offset = 0, 0
        while (i - offset >= 0 
               and i + 1 + offset < len(patt) 
               and cum_diff <= target):
            cum_diff += compare_two_rows_max_2(patt[i - offset], patt[i + 1 + offset])
            offset += 1
        if cum_diff == target:
            return i + 1
    return None

def solve_pattern(patt, target):
    row_reflection = find_row_reflection(patt, target)
    if row_reflection is not None:
        return 100 * row_reflection
    return find_row_reflection([''.join([patt[i][j] for i in range(len(patt))]) for j in range(len(patt[0]))], target)

print(sum(solve_pattern(patt, 0) for patt in patterns))
print(sum(solve_pattern(patt, 1) for patt in patterns))