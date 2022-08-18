import numpy
import numpy as np


def replace_nans(matrix: np.ndarray) -> np.ndarray:
    """
    Replace all nans in matrix with average of other values.
    If all values are nans, then return zero matrix of the same size.
    :param matrix: matrix,
    :return: replaced matrix
    """
    if np.size(matrix[~np.isnan(matrix)]) == 0:
        return np.zeros(matrix.shape)
    replaced_matrix = matrix
    line = replaced_matrix.reshape(replaced_matrix.size)
    mean = np.mean(line[~np.isnan(line)])
    replaced_matrix[np.isnan(replaced_matrix)] = mean
    return replaced_matrix


if __name__ == "__main__":
    ar = np.array([[1, np.nan], [2, 1]])
    print(replace_nans(ar))
