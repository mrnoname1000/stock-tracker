from tqdm.contrib import tmap
from tqdm.contrib.concurrent import thread_map


def vanilla_thread_map(fn, *iterables, **kwargs):
    import concurrent.futures

    max_workers = kwargs.get("max_workers")
    chunksize = kwargs.get("chunksize")

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as ex:
        return list(ex.map(fn, *iterables, chunksize=chunksize))


def thread_map(fn, *iterables, **kwargs):
    # progress bar not needed for single element
    if len(iterables[0]) == 1:
        return map(fn, *iterables)


    # determine if progress bar is wanted
    max_workers = kwargs.get("max_workers")


    # multithreading not needed for one worker
    if max_workers is not None and max_workers == 1:
        return tmap(fn, *iterables)

    return thread_map(fn, *iterables, **kwargs)
