"""The :py:mod:`item` library is the backbone of :py:mod:`EasyReflectometry`.
An :py:mod:`EasyReflectometry.sample.item` allows for the inclusion of physical and 
chemical parameterisation into our reflectometry model.  
For more information please look at the `item library documentation`_

.. _`item library documentation`: ./library.html
"""

__author__ = 'github.com/arm61'

from .items.multilayer import MultiLayer
from .items.repeating_multilayer import RepeatingMultiLayer
from .items.surfactant_layer import SurfactantLayer