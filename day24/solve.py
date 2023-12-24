from sympy import Symbol, nonlinsolve

data = [(list(map(int, x.split(' @ ')[0].split(', '))), 
         list(map(int, x.split(' @ ')[1].split(', ')))) for x in open("input.txt")]

get_eq_xy = lambda p, v: (v[1]/v[0], p[1] - p[0] * v[1] / v[0])

def count_intersections(l, xy_min, xy_max):
    count = 0
    for i in range(len(l)):
        for j in range(i + 1, len(l)):
            a1, b1 = get_eq_xy(*l[i])
            a2, b2 = get_eq_xy(*l[j])
            assert a1 != a2 or b1 != b2
            if a1 != a2:
                x_int = (b2 - b1) / (a1 - a2)
                y_int = a1 * x_int + b1
                forward = ((x_int - l[i][0][0]) * l[i][1][0] >= 0
                           and (x_int - l[j][0][0]) * l[j][1][0] >= 0)
                if (xy_min <= x_int <= xy_max 
                    and xy_min <= y_int <= xy_max
                    and forward):
                    count += 1
    return count

def solve(l):
    x, y, z, vx, vy, vz = Symbol('x'), Symbol('y'), Symbol('z'), Symbol('vx'), Symbol('vy'), Symbol('vz')
    t = [Symbol(f"t{i}", positive=True) for i in range(len(l))]
    f = []
    for i in range(len(l)):
        f.append(x - l[i][0][0] + t[i] * (vx - l[i][1][0]))
        f.append(y - l[i][0][1] + t[i] * (vy - l[i][1][1]))
        f.append(z - l[i][0][2] + t[i] * (vz - l[i][1][2]))
    solutions = nonlinsolve(tuple(f[:(6 + len(l))]), (x, y, z, vx, vy, vz, *t))
    return sum(list(solutions)[0][:3])

print(count_intersections(data, 200000000000000, 400000000000000))
print(solve(data[:5]))