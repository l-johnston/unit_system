"""Definition of Quantity as a subclass of NumPy's ndarray"""
from numbers import Number
import numpy as np
from sympy import factor
from unit_system.parse_unit import parse
from unit_system.constants import (
    TOUNITS,
    QUANTITY_ARITHMETIC,
    QUANTITY_COMPARISON,
    QUANTITY_FUNCTIONS,
)


class Quantity(np.ndarray):
    """A physical quantity data type in the SI system

    Attributes:
        value (float or array-like): numerical value(s) of the quantity
        unit (str): original SI unit expression
        to_unit (str): coerce to given SI unit expression. Defaults to 'auto'

    Example:
        >>> from unit_system import Quantity
        >>> m = Quantity(1, "m")
        >>> length = 1*m
        >>> length
        1.0 m
        >>> 2*length
        2.0 m
        >>> lengths = [1, 2, 3]*m
        >>> lengths
        [1. 2. 3.] m
        >>> lengths.sum()
        6.0 m
        >>> V = Quantity(1, "V")
        >>> kV = 1e3*V
        >>> potential = 10*kV
        >>> potential
        10000.0 V
        >>> potential.to("kV")
        10.0 kV
    """

    # can only define ndarray metadata attributes in __new__
    # temporay object, obj, is passed to __array_finalize__
    def __new__(cls, value, unit, to_unit="auto"):
        if unit == "0":
            return np.asarray(value, dtype=np.float) * 0
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
        self._qsym = None

    # pylint: disable=super-init-not-called
    # pylint: disable=unused-argument
    # normally, there's no need to define __init__, but in this case, we need to
    # update the unit expression based on the value of _tounit
    def __init__(self, *args):
        if self._unit is not None:
            self.to(self._tounit)

    @property
    def value(self):
        """ndarray: the numerical value(s) of the quantity"""
        return self.view(np.ndarray)

    @property
    def unit(self):
        """unit (str): the unit symbol expression of the quantity"""
        return self._unit

    @unit.setter
    def unit(self, unit):
        self._unit = unit
        self._tounit = "auto"
        if unit is not None:
            self.to(self._tounit)

    @property
    def qsym(self):
        r"""symbol (str): the quantity symbol for use as a label
            The symbol can be a Python expression like 'v_max**2' or
            can be a Latex expression like '$v_{\\rm max}^2$'.
        """
        return self._qsym

    @qsym.setter
    def qsym(self, symbol):
        self._qsym = symbol

    # pylint: disable=invalid-name
    # pylint complains about the two letter function name 'to'
    def to(self, unit="auto"):
        """Convert the Quantity into the desired SI unit

        Conversion is performed in-place updating the to_unit attribute.

        Args:
            unit (str): target SI unit expression

        Returns:
            Quantity: self

        Example:
            >>> from unit_system import Quantity
            >>> capacitance = Quantity(10e-12, "F")
            >>> capacitance
            1e-11 F
            >>> capacitance.to("pF")
            10.0 pF
            >>> capacitance
            10.0 pF
        """
        self._tounit = unit
        if self.unit == "1":
            value = self.view(np.ndarray)
            return value if value.size > 1 else float(value)
        if self.unit == "0":
            value = self.view(np.ndarray) * 0
            return value if value.size > 1 else float(0)
        old_basescale, old_baseunit = parse(self.unit)
        if self.size > 1:
            value = self.view(np.ndarray)
            indices = list(range(value.size))
        else:
            value = self.item()
            indices = []
        if unit != "auto":
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
        unit_str = f" {self.unit}" if self.unit not in ["1", None] else ""
        return value_str + unit_str

    def __str__(self):
        value = self.view(np.ndarray)
        value_str = str(value) if value.size > 1 else str(float(value))
        unit_str = f" {self.unit}" if self.unit not in ["1", None] else ""
        return value_str + unit_str

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
            value = self.view(np.ndarray)[index]
        except IndexError:
            value = self.item()
        if isinstance(value, Number):
            if self._unit is None:
                return value
            return Quantity(value, self._unit, self._tounit)
        return Quantity(np.copy(value), self._unit, self._tounit)

    def threshold(self, value, start=0):
        """Find fractional index of value in a 1D Quantity array

        Args:
            value (Quantity)
            start (int)

        Returns:
            (float): fractional index where value is between two consequtive elements
                or None if not found or if a scalar or if not 1D array.
        """
        if self.ndim == 0 or self.ndim > 1:
            return None
        indices = np.nonzero(value >= self[start:])[0]
        try:
            lower_index = start + indices[-1]
        except IndexError:
            return None
        lower_value = self[lower_index]
        try:
            upper_value = self[start + lower_index + 1]
        except IndexError:
            return None
        fractional = (value - lower_value) / (upper_value - lower_value)
        return lower_index + fractional

    def interpolate(self, index):
        """Compute value at fractional index of 1D Quantity array

        Args:
            index (float): fractional index

        Returns:
            (Quantity): linearly interpolated value between two consequtive elements
                or None if not found or if a scalar or if not a 1D array
        """
        if self.ndim == 0 or self.ndim > 1:
            return None
        lower_index = int(np.floor(index))
        lower_value = self[lower_index]
        upper_index = int(np.ceil(index))
        upper_value = self[upper_index]
        fractional = (upper_value - lower_value) * (index - lower_index)
        return lower_value + fractional

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
            for unit in units:
                if unit not in ["0", "0.0"]:
                    unit_str = unit
                    break
            for unit in units:
                if unit in ["0", "0.0"]:
                    continue
                if unit != unit_str:
                    raise ValueError(f"incompatible units")
        elif operation == "square":
            unit_str = "(" + units[0] + ")**2"
        elif operation == "power":
            unit_str = "(" + units[0] + ")**" + units[1]
        elif operation == "sqrt":
            unit_str = "(" + units[0] + ")**(1/2)"
        elif operation in QUANTITY_COMPARISON:
            if operation in ["equal", "not_equal"]:
                return "1"
            unit_str = units[0]
            for unit in units:
                if unit != unit_str:
                    raise ValueError(f"incompatible units")
            return "1"
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

    def __array_function__(self, func, types, args, kwargs):
        if func not in QUANTITY_FUNCTIONS:
            return NotImplemented
        if not all(issubclass(t, Quantity) for t in types):
            return NotImplemented
        return QUANTITY_FUNCTIONS[func](*args, **kwargs)


def implements(numpy_function):
    """Register an __array_function__ implementation"""

    def decorator(func):
        QUANTITY_FUNCTIONS[numpy_function] = func
        return func

    return decorator


@implements(np.concatenate)
def concatenate(arrays):
    """Join a sequence of 1-D Quantity arrays

    Args:
        arrays (Quantity): sequence of Quantity arrays
    """
    arrays[0].to("auto")
    u0 = arrays[0].unit
    unitless_arrays = [arrays[0].value]
    for array in arrays[1:]:
        array.to("auto")
        ux = array.unit
        # pylint: disable=protected-access
        if Quantity._computeunit("divide", [u0, ux]) != "1":
            raise ValueError("incompatible units")
        unitless_arrays.append(array.value)
    cat_array = np.concatenate(unitless_arrays)
    return Quantity(cat_array, u0)
