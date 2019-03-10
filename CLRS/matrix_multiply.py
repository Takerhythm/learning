def matrix_multiply(a, b):
    if len(a[0]) == len(b):
        res = [[] for i in range(len(a))]
        for i in range(len(a)):
            for j in range(len(b[0])):
                c = 0
                for k in range(len(b)):
                    c += a[i][k] * b[k][j]
                res[i].append(c)
        return res
    return '输入矩阵有误！'


if __name__ == '__main__':
    n = [
        [1, 2, 3],
        [2, 3, 4],
        [3, 4, 5]
         ]
    print(matrix_multiply(n, n))
