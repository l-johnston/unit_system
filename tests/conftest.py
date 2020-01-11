"""pytest conftest"""
import os

# pylint: disable=invalid-name
home_path = os.path.expanduser("~")
config_file = os.path.abspath(os.path.join(home_path, ".unit_system/unit_system.ini"))
collect_ignore = []
if os.path.exists(config_file):
    collect_ignore.append("test_mplinterface_si.py")
else:
    collect_ignore.append("test_mplinterface_caption.py")
