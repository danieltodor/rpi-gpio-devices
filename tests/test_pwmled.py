from src.pwmled import PWMLED
from RPi.GPIO import assert_output, assert_duty_cycle, HIGH, LOW


def test_pwmled_set_brightness_method():
    pin1 = 1
    pwmled = PWMLED(pin1)

    pwmled.set_brightness(50)
    assert pwmled.is_on() is True
    assert_output(pin1, HIGH)
    assert_duty_cycle(pin1, 50)

    pwmled.set_brightness(0)
    assert pwmled.is_off() is True
    assert_output(pin1, LOW)
    assert_duty_cycle(pin1, 0)

    pwmled.turn_off()
