from tqdm.contrib import tmap
from tqdm.contrib.concurrent import thread_map as tqdm_thread_map


def thread_map(fn, *iterables, **kwargs):
    # progress bar not needed for single element
    if len(iterables[0]) == 1:
        return map(fn, *iterables)

    # multithreading not needed for one worker
    if kwargs.get("max_workers") == 1:
        return tmap(fn, *iterables)

    return tqdm_thread_map(fn, *iterables, **kwargs)
