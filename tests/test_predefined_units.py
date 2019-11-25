"""Test predefined_units"""
from unit_system import Quantity
from unit_system.predefined_units import V

# pylint: disable=missing-function-docstring
def test_units():
    assert V == Quantity(1, "V")
