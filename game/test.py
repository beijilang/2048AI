a = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]


def rotate_cw(matrix):
    result = []
    for i in range(len(matrix)):
        row = [r[i] for r in matrix]
        row.reverse()
        result.append(row)
    return result


def rotate_ccw(matrix):
    result = []
    for i in range(len(matrix) - 1, -1, -1):
        row = [r[i] for r in matrix]
        result.append(row)
    return result


b = rotate_cw(a)
c = rotate_ccw(a)
print(b)
print(c)
