import numpy as np


def vander(array: np.ndarray) -> np.ndarray:
    """
    Create a Vandermod matrix from the given vector.
    :param array: input array,
    :return: vandermonde matrix
    """
    vander = np.ones(array.size)[:, np.newaxis]
    while vander.shape != (array.size, array.size):
        vander = np.hstack((vander, array[:, np.newaxis] * vander[:, -1][:, np.newaxis]))
    return vander
