import typing as tp


def is_power_of_two(n: int) -> bool:
    """
    Given a positive integer, write a function to find if it is a power of two or not.
    """
    if not n:
        return False
    while n % 2 == 0:
        n >>= 1
    if n != 1:
        return False
    else:
        return True
