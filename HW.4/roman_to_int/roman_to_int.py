import typing as tp


def roman_to_int(s: str) -> int:
    """
    Given a roman numeral, convert it to an integer.
    Input is guaranteed to be within the range from 1 to 3999.
    """
    dct = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    if not s:
        return 0
    summ = dct[s[-1]]
    for i in range(len(s) - 1):
        if (el := dct[s[i]]) < dct[s[i + 1]]:
            summ -= el
        else:
            summ += el
    return summ
