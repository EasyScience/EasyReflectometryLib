import traceback

from .calculator_base import CalculatorBase
from .factory import CalculatorFactory

imported_calculators = []

try:
    from .refnx.calculator import Refnx

    imported_calculators.append(Refnx)
except Exception:
    traceback.print_exc()
    print('Warning: refnx is not installed')

# try:
#     from .bornagain.calculator import BornAgain
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

__all__ = [CalculatorBase, CalculatorFactory] + imported_calculators
