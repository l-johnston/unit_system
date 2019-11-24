"""Test convert"""
from pytest import approx, raises
from unit_system import Quantity, convert

# pylint: disable=missing-function-docstring
# pylint: disable=protected-access
# pylint: disable=expression-not-assigned
def test_farhenheit():
    t = convert(72, "°F")
    expected = Quantity((72 - 32) * 5 / 9, "°C")
    assert t.value == approx(expected.value)


def test_unitnotintable():
    with raises(KeyError):
        convert(1, "Å")
