import typing as tp


def get_fizz_buzz(n: int) -> list[tp.Union[int, str]]:
    """
    If value divided by 3 - "Fizz",
       value divided by 5 - "Buzz",
       value divided by 15 - "FizzBuzz",
    else - value.
    :param n: size of sequence
    :return: list of values.
    """
    return [num if num % 3 and num % 5 else "Fizz" * (not num % 3) + "Buzz" * (not num % 5) for num in range(1, n + 1)]
