"""
Simplified VM code which works for some cases.
You need extend/rewrite code to pass all cases.
"""

import builtins
import collections.abc
import dis
# import inspect
# import inspect
import types
import typing as tp
import asyncio


class Frame:
    """
    Frame header in cpython with description
        https://github.com/python/cpython/blob/3.9/Include/frameobject.h#L17

    Text description of frame parameters
        https://docs.python.org/3/library/inspect.html?highlight=frame#types-and-members
    """

    def __init__(self,
                 frame_code: types.CodeType,
                 frame_builtins: dict[str, tp.Any],
                 frame_globals: dict[str, tp.Any],
                 frame_locals: dict[str, tp.Any]) -> None:
        self.code = frame_code
        self.builtins = frame_builtins
        self.globals = frame_globals
        self.locals = frame_locals
        self.data_stack: tp.Any = []
        self.return_value = None
        self.offset_map = {instr.offset: instr for instr in dis.get_instructions(frame_code)}
        self.current_offset = 0
        # self.is_generator = isinstance(frame_code, types.GeneratorType)

    def top(self) -> tp.Any:
        return self.data_stack[-1]

    def topn(self, n: int) -> tp.Any:
        """
        First n values from the stack
        :param n: number of values
        :return: list of values
        """
        if n > 0:
            return self.data_stack[-n:]
        else:
            return []

    def pop(self) -> tp.Any:
        return self.data_stack.pop()

    def push(self, *values: tp.Any) -> None:
        self.data_stack.extend(values)

    def popn(self, n: int) -> tp.Any:
        """
        Pop a number of values from the value stack.
        A list of n values is returned, the deepest value first.
        """
        if n > 0:
            if len(self.data_stack) >= n:
                returned = self.data_stack[-n:]
                self.data_stack[-n:] = []
                return returned
            # else:
                # print("")
        else:
            return []

    def run(self) -> tp.Any:
        while self.current_offset <= max(self.offset_map.keys()):
            instruction = self.offset_map[self.current_offset]
            # print(instruction.opname, instruction.argval, self.current_offset)
            # print(self.locals)
            rv = getattr(self, instruction.opname.lower() + "_op")(instruction.argval)
            if rv is not None:
                if self.return_value is None:
                    self.return_value = [rv]
                else:
                    self.return_value.append(rv)
            self.current_offset += 2
            # print(self.data_stack)
        return self.return_value

    # def run_gen(self) -> tp.Any:
    #     while self.current_offset <= max(self.offset_map.keys()):
    #         instruction = self.offset_map[self.current_offset]
    #         print(instruction.opname, instruction.argval)
    #         getattr(self, instruction.opname.lower() + "_op")(instruction.argval)
    #         if self.return_value is not None:
    #             yield self.return_value
    #             self.return_value = None
    #         self.current_offset += 2
    #         print(self.data_stack)
    #     # return self.return_value

    def call_function_op(self, arg: int) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.9.7/library/dis.html#opcode-CALL_FUNCTION

        Operation realization:
            https://github.com/python/cpython/blob/3.9/Python/ceval.c#L3496
        """
        # print(f"We are here {arg}", flush=True)
        if len(self.data_stack) >= arg + 1:
            arguments = self.popn(arg)
            f = self.pop()
            # print(f.__name__, arguments)
            # print(type(f), type(arguments), flush=True)

            # rv = f(*arguments)
            # if isinstance(f, type):
            #     self.push(f.__init__(*arguments))
            # else:
            self.push(f(*arguments))
        else:
            print("Not enought args\n")

    def call_function_kw_op(self, argc: int):
        kwarg_names = self.pop()
        kwargs = {key: value for key, value in zip(kwarg_names, self.popn(len(kwarg_names)))}
        args = self.popn(argc - len(kwarg_names))
        f = self.pop()
        self.push(f(*args, **kwargs))

    def call_function_ex_op(self, flags):
        pass

    def load_method_op(self, namei: str):
        tos = self.pop()
        if hasattr(tos, namei):  # self.locals[namei]):
            self.push(getattr(tos, namei))  # self.locals[namei]))
        else:
            self.push(None)

    def call_method_op(self, argc: int):
        args = self.popn(argc)
        method = self.pop()
        # print(method, args)
        if method is not None:
            self.push(method(*args))
        else:
            self.push(None)

    def load_name_op(self, arg: str) -> None:
        """
        Partial realization

        Operation description:
            https://docs.python.org/release/3.9.7/library/dis.html#opcode-LOAD_NAME

        Operation realization:
            https://github.com/python/cpython/blob/3.9/Python/ceval.c#L2416
        """
        # print(arg)
        if arg in self.locals:
            self.push(self.locals[arg])
        elif arg in self.globals:
            self.push(self.globals[arg])
        elif arg in self.builtins:
            self.push(self.builtins[arg])
        # elif hasattr(self.builtins, arg):
        #     self.push(getattr(self.builtins, arg))
        else:
            raise NameError(f'name \'{arg}\' is not defined')

    def load_global_op(self, arg: str) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.9.7/library/dis.html#opcode-LOAD_GLOBAL

        Operation realization:
            https://github.com/python/cpython/blob/3.9/Python/ceval.c#L2480
        """
        if arg in self.globals:
            self.push(self.globals[arg])
        elif arg in self.builtins:
            self.push(self.builtins[arg])
        else:
            raise NameError(f'name \'{arg}\' is not defined')

    def load_const_op(self, arg: tp.Any) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.9.7/library/dis.html#opcode-LOAD_CONST

        Operation realization:
            https://github.com/python/cpython/blob/3.9/Python/ceval.c#L1346
        """
        self.push(arg)

    def return_value_op(self, arg: tp.Any) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.9.7/library/dis.html#opcode-RETURN_VALUE

        Operation realization:
            https://github.com/python/cpython/blob/3.9/Python/ceval.c#L1911
        """
        if self.return_value is None:
            self.return_value = self.pop()

    def yield_value_op(self, arg):
        return self.top()

    def yield_from_op(self, arg):
        tos = self.top()
        assert False, print('We are in yield_from_op')
        self.push(iter(tos))

    def pop_top_op(self, arg: tp.Any) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.9.7/library/dis.html#opcode-POP_TOP

        Operation realization:
            https://github.com/python/cpython/blob/3.9/Python/ceval.c#L1361
        """
        self.pop()

    def make_function_op(self, arg: int) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.9.7/library/dis.html#opcode-MAKE_FUNCTION

        Operation realization:
            https://github.com/python/cpython/blob/3.9/Python/ceval.c#L3571

        Parse stack:
            https://github.com/python/cpython/blob/3.9/Objects/call.c#L671

        Call function in cpython:
            https://github.com/python/cpython/blob/3.9/Python/ceval.c#L4950
        """
        name = self.pop()  # the qualified name of the function (at TOS)  # noqa
        code = self.pop()  # the code associated with the function (at TOS1)

        # print(name, code)
        # TODO: use arg to parse function defaults

        def func(*args: tp.Any, **kwargs: tp.Any) -> tp.Any:
            # TODO: parse input arguments using code attributes such as co_argcount

            parsed_args: dict[str, tp.Any] = {code.co_varnames[i]: args[i] for i in range(code.co_argcount)}
            f_locals = dict(self.locals)
            f_locals.update(parsed_args)

            frame = Frame(code, self.builtins, self.globals, f_locals)  # Run code in prepared environment
            # print(f'Frame is generator = {frame.is_generator}, {type(frame.code)}')
            return frame.run()

        # def gen(*args: tp.Any, **kwargs: tp.Any) -> tp.Any:
        #     parsed_args: dict[str, tp.Any] = {code.co_varnames[i]: args[i] for i in range(code.co_argcount)}
        #     f_locals = dict(self.locals)
        #     f_locals.update(parsed_args)
        #
        #     frame = Frame(code, self.builtins, self.globals, f_locals)# Run code in prepared environment
        #     # print(f'Frame is generator = {frame.is_generator}, {type(frame.code)}')
        #     return frame.run_gen()
        # instr = [i.opname for i in dis.Bytecode(code)]
        # # print(instr, '\n\n\n\n\n\n\n\n')
        # if 'yield_value'.upper() in instr or 'yield_from'.upper() in instr:
        #     # print("We make_gen\n\n\n\n\n\n\n")
        #     self.push(gen)
        # else:
        #     self.push(func)
        self.push(func)

    def store_name_op(self, arg: str) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.9.7/library/dis.html#opcode-STORE_NAME

        Operation realization:
            https://github.com/python/cpython/blob/3.9/Python/ceval.c#L2280
        """
        self.locals[arg] = self.pop()  # pop?

    def delete_name_op(self, arg: str) -> None:
        if arg in self.locals.keys():
            del self.locals[arg]
        elif arg in self.globals.keys():
            del self.globals[arg]
        elif arg in self.builtins.keys():
            del self.builtins[arg]
        else:
            raise NameError(f'name \'{arg}\' is not defined')

    def unpack_sequence_op(self, count: int) -> None:
        seq = self.pop()
        for el in reversed(seq):
            self.push(el)

    def unpack_ex_op(self, counts: int) -> None:
        # TODO: strange
        pass

    def store_attr_op(self, namei: str) -> None:
        tos1, tos = self.topn(2)
        setattr(tos, namei, tos1)

    def delete_attr_op(self, namei: str) -> None:
        tos = self.top()
        delattr(tos, namei)

    def store_global_op(self, arg: str) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.9.7/library/dis.html#opcode-STORE_NAME

        Operation realization:
            https://github.com/python/cpython/blob/3.9/Python/ceval.c#L2280
        """
        self.globals[arg] = self.pop()

    def delete_global_op(self, arg: str) -> None:
        if arg in self.globals.keys():
            del self.globals[arg]
        elif arg in self.builtins.keys():
            del self.builtins[arg]
        else:
            raise NameError(f'name \'{arg}\' is not defined')

    def build_tuple_op(self, count: int) -> None:
        self.push(tuple(self.popn(count)))

    def build_list_op(self, count: int) -> None:
        self.push(list(self.popn(count)))

    def build_set_op(self, count: int) -> None:
        self.push(set(self.popn(count)))

    def build_map_op(self, count: int) -> None:
        items = self.popn(2 * count)
        self.push({key: value for key, value in zip(items[::2], items[1::2])})

    def build_const_key_map_op(self, count: int) -> None:
        keys = self.pop()
        self.push({key: value for key, value in zip(keys, self.popn(count))})

    def build_string_op(self, count: int) -> None:
        self.push(''.join(self.popn(count)))

    def list_to_tuple_op(self):
        self.push(tuple(self.pop()))

    def list_extend_op(self, i: int):
        tos = self.pop()
        list.extend(self.data_stack[-i], tos)

    def set_update_op(self, i):
        tos = self.pop()
        set.update(self.data_stack[-i], tos)

    def dict_update_op(self, i):
        tos = self.pop()
        dict.update(self.data_stack[-i], tos)

    def dict_merge_op(self, i: int):
        tos = self.pop()
        if tos in dict(self.data_stack[-i]).keys():
            dict.update(self.data_stack[-i], tos)
        else:
            raise ValueError(f'key \'{tos}\' is already exist')

    def load_attr_op(self, namei: str):
        tos = self.pop()
        self.push(getattr(tos, namei))

    def compare_op_op(self, opname: str) -> None:
        left_operand, right_operand = self.popn(2)
        # cmp_result = False
        if opname == "==":
            cmp_result = left_operand == right_operand
        elif opname == "!=":
            cmp_result = left_operand != right_operand
        elif opname == "in":
            cmp_result = left_operand in right_operand
        elif opname == "not in":
            cmp_result = left_operand not in right_operand
        elif opname == ">":
            cmp_result = left_operand > right_operand
        elif opname == ">=":
            cmp_result = left_operand >= right_operand
        elif opname == "<":
            cmp_result = left_operand < right_operand
        elif opname == "<=":
            cmp_result = left_operand <= right_operand
        else:
            raise NotImplementedError
        self.push(cmp_result)

    def is_op_op(self, invert):
        left_operand, right_operand = self.popn(2)
        if invert:
            self.push(left_operand is not right_operand)
        else:
            self.push(left_operand is right_operand)

    def contains_op_op(self, invert):
        left_operand, right_operand = self.popn(2)
        if invert:
            self.push(left_operand not in right_operand)
        else:
            self.push(left_operand in right_operand)

    def import_name_op(self, namei: str):
        level, fromlist = self.popn(2)
        self.push(__import__(namei, self.globals, self.locals, fromlist, level))

    def import_from_op(self, namei: str):
        module = self.top()
        self.push(getattr(module, namei))

    def import_star_op(self, arg):
        module = self.pop()
        # self.locals.update(module)
        for attr in dir(module):
            if not attr[0].startswith('_'):
                self.locals[attr] = getattr(module, attr)

    def jump_forward_op(self, delta: int):
        if delta % 2 != 0:
            raise ValueError('Strange delta')
        self.current_offset += delta

    def pop_jump_if_true_op(self, target: int):
        if self.pop():
            self.jump_absolute_op(target)

    def pop_jump_if_false_op(self, target: int):
        if not self.pop():
            self.jump_absolute_op(target)

    def jump_if_not_exc_match_op(self, target: int):
        tos1, tos = self.popn(2)
        if tos1 is not tos:
            self.jump_absolute_op(target)

    def jump_if_true_or_pop_op(self, target: int):
        if self.top():
            self.jump_absolute_op(target)
        else:
            self.pop()

    def jump_if_false_or_pop_op(self, target: int):
        if not self.top():
            self.jump_absolute_op(target)
        else:
            self.pop()

    def jump_absolute_op(self, target: int):
        self.current_offset = target - 2

    def for_iter_op(self, delta):
        tos = self.top()
        # print(tos)
        try:
            # iter_next = next(tos)
            self.push(next(tos))
        except StopIteration:
            # print(f'delta is {delta}')
            # self.jump_forward_op(delta)
            self.pop()
            self.jump_absolute_op(delta)

    def setup_finally_op(self, delta):
        pass

    def load_fast_op(self, var_num):
        if var_num in self.locals:
            self.push(self.locals[var_num])
        else:
            raise UnboundLocalError(f'no variable with name \'{var_num}\'')

    def store_fast_op(self, var_num):
        self.locals[var_num] = self.pop()

    def delete_fast_op(self, var_num):
        del self.locals[var_num]

    def load_closure_op(self, i):
        pass

    # self.push(self.locals[i]) #interesting
    # TODO:

    def load_deref_op(self, i):
        # self.push(self.locals[i])
        assert False, 'Load deref'

    def load_classderef_op(self, i):
        assert False, "load class deref"

    def store_deref_op(self, i):
        assert False, "store deref "

    def delete_deref_op(self, i):
        assert False, "delete deref"

    def raise_varargs_op(self, argc):
        if argc == 0:
            raise
        elif argc == 1:
            raise self.pop()
        elif argc == 2:
            tos1, tos = self.popn(2)
            raise tos1 from tos

    def build_slice_op(self, argc: int):
        if argc in [2, 3]:
            self.push(slice(*self.popn(argc)))
        else:
            raise ValueError(f'Invalid \'{argc}\'')

    def extended_arg_op(self, ext):
        pass

    def format_value_op(self, flags):
        value, fmt_spec = self.popn(2)
        if flags & 0x03 == 0x00:
            self.push(value)
        else:
            if flags & 0x03 == 0x01:
                value = str(value)
            elif flags & 0x03 == 0x02:
                value = repr(value)
            elif flags & 0x03 == 0x03:
                value = ascii(value)
            elif flags & 0x03 == 0x04:
                value = format(value, fmt_spec)
            self.push(value)

    def match_class_op(self, count: int):
        tos, [tos2, tos1] = self.pop(), self.topn(2)
        if isinstance(tos2, tos1):
            #TODO:
            self.pop()
            self.push(dir(tos2))
            self.push(True)
        else:
            self.push(False)

    def gen_start_op(self, kind):
        tos = self.pop()
        #TODO:

    def rot_n_op(self, count: int):
        tos = self.pop()
        below_values = self.popn(count - 1)
        self.push(tos)
        for i in below_values:
            self.push(i)

    def have_argument_op(self):
        pass
        #TODO:

    def load_assertion_error_op(self, message):
        self.push(AssertionError(message))

    def load_build_class_op(self, arg):
        self.push(__build_class__)

    def setup_with_op(self, delta):
        contextmanager = self.pop()
        self.push(contextmanager.__exit__)
        contextmanager_obj = contextmanager.__enter__()
        self.push(contextmanager_obj)

    def copy_dict_without_keys_op(self):
        tos1, tos = self.topn(2)
        self.data_stack[-1] = {key: value for key, value in tos1.items() if key not in tos}

    def get_len_op(self):
        self.push(len(self.top()))

    def match_mapping_op(self):
        self.push(isinstance(self.top(), collections.abc.Mapping))

    def match_sequence_op(self):
        tos = self.top()
        self.push(isinstance(tos, collections.abc.Mapping) and not isinstance(tos, str)
                  and not isinstance(tos, bytes)
                  and not isinstance(tos, bytearray))

    def match_keys_op(self):
        tos1, tos = self.topn(2)
        if set(tos).issubset(set(tos1)):
            self.push(tuple(tos))
            self.push(True)
        else:
            self.push(None)
            self.push(False)

    "Unary operations:"

    def unary_positive_op(self, arg) -> None:
        self.push(+self.pop())

    def unary_negative_op(self, arg) -> None:
        self.push(-self.pop())

    def unary_not_op(self, arg) -> None:
        self.push(not self.pop())

    def unary_invert_op(self, arg) -> None:
        self.push(~self.pop())

    def get_iter_op(self, arg) -> None:
        # print(self.top())
        self.push(iter(self.pop()))

    def get_yield_from_iter_op(self, arg) -> None:
        # TODO: inspect
        if not (asyncio.iscoroutine(self.top())):  # or inspect.isgeneratorfunction(self.top())):
            self.get_iter_op(arg)

    "Binary operations"

    def binary_power_op(self, arg):
        tos1, tos = self.popn(2)
        self.push(tos1 ** tos)

    def binary_multiply_op(self, arg):
        tos1, tos = self.popn(2)
        self.push(tos1 * tos)

    def binary_matrix_multiply_op(self, arg):
        tos1, tos = self.popn(2)
        self.push(tos1 @ tos)

    def binary_floor_divide_op(self, arg):
        tos1, tos = self.popn(2)
        self.push(tos1 // tos)

    def binary_true_divide_op(self, arg):
        tos1, tos = self.popn(2)
        self.push(tos1 / tos)

    def binary_modulo_op(self, arg):
        tos1, tos = self.popn(2)
        self.push(tos1 % tos)

    def binary_add_op(self, arg):
        tos1, tos = self.popn(2)
        # print( f'args are {tos} + {tos1}')
        self.push(tos1 + tos)

    def binary_subtract_op(self, arg):
        tos1, tos = self.popn(2)
        self.push(tos1 - tos)

    def binary_subscr_op(self, arg):
        tos1, tos = self.popn(2)
        self.push(tos1[tos])

    def binary_lshift_op(self, arg):
        tos1, tos = self.popn(2)
        self.push(tos1 << tos)

    def binary_rshift_op(self, arg):
        tos1, tos = self.popn(2)
        self.push(tos1 >> tos)

    def binary_and_op(self, arg):
        tos1, tos = self.popn(2)
        self.push(tos1 & tos)

    def binary_xor_op(self, arg):
        tos1, tos = self.popn(2)
        self.push(tos1 ^ tos)

    def binary_or_op(self, arg):
        tos1, tos = self.popn(2)
        self.push(tos1 | tos)

    "Inplace operations"

    def inplace_power_op(self, arg):
        tos = self.pop()
        self.data_stack[-1] **= tos

    def inplace_multiply_op(self, arg):
        tos = self.pop()
        self.data_stack[-1] *= tos

    def inplace_matrix_multiply_op(self, arg):
        tos = self.pop()
        self.data_stack[-1] @= tos

    def inplace_floor_divide_op(self, arg):
        tos = self.pop()
        self.data_stack[-1] //= tos

    def inplace_true_divide_op(self, arg):
        tos = self.pop()
        self.data_stack[-1] /= tos

    def inplace_modulo_op(self, arg):
        tos = self.pop()
        self.data_stack[-1] %= tos

    def inplace_add_op(self, arg):
        tos = self.pop()
        # print(type(tos))
        self.data_stack[-1] += tos

    def inplace_subtract_op(self, arg):
        tos = self.pop()
        self.data_stack[-1] -= tos

    def inplace_lshift_op(self, arg):
        tos = self.pop()
        self.data_stack[-1] <<= tos

    def inplace_rshift_op(self, arg):
        tos = self.pop()
        self.data_stack[-1] >>= tos

    def inplace_and_op(self, arg):
        tos = self.pop()
        self.data_stack[-1] &= tos

    def inplace_xor_op(self, arg):
        tos = self.pop()
        self.data_stack[-1] ^= tos

    def inplace_or_op(self, arg):
        tos = self.pop()
        self.data_stack[-1] |= tos

    def store_subscr_op(self, arg):
        tos2, tos1, tos = self.topn(3)
        tos1[tos] = tos2

    def delete_subscr_op(self, arg):
        tos1, tos = self.popn(2)
        del tos1[tos]

    "Miscellaneous opcodes"

    def print_expr_op(self):
        print(self.pop())

    def set_add_op(self, i: int):
        tos = self.pop()
        set.add(self.data_stack[-i], tos)

    def list_append_op(self, i: int):
        tos = self.pop()
        list.append(self.data_stack[-i], tos)

    def map_add_op(self, i: int):
        tos1, tos = self.popn(2)
        dict.__setitem__(self.data_stack[-i], tos1, tos)

    "General instructions"

    def nop_op(self, arg):
        pass

    def rot_two_op(self, arg):
        self.rot_n_op(2)

    def rot_three_op(self, arg):
        self.rot_n_op(3)

    def rot_four_op(self, arg):
        self.rot_n_op(4)

    def dup_top_op(self, arg):
        self.push(self.top())

    def dup_top_two_op(self, arg):
        for i in self.topn(2):
            self.push(i)


class VirtualMachine:
    def run(self, code_obj: types.CodeType) -> None:
        """
        :param code_obj: code for interpreting
        """
        globals_context: dict[str, tp.Any] = {'print': print}# , 'range': range, 'str': str, 'set': set, 'sorted': sorted}
        frame = Frame(code_obj, builtins.globals()['__builtins__'], globals_context, globals_context)
        return frame.run()


def compile_code(text_code: tp.Union[types.CodeType, str]) -> types.CodeType:
    """
    This is utility function with primary purpose to convert string code to code type.
    Secondary purpose - print byte code for text_code and all nested text_code
    :param text_code: text code for compiling
    :return: compiled code
    """
    if isinstance(text_code, str):
        # print("Text code:\n{}\n".format(text_code))
        # print("Disassembled code:\n")
        # dis.dis(text_code)
        # print("\n")
        code = compile(text_code, '<stdin>', 'exec')
    else:
        code = text_code

    for const in code.co_consts:
        if isinstance(const, types.CodeType):
            compile_code(const)

    # print("Disassembled code co params:\n")
    # print(
    #     "Co consts: {}\nCo freevars: {}\nCo flags: {}\n"
    #     "Co cellvars: {}\nCo kwonlyargcount: {}\nCo names: {}\n"
    #     "Co nlocals: {}\nCo varnames: {}\nCo stacksize: {}\n"
    #     "Co name: {}\nCo lnotab: {}\nCo argcount: {}\n".format(
    #         code.co_consts, code.co_freevars,
    #         code.co_flags,
    #         code.co_cellvars,
    #         code.co_kwonlyargcount,
    #         code.co_names,
    #         code.co_nlocals,
    #         code.co_varnames,
    #         code.co_stacksize,
    #         code.co_name,
    #         list(code.co_lnotab),
    #         code.co_argcount)
    # )

    return code


if __name__ == "__main__":
    # text_code = '\nx = "-".join(str(z) for z in range(5))\nprint(x)\n'
    # text_code = 'print([str(z) for z in range(5)]\n)'
    # text_code = '\nout = "hello "\nfor i in range(5):\n    out = out + str(i)\nprint(out)\n'
    # text_code = '\nx=5\n'
#     text_code = r"""
# class Thing(object):
#     def __init__(self, x):
#         self.x = x
#     def meth(self, y):
#         return self.x * y
# thing1 = Thing(2)
# thing2 = Thing(3)
# print(thing1.x, thing2.x)
# print(thing1.meth(4), thing2.meth(5))
# """
    text_code = r"""
a,b=(1,3)
b,a=a,b
print(a ** b)   
"""
    vm = VirtualMachine()
    # print(getattr(builtins.globals()["__builtins__"], 'print'))
    # print(dis.dis(text_code))
    print("rv is ", vm.run(compile_code(text_code)))
    # print(getattr(builtins.globals()["__builtins__"], 'print'))
    # print('\n'.join([iter.opname + '  ' + str(iter.arg) for iter in dis.get_instructions(text_code)]))
