from time import sleep
from rpi_gpio_devices import PWMLED


PWMLED1 = PWMLED(33)

PWMLED1.set_brightness(50)
sleep(2)
PWMLED1.set_brightness(100)
sleep(2)
PWMLED1.set_brightness(0)
# PWMLED1.turn_off() # Or simply just turn it off

PWMLED1.cleanup()
