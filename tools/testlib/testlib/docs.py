import typing as tp
import inspect


def is_function_docstring_exists(func: tp.Callable[..., tp.Any]) -> bool:
    docstring = inspect.getdoc(func)
    return docstring is not None and not set(docstring).issubset({' ', '\n'})


def is_class_docstring_exists(cls: type) -> bool:
    docstring = inspect.getdoc(cls)
    return docstring is not None and not set(docstring).issubset({' ', '\n'})
