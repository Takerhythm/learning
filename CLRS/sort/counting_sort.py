import random


def counting_sort(nums, k):
    # k为列表中最大元素，且小于等于列表长度
    n = len(nums)
    tmp_list = [0 for i in range(k+1)]
    new_list = [0 for i in range(n)]
    for i in nums:
        tmp_list[i] += 1
    for i in range(1, k+1):
        tmp_list[i] += tmp_list[i-1]
    for i in nums:
        new_list[tmp_list[i]-1] = i
        tmp_list[i] -= 1
    return new_list


if __name__ == '__main__':
    nums = [random.randint(0, 9) for i in range(10)]
    k = max(nums)
    print(nums)
    print(counting_sort(nums, k))
