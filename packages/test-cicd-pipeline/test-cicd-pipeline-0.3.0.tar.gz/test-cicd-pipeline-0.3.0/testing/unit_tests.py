from src.helpers.add_numbers import add_numbers
from src.helpers.subtract_numbers import subtract_numbers


def test_add_numbers():
    assert add_numbers(4, 5) == 9


def test_subtract_numbers():
    assert subtract_numbers(8, 5) == 3
