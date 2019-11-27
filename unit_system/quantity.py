"""Definition of Quantity as a subclass of numpy ndarray"""
from numbers import Number
import numpy as np
from sympy import factor
from unit_system.parse_unit import parse
from unit_system.constants import TOUNITS, QUANTITY_ARITHMETIC, QUANTITY_COMPARISON


class Quantity(np.ndarray):
    """A physical quantity data type in the SI system

    Usage replicates Mathcad's quantity math.
    >>> from unit_system import Quantity
    >>> F = Quantity(1, 'F')
    >>> pF = 1e-12*F
    >>> C1 = 1*pF
    >>> C1
    1e-12 F
    >>> C1.to('pF')
    1.0 pF
    >>> Ω = Quantity(1, 'Ω') # Ω is ALT+234, same as Mathcad
    >>> TΩ = 1e12*Ω
    >>> R1 = 1*TΩ
    >>> R1*C1
    1.0 s
    >>> f = Quantity([1, 2, 3], "Hz")
    >>> f
    >>> [1. 2. 3.] Hz
    >>> import numpy as np
    >>> Hz = Quantity(1, "Hz")
    >>> f = np.logspace(0, 1, 3)*Hz
    >>> f
    >>> [0. 3.162 10.] 1/s
    >>> f.to("Hz")
    >>> [0. 3.162 10.] Hz

    Args:
        value (float or array-like): numerical value(s) of the quantity
        unit (str): SI unit expression

    Returns a Quantity
    """

    # can only define ndarray metadata attributes in __new__
    # temporay object, obj, is passed to __array_finalize__
    def __new__(cls, value, unit, to_unit="auto"):
        if value == 0 or unit == "1":
            return value
        obj = np.asarray(value, dtype=np.float).view(cls)
        obj._unit = unit
        obj._tounit = to_unit
        return obj

    # pylint: disable=attribute-defined-outside-init
    # __array_finalize__ only accepts one argument, the tempory ndarray object (obj)
    # can only define ndarray metadata attributes in __array_finalize__
    # __init__ is called after __array_finalize__
    def __array_finalize__(self, obj):
        self._unit = getattr(obj, "_unit", None)
        self._tounit = getattr(obj, "_tounit", "auto")

    # pylint: disable=super-init-not-called
    # pylint: disable=unused-argument
    # normally, there's no need to define __init__, but in this case, we need to
    # update the unit expression based on the value of _tounit
    def __init__(self, *args):
        if self._unit is not None:
            self.to(self._tounit)

    @property
    def value(self):
        """Return the numerical value of the quantity"""
        return self.view(np.ndarray)

    @property
    def unit(self):
        """Return unit symbol expression of the quantity"""
        return self._unit

    # pylint: disable=invalid-name
    # pylint complains about the two letter function name 'to'
    def to(self, unit="auto"):
        """Convert the Quantity into the desired SI unit

        Args:
            unit (str): target SI unit
        """
        if self.unit == "1":
            value = self.view(np.ndarray)
            return value if value.size > 1 else float(value)
        old_basescale, old_baseunit = parse(self.unit)
        if self.size > 1:
            value = self.view(np.ndarray)
            indices = list(range(value.size))
        else:
            value = self.item()
            indices = []
        if unit != "auto":
            self._tounit = unit
            new_basescale, new_baseunit = parse(unit)
            scale = old_basescale / new_basescale
            if "°C" in unit and "°C" not in self.unit:
                if isinstance(value, np.ndarray):
                    np.add.at(value, indices, -273.15)
                    value = self.view(np.ndarray)
                else:
                    self.itemset(value - 273.15)
                    value = self.item()
            if isinstance(value, np.ndarray):
                np.multiply.at(value, indices, scale)
            else:
                self.itemset(value * scale)
            uncanceled = str(factor(f"{old_baseunit}/({new_baseunit})"))
            if uncanceled != "1":
                unit = f"{uncanceled}*{unit}"
            self._unit = unit
            return self
        for k, v in TOUNITS.items():
            if str(factor(f"{old_baseunit}/({v})")) == "1":
                if k in ["Hz", "Bq", "lm", "Gy", "Sv", "cd"] and k not in self._unit:
                    continue
                if isinstance(value, np.ndarray):
                    np.multiply.at(value, indices, old_basescale)
                else:
                    self.itemset(value * old_basescale)
                if "°C" in self._unit:
                    if isinstance(value, np.ndarray):
                        np.add.at(value, indices, 273.15)
                    else:
                        self.itemset(value + 273.15)
                self._unit = k
                break
        else:
            if isinstance(value, np.ndarray):
                np.multiply.at(value, indices, old_basescale)
            else:
                self.itemset(self.item() * old_basescale)
            self._unit = old_baseunit
        return self

    def __repr__(self):
        value = self.view(np.ndarray)
        value_str = str(value) if value.size > 1 else str(float(value))
        quantity_str = value_str + f" {self.unit}"
        return quantity_str

    def __str__(self):
        value = self.view(np.ndarray)
        value_str = str(value) if value.size > 1 else str(float(value))
        quantity_str = value_str + f" {self.unit}"
        return quantity_str

    def __format__(self, fmt=None):
        if fmt == "":
            return self.__repr__()
        value = self.view(np.ndarray)
        fmt_str = "{:" + fmt + "}"
        value_str = np.array2string(value, formatter={"float_kind": fmt_str.format})
        quantity_str = value_str + f" {self.unit}"
        return quantity_str

    def __getitem__(self, index):
        if isinstance(index, Number) and index >= self.size:
            raise IndexError
        try:
            value = super(Quantity, self).__getitem__(index)
        except IndexError:
            value = self.item()
        if isinstance(value, Number):
            if self._unit is None:
                return value
            return Quantity(value, self._unit, self._tounit)
        return value

    @staticmethod
    def _computeunit(operation, units):
        """Perform the unit symbol arithmetic using sympy

        Args:
            operation (str): arithmetic operation listed in QUANTITY_ARITHMETIC
            units (list): list of unit strings

        Returns:
            (str): baseunit str result of the operation
        """
        if operation == "multiply":
            unit_str = "*".join(units)
        elif operation in ["divide", "true_divide"]:
            unit_str = "(" + ")/(".join(units) + ")"
        elif operation in ["add", "subtract"]:
            unit_str = units[0]
            for unit in units:
                if unit != unit_str:
                    raise ValueError(f"incompatible units")
        elif operation == "square":
            unit_str = "(" + units[0] + ")**2"
        elif operation == "power":
            unit_str = "(" + units[0] + ")**" + units[1]
        elif operation == "sqrt":
            unit_str = "(" + units[0] + ")**(1/2)"
        elif operation in QUANTITY_COMPARISON:
            unit_str = units[0]
            for unit in units:
                if unit != unit_str:
                    raise ValueError(f"incompatible units")
            return units[0]
        else:
            return units[0]
        return parse(unit_str)[1]

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        if method == "at":
            return NotImplemented
        operation = ufunc.__name__
        if operation not in QUANTITY_ARITHMETIC + QUANTITY_COMPARISON:
            raise TypeError(f"'{operation}' not defined for Quantity")
        if operation == "power" and isinstance(inputs[1], Quantity):
            raise TypeError("Quantity is not a valid exponent")
        args = []
        in_units = []
        for input_ in inputs:
            if isinstance(input_, Quantity):
                basescale, baseunit = parse(input_.unit)
                in_units.append(baseunit)
                if "°C" in input_.unit:
                    args.append(input_.view(np.ndarray) * basescale + 273.15)
                else:
                    args.append(input_.view(np.ndarray) * basescale)
            elif isinstance(input_, Number):
                in_units.append(str(input_))
                args.append(input_)
            elif isinstance(input_, np.ndarray):
                args.append(input_)
            elif isinstance(input_, list):
                args.append(input_)
            else:
                return NotImplemented
        baseunit = self._computeunit(operation, in_units)
        outputs = kwargs.pop("out", None)
        out_units = []
        if outputs:
            out_args = []
            for output in outputs:
                if isinstance(output, Quantity):
                    out_units.append(output.unit)
                    out_args.append(output.view(np.ndarray))
                else:
                    out_args.append(output)
            kwargs["out"] = tuple(out_args)
        else:
            outputs = (None,) * ufunc.nout
        # pylint: disable=no-member
        # pylint complains that __array_ufunc__ is not defined in np.ndarray, but it is
        results = super(Quantity, self).__array_ufunc__(ufunc, method, *args, **kwargs)
        # pylint: enable=no-member
        if results is NotImplemented:
            return NotImplemented
        if ufunc.nout == 1:
            results = (results,)
        if operation in QUANTITY_ARITHMETIC:
            results = tuple(
                (np.asarray(result).view(Quantity) if output is None else output)
                for result, output in zip(results, outputs)
            )
        if results and isinstance(results[0], Quantity):
            result = results[0]
            # pylint: disable=protected-access
            # pylint only allows _attribute access from self
            result._unit = baseunit
            result = result.to()
        else:
            result = results[0]
        return result if len(results) == 1 else results
