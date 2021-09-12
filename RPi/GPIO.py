""" Mock objects to test switching logic """

import time

# RPi.GPIO const values (offset included)
BOARD = 10
BCM = 11

OUT = 0
IN = 1

LOW = 0
HIGH = 1

PUD_OFF = 20
PUD_DOWN = 21
PUD_UP = 22

RISING = 31
FALLING = 32
BOTH = 33

# Setup gpio_pins
gpio_pins = {}
pin_values = {
    'mode': None, # input or output
    'output': LOW, # low or high
    'input': None, # to check the level of an input pin
    'duty_cycle': 0, # pwm duty cycle
    'pwm': False, # pin was set to PWM or not
    'pull_up_down': False
}
for i in range(1, 40):
    gpio_pins[i] = {**pin_values}


def cleanup():
    pass


def get_pin(pin):
    return gpio_pins[pin]


def setmode(value):
    if value not in [BOARD, BCM]:
        raise ValueError(f'Invalid value: {value}')


def setwarnings(value):
    if not isinstance(value, bool):
        raise ValueError(f'Value must be boolean. Not: {type(value)}')


def setup(pin, mode, pull_up_down=False):
    if mode in [0, False]:
        mode = OUT
    elif mode in [1, True]:
        mode = IN
    if pull_up_down and pull_up_down not in [PUD_DOWN, PUD_UP]:
        raise ValueError(f'Invalid pull_up_down value: {pull_up_down}')
    get_pin(pin)['mode'] = mode
    get_pin(pin)['pull_up_down'] = pull_up_down


def assert_setup(pin, mode, pull_up_down=False):
    """ Assert the IN and OUT modes of the pin, and the pull_up_down state """
    if mode in [0, False]:
        mode = OUT
    elif mode in [1, True]:
        mode = IN
    current_mode = get_pin(pin)['mode']
    if current_mode != mode:
        raise ValueError(f'Expected pin mode: {mode}. Current mode: {current_mode}')
    current_pull_up_down = get_pin(pin)['pull_up_down']
    if pull_up_down and current_pull_up_down != pull_up_down:
        raise ValueError(f'Expected pull_up_down: {pull_up_down}. Current pull_up_down: {current_pull_up_down}')


# pylint: disable=W0622
def input(pin):
    return get_pin(pin)['input']


def set_input(pin, state):
    """ Set the input state of a pin (True or False) """
    if not isinstance(state, bool):
        raise ValueError(f'state must be boolean, not {type(state)}')
    if get_pin(pin)['mode'] != IN:
        raise Exception(f'Pin {pin} is not an input pin.')
    get_pin(pin)['input'] = state


def output(pin, value):
    if value in [0, False]:
        value = LOW
    elif value in [1, True]:
        value = HIGH
    if get_pin(pin)['mode'] != OUT:
        raise Exception(f'Pin was not configured to be an output: {pin}')
    get_pin(pin)['output'] = value


def assert_output(pin, value):
    """ Assert the LOW and HIGH value of the pin """
    if value in [0, False]:
        value = LOW
    elif value in [1, True]:
        value = HIGH
    output_level = get_pin(pin)['output']
    if output_level != value:
        expectation = 'HIGH' if output_level is HIGH else 'LOW'
        raise Exception(f'Pin {pin} is {expectation}')


class PWM:
    def __init__(self, pin, frequency):
        if get_pin(pin)['mode'] is not OUT:
            raise Exception(f'Pin {pin} must be set to output before initializing PWM on it')
        get_pin(pin)['pwm'] = True
        self.pin = pin
        self.frequency = frequency

    def start(self, percent):
        get_pin(self.pin)['output'] = HIGH
        get_pin(self.pin)['duty_cycle'] = percent

    def stop(self):
        get_pin(self.pin)['output'] = LOW
        get_pin(self.pin)['duty_cycle'] = 0

    def ChangeDutyCycle(self, percent):
        get_pin(self.pin)['duty_cycle'] = percent


def assert_duty_cycle(pin, duty_cycle):
    if get_pin(pin)['pwm'] is not True:
        raise Exception(f'Pin {pin} is not a PWM pin')
    elif get_pin(pin)['duty_cycle'] != duty_cycle:
        raise Exception(f'The duty cycle of this pin is {get_pin(pin)["duty_cycle"]} not {duty_cycle}')


def wait_for_edge(pin, direction, timeout=False, bouncetime=False):
    if get_pin(pin)['mode'] != IN:
        raise Exception(f'Pin {pin} was not configured as an INPUT.')
    if direction not in [FALLING, RISING]:
        raise ValueError(f'Value {direction} is not a valid direction!')
    bouncetime = bouncetime / 1000
    timeout = timeout / 1000
    wait = 0.1
    time.sleep(wait)
    time.sleep(bouncetime)
    if timeout < bouncetime + wait:
        return None
    return True
