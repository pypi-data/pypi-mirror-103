import pytest

from revolution.colors import Color
from revolution.colors import wrap_text_with_color, wrap_iterable_elements_with_color


class TestColor:
    def setup(self):
        self.color = 'red'
        self.color_obj = Color(self.color)

    # Test __init__
    def test_init_correct(self):
        assert self.color_obj._color == (Color.colors[self.color], Color.reset)

    # Test hidden methods
    def test__verify_color(self):
        assert self.color_obj._verify_color('blue') == (
            Color.colors['blue'], Color.reset)

    # Test properties
    def test_color_property(self):
        # getter
        assert self.color_obj.color == (Color.colors[self.color], Color.reset)
        # setter
        self.color_obj.color = 'blue'
        assert self.color_obj.color == (Color.colors['blue'], Color.reset)


def test_wrap_text_with_color():
    red = 'red'
    color = Color(red)

    text = 'Test'

    new_text = wrap_text_with_color(text, color.color)
    assert new_text == f'{Color.colors[red]}{text}{Color.reset}'


def test_wrap_iterable_elements_with_color():
    red = 'red'
    color = Color(red)

    spinners = ['-', '\\', '|', '/']
    new_spinners = wrap_iterable_elements_with_color(spinners, color.color)
    colored_spinners = ['\x1b[31m-\x1b[0m', '\x1b[31m\\\x1b[0m',
                        '\x1b[31m|\x1b[0m', '\x1b[31m/\x1b[0m']
    assert new_spinners == colored_spinners
