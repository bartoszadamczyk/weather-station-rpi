from typing import List

import RPi.GPIO as GPIO  # type: ignore

from .constants import MODEL, METRIC
from .reading import Reading

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


class Relay:
    def __init__(self, pin: int):
        self.pin = pin
        self.state = 0
        GPIO.setup(pin, GPIO.OUT, initial=GPIO.HIGH)

    def up(self):
        self.state = 1
        GPIO.output(self.pin, GPIO.LOW)

    def down(self):
        self.state = 0
        GPIO.output(self.pin, GPIO.HIGH)

    @property
    def id(self) -> str:
        return f"pin{self.pin}"

    async def get_readings(self) -> List[Reading]:
        return [Reading(MODEL.RELAY, self.id, METRIC.GPIO, self.state)]


class RelayCollection:
    def __init__(self, pins: List[int]):
        self.collection = []
        self.lookup = {}

        for pin in pins:
            relay = Relay(pin)
            self.collection.append(relay)
            self.lookup[pin] = relay

    def keys(self):
        return list(self.lookup.keys())

    def __getitem__(self, pin: int):
        return self.lookup[pin]

    def __iter__(self):
        yield from self.collection


def cleanup_gpio():
    print("Cleaning up gpio")
    GPIO.cleanup()
