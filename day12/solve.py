data = [(x.strip().split()[0], list(map(int,x.strip().split()[1].split(',')))) for x in open("input.txt")]

def match(row, ns):
    if len(ns) == 0:
        return '#' not in row
    n, i = ns[0], row.find('#')
    if i < 0 or i + n > len(row) or (row[i:i+n] != "#"*n 
                 and (i == 0 or row[i-1] == '.') 
                 and (i + n == len(row) or row[i + n] == '.')):
        return False
    return match(row[i+n+1:], ns[1:])

def first_n_compatible(row, n):
    i = row.find('#')  # assumes '#' will precede '?'
    return (i + n <= len(row) 
            and '.' not in row[i:i+n] 
            and (i + n == len(row) or row[i + n] != '#'))

class Solve:
    def __init__(self) -> None:
        self.cache = {}
    
    def process(self, row, ns):
        key = (row.strip('.'), ','.join(map(str,ns)))
        if key in self.cache:
            return self.cache[key]
        result = self.solve_row(row, ns)
        self.cache[key] = result
        return result

    def solve_row(self, row, ns):
        if len(row) == 0:
            return int(len(ns) == 0)
        if len(ns) == 0:
            return int('#' not in row)
        if '?' not in row:
            is_a_match = match(row, ns)
            return int(is_a_match)
        first_q, first_p, s = row.find('?'), row.find('#'), 0
        if -1 < first_p < first_q:
            if first_n_compatible(row, ns[0]):
                return self.process(row[first_p + ns[0] + 1:], ns[1:])
            else:
                return 0
        if first_n_compatible('#' + row[first_q + 1:], ns[0]):
            recur1 = self.process(row[first_q + ns[0] + 1:], ns[1:])
            s += recur1
        recur2 = self.process('.' + row[first_q + 1:], ns)
        s += recur2
        return s

print(sum(Solve().process(row, ns) for row, ns in data))
print(sum(Solve().process('?'.join([row] * 5), ns * 5) for row, ns in data))