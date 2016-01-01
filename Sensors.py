import RPi.GPIO as GPIO
from time import sleep as sleep_in_seconds

GPIO.setmode(GPIO.BCM)

## TODO : fork another process to do this and communicate over IPC.
## DO NOT trust python threads.
##
## IN THE MEANTIME
## Set up something to poll forever, calling callbacks under certain
## conditions.
class GPIOSensor:
    def __init__(self, pin=21):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.IN)

    def is_on(self):
        return GPIO.input(self.pin) == 1

    def loop_and_poll(self, callback, timeout_ms=300, history=10):
        should_loop = true
        readings = []
        while should_loop:
            sleep_in_seconds(timeout_ms * 0.01)
            readings.reverse()
            readings.append(self.is_on())
            num_items_to_trim = max(0, len(readings) - history)
            readings = readings[num_items_to_trim:]
            readings.reverse()
            should_loop = callback(readings, self.is_on())
