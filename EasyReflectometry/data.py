__author__ = 'github.com/arm61'

from typing import Union, TextIO
import numpy as np
import scipp as sc
from orsopy.fileio import orso


def load(fname: Union[TextIO, str]) -> sc.Dataset:
    """
    Load data from an ORSO .ort file. 

    :param fname: The file to be read. 
    
    :returns: A scipp Dataset for the loaded datasets.
    """
    data = {}
    coords = {}
    try: 
        f_data = orso.load_orso(fname)
        for i, o in enumerate(f_data):
            try:
                data[f'data_set{i}'] = sc.array(dims=[f'{o.info.columns[0].name}{i}'], values=o.data[:, 1], variances=np.square(o.data[:, 2]), unit=sc.Unit(o.info.columns[1].unit))
            except TypeError:
                data[f'data_set{i}'] = sc.array(dims=[f'{o.info.columns[0].name}{i}'], values=o.data[:, 1], variances=np.square(o.data[:, 2]))
            coords[data[f'data_set{i}'].dims[0]] = sc.array(dims=[f'{o.info.columns[0].name}{i}'], values=o.data[:, 0], variances=np.square(o.data[:, 3]), unit=sc.Unit(o.info.columns[0].unit)) 
    except IndexError: 
        f_data = np.loadtxt(fname)
        data[f'data_set0'] = sc.array(dims=['Qz'], values=f_data[:, 1], variances=np.square(f_data[:, 2]))
        coords[data[f'data_set0'].dims[0]] = sc.array(dims=['Qz'], values=f_data[:, 0], variances=np.square(f_data[:, 3]), unit=sc.Unit('1/angstrom'))  
    return sc.Dataset(data=data, coords=coords)
