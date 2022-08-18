import typing as tp

import numpy as np


def max_element(array: np.ndarray) -> tp.Optional[float]:
    """
    Return max element before zero for input array.
    If appropriate elements are absent, then return None
    :param array: array,
    :return: max element value or None
    """
    if array.size % 2 == 0:
        first_part = array.reshape(array.size // 2, 2)
        second_part = array[1:-1].reshape(array.size // 2 - 1, 2)
    else:
        first_part = array[1:].reshape(array.size // 2, 2)
        second_part = array[2:-1].reshape(array.size // 2 - 1, 2)
    all_candidetes = np.concatenate((first_part[first_part[:, 0] == 0], second_part[second_part[:, 0] == 0]))
    return None if all_candidetes.size == 0 else np.max(all_candidetes[:,1])
