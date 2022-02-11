__author__ = 'github.com/arm61'

from typing import Tuple

import periodictable as pt
from easyCore.Objects.ObjectClasses import Parameter

from EasyReflectometry.special.parsing import parse_formula


def weighted_average_sld(a: Parameter, b: Parameter, p: Parameter) -> Parameter:
    """
    Determine the weighted average SLD between a and b, where p is the weight.
    
    :param a: First sld
    :param b: Second sld
    :param p: Weight
    :return: Weighted average
    """
    return a * (1 - p) + b * p


def neutron_scattering_length(formula: str) -> Tuple[Parameter, Parameter]:
    """
    Determine the neutron scattering length for a chemical formula.

    :param formula: Chemical formula.
    :return: Real and imaginary descriptors for the scattering length in angstrom.
    """
    formula_as_dict = parse_formula(formula)
    scattering_length = 0 + 0j
    for key, value in formula_as_dict.items():
        scattering_length += (pt.elements.symbol(key).neutron.b_c * value)
        if pt.elements.symbol(key).neutron.b_c_i:
            inc = pt.elements.symbol(key).neutron.b_c_i
        else:
            inc = 0
            scattering_length += inc * 1j * value
    return scattering_length * 1e-5


def apm_to_sld(scattering_length: float, thickness: Parameter,
               area_per_molecule: Parameter) -> Parameter:
    """
    Find the scattering length density for a given area per molecule.

    :param scattering_length: Scattering length of component, in angstrom.
    :param thickness: Thickness of component, in angstrom.
    :param area_per_molecule: Area per molecule, in angstrom ** 2.
    :return: Scattering length density of layer in e-6 1/angstrom ** 2. 
    """
    return scattering_length / (thickness * area_per_molecule) * 1e6
