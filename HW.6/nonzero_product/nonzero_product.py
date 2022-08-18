import typing as tp

import numpy as np


def nonzero_product(matrix: np.ndarray) -> tp.Optional[float]:
    """
    Compute product of nonzero diagonal elements of matrix
    If all diagonal elements are zeros, then return None
    :param matrix: array,
    :return: product value or None
    """
    non_zero_diag = np.diag(matrix)
    non_zero_diag = non_zero_diag[non_zero_diag != 0]
    if np.size(non_zero_diag) != 0:
        return np.prod(non_zero_diag, dtype=float)
    else:
        return None
