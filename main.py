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
is_overlapped = [[[0] * D for _ in range(D)] for _ in range(D)]

b = [[0 for _ in range(D**3)] for _ in range(2)]
n = 0


for x, y, z in xyz:
    for i in range(2):
        if f[i][z][x] == 1 and r[i][z][y] == 1:
            can_filled[i][x][y][z] = 1

    if can_filled[0][x][y][z] and can_filled[1][x][y][z]:
        is_overlapped[x][y][z] = 1


# 共通した連結成分をDFSで埋める
def fill_connected_component(x: int, y: int, z: int, n: int):
    global b
    global is_overlapped
    global f_silhouetted
    global r_silhouetted
    is_inside = all(0 <= i < D for i in [x, y, z])
    position = x * (D**2) + y * D + z
    if not (is_inside and is_overlapped[x][y][z]):
        return
    b[0][position] = b[1][position] = n
    is_overlapped[x][y][z] = 0
    for i in range(2):
        f_silhouetted[i][z][x] = 1
        r_silhouetted[i][z][y] = 1

    d = [[1, 0, 0], [0, 1, 0], [0, 0, 1], [-1, 0, 0], [0, -1, 0], [0, 0, -1]]
    for dx, dy, dz in d:
        fill_connected_component(x + dx, y + dy, z + dz, n)


for x, y, z in xyz:
    if is_overlapped[x][y][z]:
        n += 1
        fill_connected_component(x, y, z, n)

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
