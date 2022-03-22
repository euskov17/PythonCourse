import string
import typing as tp


def length_of_last_word(s: str) -> int:
    """
    Takes string  consists of upper/lower-case alphabets and
    empty space characters ' '.
    Returns the length of last word (last word means the last appearing word
    if we loop from left to right) in the string.
    If the last word does not exist, return 0.
    """
