import functools
from typing import Callable, Any, TypeVar
from collections import OrderedDict

Function = TypeVar('Function', bound=Callable[..., Any])


def cache(max_size: int) -> Callable[[Function], Function]:
    """
    Returns decorator, which stores result of function
    for `max_size` most recent function arguments.
    :param max_size: max amount of unique arguments to store values for
    :return: decorator, which wraps any function passed
    """
    cache = OrderedDict()

    def real_decorator(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            key = args + tuple(sorted(kwargs.items()))
            if key not in cache:
                if len(cache) == max_size:
                    cache.popitem(last=False)
                cache[key] = func(*key)
            else:
                cache.move_to_end(key)
            return cache[key]

        return inner

    return real_decorator
