def max_crossing_sub_array(nums_list):
    left_sum = float("-inf")
    sum_list = 0
    mid = len(nums_list)//2
    max_left = mid
    for i in range(mid, -1, -1):
        sum_list += nums_list[i]
        if sum_list > left_sum:
            left_sum = sum_list
            max_left = i
    right_sum = float("-inf")
    sum_list = 0
    max_right = mid+1
    for j in range(mid+1, len(nums_list)):
        sum_list += nums_list[j]
        if sum_list > right_sum:
            right_sum = sum_list
            max_right = j
    return [max_left, max_right, left_sum+right_sum]


def max_sub_array(nums_list):
    if len(nums_list) == 1:
        return [0, 0, nums_list[0]]
    mid = len(nums_list)//2
    left_max_left, left_max_right, left_sum = max_sub_array(nums_list[:mid])
    right_max_left, right_max_right, right_sum = max_sub_array(nums_list[mid:])
    cross_left, cross_right, cross_sum = max_crossing_sub_array(nums_list)
    if left_sum >= right_sum and left_sum >= cross_sum:
        return [left_max_left, left_max_right, left_sum]
    elif right_sum >= left_sum and right_sum >= cross_sum:
        return [right_max_left, right_max_right, right_sum]
    else:
        return [cross_left, cross_right, cross_sum]


if __name__ == '__main__':
    A = [13, -3, -25, 20, -3, -16, -23, 18, 20, -7, 12, -5, -22, 15, -4, 7]
    print(max_sub_array(A))
