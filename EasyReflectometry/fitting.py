import numpy as np
import scipp as sc
from easyCore.Fitting.Fitting import Fitter as easyFitter


class Fitter(easyFitter):

    def __init__(self, model: "EasyReflectometry.experiment.model.Model",
                 interface: "EasyReflectometry.interface.InterfaceFactory"):
        """
        A convinence class for the :py:class:`easyCore.Fitting.Fitting` which will populate 
        the :py:class:`sc.Dataset` appropriately after the fitting is performed. 

        :param model: Reflectometry model
        :param interface: Analysis interface
        """
        self.interface = interface
        self.easy_f = easyFitter(model, interface.fit_func)

    def fit(self, data: sc.Dataset, method: str = 'least_squares'):
        """
        Perform the fitting and populate the datasets with the result.
        
        :param data: Dataset to be fitted to and populated
        :param method: Optimisation method
        """
        id = 0
        new_data = data.copy()
        result = self.easy_f.fit(data.coords[f'Qz_{id}'].values,
                                 data[f'R_{id}'].data.values,
                                 weights=1 / np.sqrt(data[f'R_{id}'].data.variances),
                                 method=method)
        new_data[f'R_{id}_model'] = sc.array(dims=[f'Qz_{id}'],
                                            values=self.interface.fit_func(
                                                data.coords[f'Qz_{id}'].values))
        new_data[f'SLD_{id}'] = sc.array(dims=[f'z_{id}'],
                                        values=self.interface.sld_profile()[1] * 1e-6,
                                        unit=sc.Unit('1/angstrom')**2)
        new_data[f'R_{id}_model'].attrs['model'] = sc.scalar(
            self.easy_f._fit_object.as_dict())
        new_data.coords[f'z_{id}'] = sc.array(
            dims=[f'z_{id}'],
            values=self.interface.sld_profile()[0],
            unit=(1 / new_data.coords[f'Qz_{id}'].unit).unit)
        return new_data
