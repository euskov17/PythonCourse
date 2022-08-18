import string
import sys
import math
from typing import Any, Optional
import re

PROMPT = '>>> '


def run_calc(context: Optional[dict[str, Any]] = None) -> None:
    """Run interactive calculator session in specified namespace"""
    is_ended = False
    while not is_ended:
        print(PROMPT, end='')
        if expression := sys.stdin.readline():
            names = re.sub(r'([\"\'])[^\'\"]+\1', '', expression)
            names = re.sub('[' + string.punctuation + ']', ' ', names).split()
            for name in names:
                if (not name.isdigit()) and name not in dir(math) and not (context and name in context.keys()):
                    raise NameError(f'name \'{name}\' is not defined')
            print(eval(expression[:-1], context))
        else:
            print('')
            is_ended = True
