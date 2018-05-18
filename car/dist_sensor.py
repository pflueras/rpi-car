import RPi.GPIO as GPIO
import time

class DistSensor:
    max_scan_time = 0.1

    def __init__(self, trig_pin, echo_pin):
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin

        GPIO.setup(trig_pin, GPIO.OUT)
        GPIO.setup(echo_pin, GPIO.IN)

    def read_distance(self):
        """Read the distance sensor"""

        # Set trigger to high
        GPIO.output(self.trig_pin, GPIO.HIGH)

        # Set trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(self.trig_pin, GPIO.LOW)

        time_start = time.time()
        loop_start = time.time()
        while GPIO.input(self.echo_pin) == 0 and time.time() - loop_start < DistSensor.max_scan_time:
            time_start = time.time()

        time_end = time.time()
        loop_start = time.time()
        while GPIO.input(self.echo_pin) == 1 and time.time() - loop_start < DistSensor.max_scan_time:
            time_end = time.time()

        duration = time_end - time_start
        distance = (duration * 34300) / 2

        return distance