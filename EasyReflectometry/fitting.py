import numpy as np
import scipp as sc
from easyCore.Fitting.Fitting import Fitter as easyFitter

class Fitter(easyFitter):
    def __init__(self, model, calculator):
        self.calculator = calculator
        self.easy_f = easyFitter(model, calculator.fit_func)

    def fit(self, data):
        id = 0
        new_data = data.copy()
        result = self.easy_f.fit(data.coords[f'Qz{id}'].values, data[f'data_set{id}'].data.values, weights=1/np.sqrt(data[f'data_set{id}'].data.variances), method='least_squares')
        new_data[f'data_set{id}_best_fit'] = sc.array(dims=[f'Qz{id}'], values=self.calculator.fit_func(data.coords[f'Qz{id}'].values))
        new_data[f'data_set{id}_sld'] = sc.array(dims=[f'z{id}'], values=self.calculator.sld_profile()[1] * 1e-6, unit=sc.Unit('1/angstrom') ** 2)
        new_data.coords[f'z{id}'] = sc.array(dims=[f'z{id}'], values=self.calculator.sld_profile()[0], unit=(1/new_data.coords[f'Qz{id}'].unit).unit)
        return new_data
