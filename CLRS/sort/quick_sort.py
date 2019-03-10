import random


def quick_sort(nums, start, end):
    if start >= end-1:
        return
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
    quick_sort(nums, start, lo)
    quick_sort(nums, lo+1, end)
    return nums


if __name__ == '__main__':
    nums = [random.randint(0, 999) for i in range(10)]
    print(nums)
    print(quick_sort(nums, 0, len(nums)))
