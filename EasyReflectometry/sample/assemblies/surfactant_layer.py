from __future__ import annotations

from easyCore.Fitting.Constraints import ObjConstraint
from easyCore.Objects.ObjectClasses import Parameter

from ..elements.layer_collection import LayerCollection
from ..elements.layers.layer_apm import LayerApm
from ..elements.materials.material import Material
from .base_assembly import BaseAssembly


class SurfactantLayer(BaseAssembly):
    """A surfactant layer constructs a series of layers representing the
    head and tail groups of a surfactant. This assembly allows the definition of a
    surfactant or lipid using the chemistry of the head and tail regions, additionally
    this approach will make the application of constraints such as conformal roughness
    or area per molecule more straight forward.

    More information about the usage of this assembly is available in the
    `surfactant documentation`_

    .. _`surfactant documentation`: ../sample/assemblies_library.html#surfactantlayer
    """

    def __init__(
        self,
        layers: list[LayerApm],
        name: str = 'EasySurfactantLayer',
        constrain_apm: bool = False,
        conformal_roughness: bool = False,
        interface=None,
    ):
        """Constructor.

        :param layers: List with the tail (index 0) and head (index 1) layer.
        :param name: Name for surfactant layer, defaults to 'EasySurfactantLayer'.
        :param constrain_apm: Constrain the area per molecule, defaults to :py:attr:`False`.
        :param conformal_roughness: Constrain the roughness to be the same for both layers, defaults to :py:attr:`False`.
        :param interface: Calculator interface, defaults to :py:attr:`None`.
        """
        surfactant = LayerCollection(layers[0], layers[1], name=name)
        super().__init__(
            name=name,
            type='Surfactant Layer',
            layers=surfactant,
            interface=interface,
        )

        self.interface = interface
        self.top_layer.area_per_molecule.enabled = True
        apm = ObjConstraint(
            dependent_obj=self.top_layer.area_per_molecule,
            operator='',
            independent_obj=self.bottom_layer.area_per_molecule,
        )
        self.bottom_layer.area_per_molecule.user_constraints['apm'] = apm
        self.bottom_layer.area_per_molecule.user_constraints['apm'].enabled = constrain_apm

        self._setup_roughness_constraints()
        if conformal_roughness:
            self._enable_roughness_constraints()

    # Class methods for instance creation
    @classmethod
    def default(cls, interface=None) -> SurfactantLayer:
        """Default instance of a surfactant layer object. The default lipid
        type is DPPC.

        :return: Surfactant layer object.
        """
        d2o = Material.from_pars(6.36, 0, 'D2O')
        air = Material.from_pars(0, 0, 'Air')
        tail = LayerApm.from_pars('C32D64', 16, air, 0.0, 48.2, 3, 'DPPC Tail')
        head = LayerApm.from_pars('C10H18NO8P', 10.0, d2o, 0.2, 48.2, 3.0, 'DPPC Head')
        return cls([tail, head], name='DPPC', interface=interface)

    @classmethod
    def from_pars(
        cls,
        tail_layer_molecular_formula: str,
        tail_layer_thickness: float,
        tail_layer_solvent: Material,
        tail_layer_solvent_surface_coverage: float,
        tail_layer_area_per_molecule: float,
        tail_layer_roughness: float,
        head_layer_molecular_formula: str,
        head_layer_thickness: float,
        head_layer_solvent: Material,
        head_layer_solvent_surface_coverage: float,
        head_layer_area_per_molecule: float,
        head_layer_roughness: float,
        name: str = 'EasySurfactantLayer',
        interface=None,
    ) -> SurfactantLayer:
        """Instance of a surfactant layer where the parameters are known,
        :py:attr:`head_layer` is that which the neutrons interact with first.

        :param tail_layer_molecular_formula: Molecular formula of species constituting the tail layer.
        :param tail_layer_thickness: Thicknkess of tail layer.
        :param tail_layer_solvent: Solvent in tail layer.
        :param tail_layer_solvent_surface_coverage: Fraction of tail layer not covered by molecules.
        :param tail_layer_area_per_molecule: Area per molecule of tail layer.
        :param tail_layer_roughness: Roughness of tail layer.
        :param head_layer_molecular_formula: Molecular formula of species constituting the head layer.
        :param head_layer_thickness: Thicknkess of head layer.
        :param head_layer_solvent: Solvent in head layer.
        :param head_layer_solvent_surface_coverage: Fraction of head layer not covered by molecules.
        :param head_layer_area_per_molecule: Area per molecule of head layer.
        :param head_layer_roughness: Roughness of head layer.
        :param name: Name for surfactant layer.
        """
        head_layer = LayerApm.from_pars(
            chemical_formula=head_layer_molecular_formula,
            thickness=head_layer_thickness,
            solvent=head_layer_solvent,
            solvent_surface_coverage=head_layer_solvent_surface_coverage,
            area_per_molecule=head_layer_area_per_molecule,
            roughness=head_layer_roughness,
            name=name + ' Head Layer',
        )
        tail_layer = LayerApm.from_pars(
            chemical_formula=tail_layer_molecular_formula,
            thickness=tail_layer_thickness,
            solvent=tail_layer_solvent,
            solvent_surface_coverage=tail_layer_solvent_surface_coverage,
            area_per_molecule=tail_layer_area_per_molecule,
            roughness=tail_layer_roughness,
            name=name + ' Tail Layer',
        )
        return cls([tail_layer, head_layer], name, interface)

    @property
    def constrain_apm(self) -> bool:
        """Get the area per molecule constraint status."""
        return self.bottom_layer.area_per_molecule.user_constraints['apm'].enabled

    @constrain_apm.setter
    def constrain_apm(self, status: bool):
        """Set the status for the area per molecule constraint such that the head and tail layers have the
        same area per molecule.

        :param x: Boolean description the wanted of the constraint.
        """
        self.bottom_layer.area_per_molecule.user_constraints['apm'].enabled = status
        self.bottom_layer.area_per_molecule.value = self.bottom_layer.area_per_molecule.raw_value

    @property
    def conformal_roughness(self) -> bool:
        """Get the roughness constraint status."""
        return self.bottom_layer.roughness.user_constraints['roughness_1'].enabled

    @conformal_roughness.setter
    def conformal_roughness(self, status: bool):
        """Set the status for the roughness to be the same for both layers."""
        if status:
            self._enable_roughness_constraints()
            self.bottom_layer.roughness.value = self.bottom_layer.roughness.raw_value
        else:
            self._disable_roughness_constraints()

    def constrain_solvent_roughness(self, solvent_roughness: Parameter):
        """Add the constraint to the solvent roughness.

        :param solvent_roughness: The solvent roughness parameter.
        """
        if not self.conformal_roughness:
            raise ValueError('Roughness must be conformal to use this function.')
        solvent_roughness.value = self.bottom_layer.roughness.value
        rough = ObjConstraint(solvent_roughness, '', self.bottom_layer.roughness)
        self.bottom_layer.roughness.user_constraints['solvent_roughness'] = rough

    def constain_multiple_contrast(
        self,
        another_contrast: SurfactantLayer,
        head_layer_thickness: bool = True,
        tail_layer_thickness: bool = True,
        head_layer_area_per_molecule: bool = True,
        tail_layer_area_per_molecule: bool = True,
        head_layer_fraction: bool = True,
        tail_layer_fraction: bool = True,
    ):
        """Constrain structural parameters between surfactant layer objects.

        :param another_contrast: The surfactant layer to constrain
        """
        if head_layer_thickness:
            head_layer_thickness_constraint = ObjConstraint(self.top_layer.thickness, '', another_contrast.top_layer.thickness)
            another_contrast.top_layer.thickness.user_constraints[f'{another_contrast.name}'] = head_layer_thickness_constraint
        if tail_layer_thickness:
            tail_layer_thickness_constraint = ObjConstraint(
                self.bottom_layer.thickness, '', another_contrast.bottom_layer.thickness
            )
            another_contrast.bottom_layer.thickness.user_constraints[
                f'{another_contrast.name}'
            ] = tail_layer_thickness_constraint
        if head_layer_area_per_molecule:
            head_layer_area_per_molecule_constraint = ObjConstraint(
                self.top_layer.area_per_molecule, '', another_contrast.top_layer.area_per_molecule
            )
            another_contrast.top_layer.area_per_molecule.user_constraints[
                f'{another_contrast.name}'
            ] = head_layer_area_per_molecule_constraint
        if tail_layer_area_per_molecule:
            tail_layer_area_per_molecule_constraint = ObjConstraint(
                self.bottom_layer.area_per_molecule, '', another_contrast.bottom_layer.area_per_molecule
            )
            another_contrast.bottom_layer.area_per_molecule.user_constraints[
                f'{another_contrast.name}'
            ] = tail_layer_area_per_molecule_constraint
        if head_layer_fraction:
            head_layer_fraction_constraint = ObjConstraint(
                self.top_layer.material.fraction, '', another_contrast.top_layer.material.fraction
            )
            another_contrast.top_layer.material.fraction.user_constraints[
                f'{another_contrast.name}'
            ] = head_layer_fraction_constraint
        if tail_layer_fraction:
            tail_layer_fraction_constraint = ObjConstraint(
                self.bottom_layer.material.fraction, '', another_contrast.bottom_layer.material.fraction
            )
            another_contrast.bottom_layer.material.fraction.user_constraints[
                f'{another_contrast.name}'
            ] = tail_layer_fraction_constraint

    @property
    def _dict_repr(self) -> dict:
        """A simplified dict representation."""
        return {
            'head_layer': self.top_layer._dict_repr,
            'tail_layer': self.bottom_layer._dict_repr,
            'area per molecule constrained': self.constrain_apm,
            'conformal roughness': self.conformal_roughness,
        }

    def as_dict(self, skip: list = None) -> dict:
        """Cleaned dictionary. Custom as_dict method to skip necessary things."""
        if skip is None:
            skip = []
        this_dict = super().as_dict(skip=skip)
        for i in this_dict['layers']['data']:
            del i['material']
            del i['_scattering_length_real']
            del i['_scattering_length_imag']
        this_dict['constrain_apm'] = self.constrain_apm
        this_dict['conformal_roughness'] = self.conformal_roughness
        return this_dict
