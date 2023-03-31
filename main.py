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

xyz = [(x, y, z) for x in range(D) for y in range(D) for z in range(D)]
diff = [[1, 0, 0], [0, 1, 0], [0, 0, 1], [-1, 0, 0], [0, -1, 0], [0, 0, -1]]
b = [[0 for _ in range(D**3)] for _ in range(2)]
block_id = 0

f_silhouetted = [[[0] * D for _ in range(D)] for _ in range(2)]
r_silhouetted = [[[0] * D for _ in range(D)] for _ in range(2)]
can_filled = [[[[0] * D for _ in range(D)] for _ in range(D)] for _ in range(2)]
is_overlapped = [[[0] * D for _ in range(D)] for _ in range(D)]


for x, y, z in xyz:
    for i in range(2):
        if f[i][z][x] and r[i][z][y]:
            can_filled[i][x][y][z] = 1

    if can_filled[0][x][y][z] and can_filled[1][x][y][z]:
        is_overlapped[x][y][z] = 1


def can_fill(x: int, y: int, z: int, i: int = 0):
    is_inside = 0 <= x < D and 0 <= y < D and 0 <= z < D
    return is_inside and can_filled[i][x][y][z]


def positon_1d(x: int, y: int, z: int):
    return x * (D**2) + y * D + z


def max_2d(lis: List[List]):
    return max(map(lambda inner: max(inner), lis))


def is_silhouetted(i: int, x: int, y: int, z: int):
    return f_silhouetted[i][z][x] and r_silhouetted[i][z][y]


def silhouette(i: int, x: int, y: int, z: int):
    global f_silhouetted
    global r_silhouetted
    f_silhouetted[i][z][x] = 1
    r_silhouetted[i][z][y] = 1


# 共通した連結成分をDFSで埋める
def fill_connected_component(x: int, y: int, z: int, block_id: int):
    global b
    global is_overlapped
    global can_filled
    global f_silhouetted
    global r_silhouetted
    if not (can_fill(x, y, z) and is_overlapped[x][y][z]):
        return
    position = positon_1d(x, y, z)
    b[0][position] = b[1][position] = block_id
    is_overlapped[x][y][z] = 0
    for i in range(2):
        silhouette(i, x, y, z)
        can_filled[i][x][y][z] = 0

    for dx, dy, dz in diff:
        fill_connected_component(x + dx, y + dy, z + dz, block_id)


for x, y, z in xyz:
    if is_overlapped[x][y][z]:
        # 隣接した共通ブロックがあるとき(1x1x1でないとき)のみ埋める
        for dx, dy, dz in diff:
            x2, y2, z2 = x + dx, y + dy, z + dz
            if can_fill(x2, y2, z2) and is_overlapped[x2][y2][z2]:
                block_id += 1
                fill_connected_component(x, y, z, block_id)
                break
# TODO:先に2x2x1の正方形で埋める
# L字型の体積3のブロックで埋める
for i in range(2):
    block_id2 = block_id + 1
    for x, y, z in xyz:
        if is_silhouetted(i, x, y, z) or not can_fill(x, y, z, i):
            continue
        for (dx1, dy1, dz1), (dx2, dy2, dz2) in zip(diff, [diff[-1]] + diff[:-1]):
            x2, y2, z2 = x + dx1, y + dy1, z + dz1
            x3, y3, z3 = x + dx2, y + dy2, z + dz2
            if not (can_fill(x2, y2, z2, i) and can_fill(x3, y3, z3, i)):
                continue

            can_filled[i][x][y][z] = 0
            can_filled[i][x2][y2][z2] = 0
            can_filled[i][x3][y3][z3] = 0
            silhouette(i, x, y, z)
            silhouette(i, x2, y2, z2)
            silhouette(i, x3, y3, z3)
            b[i][positon_1d(x, y, z)] = block_id2
            b[i][positon_1d(x2, y2, z2)] = block_id2
            b[i][positon_1d(x3, y3, z3)] = block_id2
            block_id2 += 1
            break


def equalize_block_cnt_to_fewer():
    global b
    global f_silhouetted
    global r_silhouetted
    more = 0 if max(b[0]) > max(b[1]) else 1
    fewer_max = min(max(b[0]), max(b[1]))
    for x, y, z in xyz:
        position = positon_1d(x, y, z)
        if b[more][position] > fewer_max:
            b[more][position] = 0
            can_filled[more][x][y][z] = 1

            r_silhouette_faded = any(b[more][positon_1d(x2, y, z)] for x2 in range(D))
            f_silhouette_faded = any(b[more][positon_1d(x, y2, z)] for y2 in range(D))
            r_silhouetted[more][z][y] = int(r_silhouette_faded)
            f_silhouetted[more][z][x] = int(f_silhouette_faded)


# 体積3のL字ブロックの数が多い方の組(more)を少ない方の組に合わせる
equalize_block_cnt_to_fewer()

# TODO:block_idのうまいやり方を考える
block_id = max_2d(b)

# 2x1x1の形のブロックでシルエットがまだない部分をできるだけ埋める(A組,B組のブロック数の違いは一旦無視してあとで調整)
for i in range(2):
    block_id2 = block_id + 1
    for x, y, z in xyz:
        if is_silhouetted(i, x, y, z) or not can_fill(x, y, z, i):
            continue

        for dx, dy, dz in diff:
            x2, y2, z2 = x + dx, y + dy, z + dz
            if not can_fill(x2, y2, z2, i):
                continue

            can_filled[i][x][y][z] = 0
            can_filled[i][x2][y2][z2] = 0
            silhouette(i, x, y, z)
            silhouette(i, x2, y2, z2)
            b[i][positon_1d(x, y, z)] = block_id2
            b[i][positon_1d(x2, y2, z2)] = block_id2
            block_id2 += 1
            break

# 2x1x1ブロックの数が多い方の組を少ない方の組に合わせる
equalize_block_cnt_to_fewer()

# 1x1x1のブロックで残りを埋める
block_id = max_2d(b)
for i in range(2):
    block_id2 = block_id + 1
    for x, y, z in xyz:
        position = positon_1d(x, y, z)
        if not can_fill(x, y, z, i):
            continue
        if b[i][position] == 0 and not is_silhouetted(i, x, y, z):
            b[i][position] = block_id2
            silhouette(i, x, y, z)
            block_id2 += 1


def output(n: int, b: List[List[int]]):
    print(n)
    print(" ".join(map(str, b[0])))
    print(" ".join(map(str, b[1])))


n = max_2d(b)
output(n, b)
