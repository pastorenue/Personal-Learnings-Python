from multiprocessing import Process, Event as pEvent
from multiprocessing import synchronize

import itertools
import time


def is_prime(n: int) -> bool:
    return n > 1 and all(n % i for i in range(2, n))

def slow_function() -> int:
    is_prime(5_000_111_000_222_021)
    return 42


def spin_proc(msg: str, done: synchronize.Event) -> None:
    for char in itertools.cycle(r'\|/-'):
        status = f"\r{char} {msg}"
        print(status, end='', flush=True)
        if done.wait(0.1):
            break
    blanks = ' ' * len(status)
    print(f"\r{blanks}\r", end='')


def supervisor_proc() -> int:
    done = pEvent()
    spinner = Process(target=spin_proc, args=('thinking!', done))
    print(f"{spinner=}")
    spinner.start()
    result = slow_function()
    done.set()
    spinner.join()
    return result


def main_proc():
    result = str(supervisor_proc())
    print(f"{result=:.>25}")


if __name__ == '__main__':
    main_proc()
