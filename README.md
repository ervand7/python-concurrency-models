# Python Multiprocessing vs Multithreading vs Coroutines (Asyncio)

| Feature                 | **Multiprocessing**                          | **Multithreading**                                          | **Coroutines (Asyncio)**                               |
|------------------------|----------------------------------------------|-------------------------------------------------------------|---------------------------------------------------------|
| **Definition**          | Multiple **separate processes**              | Multiple threads within a **single process**                | Single-threaded, cooperative multitasking              |
| **Concurrency type**    | CPU-bound tasks                              | I/O-bound tasks                                             | I/O-bound tasks                                        |
| **GIL effect**          | **Not** affected by GIL                      | Affected by GIL (only one thread runs at a time in CPython) | Runs in a single thread; not parallel                  |
| **Memory**              | Separate memory space for each process       | Shared memory between threads                               | Shared memory in one thread                            |
| **Speed for CPU tasks** | Faster for CPU-intensive tasks               | Slower due to GIL                                           | ❌ Not suitable                                        |
| **Speed for I/O tasks** | Heavier and less efficient for I/O-bound     | Fast and lightweight                                        | Very fast and lightweight (no threads/processes)       |
| **Stability**           | A crash in one process doesn’t affect others | A crash in one thread may crash the whole process           | One coroutine failing doesn’t crash others             |
| **Complexity**          | High (inter-process communication needed)    | Moderate                                                    | Can be complex due to event loop and `await` chaining  |
| **Best for**            | Heavy computations                           | Blocking I/O with libraries that don’t support `async`      | High-performance network I/O with `async` libraries    |

---

## 🧠 In short:

- ✅ Use **multiprocessing** for **CPU-bound** tasks (e.g., image processing, heavy math).
- ✅ Use **multithreading** for **I/O-bound** tasks using **blocking libraries**.
- ✅ Use **asyncio** for **I/O-bound** tasks with **`async`-friendly libraries** (e.g., `aiohttp`, `FastAPI`, `aiomysql`).

---
