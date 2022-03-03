import typing as tp
import dataclasses

import pytest

from .two_sum import two_sum


@dataclasses.dataclass
class Case:
    nums: tp.Sequence[int]
    target: int
    result: tp.List[int]

    def __str__(self) -> str:
        return f'indexes_for_{self.nums}_{self.target}'


TEST_CASES = [
    Case(nums=[2, 7, 11, 15], target=9, result=[0, 1]),
    Case(nums=[2, -7, 11, 15], target=4, result=[1, 2]),
    Case(nums=[1, 2, 3, 4], target=7, result=[2, 3]),
    Case(nums=[1, 2], target=3, result=[0, 1])
    ]


@pytest.mark.parametrize('t', TEST_CASES, ids=str)
def test_two_sum(t: Case) -> None:
    answer = two_sum(t.nums, t.target)
    assert answer == t.result
