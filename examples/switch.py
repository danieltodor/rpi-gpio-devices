from time import sleep

from rpi_gpio_devices import Switch

switch = Switch(11)

switch.turn_on()
sleep(2)
switch.turn_off()
# switch.toggle() # Or toggle the device

switch.cleanup()
