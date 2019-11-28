Usage
=====

The most common usage pattern, and especially for interactive sessions, is to import
the predefined units:

>>> from unit_system.predefined_units import *
>>> Rsense = 10.0*mΩ
>>> Rsense
0.01 Ω
>>> Rsense.to('mΩ')
10.0 mΩ

>>> Is = 10*A
>>> Is*Rsense
0.1 V

Temperature in Celsius has to be entered using:

>>> Ta = Quantity(23, "°C")

since the '°' symbol's unicode value lies outside the acceptable range for Python
variable names.

Temperature differences are expressed in kelvin:

>>> dV = 1*V
>>> dT = 1*K
>>> tempco = dV/dT
>>> tempco
1.0 kg*m**2/(A*K*s**3)
>>> tempco.to('V/K')
1.0 V/K

Arrays can be created:

>>> import numpy as np
>>> f = np.logspace(0, 1, 2)*Hz
>>> f.to("Hz")
[ 1. 10.] Hz

You can convert from a non-SI unit into the SI equivalent, but it is a one-way trip.

>>> from unit_system import convert
>>> Ta = convert(72, '°F')
>>> Ta
295.37 K
>>> Ta.to('°C')
22.22 °C

Notes
-----
- Ω is ALT+234
- µ is ALT+230
- ° is ALT+248
- day has unit symbol d that conflicts with candela symbol cd and is not supported