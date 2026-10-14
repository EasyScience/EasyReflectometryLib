# SPDX-FileCopyrightText: 2026 EasyScience contributors <https://github.com/easyscience>
# SPDX-License-Identifier: BSD-3-Clause


import numpy as np
import periodictable as pt

from easyreflectometry.special.parsing import parse_formula

AVOGADRO = 6.02214076e23  # 1 / mole

# Magnetic scattering length of one Bohr magneton in angstrom,
# p = m_n |mu_n| mu_0 mu_B / (2 pi hbar^2) (CODATA 2018). The often quoted
# gamma * r_0 / 2 = 2.6955e-5 drops the factor m_n / m_p; orsopy's `rho_of_M`
# corresponds to 2.646e-5.
MAGNETIC_SCATTERING_LENGTH = 2.69913559e-5


def weighted_average(a: float, b: float, p: float) -> float:
    """Determine the weighted average for a and b, where p is the weight.

    Parameters
    ----------
    a : float
        First value.
    b : float
        Second value.
    p : float
        Weight.

    Returns
    -------
    float
        Weighted average.
    """
    return a * (1 - p) + b * p


def neutron_scattering_length(formula: str) -> complex:
    """Determine the neutron scattering length for a chemical formula.

    Parameters
    ----------
    formula : str
        Chemical formula.

    Returns
    -------
    complex
        Real and imaginary descriptors for the scattering length in angstrom.
    """
    formula_as_dict = parse_formula(formula)
    scattering_length = 0 + 0j
    for key, value in formula_as_dict.items():
        scattering_length += pt.elements.symbol(key).neutron.b_c * value
        if pt.elements.symbol(key).neutron.b_c_i:
            inc = pt.elements.symbol(key).neutron.b_c_i
        else:
            inc = 0
        scattering_length += inc * 1j * value
    return scattering_length * 1e-5


def molecular_weight(formula: str) -> float:
    """Determine the molecular weight for a chemical formula.

    Parameters
    ----------
    formula : str
        Chemical formula.

    Returns
    -------
    float
        Molecular weight of the material in kilograms.
    """
    formula_as_dict = parse_formula(formula)
    mw = 0
    for key, value in formula_as_dict.items():
        mw += pt.elements.symbol(key).mass * value
    return mw


def area_per_molecule_to_scattering_length_density(
    scattering_length: float,
    thickness: float,
    area_per_molecule: float,
) -> float:
    """Find the scattering length density for a given area per molecule.

    Parameters
    ----------
    scattering_length : float
        Scattering length of component, in angstrom.
    thickness : float
        Thickness of component, in angstrom.
    area_per_molecule : float
        Area per molecule, in angstrom^2.

    Returns
    -------
    float
        Scattering length density of layer in e-6 1/angstrom^2.
    """
    return scattering_length / (thickness * area_per_molecule) * 1e6


def number_density_from_mass_density(density: float, molecular_weight: float) -> float:
    """Number density of formula units in 1/angstrom^3 from a mass density in g/cm^3."""
    return AVOGADRO * density / molecular_weight * 1e-24


def mass_density_from_number_density(number_density: float, molecular_weight: float) -> float:
    """Mass density in g/cm^3 from a number density of formula units in 1/angstrom^3."""
    return number_density * molecular_weight / AVOGADRO * 1e24


def density_to_sld(scattering_length: float, molecular_weight: float, density: float) -> float:
    """Find the scattering length density from the mass density of a material.

    Parameters
    ----------
    scattering_length : float
        Scattering length of component, in angstrom.
    molecular_weight : float
        Molecular weight of component, in u.
    density : float
        Mass density of the component, in gram centimeter^-3.

    Returns
    -------
    float
        Scattering length density of layer in e-6 1/angstrom^2.
    """
    # 0.602214076 is avogadros constant times 1e-24
    return 0.602214076e6 * density * scattering_length / molecular_weight


def field_frame_components(rho_m, theta_m, guide_field_angle: float) -> tuple:
    """Split an in-plane magnetic SLD into its parts along and across the field.

    Uses refl1d's public convention: ``theta_m`` is the in-plane moment angle
    and ``guide_field_angle`` (refl1d's ``Aguide``) tilts the field about the
    beam axis, 270 degrees being in the sample plane. In the field frame the
    moment is ``(rho_m cos t, rho_m sin t cos A, rho_m sin t sin A)``, the last
    component lying along the field.

    Parameters
    ----------
    rho_m : float or array
        Magnetic scattering length density.
    theta_m : float or array
        In-plane moment angle in degrees.
    guide_field_angle : float
        Field angle about the beam axis in degrees.

    Returns
    -------
    tuple
        ``(parallel, perpendicular)``: the signed component along the field
        and the magnitude of the component transverse to it.
    """
    theta = np.radians(theta_m)
    tilt = np.radians(guide_field_angle)
    parallel = rho_m * np.sin(theta) * np.sin(tilt)
    perpendicular = np.hypot(rho_m * np.cos(theta), rho_m * np.sin(theta) * np.cos(tilt))
    return parallel, perpendicular
