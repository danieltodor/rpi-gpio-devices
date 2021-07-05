from time import sleep
from rpi_gpio_devices import Button


Button1 = Button(11)

try:
    while True:
        if Button1.is_pressed():
            print('Button1 is pressed!')
        sleep(0.5)
except KeyboardInterrupt:
    Button1.cleanup()
