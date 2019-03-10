def insert_sort(nums_list):
    for j in range(1, len(nums_list)):
        cur = nums_list[j]
        i = j-1
        while i >= 0 and nums_list[i] > cur:
            nums_list[i], nums_list[i+1] = nums_list[i+1], nums_list[i]
            i -= 1
    return nums_list


if __name__ == '__main__':
    nums = [2, 5, 5, 4, 1, 3, 7, 6]
    print(insert_sort(nums))
