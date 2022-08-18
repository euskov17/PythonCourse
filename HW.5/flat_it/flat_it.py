from typing import Iterable, Generator, Any


def flat_it(sequence: Iterable[Any]) -> Generator[Any, None, None]:
    """
    :param sequence: sequence with arbitrary level of nested iterables
    :return: generator producing flatten sequence
    """
    for el in sequence:
        if hasattr(el, '__iter__') and el != sequence:
            sub_gen = flat_it(el)
            while True:
                try:
                    yield next(sub_gen)
                except StopIteration:
                    break
        else:
            yield el
