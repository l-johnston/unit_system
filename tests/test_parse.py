"""Test unit_system parse"""
from sympy import factor, pi
from unit_system.constants import PREFIXES, UNITS
from unit_system.parse_unit import parse

# pylint: disable=missing-function-docstring
def test_units():
    for given, expected in UNITS.items():
        if given in ["g", "min", "h", "°", "'", '"', "ha", "L", "t"]:
            continue
        scale, unit = parse(given)
        assert scale == 1.0
        assert unit == str(factor(expected))


def test_g():
    given, _ = ("g", "kg/1000")
    scale, unit = parse(given)
    assert scale == 0.001
    assert unit == "kg"


def test_min():
    given, _ = ("min", "60*s")
    scale, unit = parse(given)
    assert scale == 60.0
    assert unit == "s"


def test_h():
    given, _ = ("h", "3600*s")
    scale, unit = parse(given)
    assert scale == 3600.0
    assert unit == "s"


def test_deg_angle():
    given, _ = ("°", "pi/180")
    scale, unit = parse(given)
    assert scale == float(factor(pi / 180))
    assert unit == "1"


def test_minute_angle():
    given, _ = ("'", "pi/10800")
    scale, unit = parse(given)
    assert scale == float(factor(pi / 10800))
    assert unit == "1"


def test_second_angle():
    given, _ = ('"', "pi/648000")
    scale, unit = parse(given)
    assert scale == float(factor(pi / 648000))
    assert unit == "1"


def test_ha():
    given, _ = ("ha", "10**4*m**2")
    scale, unit = parse(given)
    assert scale == 10000.0
    assert unit == "m**2"


def test_liter():
    given, _ = ("L", "10**-3*m**3")
    scale, unit = parse(given)
    assert scale == 0.001
    assert unit == "m**3"


def test_t():
    given, _ = ("t", "10**3*kg")
    scale, unit = parse(given)
    assert scale == 1000.0
    assert unit == "kg"


def test_prefixedunits():
    for given, expected in UNITS.items():
        if given in ["kg", "g", "min", "h", "°", "'", '"', "ha", "L", "t"]:
            continue
        for prefix, multiplier in PREFIXES.items():
            scale, unit = parse(prefix + given)
            assert scale == float(multiplier)
            assert unit == str(factor(expected))


def test_composites():
    given, expected = ("N*m", "m**2*kg*s**-2")
    scale, unit = parse(given)
    assert scale == 1.0
    assert unit == str(factor(expected))

    given, expected = ("N/m", "kg*s**-2")
    scale, unit = parse(given)
    assert scale == 1.0
    assert unit == str(factor(expected))

    given, expected = ("N/km", "kg*s**-2")
    scale, unit = parse(given)
    assert scale == 0.001
    assert unit == str(factor(expected))

    given, expected = ("Hz**(-1/2)", "sqrt(s)")
    scale, unit = parse(given)
    assert scale == 1.0
    assert unit == str(factor(expected))
