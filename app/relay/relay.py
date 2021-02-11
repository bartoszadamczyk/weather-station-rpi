import RPi.GPIO as GPIO  # type: ignore

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


class Relay:
    def __init__(self, pin: int) -> None:
        print(f"Setup relay on pin {pin}")
        self.pin = pin
        GPIO.setup(pin, GPIO.OUT)

    def up(self) -> None:
        print(f"Set pin {self.pin} up")
        GPIO.output(self.pin, GPIO.HIGH)

    def down(self) -> None:
        print(f"Set pin {self.pin} down")
        GPIO.output(self.pin, GPIO.LOW)


def cleanup_gpio() -> None:
    print("Cleaning up pins up")
    GPIO.cleanup()
