import random


def selection_sort(nums):
    n = len(nums)
    for i in range(n-1):
        min_index = i
        for j in range(i+1, n):
            if nums[min_index] > nums[j]:
                min_index = j
        if min_index != i:
            nums[min_index], nums[i] = nums[i], nums[min_index]


if __name__ == '__main__':
    nums = [random.randint(0, 999) for i in range(10)]
    print(nums)
    selection_sort(nums)
    print(nums)
