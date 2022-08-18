import numpy as np


def add_zeros(x: np.ndarray) -> np.ndarray:
    """
    Add zeros between values of given array
    :param x: array,
    :return: array with zeros inserted
    """
    array_with_zeros = np.ndarray.repeat(x, 2).reshape(x.size, 2)
    array_with_zeros[:, 1] = 0
    return array_with_zeros.reshape(2 * x.size)[:-1]
