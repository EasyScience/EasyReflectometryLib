"""The :py:mod:`item` library is the backbone of :py:mod:`EasyReflectometry`.
An :py:mod:`EasyReflectometry.sample.item` allows for the inclusion of physical and
chemical parameterisation into our reflectometry model.
For more information please look at the `item library documentation`_

.. _`item library documentation`: ./library.html
"""
__author__ = "github.com/arm61"

from .gradient_layer import GradientLayer
from .multilayer import MultiLayer
from .repeating_multilayer import RepeatingMultiLayer
from .surfactant_layer import SurfactantLayer

# Define the __all__ so that the classes can be imported from the module
__all__ = MultiLayer, RepeatingMultiLayer, SurfactantLayer, GradientLayer
