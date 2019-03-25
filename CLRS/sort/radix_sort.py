import random


def radix_sort(nums, d):
    for i in range(d):
        # 生成临时容器，十进制数生成10个
        tmp = [[] for i in range(10)]
        # 依次按数位上值的大小放入临时数组
        for j in nums:
            tmp[j//(10**i)%10].append(j)
        # 生成该轮次排序好的数组
        nums = [j for i in tmp for j in i]
    return nums


if __name__ == '__main__':
    nums = [random.randint(0, 1000) for i in range(10)]
    print(nums)
    print(radix_sort(nums, 3))
