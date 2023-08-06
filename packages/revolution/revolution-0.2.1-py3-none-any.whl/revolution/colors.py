import platform
import subprocess


class Color:
    reset = '\x1b[0m'

    colors = {
        'black': '\x1b[30m',
        'red': '\x1b[31m',
        'green': '\x1b[32m',
        'yellow': '\x1b[33m',
        'blue': '\x1b[34m',
        'violet': '\x1b[35m',
        'cyan': '\x1b[36m',
        'white': '\x1b[37m'
    }

    def __new__(cls, color):
        """
        Overrides default __new__ method to enable color support on Windows machines.
        """

        # Enables color support for Windows machines:
        if platform.system() == 'Windows':
            subprocess.call('color', shell=True)

        instance = super(Color, cls).__new__(cls)
        return instance

    def __init__(self, color):
        self._color = self._verify_color(color)

    @property
    def color(self) -> tuple:
        return self._color

    @color.setter
    def color(self, color):
        self._color = self._verify_color(color)

    def _verify_color(self, color) -> tuple:
        # Clean `color` input first:
        cleaned_color = color.lower().strip()

        if isinstance(color, str):
            # Search for color in `colors`:
            if cleaned_color in Color.colors:
                return (Color.colors[cleaned_color], Color.reset)
            else:
                raise KeyError(
                    f'Color not found. Valid colors: {list(Color.colors)}')
        else:
            raise TypeError(
                f'color parameter of type {type(color)} must be str')


def wrap_text_with_color(text, color: tuple) -> str:
    ascii_color, ascii_reset = color
    text_fmt = '{}{}{}'

    return text_fmt.format(ascii_color, text, ascii_reset)


def wrap_iterable_elements_with_color(iterable, color: tuple) -> list:
    ascii_color, ascii_reset = color
    text_fmt = '{}{}{}'

    colored_iterable = [
        text_fmt.format(ascii_color, element, ascii_reset) for element in iterable]

    return colored_iterable
