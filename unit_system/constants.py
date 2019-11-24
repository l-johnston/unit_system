"""SI system constants conforming to NIST SP811"""
import re

PREFIXES = {
    "Y": "1E24",
    "Z": "1E21",
    "E": "1E18",
    "P": "1E15",
    "T": "1E12",
    "G": "1E9",
    "M": "1E6",
    "k": "1E3",
    "h": "1E2",
    "da": "1E1",
    "d": "1E-1",
    "c": "1E-2",
    "m": "1E-3",
    "µ": "1E-6",
    "n": "1E-9",
    "p": "1E-12",
    "f": "1E-15",
    "a": "1E-18",
    "z": "1E-21",
    "y": "1E-24",
}

PREFIX_PATTERN = "^(?P<prefix>da|[YZEPTGMkhdcmµnpfazy])?"

UNITS = {
    "m": "m",
    "kg": "kg",
    "s": "s",
    "A": "A",
    "K": "K",
    "mol": "mol",
    "cd": "cd",
    "rad": "1",
    "sr": "1",
    "Hz": "s**-1",
    "N": "m*kg*s**-2",
    "Pa": "m**-1*kg*s**-2",
    "J": "m**2*kg*s**-2",
    "W": "m**2*kg*s**-3",
    "C": "s*A",
    "V": "m**2*kg*s**-3*A**-1",
    "F": "m**-2*kg**-1*s**4*A**2",
    "Ω": "m**2*kg*s**-3*A**-2",
    "S": "m**-2*kg**-1*s**3*A**2",
    "Wb": "m**2*kg*s**-2*A**-1",
    "T": "kg*s**-2*A**-1",
    "H": "m**2*kg*s**-2*A**-2",
    "°C": "K",
    "lm": "cd",
    "lx": "m**-2*cd",
    "Bq": "s**-1",
    "Gy": "m**2*s**-2",
    "Sv": "m**2*s**-2",
    "kat": "s**-1*mol",
    "g": "kg/1000",
    "min": "60*s",
    "h": "3600*s",
    "°": "pi/180",
    "'": "pi/10800",
    '"': "pi/648000",
    "ha": "10**4*m**2",
    "L": "10**-3*m**3",
    "t": "10**3*kg",
}

UNITS_PATTERN = "(?P<unit>" + "|".join(UNITS.keys()) + ")$"

PATTERN = PREFIX_PATTERN + UNITS_PATTERN
UNIT_RE = re.compile(PATTERN)

TOUNITS = {k: v for k, v in UNITS.items() if k not in ["g", "rad", "sr", "°C"]}

QUANTITY_ARITHMETIC = [
    "add",
    "subtract",
    "multiply",
    "divide",
    "true_divide",
    "negative",
    "positive",
    "absolute",
    "fabs",
    "conj",
    "conjugate",
    "reduce",
    "square",
    "power",
    "sqrt",
    "minimum",
    "maximum",
]

QUANTITY_COMPARISON = [
    "equal",
    "not_equal",
    "less",
    "less_equal",
    "greater",
    "greater_equal",
    "isfinite",
]
