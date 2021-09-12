from time import sleep

from rpi_gpio_devices import PWMLED

pwmled = PWMLED(33)

pwmled.set_brightness(50)
sleep(2)
pwmled.set_brightness(100)
sleep(2)
pwmled.set_brightness(0)
# pwmled.turn_off() # Or simply just turn it off

pwmled.cleanup()
