from collections import UserList
import typing as tp

# https://github.com/python/mypy/issues/5264#issuecomment-399407428
if tp.TYPE_CHECKING:
    BaseList = UserList[tp.Optional[tp.Any]]
else:
    BaseList = UserList


class ListTwist(BaseList):
    """
    List-like class with additional attributes:
        * reversed, R - return reversed list
        * first, F - insert or retrieve first element;
                     Undefined for empty list
        * last, L -  insert or retrieve last element;
                     Undefined for empty list
        * size, S -  set or retrieve size of list;
                     If size less than list length - truncate to size;
                     If size greater than list length - pad with Nones
    """
    aliases = {
        'F': 'first',
        'L': 'last',
        'S': 'size',
        'R': 'reversed'
    }

    def __init__(self, lst=[]):
        self.data = list(lst)

    def __setattr__(self, key, value):
        key = self.aliases.get(key, key)
        object.__setattr__(self, key, value)

    def __getattr__(self, item):
        item = self.aliases.get(item, item)
        return object.__getattribute__(self, item)

    @property
    def reversed(self):
        return list(reversed(self.data))

    @property
    def first(self):
        return self.data[0]

    @first.setter
    def first(self, value):
        self.data[0] = value

    @property
    def last(self):
        return self.data[-1]

    @last.setter
    def last(self, value):
        self.data[-1] = value

    @property
    def size(self):
        return len(self.data)

    @size.setter
    def size(self, size_: int):
        if size_ > self.size:
            self.data.extend([None] * (size_ - self.size))
        else:
            self.data = self.data[:size_]
