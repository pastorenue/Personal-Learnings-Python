import cProfile

from scipy.optimize import minimize # type: ignore

def do_stuff(n: int) -> list[int]:
    result: list[int] = []
    def f(x: int) -> int:
        return x**4
    for x in range(n):
        result.append(f(x))
    
    return result


def simple_func():
    # c.f. https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html
    func = lambda x: (x[0] - 1) ** 2 + (x[1] - 2.5) ** 2
    x0 = (2, 0)

    constraints = (
        {"type": "ineq", "fun": lambda x: x[0] - 2 * x[1] + 2},
        {"type": "ineq", "fun": lambda x: -x[0] - 2 * x[1] + 6},
        {"type": "ineq", "fun": lambda x: -x[0] + 2 * x[1] + 2},
    )

    bounds = ((0, None), (0, None))

    result = minimize(func, x0, method="SLSQP", bounds=bounds, constraints=constraints)
    print(f"result:\n{result}")
    print(f"best fit parameters: {result.x}")


def main(arg, n):
    match arg:
        case "simple_func":
            simple_func()
        case "do_stuff":
            do_stuff(n)
        case _:
            f = lambda x: x**4
            if not n:
                n = 100
            print(f"result --> {f(n)=}")
            # simple_func()
            do_stuff(n)


def monitor(target):
    import multiprocessing as mp
    import psutil  # type: ignore
    import time

    wp = mp.Process(target=target)
    wp.start()
    p = psutil.Process(wp.pid)

    usages = []
    while wp.is_alive():
        usages.append(p.memory_info().rss)
        time.sleep(0.01)
    wp.join()
    return usages

if __name__ == "__main__":
    import sys
    import pstats

    # args = sys.argv
    # profiler = cProfile.Profile()
    # profiler.enable()
    # try:
    #     arg, n = args[1:]
    #     main(arg, int(n))
    # except IndexError:
    #     main("default", 0)
    # profiler.disable()
    # profiler.dump_stats("example.prof")
    # with cProfile.Profile() as pr:
    #     main("num", 1000000)

    # res = pstats.Stats(pr).sort_stats(pstats.SortKey.TIME)

    # res.dump_stats("example.prof")
    import sys
    print(f"This is the name of the program: {sys.argv[0]}")
    print(f"These are the argument list: {sys.argv[1:]}")
