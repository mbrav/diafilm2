import asyncio
import functools
import time

import requests
from tqdm import tqdm


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


def async_looper(concurrent: int, items: list[str], desc: str = 'Looping'):
    """Async Decorator for batch processing a list of items

    Works.

    :param concurrent: How many concurrent async threads to execute
    :type concurrent: int

    :param items: List of items to loop through
    :type items: list[str]

    :param desc: String to display in progress bar
    :type desc: str

    :return: List of responses
    :type: list
    """

    def inner_func(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            pool = asyncio.new_event_loop()
            asyncio.set_event_loop(pool)
            responses = []

            async def looper():
                loops = len(items) // concurrent + 1
                cur_loop = 0

                pbar = tqdm(total=len(items), desc=desc)
                for loop in range(loops):
                    batch = concurrent
                    if loop == len(items):
                        batch = len(items) % concurrent
                    tasks = []
                    i = cur_loop*concurrent
                    for item in items[i:i+batch]:
                        tasks.append(
                            # pool.run_in_executor(None, requests.get, item)
                            pool.run_in_executor(None, func, item))
                    for response in await asyncio.gather(*tasks):
                        pbar.update()
                        responses.append(response)
                    cur_loop += 1
            pool.run_until_complete(looper())
            return responses

        return wrapper
    return inner_func


@timer
def test():
    urls = [f'https://www.google.com/search?q={x+1}' for x in range(100)]

    @async_looper(concurrent=4, items=urls, desc='Downloading urls')
    def req(_url):
        res = requests.get(_url)
        custom = 'Do super cool custom calculation' * 123
        return res

    responses = req()
    # for res in responses:
    #     print(res, res.url)
    print(f'Got {len(responses)} responses')


if __name__ == '__main__':
    test()
