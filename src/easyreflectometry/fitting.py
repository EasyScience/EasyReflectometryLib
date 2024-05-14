__author__ = 'github.com/arm61'

import numpy as np
import scipp as sc
from easyscience.Fitting.Fitting import MultiFitter as easyFitter

from easyreflectometry.experiment import Model


class Fitter:
    def __init__(self, *args: Model):
        r"""A convinence class for the :py:class:`easyscience.Fitting.Fitting`
        which will populate the :py:class:`sc.DataGroup` appropriately
        after the fitting is performed.

        :param args: Reflectometry model
        """

        # This lets the uid be passed with the fit_func.
        def func_wrapper(func, uid):
            def wrapped(*args, **kwargs):
                return func(*args, uid, **kwargs)

            return wrapped

        self._fit_func = [func_wrapper(m.interface.fit_func, m.uid) for m in args]
        self._models = args
        self.easy_f = easyFitter(args, self._fit_func)

    def fit(self, data: sc.DataGroup, method: str = 'least_squares', id: int = 0) -> sc.DataGroup:
        """
        Perform the fitting and populate the DataGroups with the result.

        :param data: DataGroup to be fitted to and populated
        :param method: Optimisation method
        """
        refl_nums = [k[3:] for k in data['coords'].keys() if 'Qz' == k[:2]]
        x = [data['coords'][f'Qz_{i}'].values for i in refl_nums]
        y = [data['data'][f'R_{i}'].values for i in refl_nums]
        dy = [1 / np.sqrt(data['data'][f'R_{i}'].variances) for i in refl_nums]
        result = self.easy_f.fit(x, y, weights=dy, method=method)
        new_data = data.copy()
        for i, _ in enumerate(result):
            id = refl_nums[i]
            new_data[f'R_{id}_model'] = sc.array(
                dims=[f'Qz_{id}'], values=self._fit_func[i](data['coords'][f'Qz_{id}'].values)
            )
            sld_profile = self.easy_f._fit_objects[i].interface.sld_profile(self._models[i].uid)
            new_data[f'SLD_{id}'] = sc.array(dims=[f'z_{id}'], values=sld_profile[1] * 1e-6, unit=sc.Unit('1/angstrom') ** 2)
            new_data['attrs'][f'R_{id}_model'] = {'model': sc.scalar(self._models[i].as_dict())}
            new_data['coords'][f'z_{id}'] = sc.array(
                dims=[f'z_{id}'], values=sld_profile[0], unit=(1 / new_data['coords'][f'Qz_{id}'].unit).unit
            )
        return new_data


def _flatten_list(this_list: list) -> list:
    """
    Flatten nested lists.

    :param this_list: List to be flattened

    :return: Flattened list
    """
    return np.array([item for sublist in this_list for item in sublist])
