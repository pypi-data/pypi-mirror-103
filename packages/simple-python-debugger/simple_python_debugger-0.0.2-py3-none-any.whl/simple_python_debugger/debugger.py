import time


def debug(func):
    def _wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()

        print("{}(args: {} kwargs: {}) -> {}".format(
            func.__name__,
            args,
            kwargs,
            result,
        ))
        print("Time of Execution: {}".format(format(end - start, ",.2f")))

    return _wrapper
