import random


def shell_sort(nums):
    n = len(nums)
    # 分组， gap为组数(步长)
    gap = n // 2
    # 只剩一组时，排序完成
    while gap > 0:
        # 对各组进行插入排序
        for i in range(gap, n):
            j = i
            while j >= gap and nums[j-gap] > nums[j]:
                nums[j], nums[j-gap] = nums[j-gap], nums[j]
                j -= gap
        # 重新分组，步长减小
        gap //= 2


if __name__ == '__main__':
    nums = [random.randint(0, 1000) for i in range(10)]
    print(nums)
    shell_sort(nums)
    print(nums)