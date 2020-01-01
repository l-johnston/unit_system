"""Test Quantity"""
import numpy as np
from pytest import raises
from unit_system import Quantity

# pylint: disable=missing-function-docstring
# pylint: disable=protected-access
# pylint: disable=expression-not-assigned
def test_zero():
    q = Quantity(0, "m")
    assert str(q) == "0.0 m"
    q = Quantity(1, "s")
    result = 0 * q
    assert result == 0
    q = Quantity([1, 2, 3], "s")
    result = 0 * q
    assert (result == np.asarray([0.0, 0.0, 0.0])).all()
    q = Quantity(1, "0")
    result = 0 * q
    assert result == 0
    assert 0 + Quantity(1, "s") == Quantity(1, "s")


def test_class():
    assert issubclass(Quantity, np.ndarray)


def test_attributes():
    q = Quantity(1, "m")
    assert q.value == 1.0
    assert q.unit == "m"


def test_repr():
    q = Quantity(1, "Hz")
    assert q.__repr__() == "1.0 Hz"
    q = Quantity([1, 2], "Hz")
    assert q.__repr__() == "[1. 2.] Hz"


def test_str():
    q = Quantity(1, "Ω")
    assert str(q) == "1.0 Ω"


def test_to():
    q = Quantity(1, "kΩ")
    assert str(q) == "1000.0 Ω"
    q = q.to("kΩ")
    assert str(q) == "1.0 kΩ"


# pylint: disable=unneeded-not
def test_eq():
    a = Quantity(1, "m")
    b = Quantity(1000, "mm")
    assert a == b
    assert not a == "a"


def test_add():
    a = Quantity(1, "m")
    b = Quantity(1, "cm")
    c = a + b
    assert c == Quantity(1.01, "m")
    a = Quantity([1, 2], "m")
    b = Quantity([1, 2], "cm")
    c = a + b
    results = c == Quantity([1.01, 2.02], "m")
    assert results.all()


def test_add_error():
    with raises(ValueError):
        Quantity(1, "m") + Quantity(1, "s")


def test_radd_error():
    with raises(ValueError):
        1.0 + Quantity(1, "m")


def test_iadd():
    a = Quantity(1, "km")
    a += Quantity(1, "m")
    assert a == Quantity(1001, "m")


def test_iadd_error():
    with raises(ValueError):
        a = Quantity(1, "m")
        a += 1.0


def test_sub():
    a = Quantity(2, "mol")
    b = Quantity(1, "mol")
    assert a - b == Quantity(1, "mol")


def test_rsub_error():
    with raises(ValueError):
        1.0 - Quantity(1, "m")


def test_mul():
    a = Quantity(1, "kg")
    assert a * 2 == Quantity(2, "kg")
    b = Quantity(2, "m")
    assert a * b == Quantity(2, "m*kg")


def test_rmul():
    a = Quantity(1, "kg")
    assert 2 * a == Quantity(2, "kg")


def test_div():
    a = Quantity(2, "s")
    assert a / 2 == Quantity(1, "s")
    b = Quantity(2, "m")
    assert b / a == Quantity(1, "m/s")


def test_rdiv():
    a = Quantity(2, "s")
    assert 2 / a == Quantity(1, "1/s")


def test_floordiv_error():
    with raises(TypeError):
        Quantity(1, "m") // 2


def test_rfloordiv_error():
    with raises(TypeError):
        2 // Quantity(1, "m")


def test_mod_error():
    with raises(TypeError):
        Quantity(1, "m") % 2


def test_rmod_error():
    with raises(TypeError):
        2 % Quantity(1, "m")


def test_divmod_error():
    with raises(TypeError):
        divmod(Quantity(1, "m"), 2)


def test_rdivmod_error():
    with raises(TypeError):
        divmod(2, Quantity(1, "m"))


def test_pow():
    assert Quantity(2, "m") ** 2 == Quantity(4, "m**2")


def test_rpow_error():
    with raises(TypeError):
        2 ** Quantity(2, "m")


def test_neg():
    assert -Quantity(1, "m") == Quantity(-1, "m")


def test_pos():
    assert +Quantity(-1, "m") == Quantity(-1, "m")


def test_abs():
    assert abs(Quantity(-1, "m")) == Quantity(1, "m")


def test_lt():
    a = Quantity(1, "mm")
    b = Quantity(2, "m")
    assert a < b
    assert not b < a


