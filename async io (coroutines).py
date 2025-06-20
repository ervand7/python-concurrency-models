import asyncio
import time


# Simulate an asynchronous task (e.g., network or file I/O)
async def fetch_data(id: int) -> str:
    print(f"[{id}] Start fetching...")
    await asyncio.sleep(1)  # Simulate I/O delay
    print(f"[{id}] Done fetching.")
    return f"Data from task {id}"


# Simulate an asynchronous task that processes data
async def process_data(id: int) -> None:
    data = await fetch_data(id)
    print(f"[{id}] Processing: {data}")


# Main coroutine that launches multiple tasks
async def main() -> None:
    start = time.perf_counter()

    # Create coroutine tasks concurrently
    tasks = [asyncio.create_task(process_data(i)) for i in range(5)]

    # Wait for all tasks to complete
    await asyncio.gather(*tasks)

    elapsed = time.perf_counter() - start
    print(f"All tasks completed in {elapsed:.2f} seconds")


# Entry point
if __name__ == "__main__":
    asyncio.run(main())
