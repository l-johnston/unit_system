"""Convert a non-SI quantity to its SI equivalent"""
from unit_system import Quantity

__all__ = ["convert"]

CONVERSION_TABLE = {
    "mil": (2.54e-5, "m"),
    "in": (2.54e-2, "m"),
    "mi": (1.609344e3, "m"),
    "ft": (3.048e-1, "m"),
    "micron": (1e-6, "m"),
    "yd": (9.144e-1, "m"),
    "psi": (6.894757e3, "Pa"),
    "°F": ((5 / 9, 459.67), "K"),
}


def convert(value, unit):
    """Convert the non-SI quantity into its SI equivalent

    The coversion factors are defined in NIST SP-811.

    Args:
        value (float): numerical value
        unit (str): non-SI unit symbol

    Returns:
        Quantity: converted value

    Example:
        >>> from unit_system import convert
        >>> convert(1, 'ft')
        0.3048 m
    """
    try:
        scale, bu = CONVERSION_TABLE[unit]
    except KeyError:
        raise KeyError(f"{unit} is not in the conversion table") from None
    else:
        if unit == "°F":
            scale, offset = scale
            value = value + offset
        return Quantity(scale * value, bu)
