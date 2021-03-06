import random


def insert_sort(nums_list):
    for j in range(1, len(nums_list)):
        cur = nums_list[j]
        i = j-1
        while i >= 0 and nums_list[i] > cur:
            nums_list[i], nums_list[i+1] = nums_list[i+1], nums_list[i]
            i -= 1


def bucket_sort(nums):
    n = len(nums)
    # 生成n个桶
    tmp_list = [[] for i in range(n)]
    # 将元素均匀放在每个桶中
    for i in nums:
        tmp_list[int(i*n)].append(i)
    # 对各桶元素进行插入排序
    for l in tmp_list:
        insert_sort(l)
    nums = [j for i in tmp_list for j in i]
    return nums


if __name__ == '__main__':
    nums = [random.random() for i in range(100)]
    print(nums)
    print(bucket_sort(nums))
