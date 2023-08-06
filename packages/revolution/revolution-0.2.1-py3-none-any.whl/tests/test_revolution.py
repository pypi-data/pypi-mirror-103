import math
import platform
import shutil
import time

import pytest

from revolution.revolution import Revolution
from revolution.spinner import Spinner


class TestRevolution:
    def setup(self):
        self.revolution_normal = Revolution()

        self.desc = 'Running'
        self.total = 25
        self.style = 'braille'
        self.color = 'cyan'
        self.success = 'Good'
        self.interval = 0.5
        self.revolution_with_params = Revolution(
            desc=self.desc, total=self.total, style=self.style,
            color=self.color, success=self.success, interval=self.interval)

    # Testing __init__
    def test_init_method_variables_for_revolution_normal(self):
        assert self.revolution_normal._count == 0
        assert self.revolution_normal._total == None

        assert self.revolution_normal._desc == ''
        assert self.revolution_normal._desc == ''

        # Test for success:
        assert self.revolution_normal._success_message == ''
        assert self.revolution_normal._success_frame == '\x1b[32m+\x1b[0m'

        # Test for fail:
        assert self.revolution_normal._fail_message == ''
        assert self.revolution_normal._fail_frame == '\x1b[31m-\x1b[0m'

        assert self.revolution_normal._style == 'classic'

        # Test if spinner animation frames are the same:
        spinner = Spinner(self.revolution_normal._style, None, 'blue')
        spinners = [s for s in spinner]
        normal_spinners = [s for s in self.revolution_normal._spinner]
        assert spinners == normal_spinners

        # Test if intervals are the same:
        assert self.revolution_normal._interval == Spinner.spinners[
            self.revolution_normal._style][1]

        assert self.revolution_normal._rate == 0.0

    def test_init__method_variables_for_revolution_with_params(self):
        assert self.revolution_with_params._count == 0
        assert self.revolution_with_params._total == self.total

        # Test description
        assert self.revolution_with_params._desc == self.desc
        assert self.revolution_with_params._message == self.desc

        # Test success/fail
        assert self.revolution_with_params._success_message == self.success
        assert self.revolution_with_params._fail_message == self.desc

        # Test style
        if platform.system() == 'Windows':
            assert self.revolution_with_params._style == 'classic'
        else:
            assert self.revolution_with_params._style == self.style

        spinner = Spinner(self.revolution_with_params._style, None, self.color)
        spinners = [s for s in spinner]
        params_spinners = [s for s in self.revolution_with_params._spinner]
        assert spinners == params_spinners

        # Test the intervals:
        assert self.revolution_with_params._interval == self.interval

        assert self.revolution_with_params._rate == 0.0

    # Testing properties
    def test_success_property(self):
        success_message = 'Complete'

        self.revolution_normal.success = success_message
        assert self.revolution_normal.success == success_message

    def test_fail_property(self):
        fail_message = 'Fail'

        self.revolution_normal.fail = fail_message
        assert self.revolution_normal.fail == fail_message
        assert self.revolution_normal._fail_frame == '\x1b[31m-\x1b[0m'

    # Testing static methods
    def test_make_padding(self):
        num_columns = shutil.get_terminal_size()[0]
        padding = math.floor(num_columns * 0.2)

        assert padding == Revolution.make_padding()

    # Testing public methods
    def test_start_and_stop_threads(self):
        rev = Revolution()

        # Test if main event and thread function properly with `start`:
        rev.start()
        assert not rev._main_event.is_set()
        assert rev._main_thread.is_alive()
        assert rev._main_thread.daemon

        # Test if main event and thread are properly closed with `stop`:
        rev.stop()
        assert rev._main_event.is_set()
        assert not rev._main_thread.is_alive()

    def test_update(self):
        rev1 = Revolution()
        rev2 = Revolution()

        rev1.update()
        assert rev1._count == 1

        rev2.update(2)
        assert rev2._count == 2

    # Testing internal methods
    def test__spin_as_decorator(self):
        @Revolution(desc='As a decorator')
        def description():
            for _ in range(20):
                time.sleep(0.05)

        description()

    def test__spin_with_context_manager(self):
        with Revolution(desc='With a context manager') as rev:
            for _ in range(20):
                time.sleep(0.05)
                rev.update()

        with Revolution(desc='With a context manager and total', total=20, color='red') as rev:
            for _ in range(20):
                time.sleep(0.1)
                rev.update()

    def test__spin_with_for_loop_range(self):
        limit = 20

        expected_total = 0
        for i in range(limit):
            expected_total += i

        total = 0
        for i in Revolution(range(20)):
            total += i

        assert total == expected_total

    def test__spin_with_for_loop_list(self):
        numbers = list(range(20))

        expected_total = 0
        for i in numbers:
            expected_total += i

        total = 0
        for i in Revolution(numbers):
            total += i

        assert total == expected_total

    def test__spin_manual_use_with_success(self):
        rev = Revolution(desc='Manual use (success)',
                         style='braille', safe=False)
        rev.start()
        time.sleep(2)

        rev.success = 'Done!'

        rev.stop()

    def test__spin_manual_use_with_fail(self):
        rev = Revolution(desc='Manual use (fail)')
        rev.start()
        time.sleep(2)

        rev.fail = 'Unfortunate'

    def test__make_statement_for_empty_statement(self):
        statement = self.revolution_normal._make_statement()
        empty_statement = '{} {}'

        assert empty_statement in statement

    def test__make_statement_for_statement_with_total(self):
        statement = self.revolution_with_params._make_statement()
        statement_with_total = '{} {} « {}/{} » [{}]'

        assert statement_with_total in statement
