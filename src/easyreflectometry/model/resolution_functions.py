"""Resolution functions for the resolution of the experiment.
When a percentage is provided we assume that the resolution is a
Gaussian distribution with a FWHM of the percentage of the q value.
To convert from a sigma value to a FWHM value we use the formula
FWHM = 2.35 * sigma [2 * np.sqrt(2 * np.log(2)) * sigma].
"""

from __future__ import annotations

from abc import abstractmethod
from typing import List
from typing import Optional
from typing import Union

import numpy as np

DEFAULT_RESOLUTION_FWHM_PERCENTAGE = 5.0


class ResolutionFunction:
    @abstractmethod
    def smearing(self, q: Union[np.array, float]) -> np.array: ...

    @abstractmethod
    def as_dict(self, skip: Optional[List[str]] = None) -> dict: ...

    @classmethod
    def from_dict(cls, data: dict) -> ResolutionFunction:
        if data['smearing'] == 'PercentageFhwm':
            return PercentageFhwm(data['constant'])
        if data['smearing'] == 'LinearSpline':
            return LinearSpline(data['q_data_points'], data['fwhm_values'])
        raise ValueError('Unknown resolution function type')


class PercentageFhwm(ResolutionFunction):
    def __init__(self, constant: Union[None, float] = None):
        if constant is None:
            constant = DEFAULT_RESOLUTION_FWHM_PERCENTAGE
        self.constant = constant

    def smearing(self, q: Union[np.array, float]) -> np.array:
        return np.ones(np.array(q).size) * self.constant

    def as_dict(
        self, skip: Optional[List[str]] = None
    ) -> dict[str, str]:  # skip is kept for consistency of the as_dict signature
        return {'smearing': 'PercentageFhwm', 'constant': self.constant}


class LinearSpline(ResolutionFunction):
    def __init__(self, q_data_points: np.array, fwhm_values: np.array):
        self.q_data_points = q_data_points
        self.fwhm_values = fwhm_values

    def smearing(self, q: Union[np.array, float]) -> np.array:
        return np.interp(q, self.q_data_points, self.fwhm_values)

    def as_dict(
        self, skip: Optional[List[str]] = None
    ) -> dict[str, str]:  # skip is kept for consistency of the as_dict signature
        return {'smearing': 'LinearSpline', 'q_data_points': list(self.q_data_points), 'fwhm_values': list(self.fwhm_values)}
