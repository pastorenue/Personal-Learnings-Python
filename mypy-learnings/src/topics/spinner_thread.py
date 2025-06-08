import itertools
import time
from threading import Thread, Event


def spin(msg: str, done: Event) -> None:
    for char in itertools.cycle(r'\|/-'):
        status = f"\r{char} {msg}"
        print(status, end='', flush=True)
        if done.wait(0.1):
            break
    blanks = ' ' * len(status)
    print(f"\r{blanks}\r", end='')


def is_prime(n: int) -> bool:
    return n > 1 and all(n % i for i in range(2, n))


def slow_function() -> int:
    return is_prime(5_000_111_000_222_021)


def supervisor() -> int:
    done = Event()
    spinner = Thread(target=spin, args=('thinking!', done))
    print(f"{spinner=}")
    spinner.start()
    result = slow_function()
    done.set()
    spinner.join()
    return result


def main():
    result = str(supervisor())
    print(f"{result=:.>25}")



if __name__ == '__main__':
    main()
