from datetime import datetime, timezone
from typing import Optional


class Reading:
    def __init__(self, temperature: float, humidity: Optional[float] = None):
        self.temperature = temperature
        self.humidity = humidity
        self.datetime = datetime.now(tz=timezone.utc)

    def __str__(self):
        temperature = f"temperature {self.temperature:.2f}C"
        if self.humidity:
            return f"{temperature} humidity {self.humidity:.2f}"
        return temperature
