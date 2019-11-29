"""Example showing matplotlib unit interface

Generate a graph showing default labels
"""
import matplotlib.pyplot as plt
from unit_system.predefined_units import m, s

plt.style.use("./doc/examples/report.mplstyle")


def main():
    """Generate graph"""
    x = [1, 2, 3] * s
    y = [4, 5, 6] * m / s
    fig, ax = plt.subplots()
    ax.plot(x, y, "k-")
    fig.savefig("./doc/examples/default_labels_graph.png")


if __name__ == "__main__":
    main()
