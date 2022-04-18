import pytest
import dataclasses

from .length_of_last_word import length_of_last_word


@dataclasses.dataclass
class Case:
    s: str
    result: int

    def __str__(self) -> str:
        return 'length_of_last_word_of_{}'.format(self.s)


TEST_CASES = [
    Case(s='Hello world', result=5),
    Case(s='Really easy problem', result=7),
    Case(s='Or not ', result=0),
    Case(s='', result=0)
]


@pytest.mark.parametrize('t', TEST_CASES, ids=str)
def test_length_of_last_word(t: Case) -> None:
    answer = length_of_last_word(t.s)
    assert answer == t.result
