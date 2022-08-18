class LifeGame(object):
    """
    Class for Game life
    """

    def __init__(self, matrix: list[list[int]]):
        self.matrix = matrix
        self.length = len(matrix)
        self.width = len(matrix[0])

    def get_next_generation(self):
        self.matrix = [[self._get_next_generation_el(i, j) for j in range(self.width)] for i in range(self.length)]
        return self.matrix

    def _get_neighbours_dict(self, i: int, j: int) -> dict[int, int]:
        neigh = {0: 0, 1: 0, 2: 0, 3: 0}
        directions = {(first, second) for first in range(-1, 2) for second in range(-1, 2) if first or second}
        for k, l in directions:
            if 0 <= i + l < self.length and 0 <= j + k < self.width:
                neigh[self.matrix[i + l][j + k]] += 1
        return neigh

    def _get_next_generation_el(self, i: int, j: int) -> int:
        elem = self.matrix[i][j]
        neighs = self._get_neighbours_dict(i, j)
        return_value = {1: 1, 2: 2 if neighs[elem] in [2, 3] else 0,
                        3: 3 if neighs[elem] in [2, 3] else 0,
                        0: 2 if neighs[2] == 3 else 3 if neighs[3] == 3 else 0}
        return return_value[elem]
