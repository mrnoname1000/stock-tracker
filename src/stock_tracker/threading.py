import concurrent.futures

try:
    from tqdm.contrib import tmap as tqdm_map
    from tqdm.contrib.concurrent import thread_map as tqdm_thread_map
except ImportError:
    tqdm_map = None
    tqdm_thread_map = None


def vanilla_thread_map(fn, *iterables, **kwargs):
    max_workers = kwargs.get("max_workers")
    chunksize = kwargs.get("chunksize")

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as ex:
        return list(ex.map(fn, *iterables, chunksize=chunksize))


def tmap(fn, *iterables, **kwargs):
    max_workers = kwargs.get("max_workers")

    if kwargs.get("progress") and tqdm_map and tqdm_thread_map:
        tmap = tqdm_map
        thread_map = tqdm_thread_map
    else:
        tmap = map
        thread_map = vanilla_thread_map

    if len(iterables[0]) == 1 or max_workers is not None and max_workers == 1:
        return tmap(fn, *iterables, chunksize=kwargs.get("chunksize"))

    return thread_map(fn, *iterables, **kwargs)
