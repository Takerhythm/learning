import random


def counting_sort(nums, k):
    # k为列表中最大元素
    n = len(nums)
    # 生成临时列表，元素值为小于等于该索引值的个数，临时列表的索引值与nums的元素值一一对应
    tmp_list = [0 for i in range(k+1)]
    # 生成存放已排序元素的列表
    new_list = [0 for i in range(n)]
    # 计算等于该元素值的元素个数，放入临时列表
    for i in nums:
        tmp_list[i] += 1
    # 计算小于等于该元素值得元素个数（即将临时列表相邻元素值相加，比如小于5的元素个数为3，小于等于5的元素个数即为小于5的元素个数加上等于5的元素个数）
    for i in range(1, k+1):
        tmp_list[i] += tmp_list[i-1]
    # 将排序好的元素放入合适的位置，若有重复元素，重复元素倒序插入
    for i in nums:
        new_list[tmp_list[i]-1] = i
        tmp_list[i] -= 1
    return new_list


if __name__ == '__main__':
    nums = [random.randint(0, 1000) for i in range(10)]
    k = max(nums)
    print(nums)
    print(counting_sort(nums, k))
