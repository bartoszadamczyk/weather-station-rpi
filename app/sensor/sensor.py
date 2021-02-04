from .reading import Reading


class MODEL:
    DHT22 = "DHT22"
    DS18B20 = "DS18B20"


class Sensor:
    def __init__(self, pointer, model, pin=None):
        self.pointer = pointer
        self.model = model
        self.id = pin if pin else pointer.id

    def get_reading(self):
        if self.model == MODEL.DS18B20:
            return Reading(self, self.pointer.get_temperature())
        if self.model == MODEL.DHT22:
            try:
                return Reading(self, self.pointer.temperature, self.pointer.humidity)
            except RuntimeError as error:
                print(error.args[0])
                return None
