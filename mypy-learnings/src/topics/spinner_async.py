import asyncio
import itertools
import time


async def is_prime(n: int) -> bool:
    await asyncio.sleep(0.1)
    return n > 1 and all(n % i for i in range(2, n))


async def spin(msg: str):
    for char in itertools.cycle(['|', '/', '-', '\\']):
        status = f'\r{char} {msg}'
        print(status, end='', flush=True)
        try:
            await asyncio.sleep(0.1)
        except asyncio.CancelledError:
            break
    
    blanks = ' ' * len(status)
    print(f"\r{blanks}\r", end='')


async def slow():
    await is_prime(5_000_111_000_222_021)
    return 42


async def supervisor() -> int:
    spinner = asyncio.create_task(spin('thinking!'))
    print(f"{spinner=}")
    result = await slow()
    spinner.cancel()
    return result


def main():
    result = str(asyncio.run(supervisor()))
    print(f"{result=:.>25}")


if __name__ == '__main__':
    main()