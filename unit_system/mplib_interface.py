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
            qsym = "q" if qsym is None else qsym
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
            """Return the default unit for x"""
            return (x.qsym, x.unit)

    mpl.units.registry[Quantity] = QuantityConverter()
