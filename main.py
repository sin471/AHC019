from typing import List
#todo:共通部分を上下ではなく縦または横で探す
#todo:f_silhouettedとr_silhouettedをまとめられないか考える
def input_():
    D = int(input())
    f: List[List[List[int]]] = [[] for _ in range(2)]
    r: List[List[List[int]]] = [[] for _ in range(2)]

    for i in range(2):
        for _ in range(D):
            f[i].append(list(map(int, input())))
        for _ in range(D):
            r[i].append(list(map(int, input())))

    return D, f, r


D, f, r = input_()

f_silhouetted = [[[0] * D for _ in range(D)] for _ in range(2)]
r_silhouetted = [[[0] * D for _ in range(D)] for _ in range(2)]
can_filled = [[[[0] * D for _ in range(D)] for _ in range(D)] for _ in range(2)]

b = [[0 for _ in range(D**3)] for _ in range(2)]
n = 0

for i in range(2):
    for x in range(D):
        for y in range(D):
            for z in range(D):
                if f[i][z][x] == 1 and r[i][z][y] == 1:
                    can_filled[i][x][y][z] = 1


# 1組と2組どちらでも共通して埋めれる場所を探す
for x in range(D):
    for y in range(D):
        z = 0
        while z < D:
            z2 = z
            while z2 < D and can_filled[0][x][y][z2] and can_filled[1][x][y][z2]:
                if z2 == z:
                    n += 1
                for i in range(2):
                    b[i][x * (D**2) + y * D + z2] = n
                    f_silhouetted[i][z][x] = 1
                    r_silhouetted[i][z][y] = 1
                z2 += 1
            z = z2
            z += 1

for i in range(2):
    n2 = n + 1
    for x in range(D):
        for y in range(D):
            for z in range(D):
                if f_silhouetted[i][z][x] and r_silhouetted[i][z][y]:
                    continue
                if not can_filled[i][x][y][z]:
                    continue
                if b[i][x * (D**2) + y * D + z]:
                    continue

                b[i][x * (D**2) + y * D + z] = n2
                f_silhouetted[i][z][x] = 1
                r_silhouetted[i][z][y] = 1
                n2 += 1


def output(n: int, b: List[List[int]]):
    print(n)
    print(" ".join(map(str, b[0])))
    print(" ".join(map(str, b[1])))


n = max(max(b[0]), max(b[1]))
output(n, b)
