import dataclasses

import pytest

from .roman_to_int import roman_to_int


@dataclasses.dataclass
class Case:
    s: str
    result: int

    def __str__(self) -> str:
        return 'roman_to_int_of_{}'.format(self.s)


TEST_CASES = [
    Case(s='III', result=3),
    Case(s='IV', result=4),
    Case(s='IX', result=9),
    Case(s='LVIII', result=58),
    # Explanation: M = 1000, CM = 900, XC = 90 and IV = 4
    Case(s='MCMXCIV', result=1994),
    Case(s='MMXX', result=2020)
]


@pytest.mark.parametrize('t', TEST_CASES, ids=str)
def test_length_of_last_word(t: Case) -> None:
    answer = roman_to_int(t.s)
    assert answer == t.result
