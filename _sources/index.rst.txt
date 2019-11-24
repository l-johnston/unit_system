Welcome to unit_system
======================

A Python package for doing physical quantity math in the SI unit system

You can install the package from PyPI:

.. code-block::

    pip install unit_system

Usage example:

>>> from unit_system import Quantity
>>> V = Quantity(1, "V")
>>> A = Quantity(1, "A")
>>> 1*V / (1*A)
1.0 Ω

Documentation
-------------

.. toctree::
   :maxdepth: 2

   Introduction <introduction>
   Usage <usage>
   API <api>