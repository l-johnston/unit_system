"""Test Quantity"""
import numpy as np
from pytest import raises
from unit_system import Quantity

# pylint: disable=missing-function-docstring
# pylint: disable=protected-access
# pylint: disable=expression-not-assigned
def test_threshold():
    a = Quantity([0, 1, 2], "s")
    value = Quantity(0.5, "s")
    fractional_index = a.threshold(value)
    assert fractional_index == 0.5
    a = Quantity(1, "s")
    fractional_index = a.threshold(value)
    assert fractional_index is None
    a = Quantity([1.0, 2.0, 3.0], "s")
    fractional_index = a.threshold(value)
    assert fractional_index is None
    value = Quantity(3.0, "s")
    fractional_index = a.threshold(value)
    assert fractional_index is None
    a = Quantity([[0], [1], [2]], "s")
    fractional_index = a.threshold(value)
    assert fractional_index is None


def test_interpolate():
    a = Quantity([0, 1, 2], "s")
    index = 0.5
    value = a.interpolate(index)
    assert value == Quantity(0.5, "s")
    a = Quantity([0, -1, 2], "s")
    value = a.interpolate(index)
    assert value == Quantity(-0.5, "s")
    a = Quantity(1, "s")
    value = a.interpolate(index)
    assert value is None
    a = Quantity([[0], [1], [2]], "s")
    value = a.interpolate(index)
    assert value is None


def test_concatenate():
    a = Quantity([0, 1, 2], "s")
    b = Quantity([3, 4, 5], "s")
    c = np.concatenate((a, b))
    results = c == Quantity(list(range(6)), "s")
    assert results.all()


def test_concatenate_incompatible_units():
    a = Quantity([0, 1, 2], "s")
    b = Quantity([3, 4, 5], "m")
    with raises(ValueError):
        np.concatenate((a, b))


def test_concatenate_unitless():
    a = np.asarray([0, 1, 2])
    b = Quantity([3, 4, 5], "s")
    c = np.concatenate((a, b))
    results = c == np.arange(0, 6, 1)
    assert results.all()
