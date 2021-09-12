#!/usr/bin/python

import signal

from rpi_gpio_devices import Fan

sm = [
    (60, 1),
    (65, 30),
    (70, 50),
    (75, 70),
    (80, 100)
]
fan = Fan(power=29, sense=35, pwm=33, speed_mapping=sm)


def sighandle(signum, frame):
    raise InterruptedError


signal.signal(signal.SIGINT, sighandle)
signal.signal(signal.SIGTERM, sighandle)

try:
    while True:
        fan.auto_set()
except (InterruptedError, KeyboardInterrupt):
    fan.cleanup()
