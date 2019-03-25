def memorized_cut_rod(p, n):
    new_list = [float('-inf') for i in range(n+1)]
    return memorized_cut_rod_aux(p, n, new_list)

def memorized_cut_rod_aux(p, n, r):
    if r[n] >= 0:
        return r[n]
    if n == 0:
        q = 0
    else:
        q = float('-inf')
        for i in range(1, n+1):
            q = max(q, p[i]+memorized_cut_rod_aux(p, n-i, r))
    r[n] = q
    return q


def bottom_up_cut_rod(p, n):
    new_list = [i for i in range(n+1)]
    new_list[0] = 0
    for j in range(1, n+1):
        q = float('-inf')
        for i in range(1, j+1):
            q = max(q, p[i]+new_list[j-i])
        new_list[j] = q
    return new_list[n]


def extend_bottom_up_cut_rod(p, n):
    new_list = [0 for i in range(n+1)]
    len_list = [0 for i in range(n+1)]
    for j in range(1, n+1):
        q = float('-inf')
        for i in range(1, j+1):
            if q < p[i]+new_list[j-i]:
                q = p[i]+new_list[j-i]
                len_list[j] = i
        new_list[j] = q
    return new_list, len_list


def print_bottom_up_cut_rod(p, n):
    r, s = extend_bottom_up_cut_rod(p, n)
    while n > 0:
        print(s[n])
        n -= s[n]

if __name__ == '__main__':
    p = [0, 1, 5, 8, 9, 10, 17, 17, 20, 24, 30]
    print(memorized_cut_rod(p, 10))
    print(bottom_up_cut_rod(p, 10))
    print(extend_bottom_up_cut_rod(p, 10))
    print_bottom_up_cut_rod(p, 10)