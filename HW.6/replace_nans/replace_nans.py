import numpy as np


def replace_nans(matrix: np.ndarray) -> np.ndarray:
    """
    Replace all nans in matrix with average of other values.
    If all values are nans, then return zero matrix of the same size.
    :param matrix: matrix,
    :return: replaced matrix
    """
