from typing import List


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
is_overlapped = [[[0] * D for _ in range(D)] for _ in range(D)]
diff = [[1, 0, 0], [0, 1, 0], [0, 0, 1], [-1, 0, 0], [0, -1, 0], [0, 0, -1]]
b = [[0 for _ in range(D**3)] for _ in range(2)]
n = 0


for x, y, z in xyz:
    for i in range(2):
        if f[i][z][x] and r[i][z][y]:
            can_filled[i][x][y][z] = 1

    if can_filled[0][x][y][z] and can_filled[1][x][y][z]:
        is_overlapped[x][y][z] = 1


def is_inside(x: int, y: int, z: int):
    return 0 <= x < D and 0 <= y < D and 0 <= z < D


def positon_1d(x: int, y: int, z: int):
    return x * (D**2) + y * D + z


def is_silhouetted(i: int, x: int, y: int, z: int):
    return f_silhouetted[i][z][x] and r_silhouetted[i][z][y]


# silhouetted[i][x][y][z]という配列を用意すると、for文で1行埋めねばならず面倒になる
# todo:関数化したらそれでもいいかも
def silhouette(i: int, x: int, y: int, z: int):
    global f_silhouetted
    global r_silhouetted
    f_silhouetted[i][z][x] = 1
    r_silhouetted[i][z][y] = 1


# 共通した連結成分をDFSで埋める
def fill_connected_component(x: int, y: int, z: int, n: int):
    global b
    global is_overlapped
    global can_filled
    global f_silhouetted
    global r_silhouetted
    if not (is_inside(x, y, z) and is_overlapped[x][y][z]):
        return
    position = positon_1d(x, y, z)
    b[0][position] = b[1][position] = n
    is_overlapped[x][y][z] = 0
    for i in range(2):
        f_silhouetted[i][z][x] = 1
        r_silhouetted[i][z][y] = 1
        can_filled[i][x][y][z] = 0

    for dx, dy, dz in diff:
        fill_connected_component(x + dx, y + dy, z + dz, n)


for x, y, z in xyz:
    if is_overlapped[x][y][z]:
        n += 1
        fill_connected_component(x, y, z, n)


# 1x1x1のブロックで残りを埋める
n = max(*b[0], *b[1])
for i in range(2):
    n2 = n + 1
    for x, y, z in xyz:
        position = positon_1d(x, y, z)
        if is_silhouetted(i, x, y, z):
            continue
        if not can_filled[i][x][y][z]:
            continue
        if b[i][position]:
            continue

        b[i][position] = n2
        silhouette(i, x, y, z)
        n2 += 1


def output(n: int, b: List[List[int]]):
    print(n)
    print(" ".join(map(str, b[0])))
    print(" ".join(map(str, b[1])))


n = max(max(b[0]), max(b[1]))
output(n, b)
