import time
import threading

# Lock
lock = threading.Lock()
def func1():
    with lock:
        print('func1')
        time.sleep(1)
        func2()
        return 42

def func2():
    with lock:
        print('func2')
        time.sleep(1)
        print('func2 done')
        return 42

# Semaphore
semaphore = threading.Semaphore(2)
def func3():
    with semaphore:
        print('func3')
        time.sleep(1)
        print('func3 done')
        return 42

def func4():
    with semaphore:
        print('func4')
        time.sleep(1)
        print('func4 done')
        return 42

b = threading.Barrier(1)
def func5():
    print('func5')
    b.wait()
    print('func5 done')
    return 42

def func6():
    print('func6')
    b.wait()
    print('func6 done')
    return 42

def func7():
    func5()
    func6()

def data_processor(barrier: threading.Barrier, worker_id: int):
    # Phase 1: Load Data
    print(f"Worker {worker_id} loading data...")
    time.sleep(worker_id)  # Simulate different load times
    barrier.wait()
    
    # Phase 2: Process Data
    print(f"Worker {worker_id} processing data...")
    time.sleep(worker_id)
    barrier.wait()
    
    # Phase 3: Save Results
    print(f"Worker {worker_id} saving results...")
    barrier.wait()
    
    print(f"Worker {worker_id} finished")

# Synchronize 3 workers
worker_count = 3
sync_barrier = threading.Barrier(worker_count)

# Start workers
workers = []
for i in range(worker_count):
    t = threading.Thread(target=data_processor, args=(sync_barrier, i))
    workers.append(t)
    t.start()

# Wait for all workers to finish
for t in workers:
    t.join()

# if __name__ == '__main__':
#     # print(func1())
#     # print(func2())
#     # print(func3())
#     # print(func4())
#     print(threading.active_count())
#     current_thread = threading.current_thread()
#     print(current_thread.daemon)
#     print(threading.getprofile())
#     print(threading.gettrace())
#     print(func7())
#     # print(func6())

import ctypes

x = '0x14000104020'
x_ = ctypes.string_at(int(x, 16), 10)
print(x_)  # 42