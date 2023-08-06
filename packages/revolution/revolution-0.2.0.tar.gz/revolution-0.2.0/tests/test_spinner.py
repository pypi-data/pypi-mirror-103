import pytest

from revolution.spinner import Spinner


def test_style_becomes_style_if_style_is_provided():
    style = 'equal'
    spinner = Spinner(style=style)
    assert spinner._style == style


def test_style_becomes_classic_if_style_is_not_provided():
    spinner = Spinner()  # `style` not specified
    assert spinner._style == 'classic'


def test_spinner_becomes_classic_if_style_does_not_exist():
    nonexistent_style = 'shimmalummadingdong'
    spinner = Spinner(style=nonexistent_style)
    assert spinner._spinner == Spinner.spinners['classic'][0]


def test_spinner_interval_becomes_interval_if_interval_is_provided():
    my_spinner_interval = 0.75

    spinner = Spinner(interval=my_spinner_interval)
    assert spinner.interval == my_spinner_interval


def test_spinner_interval_becomes_default_if_interval_is_not_provided():
    classic_spinner_interval = Spinner.spinners['classic'][1]

    classic_spinner = Spinner(style='classic')
    assert classic_spinner.interval == classic_spinner_interval


def test_spinner_len_equals_length_of_spinner_in_spinners():
    classic_spinner_len = len(Spinner.spinners['classic'][0])

    classic_spinner = Spinner(style='classic')
    assert classic_spinner._spinner_len == classic_spinner_len


def test_spinner_iterates_over_animations_when_used_as_iterator():
    num_classic_spinner_animations = len(Spinner.spinners['classic'][0])

    classic_spinner = Spinner(style='classic')

    count = 0
    for _ in classic_spinner:
        count += 1
    assert count == num_classic_spinner_animations
