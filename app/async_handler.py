import functools
import signal
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from typing import Protocol, List, Callable, Any, TypeVar, Coroutine, Optional

import asyncio

from app.constants import MODULE_TYPE, METRIC_TYPE
from app.reading import Reading


class Producer(ABC):
    _callback = None

    @property
    @abstractmethod
    def module_id(self) -> str:
        pass

    @property
    @abstractmethod
    def module_type(self) -> MODULE_TYPE:
        pass

    @property
    @abstractmethod
    def supported_metric_types(self) -> List[METRIC_TYPE]:
        pass

    @abstractmethod
    async def get_reading(self, metric_type: METRIC_TYPE) -> Optional[Reading]:
        pass

    def register_producer_callback(
        self, callback: Callable[[Reading], Coroutine[Any, Any, None]]
    ):
        self._callback = callback


class Consumer(Protocol):
    async def consume_reading(self, reading: Reading) -> Coroutine[Any, Any, None]:
        ...


class AsyncHandler:
    def __init__(self):
        self._thread_pool_executor = ThreadPoolExecutor(max_workers=5)
        self._loop = asyncio.get_event_loop()
        self._loop.set_default_executor(self._thread_pool_executor)
        self._queue = asyncio.Queue()
        self._consumer_tasks = []
        self._cleanup_tasks = []
        self._stop_producers = False

    async def sleep(self, delay: float, tick: float = 0.1):
        if self._stop_producers:
            return
        if delay > tick:
            await asyncio.sleep(tick)
            await self.sleep(delay - tick)
        else:
            await asyncio.sleep(delay)

    async def _producer_handler(
        self,
        producer: Producer,
        interval: float = 5,
        pause: Optional[float] = None,
        delay: Optional[float] = None,
    ):
        if delay:
            await self.sleep(interval)
        while not self._stop_producers:
            for metric_type in producer.supported_metric_types:
                reading = await producer.get_reading(metric_type)
                if reading:
                    await self._queue.put(reading)
                if pause:
                    await self.sleep(pause)
            await self.sleep(interval)

    async def _producer_callback(self, reading: Reading):
        await self._queue.put(reading)

    def add_producer(
        self,
        producer: Producer,
        interval: float = 5,
        pause: Optional[float] = None,
        delay: Optional[float] = None,
    ):
        task_name = f"{producer.module_type.value}_{producer.module_id}"
        self._loop.create_task(
            self._producer_handler(producer, interval, pause, delay), name=task_name
        )
        producer.register_producer_callback(self._producer_callback)

    def add_consumer(self, consumer: Consumer):
        self._consumer_tasks.append(consumer)

    async def _consumer_handler(self):
        while True:
            reading = await self._queue.get()
            for task in self._consumer_tasks:
                await task.consume_reading(reading)
            self._queue.task_done()

    def add_cleanup(self, task: Callable[[], Coroutine[Any, Any, None]]):
        self._cleanup_tasks.append(task)

    def run_in_loop(self, task: Callable[[], Coroutine[Any, Any, None]]):
        asyncio.ensure_future(task(), loop=self._loop)

    def stop_producers(self):
        self._stop_producers = True
        print("Producers stopped")

    async def _run_cleanup_tasks(self):
        for task in self._cleanup_tasks:
            await task()
        print("Cleanup tasks done")

    async def shutdown(self):
        self.stop_producers()
        await self._run_cleanup_tasks()

        await self._queue.join()
        print("Done all tasks in the queue")

        self._loop.stop()
        print("Loop stopped")

    def start(self):
        self._loop.create_task(self._consumer_handler(), name="consumer_handler")
        self._loop.add_signal_handler(
            signal.SIGINT, functools.partial(asyncio.ensure_future, self.shutdown())
        )
        self._loop.add_signal_handler(
            signal.SIGTERM, functools.partial(asyncio.ensure_future, self.shutdown())
        )
        try:
            self._loop.run_forever()
        finally:
            self._thread_pool_executor.shutdown()
            print("Thread pool killed")


T = TypeVar("T")


async def run_in_executor(func: Callable[..., T], *args: Any) -> T:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, func, *args)
