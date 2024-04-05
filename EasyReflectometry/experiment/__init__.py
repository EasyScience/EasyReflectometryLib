from .model import Model
from .models import Models
from .resolution_functions import constant_resolution_function
from .resolution_functions import linear_spline_resolution_function

__all__ = (
    constant_resolution_function,
    linear_spline_resolution_function,
    Model,
    Models,
)
