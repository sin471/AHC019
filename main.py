from typing import List


# todo:f_silhouettedとr_silhouettedをまとめられないか考える
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

xyz = [(i, j, k) for i in range(D) for j in range(D) for k in range(D)]
f_silhouetted = [[[0] * D for _ in range(D)] for _ in range(2)]
r_silhouetted = [[[0] * D for _ in range(D)] for _ in range(2)]
can_filled = [[[[0] * D for _ in range(D)] for _ in range(D)] for _ in range(2)]
b = [[0 for _ in range(D**3)] for _ in range(2)]
n = 0

for i in range(2):
    for x, y, z in xyz:
        if f[i][z][x] == 1 and r[i][z][y] == 1:
            can_filled[i][x][y][z] = 1


# 1組と2組どちらでも共通して埋めれる場所を探す
# 共通ブロック判定の基準軸を変えたときの評価値(低いほどいい)は500ケースでもy<x<zの順だった
for x in range(D):
    for z in range(D):
        y = 0
        while y < D:
            y2 = y
            while y2 < D and can_filled[0][x][y2][z] and can_filled[1][x][y2][z]:
                if y2 == y:
                    n += 1
                for i in range(2):
                    b[i][x * (D**2) + y2 * D + z] = n
                    f_silhouetted[i][z][x] = 1
                    r_silhouetted[i][z][y2] = 1
                y2 += 1
            y = y2
            y += 1

for i in range(2):
    n2 = n + 1
    for x, y, z in xyz:
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
