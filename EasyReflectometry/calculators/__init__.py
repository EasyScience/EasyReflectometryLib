__author__ = 'github.com/wardsimon'
__version__ = '0.0.1'

import traceback

imported_calculators = []

try:
    from .refnx.calculator import Refnx

    imported_calculators.append(Refnx)
except Exception:
    traceback.print_exc()
    print('Warning: refnx is not installed')

# try:
#     from .bornagain import BornAgain
#    imported_calculators.append(BornAgain)
# except Exception:
#     traceback.print_exc()
#     print('Warning: BornAgain python is not installed')

try:
    from .refl1d.calculator import Refl1d  # noqa: F401

    imported_calculators.append(Refl1d)
except Exception:
    traceback.print_exc()
    print('Warning: refl1d is not installed')

from .base import CalculatorBase
from .factory import CalculatorFactory

__all__ = [CalculatorBase, CalculatorFactory] + imported_calculators
