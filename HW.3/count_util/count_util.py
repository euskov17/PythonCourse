import typing as tp
import re


def count_util(text: str, flags: tp.Optional[str] = None) -> dict[str, int]:
    """
    :param text: text to count entities
    :param flags: flags in command-like format - can be:
        * -m stands for counting characters
        * -l stands for counting lines
        * -L stands for getting length of the longest line
        * -w stands for counting words
    More than one flag can be passed at the same time, for example:
        * "-l -m"
        * "-lLw"
    Ommiting flags or passing empty string is equivalent to "-mlLw"
    :return: mapping from string keys to corresponding counter, where
    keys are selected according to the received flags:
        * "chars" - amount of characters
        * "lines" - amount of lines
        * "longest_line" - the longest line length
        * "words" - amount of words
    """
    result = {}
    if not flags or 'm' in flags:
        result['chars'] = len(text)
    if not flags or 'l' in flags:
        result['lines'] = text.count('\n')
    if not flags or 'L' in flags:
        result['longest_line'] = max([len(line) for line in text.split('\n')])
    if not flags or 'w' in flags:
        result['words'] = len(text.split())
    return result
