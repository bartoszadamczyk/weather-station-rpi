import board

from sensor import SensorCollection

pins = [board.D17, board.D27]

sensors = SensorCollection()

while True:
    print("Start")
    for reading in sensors.get_all_readings():
        print(reading)
