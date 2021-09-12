from datetime import datetime, timedelta

from src.base import BaseDevice, SwitchableDevice, PWMDevice
from RPi.GPIO import assert_output, assert_duty_cycle, HIGH, LOW


def test_base_device():
    BaseDevice()


def test_switchable_device_on_off_methods():
    switchable = SwitchableDevice(1)
    assert switchable.is_on() is False
    assert switchable.is_off() is True


def test_switchable_device_turn_on_off_methods():
    pin = 1
    switchable = SwitchableDevice(pin)

    switchable.turn_on()
    assert switchable.is_on() is True
    assert_output(pin, HIGH)

    switchable.turn_off()
    assert switchable.is_off() is True
    assert_output(pin, LOW)

    switchable.turn_off()


def test_switchable_device_toggle_method():
    pin = 1
    switchable = SwitchableDevice(pin)

    switchable.toggle()
    assert switchable.is_on() is True
    assert_output(pin, HIGH)

    switchable.toggle()
    assert switchable.is_off() is True
    assert_output(pin, LOW)

    switchable.turn_off()


def test_switchable_device_ontime_method():
    switchable = SwitchableDevice(1)

    assert switchable.ontime() is 0
    switchable.turn_on()
    assert switchable.ontime() is 0
    ten_minutes_ago = datetime.now() - timedelta(minutes=10)
    switchable.turned_on_at = ten_minutes_ago
    assert switchable.ontime() == 10 * 60

    switchable.turn_off()


def test_pwm_device_turn_on_off_methods_single_pin():
    pin1 = 1
    pwm = PWMDevice(pin1)

    assert pwm.is_off() is True
    assert pwm.is_on() is False
    assert_output(pin1, LOW)

    pwm.turn_on()
    assert pwm.is_off() is False
    assert pwm.is_on() is True
    assert_output(pin1, HIGH)
    assert_duty_cycle(pin1, 0)

    pwm.turn_off()
    assert pwm.is_off() is True
    assert pwm.is_on() is False
    assert_output(pin1, LOW)

    pwm.turn_off()


def test_pwm_device_turn_on_off_methods():
    pin1, pin2 = 1, 2
    pwm = PWMDevice(pin1, pin2)

    assert pwm.is_off() is True
    assert pwm.is_on() is False
    assert_output(pin1, LOW)
    assert_output(pin2, LOW)

    pwm.turn_on()
    assert pwm.is_off() is False
    assert pwm.is_on() is True
    assert_output(pin1, HIGH)
    assert_output(pin2, HIGH)
    assert_duty_cycle(pin1, 0)

    pwm.turn_off()
    assert pwm.is_off() is True
    assert pwm.is_on() is False
    assert_output(pin1, LOW)
    assert_output(pin2, LOW)

    pwm.turn_off()


def test_pwm_device_set_duty_cycle_method_single_pin():
    pin1 = 1
    pwm = PWMDevice(pin1)

    pwm.set_duty_cycle(50)
    assert_duty_cycle(pin1, 50)
    assert pwm.is_on() is True
    assert pwm.is_off() is False
    assert_output(pin1, HIGH)

    pwm.set_duty_cycle(0)
    assert_duty_cycle(pin1, 0)
    assert_output(pin1, LOW)
    assert pwm.is_on() is False
    assert pwm.is_off() is True

    pwm.turn_on()
    pwm.set_duty_cycle(0, z_off=False)
    assert_duty_cycle(pin1, 0)
    assert pwm.is_on() is True
    assert pwm.is_off() is False
    assert_output(pin1, HIGH)

    pwm.turn_off()


def test_pwm_device_set_duty_cycle_method():
    pin1, pin2 = 1, 2
    pwm = PWMDevice(pin1, pin2)

    pwm.set_duty_cycle(50)
    assert_duty_cycle(pin1, 50)
    assert pwm.is_on() is True
    assert pwm.is_off() is False
    assert_output(pin1, HIGH)
    assert_output(pin2, HIGH)

    pwm.set_duty_cycle(0)
    assert_duty_cycle(pin1, 0)
    assert_output(pin1, LOW)
    assert_output(pin2, LOW)
    assert pwm.is_on() is False
    assert pwm.is_off() is True

    pwm.turn_on()
    pwm.set_duty_cycle(0, z_off=False)
    assert_duty_cycle(pin1, 0)
    assert pwm.is_on() is True
    assert pwm.is_off() is False
    assert_output(pin1, HIGH)
    assert_output(pin2, HIGH)

    pwm.turn_off()
