import typing as tp


def two_sum(nums: tp.Sequence[int], target: int) -> tp.List[int]:
    """
    Takes a list of integers, return indices of the two numbers
    such that they add up to a specific target.
    You may assume that each input would have exactly one solution,
    and you may not use the same element twice.
    :param nums: list of integers
    :param target: specific target
    :return: list of the two indices
    """
    if nums:
        value_to_ind = {target - nums[0]: 0}
        for i in range(1, len(nums)):
            if nums[i] in value_to_ind:
                return [value_to_ind[nums[i]], i]
            else:
                value_to_ind[target - nums[i]] = i
    raise Exception('No two sum solution')
