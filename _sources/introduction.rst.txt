Introduction
============

The ``unit_system`` package provides a way to perform physical quantity math, in
the `SI system`_, in Python. A physical quantity is the product of a number and a unit
such as 1*m. As is, Python doesn't implement a physical quantity data type,
and without a package like this one, users perform such calculations with pure
numbers and track the unit manually. Manually tracking the unit through a series of
calculations is tedious and error prone. One of the strenghs of Mathcad is its built-in
unit system support that lowers the barrier to including units in computations
while working in an interactive notebook. This package brings this ease-of-use
experience to Python and in particular, interactive enviroments like `Jupyter`_.

The main export of ``unit_system`` is Quantity that is a subclass of `NumPy`_'s
ndarray combining the numerical value and unit in a single data structure. By making
Quantity a subclass of ndarray, it handles scalers and arrays in the same way and
leverages NumPy. For example, scaler quantities can be created:

>>> from unit_system import Quantity
>>> length = Quantity(1.2, "m")
>>> length
1.2 m

Arithmetic with scalers can be performed:

>>> l1 = Quantity(1.2, "m")
>>> l2 = Quantity(3.6, "m")
>>> l1 + l2
4.8 m

To simplify creation of quantities and improve readability, there are predefined units
like in Mathcad:

>>> from unit_system.predefined_units import *
>>> l1 = 1.2*m
>>> l2 = 3.6*m
>>> l1 + l2
4.8 m

Arrays are easy to generate as well and leverage NumPy's functionality:

>>> lengths = [1.2, 3.6, 5.4, 7.9]*m
>>> perimeter = lengths.sum()
>>> perimeter
18.1 m

Comparison to Unyt
------------------
There are several other packages that enable physical quantity math in Python. The
best one among these is `Unyt`_. Unyt takes a similar approach in subclassing ndarray and
using Sympy to do the unit math. So, why not just use Unyt?

One of the main objectives of ``unit_system`` is to replicate the Mathcad experience
in an interactive Python session, and to that end, the appearance of the output should
be the same - just show the quantity such as '18.1 m'. With Unyt, the output shows the
data structure. For example,

>>> from unyt import m
>>> l1 = 1.2*m
>>> l2 = 3.6*m
>>> l1 + l2
unyt_quantity(4.8, 'm')

This output is consistent with Python's principle of making the repr an
executable statement, but it's not consistent with Mathcad or how we want to
read the quantity.

Another objective, and philosphical difference with Unyt, is to
force computation within a single unit system. Unyt, however,
allows mixing systems in a single expression. For example:

>>> from unyt import m, ft
>>> 1.2*m + 3.6*ft
unyt_quantity(2.29728, 'm')

This encourages round-trips between systems and encourages continued use of
non-SI systems. This package provides a ``convert`` function to
convert a non-SI quantity into its SI equivalent. For example:

>>> from unit_system.predefined_units import *
>>> from unit_system import convert
>>> l1 = 1.2*m
>>> l2 = convert(3.6, "ft")
>>> l1 + l2
2.29728 m

Here, the conversion is made explict and round trips are not allowed.

Another benefit to ``unit_system`` is its integration with Matplotlib as
described in :doc:`/usage`.

.. _SI system: https://www.nist.gov/pml/special-publication-811
.. _Jupyter: https://jupyter.org/
.. _NumPy: https://github.com/numpy/numpy
.. _Unyt: https://github.com/yt-project/unyt