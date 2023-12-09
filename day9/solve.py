data = [list(map(int,x.strip().split())) for x in open("input.txt")]

def predict_extreme(l, mode='next'):
    if all(x == 0 for x in l): 
        return 0
    diffs = [l[i+1] - l[i] for i in range(len(l)-1)]
    return l[-1 if mode == 'next' else 0] + predict_extreme(diffs, mode) * (1 if mode == 'next' else -1)

print(sum(predict_extreme(l, 'next') for l in data))
print(sum(predict_extreme(l, 'previous') for l in data))