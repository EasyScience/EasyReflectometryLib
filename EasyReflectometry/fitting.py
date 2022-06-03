__author__ = 'github.com/arm61'

from typing import Callable, List, Union
import numpy as np
import scipp as sc

from easyCore.Fitting.Fitting import MultiFitter as easyFitter

from EasyReflectometry.experiment.model import Model


class Fitter:

    def __init__(self, model: Union[Model, List[Model]],
                 fit_func: Union[Callable, List[Callable]]):
        """
        A convinence class for the :py:class:`easyCore.Fitting.Fitting` which will populate 
        the :py:class:`sc.Dataset` appropriately after the fitting is performed. 

        :param model: Reflectometry model
        :param interface: Analysis interface
        """
        self.easy_f = easyFitter(model, fit_func)

    def fit(self, data: sc.Dataset, method: str = 'least_squares', id=0):
        """
        Perform the fitting and populate the datasets with the result.
        
        :param data: Dataset to be fitted to and populated
        :param method: Optimisation method
        """
        refl_nums = [k[3:] for k, v in data.coords.items() if 'Qz' == k[:2]]
        x = [data.coords[f'Qz_{i}'].values for i in refl_nums]
        y = [data[f'R_{i}'].data.values for i in refl_nums]
        dy = [1 / np.sqrt(data[f'R_{i}'].data.variances) for i in refl_nums]
        result = self.easy_f.fit_lists(x, y, weights_list=dy, method=method)
        new_data = data.copy()
        for i, x in enumerate(result.x):
            id = refl_nums[i]
            new_data[f'R_{id}_model'] = sc.array(dims=[f'Qz_{id}'],
                                                values=self.easy_f._fit_functions[i](
                                                    data.coords[f'Qz_{id}'].values, 
                                                    self.easy_f._fit_objects[i].uid))
            sld_profile = self.easy_f._fit_objects[i].interface.sld_profile(self.easy_f._fit_objects[i].uid) 
            new_data[f'SLD_{id}'] = sc.array(
                dims=[f'z_{id}'],
                values=sld_profile[1] * 1e-6,
                unit=sc.Unit('1/angstrom')**2)
            new_data[f'R_{id}_model'].attrs['model'] = sc.scalar(
                self.easy_f._fit_objects[i].as_dict())
            new_data.coords[f'z_{id}'] = sc.array(
                dims=[f'z_{id}'],
                values=sld_profile[0],
                unit=(1 / new_data.coords[f'Qz_{id}'].unit).unit)
        return new_data
        


def _flatten_list(this_list: list) -> list:
    """
    Flatten nested lists.

    :param this_list: List to be flattened

    :return: Flattened list
    """
    return np.array([item for sublist in this_list for item in sublist])
