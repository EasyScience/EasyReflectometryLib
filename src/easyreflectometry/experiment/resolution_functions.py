"""Resolution functions for the resolution of the experiment.
When a percentage is provided we assume that the resolution is a
Gaussian distribution with a FWHM of the percentage of the q value.
To convert from a sigma value to a FWHM value we use the formula
FWHM = 2.35 * sigma [2 * np.sqrt(2 * np.log(2)) * sigma].
"""

from __future__ import annotations

from abc import abstractmethod

# from typing import Callable
from typing import Union

import numpy as np

DEFAULT_RESOLUTION_FWHM_PERCENTAGE = 5.0


class ResolutionFunction:
    @abstractmethod
    def smearing(q: Union[np.array, float]) -> np.array: ...

    @abstractmethod
    def as_dict() -> dict: ...

    @classmethod
    def from_dict(cls, data: dict) -> ResolutionFunction:
        if data['smearing'] == 'PercentageFhwm':
            return PercentageFhwm(data['constant'])
        if data['smearing'] == 'LinearSpline':
            return LinearSpline(data['q_data_points'], data['fwhm_values'])
        raise ValueError('Unknown resolution function type')


class PercentageFhwm:
    def __init__(self, constant: Union[None, float] = None):
        if constant is None:
            constant = DEFAULT_RESOLUTION_FWHM_PERCENTAGE
        self.constant = constant

    def smearing(self, q: Union[np.array, float]) -> np.array:
        return np.ones(np.array(q).size) * self.constant

    def as_dict(self) -> dict:
        return {'smearing': 'PercentageFhwm', 'constant': self.constant}


class LinearSpline:
    def __init__(self, q_data_points: np.array, fwhm_values: np.array):
        self.q_data_points = q_data_points
        self.fwhm_values = fwhm_values

    def smearing(self, q: Union[np.array, float]) -> np.array:
        return np.interp(q, self.q_data_points, self.fwhm_values)

    def as_dict(self) -> dict:
        return {'smearing': 'LinearSpline', 'q_data_points': self.q_data_points, 'fwhm_values': self.fwhm_values}


# def percentage_fhwm_resolution_function(constant: float) -> Callable[[np.array], np.array]:
#     """Create a resolution function that is constant across the q range.

#     :param constant: The constant resolution value.
#     """

#     def _constant(q: Union[np.array, float]) -> np.array:
#         """Function that calculates the resolution at a given q value.

#         The function uses the data points from the encapsulating function and produces a linearly interpolated between them.
#         """
#         return np.ones(np.array(q).size) * constant

#     return _constant


# def linear_spline_resolution_function(q_data_points: np.array, fwhm_values: np.array) -> Callable[[np.array], np.array]:
#     """Create a resolution function that is linearly interpolated between given data points.

#     :param q_data_points: The q values at which the resolution is defined.
#     :param fwhm_values: The resolution values at the given q values.
#     """

#     def _linear(q: np.array) -> np.array:
#         """Function that calculates the resolution at a given q value.

#         The function uses the data points from the encapsulating function and produces a linearly interpolated between them.
#         """
#         return np.interp(q, q_data_points, fwhm_values)

#     return _linear


# def is_percentage_fhwm_resolution_function(resolution_function: Callable[[np.array], np.array]) -> bool:
#     """Check if the resolution function is a constant."""
#     return 'constant' in resolution_function.__name__
