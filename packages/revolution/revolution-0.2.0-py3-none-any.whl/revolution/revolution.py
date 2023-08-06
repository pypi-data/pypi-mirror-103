import math
import platform
import shutil
import sys
import threading
import time
import traceback
import types

from .spinner import Spinner
from .colors import Color
from .colors import wrap_text_with_color


class Revolution:
    def __call__(self, *args, **kwargs):
        """
        Allows `Revolution` to be called as a function decorator.
        """

        # If the decorator doesn't have any arguments:
        if hasattr(self, '_func'):
            self.start()
            result = self._func(*args, **kwargs)
            self._main_event.set()
            while not self._spin_event.is_set():
                pass
            return result
        # ...otherwise, the function is in *args:
        else:
            func = args[0]
            if isinstance(func, types.FunctionType):
                def wrapper(*margs, **mkwargs):
                    self.start()

                    result = func(*margs, **mkwargs)

                    if self._total:
                        self._count += 1
                        if self._total == self._count:
                            while not self._spin_event.is_set():
                                pass
                            return result
                    else:
                        self._main_event.set()
                        while not self._spin_event.is_set():
                            pass
                        return result
                return wrapper

    def __enter__(self):
        """
        Entry point for with statements. Used in conjunction with __exit__.
        """

        self.start()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """
        Exit point for with statements. Used in conjunction with __enter__.
        """

        self._main_event.set()
        if (exc_type, exc_value, exc_traceback) == (None, None, None):
            while not self._spin_event.is_set():
                pass
            return
        traceback.print_exception(exc_type, exc_value, exc_traceback)

    def __iter__(self):
        """
        Allows for loops to be used with Revolution objects. Used in conjunction with
        __next__.
        """

        self.start()
        return self

    def __next__(self):
        """
        Used in conjunction with with __iter__.
        """

        # If the for loop was given an iterable such as a list:
        if hasattr(self, '_iter'):
            if self._count < self._stop:
                return_value = self._iter[self._count]
                self._count += self._step
                return return_value
            raise StopIteration
        # otherwise, it's likely a range object and so:
        else:
            if self._count < self._stop:
                return_value = self._count
                self._count += self._step
                return return_value
            raise StopIteration

    def __init__(self, func=None, desc='', total=None, style='',
                 color='blue', success=None, safe=True, interval=None):
        """
        Initializes a Revolution object.

        Parameters
        ==========
        func : list or range, optional
            If this is a list or range object, it will iterate over each of the elements
            and return them one by one.

            This parameter is necessary to be able to use a Revolution object as a function
            decorator.

        desc : str, optional
            A string to use in place of the text that displays beside the spinner.

        total : int, optional
            An integer that indicates the total number of expected iterations.

            It's recommended that you do not include this when using a Revolution object
            as a function decorator.

        style : str, optional
            A string that indicates which spinner style to use. If style is None or if it
            doesn't exist, the classic style will be used.

            Available options can be viewed by running `revolution --example` or
            `revolution -e` in your console.

        color : str, optional
            A string that indicates which color should be used for the spinner. If a color
            is not provided, the color will default to 'blue'.

            Available options:
                * 'black'
                * 'red'
                * 'green'
                * 'yellow'
                * 'blue'
                * 'violet'
                * 'cyan'
                * 'white'

        success : str, optional
            A string that will be displayed beside the spinner when the spinner animation
            stops.

        safe : bool, optional
            If True (default), spinners on Windows machines will always use the
            'classic' style (even if a different style is provided). 

            If you are using a certain spinner style and are unsure as to how it will 
            appear on Windows machines, it is recommended that you leave `safe` set to
            its default value.

        interval : float, optional
            A float value that is used to indicate the refresh rate of the entire spinner.
        """

        if func:
            # If `func` is provided a range object or list:
            if isinstance(func, range) or isinstance(func, list):
                try:
                    self._count = func.start
                    self._stop = func.stop
                    self._step = func.step

                    self._total = func.end
                except AttributeError:
                    self._count = 0
                    self._stop = len(func)
                    self._step = 1
                    self._iter = func

                    self._total = self._stop
            # ...otherwise, it must be a FunctionType:
            else:
                self._func = func
                self._count = 0
                self._total = total
        else:
            self._count = 0
            self._total = total

        self._desc = desc
        self._message = desc

        # For success messages:
        self._success_message = success or desc
        green = Color('green')
        self._success_frame = wrap_text_with_color('+', green.color)
        self._frame = self._success_frame

        # For fail messages:
        self._fail_message = desc
        red = Color('red')
        self._fail_frame = wrap_text_with_color('-', red.color)

        # Determines which spinner style should be used based on the OS:
        if safe:
            if platform.system() == 'Windows':
                self._style = 'classic'
            else:
                self._style = style or 'classic'
        else:
            self._style = style or 'classic'

        self._spinner = Spinner(self._style, interval, color)
        self._interval = self._spinner.interval

        self._rate = 0.0

    @property
    def success(self):
        return self._success_message

    @success.setter
    def success(self, text):
        self._success_message = text
        self._message = self._success_message

        try:
            self.stop()
        except AttributeError:
            pass

    @property
    def fail(self):
        return self._fail_message

    @fail.setter
    def fail(self, text):
        self._fail_message = text
        self._message = self._fail_message
        self._frame = self._fail_frame

        try:
            self.stop()
        except AttributeError:
            pass

    @staticmethod
    def make_padding() -> int:
        """
        Returns number of columns to use for spacing.
        """
        num_columns = shutil.get_terminal_size()[0]
        padding = math.floor(num_columns * 0.2)
        return padding

    def start(self):
        """
        Starts the method responsible for animating spinner frames to the console.

        If this method is used manually and externally, the user is responsible for
        calling the `stop` method as well (or `success` or `fail`).
        """

        self._main_event = threading.Event()
        # self._main_thread targets the function responsible for animating frames:
        self._main_thread = threading.Thread(target=self._spin)

        # Set self._main_thread as daemon so this internal thread will quit if the
        # main thread quits:
        self._main_thread.setDaemon(True)
        self._main_thread.start()

    def stop(self):
        """
        Stops the method responsible for animating spinner frames to the console.

        If a user manually calls a Revolution object's `start` method, then they
        are responsible for calling that object's `stop` method as well.
        """

        if not self._main_event.is_set():
            self._main_event.set()
            self._main_thread.join()

    def update(self, step=1):
        """
        Updates the `_count` member variable.

        Parameters
        ==========
        step : int, optional
            Indicates by how much the _count member variable should be incremented.

        Example
        =======
        >>> from revolution import Revolution
        >>> rev = Revolution()
        >>> rev.start()
        >>> rev.update()
        >>> rev.update(2)
        >>> rev.stop()
        """
        self._count += step

    def _spin(self):
        """
        Prints a spinner animation frame to the console.
        """

        # For preventing premature ejection:
        self._spin_event = threading.Event()

        # Enable thread for measuring rate:
        self._rate_event = threading.Event()
        rate_thread = threading.Thread(target=self._update_rate)
        rate_thread.setDaemon(True)
        rate_thread.start()

        self._statement = self._make_statement()

        while True:
            for frame in self._spinner:
                print('\r', end='')
                sys.stdout.write(self._statement.format(
                    frame, self._desc, self._count, self._total, self._rate))

                if self._main_event.is_set() or self._count == self._total:
                    print('\r', end='')
                    sys.stdout.write(self._statement.format(
                        self._frame, self._message, self._count, self._total, self._rate) + '\n')

                    self._rate_event.set()
                    self._spin_event.set()
                    return

                time.sleep(self._interval)

    def _make_statement(self):
        """
        Returns a string containing the format to display based on whether a Revolution
        instance's `total` parameter is provided a value.
        """

        if self._total:
            statement = ' {} {} « {}/{} » [{}]' + (' ' * self.make_padding())
        else:
            statement = ' {} {}' + (' ' * self.make_padding())
        return statement

    def _update_rate(self):
        """
        Calculates the number of iterations per second by dividing the current `_count`
        by the running time of the spinner.
        """

        if self._total:
            start = time.perf_counter()
            while not self._rate_event.is_set():
                self._rate = f'{round(self._count / (time.perf_counter() - start), 4)} it/s'
                time.sleep(0.25)
