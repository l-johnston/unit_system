"""SI unit system package"""
import os
import configparser
from unit_system.quantity import Quantity
from unit_system.convert import convert
from unit_system.version import __version__
import unit_system.mplib_interface as mpli
from unit_system.predefined_units import predefined_units

# pylint: disable=invalid-name
home_path = os.path.expanduser("~")
config_file = os.path.abspath(os.path.join(home_path, ".unit_system/unit_system.ini"))
if os.path.exists(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    try:
        options = config["unit_system"]
    except configparser.NoSectionError:
        pass
    else:
        label_style = options.get("matplotlib_label_style", "si")
        try:
            mpli.QuantityConverter.label_style = label_style
        except AttributeError:
            pass

globals().update(predefined_units)
__all__ = ["Quantity", "convert"] + list(predefined_units.keys())
