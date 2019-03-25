import random


def randomized_select(nums, start, end, idx):
    if start == end:
        return nums[start]
    lo = start
    hi = end-1
    mid = nums[lo]
    while lo < hi:
        while lo < hi and nums[hi] > mid:
            hi -= 1
        nums[lo] = nums[hi]
        while lo < hi and nums[lo] <= mid:
            lo += 1
        nums[hi] = nums[lo]
    nums[lo] = mid
    if lo == idx:
        return nums[lo]
    elif idx > lo:
        return randomized_select(nums, lo+1, end, idx)
    elif idx < lo:
        return randomized_select(nums, start, lo, idx)


if __name__ == '__main__':
    nums = [random.randint(0, 10) for i in range(10)]
    print(nums)
    print(randomized_select(nums, 0, 10, 2))
    print(nums)
