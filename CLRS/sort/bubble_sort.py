import random


def bubble_sort(nums):
    for j in range(len(nums)-1, 0, -1):
        for i in range(j):
            if nums[i] > nums[i+1]:
                nums[i], nums[i+1] = nums[i+1], nums[i]


if __name__ == '__main__':
    nums = [random.randint(0, 1000) for i in range(10)]
    print(nums)
    bubble_sort(nums)
    print(nums)