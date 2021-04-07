from typing import Protocol, List

import asyncio

from .reading import Reading


class Producer(Protocol):
    async def get_readings(self) -> List[Reading]:
        ...


class Consumer(Protocol):
    async def consume_reading(self, reading: Reading):
        ...


class AsyncHandler:
    def __init__(self):
        self.queue = asyncio.Queue()
        self.loop = asyncio.get_event_loop()
        self.producer_tasks = []
        self.consumer_tasks = []
        self.cleanup_tasks = []

    async def _producer_handler(self, producer: Producer, interval: int = 5):
        while True:
            readings = await producer.get_readings()
            for reading in readings:
                await self.queue.put(reading)
            await asyncio.sleep(interval)

    def add_producer(self, producer: Producer, interval: int = 5):
        self.loop.create_task(self._producer_handler(producer, interval))

    def add_consumer(self, consumer: Consumer):
        self.consumer_tasks.append(consumer)

    async def _consumer_handler(self):
        while True:
            reading = await self.queue.get()
            for task in self.consumer_tasks:
                await task.consume_reading(reading)

    def add_cleanup(self, task):
        self.cleanup_tasks.append(task)

    def start(self):
        self.loop.create_task(self._consumer_handler())
        try:
            self.loop.run_forever()
        finally:
            for task in self.cleanup_tasks:
                task()
