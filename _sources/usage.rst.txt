Usage
=====

>>> from unit_system import Quantity
>>> mΩ = Quantity(10**-3, 'Ω') # same as Mathcad in that unit symbols are variables
>>> Rsense = 10.0*mΩ
>>> Rsense # repr same as Mathcad in the default result format
0.01 Ω
>>> Rsense.to('mΩ') # same as Mathcad in that you can change the scaling
10.0 mΩ
>>> A = Quantity(1, 'A')
>>> Is = 10*A
>>> Is*Rsense
0.1 V
>>> dV = Quantity(1, 'V')
>>> dT = Quantity(1, 'K') # temperature differences are expressed in kelvin
>>> tempco = dV/dT
>>> tempco
1.0 kg*m**2/(A*K*s**3) # same as Mathcad where result is in SI base units
>>> tempco.to('V/K')
1.0 V/K
>>> torque = Quantity(1, 'N*m')
>>> torque # same result as Mathcad
1.0 J
>>> torque.to('N*m') # an improvement over Mathematica and others that print 1.0 m*N
1.0 N*m
>>> import numpy as np
>>> Hz = Quantity(1, "Hz")
>>> f = np.logspace(0, 1, 2)*Hz
>>> f.to("Hz")
>>> [ 1. 10.] Hz

You can convert from non-SI unit into the SI base unit. It's a one-way trip.

>>> from unit_system import convert
>>> Ta = convert(72, '°F')
>>> Ta
295.37 K
>>> Ta.to('°C')
22.22 °C

You can load predefined units like the ones in Mathcad.

>>> from unit_system.predefined_units import *
>>> 1*mΩ * 1*A
0.001 V

Notes
-----
- Ω is ALT+234
- µ is ALT+230
- ° is ALT+248
- day has unit symbol d that conflicts with candela symbol cd and is not supported