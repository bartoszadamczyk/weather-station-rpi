from typing import List

import RPi.GPIO as GPIO  # type: ignore

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


class Relay:
    def __init__(self, pin: int):
        print(f"Setup relay on pin {pin}")
        self.pin = pin
        GPIO.setup(pin, GPIO.OUT, initial=GPIO.HIGH)

    def up(self):
        print(f"Set pin {self.pin} up")
        GPIO.output(self.pin, GPIO.LOW)

    def down(self):
        print(f"Set pin {self.pin} down")
        GPIO.output(self.pin, GPIO.HIGH)


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
