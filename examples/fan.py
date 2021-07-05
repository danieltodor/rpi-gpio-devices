from time import sleep
from rpi_gpio_devices import Fan


# Basic usage
pwm_fan = Fan(power=29, sense=35, pwm=33)

try:
    while True:
        pwm_fan.auto_set()
except KeyboardInterrupt:
    pwm_fan.cleanup()


# Provide your own settings
speed_map = (
    (30, 1),
    (40, 50),
    (50, 100),
)
external_fan = Fan(power=29, sense=35, pwm=33, speed_map=speed_map, cycletime=0, idle_limit=0)

external_fan.set_speed(50)
sleep(5)
external_fan.set_speed(0)
# external_fan.turn_off() # Or just turn it off
try:
    while True:
        temp = external_temp() # Write a function that reads temperature from a sensor
        external_fan.auto_set(temp)
        # Do some other stuff
        sleep(5)
except KeyboardInterrupt:
    external_fan.cleanup()
