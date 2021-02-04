from datetime import datetime, timezone


class Reading:
    def __init__(self, sensor, temperature, humidity=None):
        self.sensor = sensor
        self.temperature = temperature
        self.humidity = humidity
        self.datetime = datetime.now(tz=timezone.utc)

    def __str__(self):
        if self.humidity:
            return "sensor {} ID {} temperature {:.2f}C humidity {:.2f}%".format(
                self.sensor.model, self.sensor.id, self.temperature, self.humidity
            )
        return "sensor {} ID {} temperature {:.2f}C".format(
            self.sensor.model, self.sensor.id, self.temperature
        )
