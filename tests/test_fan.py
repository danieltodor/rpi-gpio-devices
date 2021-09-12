from datetime import datetime, timedelta
import pytest

from src.fan import Fan
from RPi.GPIO import assert_output, assert_duty_cycle, assert_setup, HIGH, LOW, IN, PUD_UP


def test_fan_turn_on_off_method_single_pin():
    pin1 = 1
    fan = Fan(pin1)

    assert fan.is_off() is True
    fan.turn_on()
    assert fan.is_on() is True
    assert_output(pin1, HIGH)

    fan.turn_off()
    assert fan.is_off() is True
    assert_output(pin1, LOW)

    fan.turn_off()


def test_fan_set_speed_method_without_pwm_pin():
    pin1 = 1
    fan = Fan(pin1)

    with pytest.raises(ValueError):
        fan.set_speed(50)


def test_fan_set_speed_method():
    pin1, pin2, pin3 = 1, 2, 3
    fan = Fan(pin1, pin2, pin3)

    assert fan.is_off() is True
    fan.set_speed(50)
    assert fan.is_on() is True
    assert_duty_cycle(pin3, 50)
    assert_output(pin1, HIGH)
    assert_output(pin2, LOW)
    assert_output(pin3, HIGH)
    assert_setup(pin2, IN, PUD_UP)

    fan.set_speed(1)
    assert fan.is_on() is True
    assert_output(pin1, HIGH)
    assert_output(pin3, HIGH)

    fan.set_speed(0)
    assert fan.is_off() is True
    assert_output(pin1, LOW)
    assert_output(pin3, LOW)

    fan.turn_off()


def test_fan_smart_set_speed_method():
    pin1, pin2, pin3 = 1, 2, 3
    il = 300
    fan = Fan(pin1, pin2, pin3, idle_limit=il)

    fan.smart_set_speed(50)
    fan.smart_set_speed(0)
    assert fan.is_on() is True
    assert_output(pin1, HIGH)
    assert_output(pin3, HIGH)

    ten_minutes_ago = datetime.now() - timedelta(minutes=10)
    fan.turned_on_at = ten_minutes_ago
    fan.smart_set_speed(0)
    assert fan.is_off() is True
    assert_output(pin1, LOW)
    assert_output(pin3, LOW)

    fan.turn_off()


def test_fan_read_hw_temperature_method():
    pin1, pin2, pin3 = 1, 2, 3
    fan = Fan(pin1, pin2, pin3)

    assert fan.read_hw_temperature() > 15


def test_fan_measure_rpm_method():
    pin1, pin2, pin3 = 1, 2, 3
    edges = 10
    fan = Fan(pin1, pin2, pin3, rpm_measurement_edges=edges)

    fan.set_speed(50)
    assert fan.measure_rpm() > 100

    fan.turn_off()


def test_fan_measure_rpm_method_too_small_timeout():
    pin1, pin2, pin3 = 1, 2, 3
    edges = 10
    timeout = 1
    fan = Fan(pin1, pin2, pin3, rpm_measurement_edges=edges, rpm_measurement_timeout=timeout)

    fan.set_speed(50)
    assert fan.measure_rpm() == 0

    fan.turn_off()


def test_fan_measure_rpm_method_without_sense_pin():
    pin1, pin2 = 1, 2
    fan = Fan(pin1, pwm=pin2)

    with pytest.raises(ValueError):
        fan.measure_rpm()


def test_fan_temp_to_speed_method():
    pin1, pin2, pin3 = 1, 2, 3
    sm = [
        (20, 1),
        (40, 30),
        (70, 50),
        (75, 70),
        (80, 100)
    ]
    fan = Fan(pin1, pin2, pin3, speed_mapping=sm)

    assert fan.temp_to_speed(10) == 0
    assert fan.temp_to_speed(20) == 1
    assert fan.temp_to_speed(70) == 50
    assert fan.temp_to_speed(80) == 100
    assert fan.temp_to_speed(85) == 100


def test_fan_temp_to_speed_method_single_level():
    pin1, pin2, pin3 = 1, 2, 3
    sm = [
        (40, 30)
    ]
    fan = Fan(pin1, pin2, pin3, speed_mapping=sm)

    assert fan.temp_to_speed(39) == 0
    assert fan.temp_to_speed(40) == 30
    assert fan.temp_to_speed(70) == 30


def test_fan_auto_set_method():
    pin1, pin2, pin3 = 1, 2, 3
    il = 300
    ct = 0
    sm = [
        (20, 1),
        (40, 30),
        (70, 50),
        (75, 70),
        (80, 100)
    ]
    fan = Fan(pin1, pin2, pin3, speed_mapping=sm, idle_limit=il, cycletime=ct)

    temp = 19
    fan.auto_set(temp)
    assert fan.is_off() is True
    assert_output(pin1, LOW)
    assert_output(pin3, LOW)
    assert_duty_cycle(pin3, 0)

    temp = 42
    fan.auto_set(temp)
    assert fan.is_on() is True
    assert_output(pin1, HIGH)
    assert_output(pin3, HIGH)
    assert_duty_cycle(pin3, 30)

    # # This test was commented out to simulate a high cycletime environment,
    # # where the temp changes between readings can be high.
    # temp = 25
    # fan.auto_set(temp)
    # assert fan.is_on() is True
    # assert_output(pin1, HIGH)
    # assert_output(pin3, HIGH)
    # assert_duty_cycle(pin3, 0)

    temp = 19
    fan.auto_set(temp)
    assert fan.is_on() is True
    assert_output(pin1, HIGH)
    assert_output(pin3, HIGH)
    assert_duty_cycle(pin3, 0)

    ten_minutes_ago = datetime.now() - timedelta(minutes=10)
    fan.turned_on_at = ten_minutes_ago
    temp = 19
    fan.auto_set(temp)
    assert fan.is_off() is True
    assert_output(pin1, LOW)
    assert_output(pin3, LOW)
    assert_duty_cycle(pin3, 0)

    fan.turn_off()
