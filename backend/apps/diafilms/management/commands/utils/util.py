import functools
import time


def timer(func):
    """Timer Decorator for measuring execution performance

    Args:
        none

    Returns:
        value
    """
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()

        value = func(*args, **kwargs)

        run_time = time.perf_counter() - start_time

        if run_time < 0.01:
            fraction = 1/run_time
            print(
                f"Finished {func.__name__!r} in 1/{fraction:.1f} fraction of a second!")
        else:
            print(f"Finished {func.__name__!r} in {run_time:.2f} secs")

        return value
    return wrapper_timer
