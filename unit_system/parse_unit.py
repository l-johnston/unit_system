"""Parse unit expression to SI base units"""
from functools import lru_cache
from sympy import factor, pi
from unit_system.constants import PREFIXES, UNITS, UNIT_RE


@lru_cache(maxsize=1024)
def parse(unit):
    """Parse unit to SI base units

    Args:
        unit (str): unit expression

    Returns:
        (tuple(float, str)): scale factor, base unit expression
    """
    # The algorithm proceeds in three stages:
    #     = split the original unit expression into atomic units
    #       using | as a separator, for example:
    #       'F**2/(s**2*m)' -> 'F^2|/||(|s^2|*|m|)|' ->
    #           ['F^2', '/', '', '(', 's^2', '*', 'm', ')', '']
    #     = replace each derived unit with the equivalent base units
    #     = Using Sympy, factor the base unit expression
    def replace(match):
        """Replace prefixes with scale factor and derived unit with base units"""
        scale = PREFIXES.get(match.group("prefix"), None)
        base_unit = UNITS.get(match.group("unit"), match.group("unit"))
        if scale is None:
            return f"({base_unit})"
        return f"({scale}*{base_unit})"

    replacements = [("**", "^"), ("*", "|*|"), ("/", "|/|"), ("(", "|(|"), (")", "|)|")]
    piped_unit = unit
    for old, new in replacements:
        piped_unit = piped_unit.replace(old, new)
    base_units = []
    for atom in piped_unit.split("|"):
        if atom in ["*", "/", "(", ")"]:
            base_units.append(atom)
        elif "^" in atom:
            derived_unit, power = atom.split("^")
            base_unit = UNIT_RE.sub(replace, derived_unit)
            base_units.append(f"{base_unit}**{power}")
        else:
            derived_unit = atom
            base_unit = UNIT_RE.sub(replace, derived_unit)
            base_units.append(f"{base_unit}")
    factored = factor("".join(base_units))
    scale, base_unit = factored.as_coeff_Mul()
    if base_unit == pi:
        base_unit = "1"
        scale = float(scale) * float(pi)
    return (float(scale), str(base_unit))
