import functools
import signal
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from typing import Protocol, List, Callable, Any, TypeVar, Coroutine, Optional

import asyncio

from .constants import COMPONENT_TYPE, METRIC_TYPE
from .reading import Reading
from .relay import cleanup_gpio


class Producer(ABC):
    _callback = None

    @property
    @abstractmethod
    def component_id(self) -> str:
        pass

    @property
    @abstractmethod
    def component_type(self) -> COMPONENT_TYPE:
        pass

    @property
    @abstractmethod
    def supported_metrics(self) -> List[METRIC_TYPE]:
        pass

    @abstractmethod
    async def get_reading(self, metric: METRIC_TYPE) -> Optional[Reading]:
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
        self, producer: Producer, interval: float = 5, pause: Optional[float] = None
    ):
        while not self._stop_producers:
            for metric in producer.supported_metrics:
                reading = await producer.get_reading(metric)
                if reading:
                    await self._queue.put(reading)
                if pause:
                    await self.sleep(pause)
            await self.sleep(interval)

    async def _producer_callback(self, reading: Reading):
        await self._queue.put(reading)

    def add_producer(
        self, producer: Producer, interval: float = 5, pause: Optional[float] = None
    ):
        self._loop.create_task(self._producer_handler(producer, interval, pause))
        producer.register_producer_callback(self._producer_callback)

    def add_consumer(self, consumer: Consumer):
        self._consumer_tasks.append(consumer)

    async def _consumer_handler(self):
        while True:
            reading = await self._queue.get()
            for task in self._consumer_tasks:
                await task.consume_reading(reading)

    def add_cleanup(self, task: Callable[[None], Coroutine[Any, Any, None]]):
        self._cleanup_tasks.append(task)

    async def shutdown(self):
        self._stop_producers = True
        print("Producers stopped")
        for task in self._cleanup_tasks:
            await task()
        print("Cleanup tasks done")
        await asyncio.sleep(1)
        for task in asyncio.all_tasks(self._loop):
            print("Killing one task")
            task.cancel()
        self._loop.stop()
        print("Loop stopped")

    def start(self):
        self._loop.create_task(self._consumer_handler())
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
            cleanup_gpio()


T = TypeVar("T")


async def run_in_executor(func: Callable[..., T], *args: Any) -> T:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, func, *args)
