import typing as tp

import numpy as np


def nearest_value(matrix: np.ndarray, value: float) -> tp.Optional[float]:
    """
    Find nearest value in matrix.
    If matrix is empty return None
    :param matrix: input matrix
    :param value: value to find
    :return: nearest value in matrix or None
    """
    if matrix.size == 0:
        return None
    return matrix.reshape(matrix.size)[(np.abs(matrix - value)).argmin()]
