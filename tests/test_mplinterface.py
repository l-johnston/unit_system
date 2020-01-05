"""Test matplotlib units interface"""
import matplotlib.pyplot as plt
from matplotlib.units import ConversionError
from pytest import raises
from unit_system.predefined_units import A, V, m, s, Hz, Quantity

# pylint: disable=missing-function-docstring
def test_label():
    x = [1, 2, 3] * A
    y = [4, 5, 6] * V
    _, ax = plt.subplots()
    ax.plot(x, y)
    assert ax.xaxis.have_units()
    expected = "$I\\;/\\;{\\rm A}$"
    assert ax.xaxis.get_label().get_text() == expected
    assert ax.yaxis.have_units()
    expected = "$U\\;/\\;{\\rm V}$"
    assert ax.yaxis.get_label().get_text() == expected


def test_labelwithpar():
    x = [1, 2, 3] * s
    y = [4, 5, 6] * m / s
    _, ax = plt.subplots()
    ax.plot(x, y)
    assert ax.xaxis.have_units()
    expected = "$t\\;/\\;{\\rm s}$"
    assert ax.xaxis.get_label().get_text() == expected
    assert ax.yaxis.have_units()
    expected = "$q\\;/\\;{\\rm (m/s)}$"
    assert ax.yaxis.get_label().get_text() == expected


def test_labelwithpwr():
    x = [1, 2, 3] * s
    y = [4, 5, 6] * m ** 2 / s ** 2
    _, ax = plt.subplots()
    ax.plot(x, y)
    expected = "$q\\;/\\;{\\rm (m^2/s^2)}$"
    assert ax.yaxis.get_label().get_text() == expected
    y.to("(m/s)**2")
    _, ax = plt.subplots()
    ax.plot(x, y)
    expected = "$q\\;/\\;{\\rm (m/s)^2}$"
    assert ax.yaxis.get_label().get_text() == expected


def test_qsym():
    x = [1, 2, 3] * s
    x.qsym = "t_r"
    y = [4, 5, 6] * (m / s) ** 2
    y.qsym = "v_max**2"
    _, ax = plt.subplots()
    ax.plot(x, y)
    assert ax.xaxis.have_units()
    expected = "$t_{\\rm r}\\;/\\;{\\rm s}$"
    assert ax.xaxis.get_label().get_text() == expected
    assert ax.yaxis.have_units()
    expected = "$v_{\\rm max}^2\\;/\\;{\\rm (m^2/s^2)}$"
    assert ax.yaxis.get_label().get_text() == expected
    y.qsym = r"$v_{\rm max}^2$"
    _, ax = plt.subplots()
    ax.plot(x, y)
    expected = "$v_{\\rm max}^2\\;/\\;{\\rm (m^2/s^2)}$"
    assert ax.yaxis.get_label().get_text() == expected


def test_std_qsym():
    x = [1, 2, 3] * Hz
    x.to("Hz")
    dB = Quantity(1, "dB")
    y = [4, 5, 6] * dB
    _, ax = plt.subplots()
    ax.plot(x, y)
    expected = "$f\\;/\\;{\\rm Hz}$"
    assert ax.xaxis.get_label().get_text() == expected
    expected = "$q\\;/\\;{\\rm dB}$"
    assert ax.yaxis.get_label().get_text() == expected


def test_set_units():
    x = [0, 1, 2] * s
    y = [1, 2, 3] * m
    _, ax = plt.subplots()
    ax.plot(x, y, xunits="ms")
    results = ax.lines[0].get_data()[0] == Quantity([0, 1000, 2000], "ms", "ms")
    assert results.all()


def test_set_wrong_units():
    with raises(ConversionError):
        x = [0, 1, 2] * s
        y = [1, 2, 3] * m
        plt.plot(x, y, xunits="mm")
