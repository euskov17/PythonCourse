import dis
import types
from collections import Counter


def count_operations(source_code: types.CodeType) -> dict[str, int]:
    """Count byte code operations in given source code.

    :param source_code: the bytecode operation names to be extracted from
    :return: operation counts
    """
    all_instructions = dict(Counter([instruction.opname for instruction in dis.get_instructions(source_code)]))
    for instruction in dis.get_instructions(source_code):
        if instruction.argval and isinstance(instruction.argval, types.CodeType):
            inner_calls = count_operations(instruction.argval)
            for key in inner_calls.keys():
                if key in all_instructions.keys():
                    all_instructions[key] += inner_calls[key]
                else:
                    all_instructions[key] = inner_calls[key]
    return all_instructions
