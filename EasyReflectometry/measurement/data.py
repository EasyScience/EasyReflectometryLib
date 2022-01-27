__author__ = 'github.com/arm61'
__version__ = '0.0.1'

from typing import Union, TextIO
import scipp as sc
from orsopy.fileio import orso


def load(fname: Union[TextIO, str]) -> sc.Dataset:
    return orso.load_orso(fname)
