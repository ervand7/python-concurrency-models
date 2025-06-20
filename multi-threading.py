import time
from concurrent.futures import ThreadPoolExecutor
from threading import Thread, Lock, RLock, Semaphore, Condition, Event
from typing import List

# Shared resource and synchronization primitives
counter: int = 0  # Shared variable to demonstrate race conditions
counter_lock: Lock = Lock()  # Ensures exclusive access to `counter`
reentrant_lock: RLock = RLock()  # Reentrant lock for nested locking in same thread
semaphore: Semaphore = Semaphore(2)  # Allows only 2 threads into a section at once
condition: Condition = Condition()  # Used to notify threads when a condition is met
event: Event = Event()  # Used to signal threads from another thread


# Thread-safe increment using Lock
def increment_with_lock() -> None:
    global counter
    for _ in range(100000):
        with counter_lock:
            counter += 1


# Unsafe increment (race condition example)
def unsafe_increment() -> None:
    global counter
    for _ in range(100000):
        counter += 1  # Not protected — may result in data races


# Demonstrates nested locking with RLock
def reentrant_lock_example() -> None:
    with reentrant_lock:
        print("Outer lock acquired")
        with reentrant_lock:
            print("Inner lock acquired")  # Safe due to reentrant nature
        print("Inner lock released")
    print("Outer lock released")


# Semaphore allows only 2 threads to enter this block at a time
def semaphore_example(i: int) -> None:
    with semaphore:
        print(f"Thread {i} entered the critical section")
        time.sleep(1)
        print(f"Thread {i} leaving the critical section")


# A thread waits until it is notified via condition
def condition_example() -> None:
    with condition:
        print("Thread waiting for condition...")
        condition.wait()  # Wait until another thread notifies
        print("Thread resumed after condition notified")


# A thread waits until an event is set
def event_example() -> None:
    print("Waiting for event to be set...")
    event.wait()  # Block until `event.set()` is called
    print("Event has been set!")


# Daemon thread runs in the background and ends with main program
def daemon_example() -> None:
    while True:
        print("Daemon thread is running...")
        time.sleep(1)


# Function used with ThreadPoolExecutor — squares a number
def thread_pool_example(x: int) -> int:
    return x * x


# Main execution flow demonstrating all threading concepts
def main() -> None:
    global counter

    # 1. Creating and starting threads using safe increment
    t1: Thread = Thread(target=increment_with_lock)
    t2: Thread = Thread(target=increment_with_lock)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print("Counter after lock-safe increment:", counter)

    # 2. Race condition demonstration without lock
    counter = 0
    t3: Thread = Thread(target=unsafe_increment)
    t4: Thread = Thread(target=unsafe_increment)
    t3.start()
    t4.start()
    t3.join()
    t4.join()
    print("Counter after unsafe increment (with race condition):", counter)

    # 3. RLock usage
    reentrant_lock_example()

    # 4. Semaphore usage with 4 threads
    for i in range(4):
        Thread(target=semaphore_example, args=(i,)).start()

    # 5. Condition variable to control thread execution
    Thread(target=condition_example).start()
    time.sleep(2)
    with condition:
        condition.notify()  # Wake up the waiting thread

    # 6. Event to signal between threads
    Thread(target=event_example).start()
    time.sleep(2)
    event.set()  # Trigger the event to unblock the thread

    # 7. Daemon thread example
    daemon: Thread = Thread(target=daemon_example)
    daemon.daemon = True  # Will exit when main program ends
    daemon.start()

    # 8. ThreadPoolExecutor to parallelize function calls
    with ThreadPoolExecutor(max_workers=4) as executor:
        results: List[int] = list(executor.map(thread_pool_example, range(5)))
        print("Results from ThreadPoolExecutor:", results)

    time.sleep(3)
    print("Main thread exiting.")


if __name__ == "__main__":
    main()
