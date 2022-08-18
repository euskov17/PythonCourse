from types import FunctionType
from typing import Any

CO_VARARGS = 4
CO_VARKEYWORDS = 8

ERR_TOO_MANY_POS_ARGS = 'Too many positional arguments'
ERR_TOO_MANY_KW_ARGS = 'Too many keyword arguments'
ERR_MULT_VALUES_FOR_ARG = 'Multiple values for arguments'
ERR_MISSING_POS_ARGS = 'Missing positional arguments'
ERR_MISSING_KWONLY_ARGS = 'Missing keyword-only arguments'
ERR_POSONLY_PASSED_AS_KW = 'Positional-only argument passed as keyword argument'


def bind_args(func: FunctionType, *args: Any, **kwargs: Any) -> dict[str, Any]:
    """Bind values from `args` and `kwargs` to corresponding arguments of `func`

    :param func: function to be inspected
    :param args: positional arguments to be bound
    :param kwargs: keyword arguments to be bound
    :return: `dict[argument_name] = argument_value` if binding was successful,
             raise TypeError with one of `ERR_*` error descriptions otherwise
    """
    args_dct = {}
    if func.__defaults__:
        default_args = list(func.__defaults__)
    else:
        default_args = []
    if func.__kwdefaults__:
        kwdefault_args = dict(func.__kwdefaults__)
    else:
        kwdefault_args = {}
    args_list = list(args)
    pos_args_cnt = func.__code__.co_posonlyargcount
    unused_kwargs_keys = list(kwargs.keys())
    kwonly_arg_count = func.__code__.co_kwonlyargcount
    posonly_arg_count = func.__code__.co_posonlyargcount
    arg_count = func.__code__.co_argcount
    is_var_args = bool(func.__code__.co_flags & CO_VARARGS)
    is_kwvar_args = bool(func.__code__.co_flags & CO_VARKEYWORDS)
    var_names = func.__code__.co_varnames[:arg_count + is_kwvar_args + is_var_args + kwonly_arg_count]
    iter = 0
    make_var_args = False
    make_kwvar_args = False
    for arg in var_names:
        iter += 1
        if iter <= posonly_arg_count:
            if arg in unused_kwargs_keys and not is_kwvar_args:
                raise TypeError(ERR_POSONLY_PASSED_AS_KW)
            elif args_list:
                args_dct[arg] = args_list.pop(0)
            elif default_args and len(default_args) + iter - 1 >= len(var_names):
                args_dct[arg] = default_args[0]
            else:
                raise TypeError(ERR_MISSING_POS_ARGS)
        elif arg_count < iter <= arg_count + kwonly_arg_count:
            if args_list and not is_var_args:
                raise TypeError(ERR_TOO_MANY_POS_ARGS)
            elif arg in unused_kwargs_keys:
                args_dct[arg] = kwargs[arg]
                unused_kwargs_keys.remove(arg)
            elif arg in kwdefault_args.keys():
                args_dct[arg] = kwdefault_args[arg]
            else:
                raise TypeError(ERR_MISSING_KWONLY_ARGS)
        elif iter > arg_count + kwonly_arg_count:
            if is_var_args and not make_var_args:
                args_dct[arg] = tuple(args_list)
                args_list.clear()
                make_var_args = True
            elif is_kwvar_args and not make_kwvar_args:
                args_dct[arg] = {key: kwargs[key] for key in unused_kwargs_keys}
                kwargs.clear()
                make_kwvar_args = True
            else:
                raise TypeError(ERR_TOO_MANY_POS_ARGS)
        elif arg in unused_kwargs_keys:
            args_dct[arg] = kwargs[arg]
            unused_kwargs_keys.remove(arg)
        elif arg in kwdefault_args.keys() and arg not in kwargs.keys():
            args_dct[arg] = kwdefault_args[arg]
        elif args_list:
            args_dct[arg] = args_list.pop(0)
            pos_args_cnt -= 1
        elif default_args and len(default_args) + iter - 1 >= arg_count:
            args_dct[arg] = default_args[0]
        else:
            raise TypeError(ERR_MISSING_POS_ARGS)
        if len(default_args) + iter - 1 >= len(var_names):
            if default_args:
                default_args.pop(0)
            else:
                raise TypeError(ERR_MISSING_POS_ARGS)
    if args_list:
        if set(var_names) & set(kwargs.keys()):
            raise TypeError(ERR_MULT_VALUES_FOR_ARG)
        else:
            raise TypeError(ERR_TOO_MANY_POS_ARGS)
    return args_dct
