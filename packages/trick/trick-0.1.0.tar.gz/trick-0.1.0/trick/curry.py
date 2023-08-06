from functools import wraps 


def curry(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if len(args) + len(kwargs) >= func.__code__.co_argcount:
            return func(*args, **kwargs)
        return lambda *x, **y: wrapper(*args, *x, **kwargs, **y)
    return wrapper

