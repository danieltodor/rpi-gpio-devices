from time import sleep
from rpi_gpio_devices import LED


LED1 = LED(11)

LED1.turn_on()
sleep(2)
LED1.turn_off()
# LED1.toggle() # Or toggle the device

LED1.cleanup()
