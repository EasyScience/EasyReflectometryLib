__author__ = 'github.com/wardsimon'
__version__ = '0.0.1'


import os, sys
import traceback


# try:
#     from easyReflectometryLib.interfaces.cryspy import Cryspy  # noqa: F401
# except ImportError:
#     # TODO make this a proper message (use logging?)
#     print('Warning: CrysPy is not installed')

# try:
#     from easyReflectometryLib.Interfaces.CFML import CFML
# except Exception:
#     traceback.print_exc()
#     print('Warning: CFML is not installed')
    
# try:
#     from easyReflectometryLib.Interfaces.GSASII import GSASII  # noqa: F401
# except Exception:
#     traceback.print_exc()
#     print('Warning: GSAS-II is not installed')

try:
    from easyReflectometryLib.interfaces.refnx import Refnx  # noqa: F401
except Exception:
    traceback.print_exc()
    print('Warning: refnx is not installed')


from easyReflectometryLib.interfaces.interfaceTemplate import InterfaceTemplate