# pylint: disable=pointless-statement
def test_lt_error():
    a = Quantity(1, "mm")
    b = Quantity(2, "kg")
    with raises(ValueError):
        a < b
    with raises(ValueError):
        a < 2.0


def test_gt():
    a = Quantity(1, "mm")
    b = Quantity(2, "m")
    assert b > a
    assert not a > b


def test_gt_error():
    a = Quantity(1, "mm")
    b = Quantity(2, "kg")
    with raises(ValueError):
        b > a
    with raises(ValueError):
        a > 2.0


def test_le():
    a = Quantity(1, "mm")
    b = Quantity(1, "m")
    assert a <= b
    assert a <= Quantity(0.001, "m")


def test_ge():
    a = Quantity(1, "mm")
    b = Quantity(1, "m")
    assert b >= a
    assert a >= Quantity(0.001, "m")


def test_ne():
    a = Quantity(1, "m")
    b = Quantity(1.01, "m")
    assert a != b
    assert a != "a"


def test_celcius():
    t = Quantity(25, "°C")
    assert t == Quantity(298.15, "K")


def test_celcius_to():
    t = Quantity(25, "°C")
    t.to("°C")
    assert t == Quantity(25, "°C", "°C")
    t = Quantity([25, 25], "°C")
    t.to("°C")
    results = t == Quantity([25, 25], "°C", "°C")
    assert results.all()


def test_celcius_add():
    t = Quantity(25, "°C")
    t1 = t + Quantity(5, "K")
    assert t1 == Quantity(303.15, "K")
    t2 = t + Quantity(5, "°C")
    assert t2 == Quantity(576.3, "K")


def test_celcius_sub():
    ta = Quantity(23, "°C")
    tamax = Quantity(70, "°C")
    assert tamax - ta == Quantity(47, "K")


def test_array_repr():
    a = Quantity([1, 2], "m")
    assert a.__repr__() == "[1. 2.] m"


def test_array_value():
    a = Quantity([1, 2], "m")
    result = a.value == np.asarray([1.0, 2.0])
    assert result.all()


def test_ufunc():
    m = Quantity(1, "m")
    a = np.asarray([1, 10]) * m
    result = np.log10(a / m) == np.asarray([0.0, 1.0])
    assert result.all()


def test_uncanceledto():
    a = Quantity(1, "m")
    b = a.to("s")
    assert b.unit == "m/s*s"
    a = Quantity([1, 2, 3], "m")
    b = a.to("s")
    assert b.unit == "m/s*s"


def test_indexarray():
    a = Quantity([1, 2, 3], "m")
    assert a[0] == Quantity(1, "m")


def test_indexerror():
    a = Quantity(1, "m")
    with raises(IndexError):
        a[1]


def test_cubed():
    a = Quantity(2, "m")
    assert a ** 3 == Quantity(8, "m**3")


def test_sqrt():
    a = Quantity(4, "m")
    b = np.sqrt(a)
    assert b.value == 2
    assert b.unit == "sqrt(m)"


def test_indexscaler():
    a = Quantity(1, "m")
    assert a[0] == Quantity(1, "m")


def test_toauto():
    a = Quantity([1, 1], "Hz", "1/s")
    a.to("auto")
    results = a == Quantity([1, 1], "1/s")
    assert results.all()


def test_slice():
    a = Quantity([1, 2, 3], "m")
    results = a[:2] == Quantity([1, 2], "m")
    assert results.all()


def test_nounit():
    a = Quantity(1, "m")
    a._unit = None
    assert a[0] == 1.0


def test_ufuncwithlist():
    a = Quantity([1, 2, 3], "m")
    b = np.multiply(a, [1, 2, 3])
    results = b == Quantity([1, 4, 9], "m")
    assert results.all()


def test_ufuncaterror():
    a = Quantity([1, 2, 3], "m")
    with raises(TypeError):
        np.multiply.at(a, [0, 1, 2], 2)


def test_ufuncout():
    a = Quantity([1, 2, 3], "m")
    b = np.asarray([4.0, 5.0, 6.0])
    np.multiply(a, 2.0, out=b)
    results = b == np.asarray([2.0, 4.0, 6.0])
    assert results.all()


def test_format():
    a = Quantity(1.1234, "m")
    assert f"{a}" == "1.1234 m"
    assert f"{a:.2f}" == "1.12 m"
