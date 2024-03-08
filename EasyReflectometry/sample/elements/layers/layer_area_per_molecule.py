from __future__ import annotations

from copy import deepcopy

from easyCore import np
from easyCore.Fitting.Constraints import FunctionalConstraint
from easyCore.Objects.ObjectClasses import Parameter

from EasyReflectometry.special.calculations import area_per_molecule_to_sld
from EasyReflectometry.special.calculations import neutron_scattering_length

from ..materials.material import Material
from ..materials.material_solvated import MATERIAL_SOLVATED_DETAILS
from ..materials.material_solvated import MaterialSolvated
from .layer import LAYER_DETAILS
from .layer import Layer

LAYER_AREA_PER_MOLECULE_DETAILS = {
    'molecular_formula': 'C10H18NO8P',
    'area_per_molecule': {
        'description': 'Surface coverage',
        'value': 48.2,
        'units': 'angstrom ** 2',
        'min': 0,
        'max': np.inf,
        'fixed': True,
    },
    'sl': {
        'description': 'The real scattering length for a molecule formula in angstrom.',
        'url': 'https://www.ncnr.nist.gov/resources/activation/',
        'value': 4.186,
        'units': 'angstrom',
        'min': -np.Inf,
        'max': np.Inf,
        'fixed': True,
    },
    'isl': {
        'description': 'The real scattering length for a molecule formula in angstrom.',
        'url': 'https://www.ncnr.nist.gov/resources/activation/',
        'value': 0.0,
        'units': 'angstrom',
        'min': -np.Inf,
        'max': np.Inf,
        'fixed': True,
    },
}
LAYER_AREA_PER_MOLECULE_DETAILS.update(LAYER_DETAILS)
LAYER_AREA_PER_MOLECULE_DETAILS.update(MATERIAL_SOLVATED_DETAILS)


