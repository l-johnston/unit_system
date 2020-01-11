"""Test matplotlib units interface - caption label style"""
import matplotlib.pyplot as plt
from unit_system.predefined_units import A, V, Quantity

# pylint: disable=missing-function-docstring
def test_label():
    x = [1, 2, 3] * A
    y = [4, 5, 6] * V
    _, ax = plt.subplots()
    ax.plot(x, y)
    assert ax.xaxis.get_label().get_text() == r"${\rm Current\;(A)}$"
    assert ax.yaxis.get_label().get_text() == r"${\rm Voltage\;(V)}$"
    x = [1, 2, 3] * A ** 2
    y = Quantity([4, 5, 6], "cd")
    ax.clear()
    ax.plot(x, y)
    assert ax.xaxis.get_label().get_text() == r"${\rm \;(A^2)}$"
    assert ax.yaxis.get_label().get_text() == r"${\rm \;(cd)}$"
    x = [1, 2, 3] * A
    y = [4, 5, 6] * V
    ax.clear()
    ax.plot(x, y, xunits="mA")
    assert ax.xaxis.get_label().get_text() == r"${\rm Current\;(mA)}$"
