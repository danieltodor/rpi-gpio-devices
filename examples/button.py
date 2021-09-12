from time import sleep

from rpi_gpio_devices import Button

button = Button(11)

try:
    while True:
        if button.is_pressed():
            print('Button is pressed!')
        sleep(0.5)
except KeyboardInterrupt:
    button.cleanup()
