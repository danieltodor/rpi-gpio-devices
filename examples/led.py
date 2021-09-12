from time import sleep

from rpi_gpio_devices import LED

led = LED(11)

led.turn_on()
sleep(2)
led.turn_off()
# led.toggle() # Or toggle the device

led.cleanup()
