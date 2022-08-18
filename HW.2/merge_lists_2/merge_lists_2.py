import heapq
import typing as tp


def merge_2(seq: tp.Sequence[tp.Sequence[int]]) -> list[int]:
    """
    :param seq: sequence of sorted sequences
    :return: merged sorted list
    """
    values = [(s[0], i, 0) for i, s in zip(range(len(seq)), seq) if len(seq[i])]
    result = []
    while values:
        heapq.heapify(values)
        pop_val = heapq.heappop(values)
        result.append(pop_val[0])
        if pop_val[2] + 1 < len(seq[pop_val[1]]):
            heapq.heappush(values, (seq[pop_val[1]][pop_val[2] + 1], pop_val[1], pop_val[2] + 1))
    return result
