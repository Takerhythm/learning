import random


def radix_sort(nums, d):
    for i in range(d):
        tmp = [[] for i in range(10)]
        for j in nums:
            tmp[j//(10**i)%10].append(j)
        nums = [j for i in tmp for j in i]
    return nums


if __name__ == '__main__':
    nums = [random.randint(0, 1000) for i in range(10)]
    print(nums)
    print(radix_sort(nums, 3))
