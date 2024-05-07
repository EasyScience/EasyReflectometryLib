__author__ = 'github.com/arm61'

from typing import TextIO
from typing import Union

import scipp as sc
from orsopy.fileio import orso


def load(fname: Union[TextIO, str]) -> sc.DataGroup:
    return orso.load_orso(fname)
