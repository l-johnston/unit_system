"""Matplotlib Conversion Interface"""
try:
    import matplotlib as mpl
    from matplotlib.units import ConversionInterface, ConversionError
except ModuleNotFoundError:
    pass
else:
    import re
    from unit_system import Quantity

    class QuantityConverter(ConversionInterface):
        """Matplotlib interface for Quantity"""

        label_style = "si"

        @staticmethod
        def axisinfo(unit, axis):
            """Return default axis label"""
            if QuantityConverter.label_style == "caption":
                label = QuantityConverter._caption_style(unit)
            else:
                label = QuantityConverter._si_style(unit)
            return mpl.units.AxisInfo(label=label)

        @staticmethod
        def default_units(x, axis):
            """Return the quantity and unit symbols for Quantity x"""
            return (x.qsym, x.unit)

        @staticmethod
        def convert(obj, unit, axis):
            """convert unit (qsym, usym)"""
            if isinstance(unit, tuple):
                qsym, usym = unit
            else:
                qsym = None
                usym = unit
            obj.to(usym)
            if obj.unit != usym:
                raise ConversionError("Incompatible units")
            if qsym is not None:
                obj.qsym = qsym
            return obj

        @staticmethod
        def _si_style(unit):
            if isinstance(unit, tuple):
                qsym, usym = unit
            else:
                qsym = None
                usym = unit
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
            return label

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

            for unit, qsym in standard_symbols.items():
                if re.match(f".*{unit}$", usym) is not None:
                    break
            else:
                qsym = "q"
            return qsym

        @staticmethod
        def _lookup_qlabel(usym):
            """Assign appropriate quantity label based on the unit symbol"""

            if "*" in usym or "/" in usym or "**" in usym:
                return ""

            standard_symbols = {
                "V": "Voltage",
                "A": "Current",
                "Ω": "Resistance",
                "F": "Capacitance",
                "H": "Inductance",
                "s": "Time",
                "Hz": "Frequency",
                "K": "Temperature",
                "°C": "Temperature",
                "m": "Length",
                "W": "Power",
                "J": "Energy",
                "g": "Mass",
                "Pa": "Pressure",
            }

            for unit, qlabel in standard_symbols.items():
                if re.match(f".*{unit}$", usym) is not None:
                    break
            else:
                qlabel = ""
            return qlabel

        @staticmethod
        def _caption_style(unit):
            if isinstance(unit, tuple):
                qlabel, usym = unit
            else:
                qlabel = None
                usym = unit
            qlabel = (
                QuantityConverter._lookup_qlabel(usym) if qlabel is None else qlabel
            )
            usym = usym.replace("**", "^")
            usym = usym.replace("*", r"\cdot")
            return r"${\rm " + f"{qlabel}" + r"\;(" + f"{usym}" + ")}$"

    mpl.units.registry[Quantity] = QuantityConverter()
