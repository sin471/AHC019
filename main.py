D = int(input())
#Todo:中身をを01リテラル型にする
f: list[list[str]] = [[] for _ in range(2)]
r: list[list[str]] = [[] for _ in range(2)]

f_silhouetted = [[[0] * D for _ in range(D)] for _ in range(2)]
r_silhouetted = [[[0] * D for _ in range(D)] for _ in range(2)]

for i in range(2):
    for _ in range(D):
        f[i].append(input())
    for _ in range(D):
        r[i].append(input())

b = [[0 for _ in range(D**3)] for _ in range(2)]
n = 0

for i in range(2):
    for x in range(D):
        for y in range(D):
            for z in range(D):
                if not (f[i][z][x] == "1" and r[i][z][y] == "1"):
                    continue

                if f_silhouetted[i][z][x] and r_silhouetted[i][z][y]:
                    b[i][x * (D**2) + y * D + z] = 0
                    continue

                n += 1
                b[i][x * (D**2) + y * D + z] = n
                f_silhouetted[i][z][x] = 1
                r_silhouetted[i][z][y] = 1


print(n)
print(" ".join(map(str, b[0])))
print(" ".join(map(str, b[1])))
