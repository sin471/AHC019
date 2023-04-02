from copy import deepcopy
from itertools import permutations
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


# block_sampleはblockを構成する任意の1単位ブロックを[0,0,0]とした[dx,dy,dz]のベクトルで表現する
# 手前にあるブロックほど先に試行されるので、体積の大きいブロックをlistの手前に置く
block_samples = [
    # 3x3x3型
    [
        [-1, -1, -1],
        [-1, -1, 0],
        [-1, -1, 1],
        [-1, 0, -1],
        [-1, 0, 0],
        [-1, 0, 1],
        [-1, 1, -1],
        [-1, 1, 0],
        [-1, 1, 1],
        [0, -1, -1],
        [0, -1, 0],
        [0, -1, 1],
        [0, 0, -1],
        [0, 0, 0],
        [0, 0, 1],
        [0, 1, -1],
        [0, 1, 0],
        [0, 1, 1],
        [1, -1, -1],
        [1, -1, 0],
        [1, -1, 1],
        [1, 0, -1],
        [1, 0, 0],
        [1, 0, 1],
        [1, 1, -1],
        [1, 1, 0],
        [1, 1, 1],
    ],
    # 3x3x2型
    [
        [-1, -1, 0],
        [-1, -1, 1],
        [-1, 0, 0],
        [-1, 0, 1],
        [-1, 1, 0],
        [-1, 1, 1],
        [0, -1, 0],
        [0, -1, 1],
        [0, 0, 0],
        [0, 0, 1],
        [0, 1, 0],
        [0, 1, 1],
        [1, -1, 0],
        [1, -1, 1],
        [1, 0, 0],
        [1, 0, 1],
        [1, 1, 0],
        [1, 1, 1],
    ],
    # 3x2x2
    [
        [-1, -1, -1],
        [-1, -1, 0],
        [-1, 0, -1],
        [-1, 0, 0],
        [0, -1, -1],
        [0, -1, 0],
        [0, 0, -1],
        [0, 0, 0],
        [1, -1, -1],
        [1, -1, 0],
        [1, 0, -1],
        [1, 0, 0],
    ],
    # 3x3x1
    [
        [-1, -1, 0],
        [-1, 0, 0],
        [-1, 1, 0],
        [0, -1, 0],
        [0, 0, 0],
        [0, 1, 0],
        [1, -1, 0],
        [1, 0, 0],
        [1, 1, 0],
    ],
    # 2x2x2
    [
        [-1, -1, -1],
        [-1, -1, 0],
        [-1, 0, -1],
        [-1, 0, 0],
        [0, -1, -1],
        [0, -1, 0],
        [0, 0, -1],
        [0, 0, 0],
    ],
    # 3x2x1
    [[-1, -1, -1], [-1, 0, -1], [0, -1, -1], [0, 0, -1], [1, -1, -1], [1, 0, -1]],
    # 2x2x1形ブロック
    [
        [1, 1, 0],
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 0],
    ],
    # 体積4,T字型ブロック
    [[1, 0, 0], [0, 1, 0], [-1, 0, 0], [0, 0, 0]],
    # 体積3,L字型ブロック
    [[1, 0, 0], [0, 1, 0], [0, 0, 0]],
    # 3x1x1型ブロック
    [[1, 0, 0], [0, 0, 0], [-1, 0, 0]],
    # 2x1x1型ブロック
    [[1, 0, 0], [0, 0, 0]],
]


def generate_rotated_blocks(block_samples: List[List[List[int]]]):
    """
    block_samples内の
    block_sample一つにつき、同じ形で、回転させた24パターンのblockを生成する
    """

    def shuffle(block_sample: List[List[int]], string: str):
        block_sample2 = deepcopy(block_sample)
        for i in range(len(block_sample2)):
            for j in range(3):
                # ord(x)=120
                block_sample2[i][ord(string[j]) - 120] = block_sample[i][j]

        return block_sample2

    signs = [[1, 1, 1], [-1, -1, 1], [1, -1, -1], [-1, 1, -1]]
    blocks: List[List[List[List[int]]]] = []

    for block_sample in block_samples:
        inner_blocks: List[List[List[int]]] = []

        for i in permutations("xyz"):
            block_sample = shuffle(block_sample, "".join(i))

            for sx, sy, sz in signs:
                inner_blocks.append(
                    list(map(lambda x: [sx * x[0], sy * x[1], sz * x[2]], block_sample))
                )
        blocks.append(inner_blocks)

    return blocks


blocks = generate_rotated_blocks(block_samples)
for block in blocks:
    for i in range(2):
        block_id2 = block_id + 1
        for x, y, z in xyz:
            if is_silhouetted(i, x, y, z) or not can_fill(x, y, z, i):
                continue
            for rotated_block in block:
                if not all(
                    can_fill(x + dx, y + dy, z + dz, i) for dx, dy, dz in rotated_block
                ):
                    continue
                for dx, dy, dz in rotated_block:
                    can_filled[i][x + dx][y + dy][z + dz] = 0
                    silhouette(i, x + dx, y + dy, z + dz)
                    b[i][positon_1d(x + dx, y + dy, z + dz)] = block_id2

                block_id2 += 1
                break
    equalize_block_cnt_to_fewer()
    block_id = max_2d(b)

# 1x1x1のブロックで残りを埋める
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
