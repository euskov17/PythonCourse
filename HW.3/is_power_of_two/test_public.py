import dataclasses
import pytest

from .is_power_of_two import is_power_of_two


@dataclasses.dataclass
class Case:
    n: int
    result: bool

    def __str__(self) -> str:
        return 'is_power_of_two_on_{}'.format(self.n)


TEST_CASES = [
    Case(n=0, result=False),
    Case(n=1, result=True),
    Case(n=2, result=True),
    Case(n=4, result=True),
    Case(n=512, result=True),
    Case(n=1025, result=False),
    Case(n=2050, result=False)
]


@pytest.mark.parametrize('t', TEST_CASES, ids=str)
def test_is_power_of_two(t: Case) -> None:
    answer = is_power_of_two(t.n)
    assert answer == t.result
