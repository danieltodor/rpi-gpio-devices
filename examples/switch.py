from time import sleep
from rpi_gpio_devices import Switch


Switch1 = Switch(11)

Switch1.turn_on()
sleep(2)
Switch1.turn_off()
# Switch1.toggle() # Or toggle the device

Switch1.cleanup()
