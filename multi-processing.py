import os
import time
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import (
    Process,
    Queue,
    Pipe,
    Value,
    Array,
    Pool,
    Manager,
    connection,
    queues,
)
from multiprocessing.managers import DictProxy
from multiprocessing.sharedctypes import Synchronized, SynchronizedArray
from typing import List


# CPU-bound task to demonstrate GIL is not an issue with multiprocessing
def cpu_bound_task(x: int) -> int:
    count: int = 0
    for i in range(10 ** 6):
        count += i % x
    return count


# Demonstrates creating basic Process
def simple_process(name: str) -> None:
    print(f"[{os.getpid()}] Hello from process: {name}")


# Demonstrates Queue (interprocess communication)
def queue_worker(q: queues.Queue) -> None:
    for i in range(5):
        q.put(f"Message {i} from {os.getpid()}")


# Demonstrates Pipe (duplex communication)
def pipe_worker(conn: connection.Connection) -> None:
    conn.send("Hello from child process!")
    conn.close()


# Demonstrates sharing value across processes
def value_worker(val: Synchronized) -> None:
    for _ in range(5):
        with val.get_lock():
            val.value += 1
        time.sleep(0.1)


# Demonstrates shared array
def array_worker(arr: SynchronizedArray) -> None:
    for i in range(len(arr)):
        arr[i] += 1


# Demonstrates Manager for shared state
def manager_worker(shared_dict: DictProxy, idx: int) -> None:
    shared_dict[idx] = f"Done by {os.getpid()}"


def main() -> None:
    print(f"[{os.getpid()}] Main process starting")

    # 1. Creating processes with Process
    p1 = Process(target=simple_process, args=("Process-1",))
    p1.start()
    p1.join()

    # 2. Queue example
    q = Queue()
    p2: Process = Process(target=queue_worker, args=(q,))
    p2.start()
    p2.join()
    while not q.empty():
        print(q.get())

    # 3. Pipe example
    parent_conn, child_conn = Pipe()
    p3 = Process(target=pipe_worker, args=(child_conn,))
    p3.start()
    print(parent_conn.recv())
    p3.join()

    # 4. Value example
    val: Synchronized = Value('i', 0)
    p4: Process = Process(target=value_worker, args=(val,))
    p4.start()
    p4.join()
    print("Value after process:", val.value)

    # 5. Array example
    arr: SynchronizedArray = Array('i', [1, 2, 3])
    p5: Process = Process(target=array_worker, args=(arr,))
    p5.start()
    p5.join()
    print("Array after process:", list(arr))

    # 6. Manager example
    with Manager() as manager:
        shared_dict: DictProxy = manager.dict()
        processes: List[Process] = [Process(target=manager_worker, args=(shared_dict, i)) for i in range(4)]
        for p in processes:
            p.start()
        for p in processes:
            p.join()
        print("Shared dict via Manager:", dict(shared_dict))

    # 7. Pool example
    with Pool(4) as pool:
        results: List[int] = pool.map(cpu_bound_task, [2, 3, 4, 5])
        print("Results from multiprocessing.Pool:", results)

    # 8. ProcessPoolExecutor example
    with ProcessPoolExecutor(max_workers=4) as executor:
        futures: List[int] = list(executor.map(cpu_bound_task, range(2, 6)))
        print("Results from ProcessPoolExecutor:", futures)

    print(f"[{os.getpid()}] Main process exiting")


if __name__ == "__main__":
    main()
