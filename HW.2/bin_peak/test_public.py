import copy
import dataclasses
import itertools

import typing as tp

import pytest


from .bin_peak import find_peak_index


@dataclasses.dataclass
class Case:
    nums: tp.Sequence[int]
    peaks_indices: tp.AbstractSet[int]
    name: tp.Optional[str] = None

    def __str__(self) -> str:
        if self.name is not None:
            return self.name
        return 'find_in_{}'.format(self.nums)


BIG_VALUE = 10**5


def get_range_with_peak_on_position(range_size: int, position: int) -> tp.List[int]:
    if position >= range_size or position < 0:
        raise ValueError("Position should be in [0, range_size)")

    return list(itertools.chain(range(position), [range_size + 1], range(range_size - position - 1, position, -1)))


TEST_CASES = [
    Case(nums=[1], peaks_indices={0}),
    Case(nums=[1, 2], peaks_indices={1}),
    Case(nums=[1, 1], peaks_indices={0, 1}),
    Case(nums=[2, 1], peaks_indices={0}),
    Case(nums=[1, 2, 1], peaks_indices={1}),
    Case(nums=[2, 1, 3], peaks_indices={0, 2}),
    Case(nums=[1, 2, 2], peaks_indices={1, 2}),
    Case(nums=[1, 2, 2, 1], peaks_indices={1, 2}),
    Case(nums=[1, 2, 1, 1], peaks_indices={1, 3}),
    Case(nums=[2, 2, 2, 2], peaks_indices={0, 1, 2, 3}),
    Case(nums=[2, 1, 1, 2], peaks_indices={0, 3}),
    Case(nums=[1, 2, 3, 4], peaks_indices={3}),
    Case(nums=[3, 2, 1, 2, 3], peaks_indices={0, 4}),
    Case(nums=[3, 2, 3, 2, 3], peaks_indices={0, 2, 4}),
    Case(nums=[1, 4, 3, 2, 1], peaks_indices={1}),
    Case(nums=[-4, -5, -6, -4], peaks_indices={0, 3}),

    Case(nums=get_range_with_peak_on_position(BIG_VALUE, 0),
         peaks_indices={0},
         name="min_in_big_range"),
    Case(nums=get_range_with_peak_on_position(BIG_VALUE, BIG_VALUE - 1),
         peaks_indices={BIG_VALUE - 1},
         name="max_in_big_range"),
    Case(nums=get_range_with_peak_on_position(BIG_VALUE, BIG_VALUE // 2),
         peaks_indices={BIG_VALUE // 2},
         name="middle_in_big_range"),
]


@pytest.mark.parametrize('t', TEST_CASES, ids=str)
def test_find_value(t: Case) -> None:
    nums_copy = copy.deepcopy(t.nums)

    answer = find_peak_index(nums_copy)

    assert t.nums == nums_copy, "You shouldn't change inputs"
    assert answer in t.peaks_indices
