import copy
import dataclasses
import dis
import itertools

import typing as tp

import pytest


from .bin_min import find_min


T = tp.TypeVar('T')


@dataclasses.dataclass
class Case:
    nums: tp.Sequence[int]

    def __str__(self) -> str:
        return 'find_min_in_{}'.format(self.nums)


BIG_VALUE = 10**5


def get_range_with_peak_on_position(range_size: int, position: int) -> tp.List[int]:
    if position >= range_size or position < 0:
        raise ValueError("Position should be in [0, range_size)")

    return list(itertools.chain(range(position), [range_size + 1], range(range_size - position - 1, position, -1)))


TEST_CASES = [
    Case(nums=[1]),
    Case(nums=[1, 2]),
    Case(nums=[2, 1]),
    Case(nums=[1, 2, 3]),
    Case(nums=[3, 1, 2]),
    Case(nums=[2, 3, 1]),
    Case(nums=[-3, -2, 1, 3, 7]),
    Case(nums=[7, -3, -2, 1, 3]),
    Case(nums=[3, 7, -3, -2, 1]),
    Case(nums=[1, 3, 7, -3, -2]),
    Case(nums=[-2, 1, 3, 7, -3]),
    Case(nums=[-7, -3, -2, 1, 3, 7]),
    Case(nums=[7, -7, -3, -2, 1, 3]),
    Case(nums=[3, 7, -7, -3, -2, 1]),
    Case(nums=[1, 3, 7, -7, -3, -2]),
    Case(nums=[-2, 1, 3, 7, -7, -3]),
    Case(nums=[-3, -2, 1, 3, 7, -7]),
]


def dummy_implementation(nums: tp.Sequence[tp.Any]) -> tp.Optional[tp.Any]:
    return min(nums)


@pytest.mark.parametrize('t', TEST_CASES, ids=str)
def test_find_value(t: Case) -> None:
    nums_copy = copy.deepcopy(t.nums)

    answer = find_min(nums_copy)

    assert t.nums == nums_copy, "You shouldn't change inputs"

    is_used_min = any(i.argval == 'min' for i in dis.get_instructions(find_min))
    assert not is_used_min, "You should use iteration ONLY, not manually min"

    is_used_sorted = any(i.argval == 'sorted' for i in dis.get_instructions(find_min))
    assert not is_used_sorted, "You should use iteration ONLY, not manually sorting"

    assert answer == dummy_implementation(t.nums)
