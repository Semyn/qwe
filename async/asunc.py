import asyncio
import aiofiles
import datetime
import inspect
import uuid

class AsyncLogger:
    def __init__(self, filename):
        self.filename = filename

    async def log(self, level: str, message: str):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        caller = inspect.stack()[2].function
        log_message = f"{timestamp} [{level}] ({caller}): {message}\n"
        async with aiofiles.open(self.filename, mode='a') as f:
            await f.write(log_message)

def get_unique_log_filename():
    now = datetime.datetime.now()
    filename = now.strftime("%Y%m%d_%H%M%S") + "_log_" + str(uuid.uuid4()) + ".txt"
    return filename

import asyncio
import random

class AsyncTaskQueue:
    def __init__(self, logger):
        self.queue = asyncio.Queue()
        self.logger = logger
        self.running = True

    async def add_task(self, task):
        await self.queue.put(task)
        await self.logger.log('INFO', f"Task added: {task}")
    
    async def process_task(self, task):
        await self.logger.log('DEBUG', f"Processing task: {task}")
        await asyncio.sleep(random.uniform(0.5, 1.5))
        await self.logger.log('INFO', f"Completed task: {task}")

    async def worker(self):
        while self.running or not self.queue.empty():
            try:
                task = await asyncio.wait_for(self.queue.get(), timeout=1)
                await self.process_task(task)
                self.queue.task_done()
                await self.logger.log('DEBUG', f"Remaining tasks in queue: {self.queue.qsize()}")
            except asyncio.TimeoutError:
                if not self.running:
                    break
        await self.logger.log('ERROR', "Worker has stopped due to queue closure or timeout.")
    
    async def close(self):
        self.running = False
        await self.queue.join()


async def main():
    filename = get_unique_log_filename()
    logger = AsyncLogger(filename)
    queue = AsyncTaskQueue(logger)

    worker_task = asyncio.create_task(queue.worker())

    for i in range(5):
        await queue.add_task(f"Task {i+1}")
        await asyncio.sleep(0.2)
    await queue.close()
    await worker_task
    print(f"Лог сохранен в файл: {filename}")

asyncio.run(main())