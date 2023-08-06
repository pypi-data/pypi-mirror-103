"""
SARAR decorators functions

More details about decorators here: https://gist.github.com/Zearin/2f40b7b9cfc51132851a
"""

from functools import wraps


def emptychecked(func):
    """
    A decorator (for functions and methods) prohibiting all empty arguments.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        # assert len(args) == len(f.__code__.co_varnames)
        for i in range(len(func.__code__.co_varnames)):
            arg_name = func.__code__.co_varnames[i]
            if kwargs and not args:
                if i < len(kwargs):
                    arg_val = list(kwargs.values())[i]
                    if not arg_val and type(arg_val) not in [bool, int, float, complex]:
                        raise Exception(f"The argument `{arg_name}` cannot be empty!")
            else:
                if i < len(args):
                    arg_val = args[i]
                    if not arg_val and type(arg_val) not in [bool, int, float, complex]:
                        raise Exception(f"The argument `{arg_name}` cannot be empty!")
        return func(*args, **kwargs)

    return wrapper


def specificemptychecked(*decorator_args):
    """
    A decorator (for functions and methods) prohibiting specified arguments to be empty.
    """
    # Inspired by https://stackoverflow.com/a/15300191

    def wrapper(func):
        @wraps(func)
        def new_f(*args, **kwds):
            assert len(args) == len(func.__code__.co_varnames)
            for i in range(len(func.__code__.co_varnames)):
                arg_name = func.__code__.co_varnames[i]
                arg_val = args[i]
                for decorator_arg_name in decorator_args:
                    if arg_name == decorator_arg_name:
                        if not arg_val:
                            raise Exception(f"The argument `{arg_name}` cannot be empty!")
            return func(*args, **kwds)

        new_f.__name__ = func.__name__
        return new_f

    return wrapper


def print_types_hints(func):
    """
    A debug decorator (for functions and methods) printing types hints.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        for key, value in func.__annotations__.items():
            print(value, key)
        return func(*args, **kwargs)

    return wrapper
