import sys, time
import multiprocessing as mp

DELAY = 0.1
DISPLAY = [ '|', '/', '-', '\\' ]

def spinner_func(before='', after=''):
    write, flush = sys.stdout.write, sys.stdout.flush
    pos = -1
    while True:
        pos = (pos + 1) % len(DISPLAY)
        msg = before + DISPLAY[pos] + after
        write(msg); flush()
        write('\x08' * len(msg))
        time.sleep(DELAY)


def compute():
    time.sleep(2)
    return 42

if __name__ == '__main__':
    spinner = mp.Process(None, target=spinner_func, args=('Computing:... ', ''))
    spinner.start()
    try:
        result = compute()
        print(f"Result: {result}")
    except:
        pass
    finally:
        spinner.terminate()
