__author__ = 'github.com/arm61'

from typing import Union, TextIO, List, Dict
import numpy as np
import scipp as sc
from orsopy.fileio import orso, Header


def load(fname: Union[TextIO, str]) -> sc.Dataset:
    """
    Load data from an ORSO .ort file. 

    :param fname: The file to be read. 
    
    :return: A scipp Dataset for the loaded datasets.
    """
    try:
        return _load_orso(fname)
    except (IndexError, ValueError):
        return _load_txt(fname)


def _load_orso(fname: Union[TextIO, str]) -> sc.Dataset:
    """
    Load from an ORSO compatible file.
    
    :param fname: The path for the file to be read.

    :return: A populated scipp dataset. 
    """
    data = {}
    f_data = orso.load_orso(fname)
    for i, o in enumerate(f_data):
        coords = {}
        coords[f'Qz{i}'] = sc.array(dims=[f'{o.info.columns[0].name}{i}'],
                                    values=o.data[:, 0],
                                    variances=np.square(o.data[:, 3]),
                                    unit=sc.Unit(o.info.columns[0].unit))
        try:
            ordinate = sc.array(dims=[f'{o.info.columns[0].name}{i}'],
                                values=o.data[:, 1],
                                variances=np.square(o.data[:, 2]),
                                unit=sc.Unit(o.info.columns[1].unit))
        except TypeError:
            ordinate = sc.array(dims=[f'{o.info.columns[0].name}{i}'],
                                values=o.data[:, 1],
                                variances=np.square(o.data[:, 2]))
        attrs = {'orso_header': sc.scalar(Header.asdict(o.info))}
        data[f'R{i}'] = sc.DataArray(data=ordinate, coords=coords, attrs=attrs)
    return sc.Dataset(data=data)


def _load_txt(fname: Union[TextIO, str]) -> sc.Dataset:
    """
    Load data from a simple txt file.
    
    :param fname: The path for the file to be read.

    :return: A populated scipp dataset. 
    """
    f_data = np.loadtxt(fname)
    data = {
        'R0': sc.array(dims=['Qz0'],
                       values=f_data[:, 1],
                       variances=np.square(f_data[:, 2]))
    }
    coords = {
        data['R0'].dims[0]:
        sc.array(dims=['Qz0'],
                 values=f_data[:, 0],
                 variances=np.square(f_data[:, 3]),
                 unit=sc.Unit('1/angstrom'))
    }
    return sc.Dataset(data=data, coords=coords)
