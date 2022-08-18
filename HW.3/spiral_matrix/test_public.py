import dataclasses
import pytest
import typing as tp

from .spiral_matrix import generate_matrix


@dataclasses.dataclass
class Case:
    n: int
    result: tp.List[tp.List[int]]

    def __str__(self) -> str:
        return 'generate_matrix_of_{}'.format(self.n)


TEST_CASES = [
    Case(n=1, result=[[1]]),
    Case(n=2, result=[[1, 2],
                      [4, 3]]),
    Case(n=3, result=[[1, 2, 3],
                      [8, 9, 4],
                      [7, 6, 5]]),
    Case(n=4, result=[[1,  2,  3, 4],
                      [12, 13, 14, 5],
                      [11, 16, 15, 6],
                      [10,  9,  8, 7]])
]


@pytest.mark.parametrize('t', TEST_CASES, ids=str)
def test_generate_matrix(t: Case) -> None:
    answer = generate_matrix(t.n)
    assert answer == t.result
