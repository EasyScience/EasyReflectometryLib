__author__ = 'github.com/wardsimon'
__version__ = '0.0.1'

import traceback

try:
    from EasyReflectometryLib.interfaces.refnx import Refnx  # noqa: F401
except Exception:
    traceback.print_exc()
    print('Warning: refnx is not installed')

# try:
#     from EasyReflectometry.interfaces.bornagain import BornAgain  # noqa: F401
# except Exception:
#     traceback.print_exc()
#     print('Warning: BornAgain python is not installed')

try:
    from EasyReflectometryLib.interfaces.refl1d import Refl1d  # noqa: F401
except Exception:
    traceback.print_exc()
    print('Warning: refl1d is not installed')

from EasyReflectometryLib.interfaces.interfaceTemplate import InterfaceTemplate

_ = InterfaceTemplate
