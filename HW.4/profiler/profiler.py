def profiler(func):  # type: ignore
    """
    Returns profiling decorator, which counts calls of function
    and measure last function execution time.
    Results are stored as function attributes: `calls`, `last_time_taken`
    :param func: function to decorate
    :return: decorator, which wraps any function passed
    """
    import time
    import functools

    is_first_call = False

    @functools.wraps(func)
    def inner(*args, **kwargs):
        nonlocal is_first_call
        if is_first_call:
            inner.calls = 0
            is_first_call = False
        calls_start = inner.calls
        inner.calls += 1
        start = time.time()
        rv = func(*args, **kwargs)
        end = time.time()
        inner.last_time_taken = end - start
        if not calls_start:
            is_first_call = True
        else:
            is_first_call = False
        return rv

    inner.last_time_taken = 0
    inner.calls = 0
    return inner
