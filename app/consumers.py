from .reading import Reading


class ReadingsLogger:
    count = 0

    async def consume_reading(self, reading: Reading):
        if self.count < 50 or self.count % 100:
            print(reading)
        self.count += 1
