import sys
import math
from typing import Any, Optional

PROMPT = '>>> '


def run_calc(context: Optional[dict[str, Any]] = None) -> None:
    """Run interactive calculator session in specified namespace"""


if __name__ == '__main__':
    context = {'math': math}
    run_calc(context)
