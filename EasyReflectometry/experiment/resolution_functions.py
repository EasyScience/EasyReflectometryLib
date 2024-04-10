"""Resolution functions for the resolution of the experiment.
When a percentage is provided we assume that the resolution is a
Gaussian distribution with a FWHM of the percentage of the q value.
To convert from a sigma value to a FWHM value we use the formula
FWHM = 2.35 * sigma [2 * np.sqrt(2 * np.log(2)) * sigma].
"""

from typing import Callable
from typing import Union

import numpy as np


def constant_resolution_function(constant: float) -> Callable[[np.array], np.array]:
    """Create a resolution function that is constant across the q range.

    :param constant: The constant resolution value.
    """

    def _constant(q: Union[np.array, float]) -> np.array:
        """Function that calculates the resolution at a given q value.

        The function uses the data points from the encapsulating function and produces a linearly interpolated between them.
        """
        return np.ones(np.array(q).size) * constant

    return _constant


def linear_spline_resolution_function(q_data_points: np.array, resolution_points: np.array) -> Callable[[np.array], np.array]:
    """Create a resolution function that is linearly interpolated between given data points.

    :param q_data_points: The q values at which the resolution is defined.
    :param resolution_points: The resolution values at the given q values.
    """

    def _linear(q: np.array) -> np.array:
        """Function that calculates the resolution at a given q value.

        The function uses the data points from the encapsulating function and produces a linearly interpolated between them.
        """
        return np.interp(q, q_data_points, resolution_points)

    return _linear


def is_constant_resolution_function(resolution_function: Callable[[np.array], np.array]) -> bool:
    """Check if the resolution function is a constant."""
    if resolution_function.__qualname__.split('.')[0] == 'constant_resolution_function':
        return True
    else:
        return False
