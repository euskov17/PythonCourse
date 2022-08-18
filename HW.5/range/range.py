from typing import Iterable, Sized


class Range(Sized, Iterable[int]):
    """The range-like type, which represents an immutable sequence of numbers"""

    def __init__(self, *args: int) -> None:
        """
        :param args: either it's a single `stop` argument
            or sequence of `start, stop[, step]` arguments.
        If the `step` argument is omitted, it defaults to 1.
        If the `start` argument is omitted, it defaults to 0.
        If `step` is zero, ValueError is raised.
        """
        self.data = range(*args)
        if len(args) == 1:
            self._args = [0, *args]
        elif len(args) == 2 or args[2] == 1:
            self._args = [*args][:2]
        else:
            self._args = args

    def __iter__(self) -> 'RangeIterator':
        for el in self.data:
            yield el

    def __repr__(self) -> str:
        return f"Range({','.join(map(str, self._args))})"

    def __str__(self) -> str:
        return f"range({', '.join(map(str, self._args))})"

    def __contains__(self, key: int) -> bool:
        return key in self.data

    def __getitem__(self, key: int) -> int:
        return self.data[key]

    def __len__(self) -> int:
        return len(self.data)
