import heapq
import typing as tp
import io


def merge_3(input_streams: tp.Sequence[tp.IO[bytes]], output_stream: tp.IO[bytes]) -> None:
    """
    Merge input_streams in output_stream
    :param input_streams: list of input streams. Contains byte-strings separated by "\n". Nonempty stream ends with "\n"
    :param output_stream: output stream. Contains byte-strings separated by "\n". Nonempty stream ends with "\n"
    :return: None
    """
    my_heap = [(int(line[:-1].decode()), stream_num) for stream, stream_num in
               zip(input_streams, range(len(input_streams)))
               if (line := stream.readline())]
    heapq.heapify(my_heap)
    while my_heap:
        pop_elem = heapq.heappop(my_heap)
        s = str(pop_elem[0]).encode()
        output_stream.write(s)
        output_stream.write(bytes('\n', 'utf-8'))
        new_line = input_streams[pop_elem[1]].readline()
        if new_line:
            heapq.heappush(my_heap, (int(new_line[:-1].decode()), pop_elem[1]))
