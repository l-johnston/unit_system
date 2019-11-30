"""Matplotlib Conversion Interface"""
try:
    import matplotlib as mpl
    from matplotlib.units import ConversionInterface
except ModuleNotFoundError:
    pass
else:
    from unit_system import Quantity

    class QuantityConverter(ConversionInterface):
        """Matplotlib interface for Quantity"""

        @staticmethod
        def axisinfo(unit, axis):
            """Return default axis label"""
            qsym, usym = unit
            qsym = QuantityConverter._lookup_qsym(usym) if qsym is None else qsym
            qsym = QuantityConverter._parse_qsym(qsym)
            if "*" in usym or "/" in usym or "**" in usym:
                usym = usym.replace("**", "^")
                usym = usym.replace("*", r"\cdot")
                if usym.startswith("("):
                    label = f"${qsym}" + r"\;/\;{\rm " + f"{usym}" + "}$"
                else:
                    label = f"${qsym}" + r"\;/\;{\rm (" + f"{usym}" + ")}$"
            else:
                label = f"${qsym}" + r"\;/\;{\rm " + f"{usym}" + "}$"
            return mpl.units.AxisInfo(label=label)

        @staticmethod
        def default_units(x, axis):
            """Return the quantity and unit symbols for Quantity x"""
            return (x.qsym, x.unit)

        @staticmethod
        def _parse_qsym(qsym):
            """Parse qsym into latex expression unless it is already latex"""
            if qsym.startswith("$") and qsym.endswith("$"):
                return qsym[1:-1]
            qsym = qsym.replace("**", "^")
            try:
                subscript_start = qsym.index("_")
            except ValueError:
                return qsym
            try:
                subscript_stop = qsym.index("^")
            except ValueError:
                subscript_stop = len(qsym)
            subscript = qsym[subscript_start + 1 : subscript_stop]
            sym = qsym[:subscript_start]
            pwr = qsym[subscript_stop:]
            qsym = f"{sym}" + r"_{\rm " + f"{subscript}" + "}" + f"{pwr}"
            return qsym

        @staticmethod
        def _lookup_qsym(usym):
            """Assign appropriate quantity symbol based on the unit symbol

            Standard quantity symbols defined in ISO-31.
            """

            if "*" in usym or "/" in usym or "**" in usym:
                return "q"

            standard_symbols = {
                "V": "U",
                "A": "I",
                "Ω": "R",
                "F": "C",
                "H": "L",
                "s": "t",
                "Hz": "f",
                "K": "T",
                "°C": "T",
                "m": "l",
                "W": "P",
                "J": "E",
                "g": "m",
                "Pa": "p",
            }
            return standard_symbols.get(usym[-1], "q")

    mpl.units.registry[Quantity] = QuantityConverter()
