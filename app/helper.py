import signal


class GracefulKiller:
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signals, frame_type):
        self.kill_now = True


def get_cpu_temperature() -> float:
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as cpu_temperature_file:
        return int(cpu_temperature_file.read()) / 1000
