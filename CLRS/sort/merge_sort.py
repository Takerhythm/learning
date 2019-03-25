def merge_sort(nums_list):
    if len(nums_list) <= 1:
        return nums_list
    # 递归分解数组
    middle = len(nums_list) // 2
    nums1 = merge_sort(nums_list[:middle])
    nums2 = merge_sort(nums_list[middle:])
    # 递归合并数组并排序
    return merge(nums1, nums2)


def merge(nums1, nums2):
    l1 = len(nums1)-1
    l2 = len(nums2)-1
    i = 0
    j = 0
    new_list = []
    # 生成新的列表按升序存储两个子列表的元素
    while i <= l1 and j <= l2:
        if nums1[i] < nums2[j]:
            new_list.append(nums1[i])
            i += 1
        else:
            new_list.append((nums2[j]))
            j += 1
    # 将剩余子列表的元素加入新列表
    if i > l1:
        new_list += nums2[j:]
    else:
        new_list += nums1[i:]
    return new_list


if __name__ == '__main__':
    nums_list = [2, 5, 5, 4, 1, 3, 7, 6]
    print(merge_sort(nums_list))
