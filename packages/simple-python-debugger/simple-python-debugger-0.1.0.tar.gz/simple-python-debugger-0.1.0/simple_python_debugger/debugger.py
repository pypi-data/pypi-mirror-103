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

        time_taken = format(end - start, ",.2f")
        print("Time of Execution: {} seconds".format(time_taken))

    return _wrapper
