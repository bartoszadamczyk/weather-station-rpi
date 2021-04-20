import functools
from typing import List, Optional

import RPi.GPIO as GPIO  # type: ignore

from app.async_handler import Producer, run_in_executor
from app.constants import MODULE_TYPE, METRIC_TYPE
from app.reading import Reading

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


class Relay(Producer):
    def __init__(self, pin: int):
        super().__init__()
        self._pin = pin
        self._state = 0
        self._is_active = False
        GPIO.setup(pin, GPIO.OUT, initial=GPIO.HIGH)

    async def init(self):
        if self._is_active:
            return
        self._state = 0
        self._is_active = True
        await run_in_executor(
            functools.partial(GPIO.setup, self._pin, GPIO.OUT, initial=GPIO.HIGH)
        )
        await self._callback(self._get_reading(METRIC_TYPE.STATE))

    async def up(self):
        if self._is_active and self._state == 0:
            self._state = 1
            await run_in_executor(GPIO.output, self._pin, GPIO.LOW)
            await self._callback(self._get_reading(METRIC_TYPE.STATE))

    async def down(self):
        if self._is_active and self._state == 1:
            self._state = 0
            await run_in_executor(GPIO.output, self._pin, GPIO.HIGH)
            await self._callback(self._get_reading(METRIC_TYPE.STATE))

    async def cleanup(self):
        if self._is_active:
            self._is_active = False
            self._state = 0
            await run_in_executor(GPIO.cleanup, self._pin)
            await self._callback(self._get_reading(METRIC_TYPE.STATE))

    @property
    def module_id(self) -> str:
        return f"pin{self._pin}"

    @property
    def module_type(self) -> MODULE_TYPE:
        return MODULE_TYPE.RELAY

    @property
    def supported_metric_types(self) -> List[METRIC_TYPE]:
        return [METRIC_TYPE.STATE]

    def _get_reading(self, metric_type: METRIC_TYPE):
        return Reading(self.module_type, self.module_id, metric_type, self._state)

    async def get_reading(self, metric_type: METRIC_TYPE) -> Optional[Reading]:
        if metric_type in self.supported_metric_types:
            return self._get_reading(metric_type)
        return None


class RelayHandler:
    def __init__(self, pins: List[int]):
        self._collection = []
        self._lookup = {}

        for pin in pins:
            relay = Relay(pin)
            self._collection.append(relay)
            self._lookup[pin] = relay

    def keys(self):
        return list(self._lookup.keys())

    def __getitem__(self, pin: int):
        return self._lookup[pin]

    def __iter__(self):
        yield from self._collection

    async def init(self):
        for rely in self:
            await rely.init()

    async def cleanup(self):
        for rely in self:
            await rely.cleanup()


def cleanup_gpio():
    print("Final GPIO cleanup")
    GPIO.cleanup()
