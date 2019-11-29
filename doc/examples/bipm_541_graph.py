"""Example showing matplotlib unit interface

This example reproduces the graph from BIPM SI Brochure section 5.4.1 and shows
the use of the qsym attribute of Quantity.
"""

import matplotlib.pyplot as plt
from unit_system.predefined_units import m, s, Quantity

plt.style.use("./doc/examples/report.mplstyle")


def main():
    """Generate BIPM SI Brochure 5.4.1 graph"""
    kPa = Quantity(1e3, "Pa")
    x = [48.73, 72.87, 135.42] * kPa
    x.to("kPa")
    x.qsym = "p"
    y = [94766, 94771, 94784] * (m / s) ** 2
    y.to("(m/s)**2")
    y.qsym = "v^2"
    fig, ax = plt.subplots()
    ax.plot(x, y, "Dk-")
    ax.set_xlim(0, 150)
    ax.set_ylim(94750, 94790)
    ax.set_yticks([94750, 94760, 94770, 94780, 94790])
    ax.grid(which="major", axis="y")
    fig.savefig("./doc/examples/bipm_graph.png")


if __name__ == "__main__":
    main()
