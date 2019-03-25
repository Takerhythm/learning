import random


def quick_sort(nums, start, end):
    # 起始位置与终止位置相同时，该次排序完成
    if start >= end-1:
        return
    lo = start
    hi = end-1
    # 设起始位置为主元
    mid = nums[lo]
    # 将主元放置合适位置并排序，使主元左侧元素都比主元小，右侧元素都比主元大
    while lo < hi:
        while lo < hi and nums[hi] > mid:
            hi -= 1
        nums[lo] = nums[hi]
        while lo < hi and nums[lo] <= mid:
            lo += 1
        nums[hi] = nums[lo]
    nums[lo] = mid
    # 对两侧元素递归排序
    quick_sort(nums, start, lo)
    quick_sort(nums, lo+1, end)
    return nums


if __name__ == '__main__':
    nums = [random.randint(0, 1000) for i in range(10)]
    print(nums)
    print(quick_sort(nums, 0, len(nums)))