class LayerAreaPerMolecule(Layer):
    """The :py:class:`LayerAreaPerMolecule` class allows a layer to be defined in terms of some
    molecular formula an area per molecule, and a solvent.

    """

    # Added in __init__
    #: Real part of the scattering length.
    _scattering_length_real: Parameter
    #: Imaginary part of the scattering length.
    _scattering_length_imag: Parameter
    #: Area per molecule in the layer in Anstrom^2.
    _area_per_molecule: Parameter

    # Other typer than in __init__.super()
    material: MaterialSolvated

    def __init__(
        self,
        molecular_formula: str,
        thickness: Parameter,
        solvent: Material,
        solvent_fraction: Parameter,
        area_per_molecule: Parameter,
        roughness: Parameter,
        name: str = 'EasyLayerAreaPerMolecule',
        interface=None,
    ):
        """Constructor.

        :param molecular_formula: Formula for the molecule in the layer.
        :param thickness: Layer thickness in Angstrom.
        :param solvent: Solvent containing the molecule.
        :param solvent_fraction: Fraction of solvent in layer. Fx solvation or surface coverage.
        :param area_per_molecule: Area per molecule in the layer
        :param roughness: Upper roughness on the layer in Angstrom.
        :param name: Name of the layer, defaults to "EasyLayerAreaPerMolecule"
        :param interface: Interface object, defaults to `None`
        """
        scattering_length = neutron_scattering_length(molecular_formula)
        default_options = deepcopy(LAYER_AREA_PER_MOLECULE_DETAILS)
        del default_options['sl']['value']
        del default_options['isl']['value']
        scattering_length_real = Parameter('scattering_length_real', scattering_length.real, **default_options['sl'])
        scattering_length_imag = Parameter('scattering_length_imag', scattering_length.imag, **default_options['isl'])
        sld_real = area_per_molecule_to_sld(scattering_length_real.raw_value, thickness.raw_value, area_per_molecule.raw_value)
        sld_imag = area_per_molecule_to_sld(scattering_length_imag.raw_value, thickness.raw_value, area_per_molecule.raw_value)

        material = Material.from_pars(sld_real, sld_imag, name=molecular_formula, interface=interface)

        constraint = FunctionalConstraint(
            dependent_obj=material.sld,
            func=area_per_molecule_to_sld,
            independent_objs=[scattering_length_real, thickness, area_per_molecule],
        )
        thickness.user_constraints['area_per_molecule'] = constraint
        area_per_molecule.user_constraints['area_per_molecule'] = constraint
        scattering_length_real.user_constraints['area_per_molecule'] = constraint

        iconstraint = FunctionalConstraint(
            dependent_obj=material.isld,
            func=area_per_molecule_to_sld,
            independent_objs=[scattering_length_imag, thickness, area_per_molecule],
        )
        thickness.user_constraints['iarea_per_molecule'] = iconstraint
        area_per_molecule.user_constraints['iarea_per_molecule'] = iconstraint
        scattering_length_imag.user_constraints['iarea_per_molecule'] = iconstraint

        solvated_material = MaterialSolvated(
            material=material,
            solvent=solvent,
            solvent_fraction=solvent_fraction,
            interface=interface,
        )
        super().__init__(
            material=solvated_material,
            thickness=thickness,
            roughness=roughness,
            name=name,
            interface=interface,
        )
        self._add_component('_scattering_length_real', scattering_length_real)
        self._add_component('_scattering_length_imag', scattering_length_imag)
        self._add_component('_area_per_molecule', area_per_molecule)
        self._molecular_formula = molecular_formula
        self.interface = interface

    # Class methods for instance creation
    @classmethod
    def default(cls, interface=None) -> LayerAreaPerMolecule:
        """A default instance for layer defined from molecule formula and area per molecule.

        :param interface: Calculator interface, defaults to `None`.
        """
        area_per_molecule = Parameter('area_per_molecule', **LAYER_AREA_PER_MOLECULE_DETAILS['area_per_molecule'])
        thickness = Parameter('thickness', **LAYER_AREA_PER_MOLECULE_DETAILS['thickness'])
        roughness = Parameter('roughness', **LAYER_AREA_PER_MOLECULE_DETAILS['roughness'])
        solvent_fraction = Parameter('solvent_fraction', **LAYER_AREA_PER_MOLECULE_DETAILS['solvent_fraction'])
        solvent = Material.from_pars(6.36, 0, 'D2O', interface=interface)
        return cls(
            molecular_formula=LAYER_AREA_PER_MOLECULE_DETAILS['molecular_formula'],
            thickness=thickness,
            solvent=solvent,
            solvent_fraction=solvent_fraction,
            area_per_molecule=area_per_molecule,
            roughness=roughness,
            interface=interface,
        )

    @classmethod
    def from_pars(
        cls,
        molecular_formula: str,
        thickness: float,
        solvent: Material,
        solvent_fraction: float,
        area_per_molecule: float,
        roughness: float,
        name: str = 'EasyLayerAreaPerMolecule',
        interface=None,
    ) -> LayerAreaPerMolecule:
        """An instance for a layer described with the area per molecule, where the parameters are known.

        :param molecular_formula: Formula for the molecule in the layer.
        :param thickness: Layer thickness in Angstrom.
        :param solvent: Solvent in the layer.
        :param solvent_fraction: Fraction of solvent in layer. Fx solvation or coverage.
        :param area_per_molecule: Area per molecule.
        :param roughness: Upper roughness on the layer in Angstrom.
        :param name: Identifier, defaults to 'EasyLayerAreaPerMolecule'.
        :param interface: Calculator interface, defaults to `None`.
        """
        default_options = deepcopy(LAYER_AREA_PER_MOLECULE_DETAILS)
        del default_options['area_per_molecule']['value']
        area_per_molecule = Parameter('area_per_molecule', area_per_molecule, **default_options['area_per_molecule'])
        del default_options['thickness']['value']
        thickness = Parameter('thickness', thickness, **default_options['thickness'])
        del default_options['roughness']['value']
        roughness = Parameter('roughness', roughness, **default_options['roughness'])
        del default_options['solvent_fraction']['value']
        solvent_fraction = Parameter('solvent_fraction', solvent_fraction, **default_options['solvent_fraction'])

        return cls(
            molecular_formula=molecular_formula,
            thickness=thickness,
            solvent=solvent,
            solvent_fraction=solvent_fraction,
            area_per_molecule=area_per_molecule,
            roughness=roughness,
            name=name,
            interface=interface,
        )

    @property
    def area_per_molecule(self) -> Parameter:
        """Get the area per molecule."""
        return self._area_per_molecule

    @property
    def solvent(self) -> Material:
        """Get the solvent material."""
        return self.material.solvent

    @solvent.setter
    def solvent(self, new_solvent: Material) -> None:
        """Set the solvent material.

        :param new_solvent: New solvent material.
        """
        self.material.solvent = new_solvent

    @property
    def solvent_fraction(self) -> Parameter:
        """Get the fraction of the layer occupied by the solvent.
        This could be a result of either water solvating the molecule, or incomplete surface coverage of the molecules.
        """
        return self.material.solvent_fraction

    @solvent_fraction.setter
    def solvent_fraction(self, solvent_fraction: float) -> None:
        """Set the fraction of the layer occupied by the solvent.
        This could be a result of either water solvating the molecule, or incomplete surface coverage of the molecules.

        :param solvent_fraction: Fraction of layer described by the solvent.
        """
        self.material.solvent_fraction = solvent_fraction

    @property
    def molecular_formula(self) -> str:
        """Get the formula of molecule the layer."""
        return self._molecular_formula

    @molecular_formula.setter
    def molecular_formula(self, formula_string: str) -> None:
        """Set the formula of the molecule in the material.

        :param formula_string: String that defines the molecular formula.
        """
        self._molecular_formula = formula_string
        scattering_length = neutron_scattering_length(formula_string)
        self._scattering_length_real.value = scattering_length.real
        self._scattering_length_imag.value = scattering_length.imag
        self.material.material.name = formula_string
        self.material._update_name()

    @property
    def _dict_repr(self) -> dict[str, str]:
        """Dictionary representation of the :py:class:`Layerarea_per_molecule` object. Produces a simple dictionary"""
        dict_repr = super()._dict_repr
        dict_repr['molecular_formula'] = self._molecular_formula
        dict_repr['area_per_molecule'] = f'{self.area_per_molecule.raw_value:.2f} ' f'{self.area_per_molecule.unit}'
        return dict_repr

    def as_dict(self, skip: list = None) -> dict[str, str]:
        """Produces a cleaned  using a austom as_dict method to skip necessary things.

        :param skip: List of keys to skip, defaults to :py:attr:`None`.
        """
        if skip is None:
            skip = []
        this_dict = super().as_dict(skip=skip)
        del this_dict['material']
        del this_dict['_scattering_length_real']
        del this_dict['_scattering_length_imag']
        return this_dict
