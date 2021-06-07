__author__ = 'github.com/wardsimon'
__version__ = '0.0.1'

import os, sys
import traceback

try:
    from easyReflectometryLib.Interfaces.refnx import Refnx  # noqa: F401
except Exception:
    traceback.print_exc()
    print('Warning: refnx is not installed')

try:
    from easyReflectometryLib.Interfaces.bornagain import BornAgain  # noqa: F401
except Exception:
    traceback.print_exc()
    print('Warning: BornAgain python is not installed')

from easyReflectometryLib.Interfaces.interfaceTemplate import InterfaceTemplate
