from src.button import Button
from RPi.GPIO import assert_setup, set_input, IN, PUD_DOWN, PUD_UP


def test_button_is_pressed_method_low_polarity():
    pin1 = 1
    button = Button(pin1, polarity='low')

    assert_setup(pin1, IN, PUD_UP)

    set_input(pin1, True)
    assert button.is_pressed() is False

    set_input(pin1, False)
    assert button.is_pressed() is True


def test_button_is_pressed_method_high_polarity():
    pin1 = 1
    button = Button(pin1, polarity='high')

    assert_setup(pin1, IN, PUD_DOWN)

    set_input(pin1, True)
    assert button.is_pressed() is True

    set_input(pin1, False)
    assert button.is_pressed() is False
