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

f_silhouetted = [[[0] * D for _ in range(D)] for _ in range(2)]
r_silhouetted = [[[0] * D for _ in range(D)] for _ in range(2)]
b = [[0 for _ in range(D**3)] for _ in range(2)]
n = 0

for i in range(2):
    for x in range(D):
        for y in range(D):
            for z in range(D):
                if not (f[i][z][x] == 1 and r[i][z][y] == 1):
                    continue

                if f_silhouetted[i][z][x] and r_silhouetted[i][z][y]:
                    continue

                n += 1
                b[i][x * (D**2) + y * D + z] = n
                f_silhouetted[i][z][x] = 1
                r_silhouetted[i][z][y] = 1

    # 1組のブロックの中で2組に使い回せるものを使い回す
    if i == 0:
        b0_cnt = max(b[0])
        b1_cnt = 0
        for j, _ in enumerate(b[0]):
            x, y, z = j // (D**2), (j % (D**2)) // D, j % D
            if f[1][z][x] and r[1][z][y] and b1_cnt < b0_cnt:
                b1_cnt += 1
                b[1][j] = b1_cnt
                f_silhouetted[1][z][x] = 1
                r_silhouetted[1][z][y] = 1


def output(n: int, b: List[List[int]]):
    print(n)
    print(" ".join(map(str, b[0])))
    print(" ".join(map(str, b[1])))


output(n, b)
