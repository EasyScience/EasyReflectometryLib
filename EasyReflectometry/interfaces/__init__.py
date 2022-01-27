__author__ = 'github.com/wardsimon'
__version__ = '0.0.1'

import os, sys
import traceback

try:
    from EasyReflectometry.interfaces.refnx import Refnx  # noqa: F401
except Exception:
    traceback.print_exc()
    print('Warning: refnx is not installed')

try:
    from EasyReflectometry.interfaces.bornagain import BornAgain  # noqa: F401
except ModuleNotFoundError:
    traceback.print_exc()
    print('Warning: BornAgain python is not installed')

try:
    from EasyReflectometry.interfaces.refl1d import Refl1d  # noqa: F401
except Exception:
    traceback.print_exc()
    print('Warning: refl1d is not installed')

from EasyReflectometry.interfaces.interfaceTemplate import InterfaceTemplate
