import typing as tp


def find_min(nums: tp.Sequence[int]) -> int:
    """
    Find minimum in rotated not empty sorted sequence without dublicates.
    :param nums: sequence of integer
    :return: minimum value
    """
    left_bound, right_bound = 0, len(nums) - 1
    while right_bound > left_bound:
        if nums[left_bound] < nums[right_bound]:
            return nums[left_bound]
        middle = int((right_bound + left_bound) // 2)
        if nums[left_bound] > nums[middle]:
            right_bound = middle
        else:
            left_bound = middle + 1
    return nums[left_bound]
