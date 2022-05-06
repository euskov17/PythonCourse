import typing as tp

import numpy as np


def max_element(array: np.ndarray) -> tp.Optional[float]:
    """
    Return max element before zero for input array.
    If appropriate elements are absent, then return None
    :param array: array,
    :return: max element value or None
    """
