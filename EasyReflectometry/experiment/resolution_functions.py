from typing import Callable

import numpy as np


def constant_resolution_function(constant: float) -> Callable[[np.array], np.array]:
    """Create a resolution function that is constant across the q range.

    :param constant: The constant resolution value.
    """

    def _constant(q: np.array) -> np.array:
        """Function that calculates the resolution at a given q value.

        The function uses the data points from the encapsulating function and produces a linearly interpolated between them.
        """
        return np.ones(len(q)) * constant

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
