"""Compare resources used by list vs generator.

Outputs memory usage and time to complete for functions with large
iterables using a list vs generator.

Args:
    check (str): iterable and resource combo.
    number (integer): size of iterable or number of times called.

Examples:
    See output regarding memory or time::
        $ python list_gen_resources.py list_mem 80000
        # Increment memory used by iterable: 3.1 MiB

        $ python list_gen_resources.py gen_mem 80000
        # Increment memory used by iterable: 0.0 MiB

        $ python list_gen_resources.py list_time 1000
        iter_list() time: 5.65961676599909

        $ python list_gen_resources.py gen_time 1000
        iter_gen() time: 6.189864045001741

        $ python -m list_gen_resources malloc
        list_gen_resources.py:58: size=15.3 MiB, count=399984, average=40 B
        list_gen_resources.py:59: size=408 B, count=3, average=136 B
"""

from memory_profiler import profile
import sys
from timeit import timeit
import tracemalloc


TIMEIT_CALLS = 1000
ITER_LEN = 80000


def iter_list(length=None):
    iterable_length = length or ITER_LEN
    x = [i ** 2 for i in range(iterable_length)]

    for i in x:
        assert i > -1


def iter_gen(length=None):
    iterable_length = length or ITER_LEN
    x = (i ** 2 for i in range(iterable_length))

    for i in x:
        assert i > -1

def malloc_check():
    tracemalloc.start()

    # ... run your application ...
    my_list = [i ** 2 for i in range(ITER_LEN * 5)]
    my_gen = (i ** 2 for i in range(ITER_LEN * 5))

    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('lineno')

    for stat in top_stats:
        print(stat)


if __name__ == "__main__":
    func = sys.argv[1]
    try:
        num = int(sys.argv[2])
    except (IndexError, ValueError):
        num = None

    match func:
        case "list_mem":
            list_profiled = profile(iter_list)
            list_profiled(num)
        case "gen_mem":
            gen_profiled = profile(iter_gen)
            gen_profiled(num)
        case "list_time":
            call_count = num or TIMEIT_CALLS
            print(f"iter_list() time: {timeit(iter_list, number=call_count)}")
        case "gen_time":
            call_count = num or TIMEIT_CALLS
            print(f"iter_gen() time: {timeit(iter_gen, number=call_count)}")
        case "malloc":
            malloc_check()
