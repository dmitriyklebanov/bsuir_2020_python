import functools
import warnings


def cached(func):
    '''Cache function arguments and its result.

    Supports only hashable function arguments. Warn if arguments are not hashable.
    '''

    cache = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            params = (args, tuple(kwargs.items()))
            if params in cache:
                return cache[params]
            else:
                res = func(*args, **kwargs)
                cache[params] = res
                return res
        except TypeError:
            warnings.warn(
                'cached: arguments are not hashable. Caching is unavailable.',
                RuntimeWarning)
            return func(*args, **kwargs)
    return wrapper
