import typing as tp


def find_peak_index(nums: tp.Sequence[int]) -> int:
    """
    Find `peak` value in sequence and return its index. Peak means that both neighbours are less or equals to value.
    :param nums: sequence of integers
    :return: index of peak value
    """
    if len(nums) == 1:
        return 0
    if nums[0] > nums[1]:
        return 0
    if nums[-1] > nums[-2]:
        return len(nums) - 1
    left_bound, right_bound = 0, len(nums) - 1
    while right_bound > left_bound:
        middle = int((right_bound + left_bound) // 2)
        if middle == left_bound:
            if nums[left_bound] > nums[right_bound]:
                return left_bound
            else:
                return right_bound
        if nums[left_bound] < nums[middle] < nums[right_bound]:
            left_bound = middle
        else:
            right_bound = middle
    return right_bound
