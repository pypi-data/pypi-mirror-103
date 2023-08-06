from .colors import Color
from .colors import wrap_iterable_elements_with_color


class Spinner:
    spinners = {
        'classic': (['|', '/', '-', '\\'], 0.1),
        'dots': (['▫ ▫ ▫', '▪ ▫ ▫', '▫ ▪ ▫', '▫ ▫ ▪'], 0.2),
        'equal': (
            ['⁼ ⁼ ⁼ ⁼ ⁼', '= ⁼ ⁼ ⁼ ⁼', '⁼ = ⁼ ⁼ ⁼', '⁼ ⁼ = ⁼ ⁼', '⁼ ⁼ ⁼ = ⁼', '⁼ ⁼ ⁼ ⁼ ='], 0.2),

        'braille': (['⠏', '⠹', '⠼', '⠧'], 0.1),
        'braille_long': (['⡏', '⢹', '⣸', '⣇'], 0.1),
        'braille_crawl': (['⠌', '⠒', '⠡', '⠨'], 0.1),
        'braille_bounce': (['⣶', '⣭', '⠿', '⣭'], 0.1),
        'arc': (['◜', '◝', '◞', '◟'], 0.1),
        'clear_quadrants': (['◴', '◷', '◶', '◵'], 0.1),
    }

    def __iter__(self):
        # Sets internal `_count` to 0 each time we begin a for-based loop:
        self._count = 0
        return self

    def __next__(self):
        # If there are still animations to print, continue printing them:
        if self._count < self._spinner_len:
            spinner_frame = self._spinner[self._count]
            self._count += 1
            return spinner_frame

        # Otherwise, quit:
        raise StopIteration

    def __init__(self, style=None, interval=None, color=None):
        # If style is empty, default to 'classic':
        self._style = style or 'classic'

        while True:
            try:
                # `spinner_tuple` is a tuple containing a list of spinner animations
                # and an interval indicating how often to refresh the animation:
                spinner_tuple = self.spinners[self._style]
                break
            # If the given style doesn't exist, default to 'classic':
            except KeyError:
                self._style = 'classic'

        # `self.interval` is intended to be public:
        self._spinner, self.interval = spinner_tuple

        # If a color is provided, we should color the animation frames:
        if color:
            color_obj = Color(color)
            self._spinner = wrap_iterable_elements_with_color(
                self._spinner, color_obj.color)
        # If user specifies an interval, use that instead:
        if interval:
            self.interval = interval

        # `_spinner_len` is used internally to indicate when the spinner animation
        # should fully reset:
        self._spinner_len = len(self._spinner)
