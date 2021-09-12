#!/usr/bin/python

from time import sleep
import os
import sys
import signal

from rpi_gpio_devices import LED, Button

power_button = Button(5)
led = LED(11)


def sighandle(signum, frame):
    raise InterruptedError


signal.signal(signal.SIGINT, sighandle)
signal.signal(signal.SIGTERM, sighandle)


def welcome_light():
    for _ in range(5):
        led.turn_on()
        sleep(0.2)
        led.turn_off()
        sleep(0.2)


def shutdown_light():
    led.turn_on()
    sleep(3)
    led.turn_off()


def shutdown():
    os.system("shutdown -H now")


welcome_light()
try:
    while True:
        if power_button.is_pressed():
            shutdown_light()
            break
        sleep(1)
except (InterruptedError, KeyboardInterrupt):
    power_button.cleanup()
    sys.exit()

power_button.cleanup()
shutdown()
