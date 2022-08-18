import typing as tp


def generate_matrix(n: int) -> tp.List[tp.List[int]]:
    """
    Takes integer n and returns spiral matrix with elements from 1 to n**2
    """
    spiral_matrix = [[0 for _ in range(n)] for _ in range(n)]
    up_down = 0
    left_right = 1
    cur_pos = [0, 0]
    for i in range(1, n ** 2 + 1):
        spiral_matrix[cur_pos[0]][cur_pos[1]] = i
        if not (0 <= cur_pos[0] + up_down < n and 0 <= cur_pos[1] + left_right < n and not \
                spiral_matrix[cur_pos[0] + up_down][cur_pos[1] + left_right]):
            if left_right:
                if cur_pos[0] + 1 < n and not spiral_matrix[cur_pos[0] + 1][cur_pos[1]]:
                    left_right, up_down = 0, 1
                else:
                    left_right, up_down = 0, -1
            elif cur_pos[1] + 1 < n and not spiral_matrix[cur_pos[0]][cur_pos[1] + 1]:
                left_right, up_down = 1, 0
            else:
                left_right, up_down = -1, 0
        cur_pos = [cur_pos[0] + up_down, cur_pos[1] + left_right]
    return spiral_matrix
