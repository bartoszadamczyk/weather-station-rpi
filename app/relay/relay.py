import RPi.GPIO as GPIO  # type: ignore

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


class Relay:
    def __init__(self, pin: int) -> None:
        self.pin = pin
        GPIO.setup(pin, GPIO.OUT)

    def up(self) -> None:
        GPIO.output(self.pin, GPIO.HIGH)

    def down(self) -> None:
        GPIO.output(self.pin, GPIO.LOW)


def cleanup_gpio() -> None:
    GPIO.cleanup()
