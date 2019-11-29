"""Test matplotlib units interface"""
import matplotlib.pyplot as plt
from unit_system.predefined_units import A, V, m, s

# pylint: disable=missing-function-docstring
def test_label():
    x = [1, 2, 3] * A
    y = [4, 5, 6] * V
    _, ax = plt.subplots()
    ax.plot(x, y)
    assert ax.xaxis.have_units()
    expected = "$q\\;/\\;{\\rm A}$"
    assert ax.xaxis.get_label().get_text() == expected
    assert ax.yaxis.have_units()
    expected = "$q\\;/\\;{\\rm V}$"
    assert ax.yaxis.get_label().get_text() == expected


def test_labelwithpar():
    x = [1, 2, 3] * s
    y = [4, 5, 6] * m / s
    _, ax = plt.subplots()
    ax.plot(x, y)
    assert ax.xaxis.have_units()
    expected = "$q\\;/\\;{\\rm s}$"
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
    x.qsym = "t"
    y = [4, 5, 6] * m / s
    y.qsym = "v"
    _, ax = plt.subplots()
    ax.plot(x, y)
    assert ax.xaxis.have_units()
    expected = "$t\\;/\\;{\\rm s}$"
    assert ax.xaxis.get_label().get_text() == expected
    assert ax.yaxis.have_units()
    expected = "$v\\;/\\;{\\rm (m/s)}$"
    assert ax.yaxis.get_label().get_text() == expected
