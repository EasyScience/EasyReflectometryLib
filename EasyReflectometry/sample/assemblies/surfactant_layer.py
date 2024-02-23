from __future__ import annotations

from easyCore.Fitting.Constraints import ObjConstraint
from easyCore.Objects.ObjectClasses import Parameter

from ..elements.layer_collection import LayerCollection
from ..elements.layers.layer_apm import LayerApm
from ..elements.materials.material import Material
from .base_assembly import BaseAssembly


class SurfactantLayer(BaseAssembly):
    """
    A :py:class:`SurfactantLayer` constructs a series of layers representing the
    head and tail groups of a surfactant. This assembly allows the definition of a
    surfactant or lipid using the chemistry of the head and tail regions, additionally
    this approach will make the application of constraints such as conformal roughness
    or area per molecule more straight forward.

    More information about the usage of this assembly is available in the
    `surfactant documentation`_

    .. _`surfactant documentation`: ./assemblies_library.html#surfactantlayer
    """

    def __init__(
        self,
        layers: list[LayerApm],
        name: str = 'EasySurfactantLayer',
        constrain_apm: bool = False,
        conformal_roughness: bool = False,
        interface=None,
    ):
        """
        :param head: Head layer object
        :param tail: Tail layer object
        :param name: Name for surfactant layer
        """
        surfactant = LayerCollection(layers[0], layers[1], name=name)
        super().__init__(
            name=name,
            type='Surfactant Layer',
            layers=surfactant,
            interface=interface,
        )

        self.interface = interface
        self.bottom_layer.area_per_molecule.enabled = True
        apm = ObjConstraint(self.bottom_layer.area_per_molecule, '', self.top_layer.area_per_molecule)
        self.top_layer.area_per_molecule.user_constraints['apm'] = apm
        self.top_layer.area_per_molecule.user_constraints['apm'].enabled = constrain_apm

        self._setup_roughness_constraints()
        if conformal_roughness:
            self._enable_roughness_constraints()

    # Class constructors
    @classmethod
    def default(cls, interface=None) -> SurfactantLayer:
        """
        Default constructor for a surfactant layer object. The default lipid
        type is DPPC.

        :return: Surfactant layer object.
        """
        d2o = Material.from_pars(6.36, 0, 'D2O')
        air = Material.from_pars(0, 0, 'Air')
        head = LayerApm.from_pars('C10H18NO8P', 10.0, d2o, 0.2, 48.2, 3.0, 'DPPC Head')
        tail = LayerApm.from_pars('C32D64', 16, air, 0.0, 48.2, 3, 'DPPC Tail')
        return cls([tail, head], name='DPPC', interface=interface)

    @classmethod
    def from_pars(
        cls,
        top_layer_chemical_structure: str,
        top_layer_thickness: float,
        top_layer_solvent: Material,
        top_layer_solvation: float,
        top_layer_area_per_molecule: float,
        top_layer_roughness: float,
        bottom_layer_chemical_structure: str,
        bottom_layer_thickness: float,
        bottom_layer_solvent: Material,
        bottom_layer_solvation: float,
        bottom_layer_area_per_molecule: float,
        bottom_layer_roughness: float,
        name: str = 'EasySurfactantLayer',
        interface=None,
    ) -> SurfactantLayer:
        """
        Constructor for the surfactant layer where the parameters are known,
        :py:attr:`top_layer` is that which the neutrons interact with first.

        :param top_layer_chemical_structure: Chemical formula for first layer
        :param top_layer_thickness: Thicknkess of first layer
        :param top_layer_solvent: Solvent in first layer
        :param top_layer_solvation: Fractional solvation of first layer by
            :py:attr:`top_layer_solvent`
        :param top_layer_area_per_molecule: Area per molecule of first layer
        :param top_layer_roughness: Roughness of first layer
        :param bottom_layer_chemical_structure: Chemical formula for second layer
        :param bottom_layer_thickness: Thicknkess of second layer
        :param bottom_layer_solvent: Solvent in second layer
        :param bottom_layer_solvation: Fractional solvation of second layer by
            :py:attr:`bottom_layer_solvent`
        :param bottom_layer_area_per_molecule: Area per molecule of second layer
        :param bottom_layer_roughness: Roughness of second layer
        :param name: Name for surfactant layer
        """
        top_layer = LayerApm.from_pars(
            top_layer_chemical_structure,
            top_layer_thickness,
            top_layer_solvent,
            top_layer_solvation,
            top_layer_area_per_molecule,
            top_layer_roughness,
            name=name + ' Top Layer',
        )
        bottom_layer = LayerApm.from_pars(
            bottom_layer_chemical_structure,
            bottom_layer_thickness,
            bottom_layer_solvent,
            bottom_layer_solvation,
            bottom_layer_area_per_molecule,
            bottom_layer_roughness,
            name=name + ' Bottom Layer',
        )
        return cls([top_layer, bottom_layer], name, interface)

    @property
    def constrain_apm(self) -> bool:
        """
        :return: if the area per molecule is constrained
        """
        return self.top_layer.area_per_molecule.user_constraints['apm'].enabled

    @constrain_apm.setter
    def constrain_apm(self, x: bool):
        """
        Set the constraint such that the head and tail layers have the
        same area per molecule.

        :param x: Boolean description the presence of the constraint.
        """
        self.top_layer.area_per_molecule.user_constraints['apm'].enabled = x
        self.top_layer.area_per_molecule.value = self.top_layer.area_per_molecule.raw_value

    @property
    def conformal_roughness(self) -> bool:
        """
        :return: is the roughness is the same for both layers.
        """
        return self.top_layer.roughness.user_constraints['roughness_1'].enabled

    @conformal_roughness.setter
    def conformal_roughness(self, x: bool):
        """
        Set the roughness to be the same for both layers.
        """
        if x:
            self._enable_roughness_constraints()
            self.top_layer.roughness.value = self.top_layer.roughness.raw_value
        else:
            self._disable_roughness_constraints()

    def constrain_solvent_roughness(self, solvent_roughness: Parameter):
        """
        Add the constraint to the solvent roughness.

        :param solvent_roughness: The solvent roughness parameter.
        """
        if not self.conformal_roughness:
            raise ValueError('Roughness must be conformal to use this function.')
        solvent_roughness.value = self.top_layer.roughness.value
        rough = ObjConstraint(solvent_roughness, '', self.top_layer.roughness)
        self.top_layer.roughness.user_constraints['solvent_roughness'] = rough

    def constain_multiple_contrast(
        self,
        another_contrast: 'SurfactantLayer',
        top_layer_thickness: bool = True,
        bottom_layer_thickness: bool = True,
        top_layer_area_per_molecule: bool = True,
        bottom_layer_area_per_molecule: bool = True,
        top_layer_fraction: bool = True,
        bottom_layer_fraction: bool = True,
    ):
        """
        Constrain structural parameters between surfactant layer objects.

        :param another_contrast: The surfactant layer to constrain
        """
        if top_layer_thickness:
            top_layer_thickness_constraint = ObjConstraint(self.top_layer.thickness, '', another_contrast.top_layer.thickness)
            another_contrast.top_layer.thickness.user_constraints[f'{another_contrast.name}'] = top_layer_thickness_constraint
        if bottom_layer_thickness:
            bottom_layer_thickness_constraint = ObjConstraint(
                self.bottom_layer.thickness, '', another_contrast.bottom_layer.thickness
            )
            another_contrast.bottom_layer.thickness.user_constraints[
                f'{another_contrast.name}'
            ] = bottom_layer_thickness_constraint
        if top_layer_area_per_molecule:
            top_layer_area_per_molecule_constraint = ObjConstraint(
                self.top_layer.area_per_molecule, '', another_contrast.top_layer.area_per_molecule
            )
            another_contrast.top_layer.area_per_molecule.user_constraints[
                f'{another_contrast.name}'
            ] = top_layer_area_per_molecule_constraint
        if bottom_layer_area_per_molecule:
            bottom_layer_area_per_molecule_constraint = ObjConstraint(
                self.bottom_layer.area_per_molecule, '', another_contrast.bottom_layer.area_per_molecule
            )
            another_contrast.bottom_layer.area_per_molecule.user_constraints[
                f'{another_contrast.name}'
            ] = bottom_layer_area_per_molecule_constraint
        if top_layer_fraction:
            top_layer_fraction_constraint = ObjConstraint(
                self.top_layer.material.fraction, '', another_contrast.top_layer.material.fraction
            )
            another_contrast.top_layer.material.fraction.user_constraints[
                f'{another_contrast.name}'
            ] = top_layer_fraction_constraint
        if bottom_layer_fraction:
            bottom_layer_fraction_constraint = ObjConstraint(
                self.bottom_layer.material.fraction, '', another_contrast.bottom_layer.material.fraction
            )
            another_contrast.bottom_layer.material.fraction.user_constraints[
                f'{another_contrast.name}'
            ] = bottom_layer_fraction_constraint

    @property
    def _dict_repr(self) -> dict:
        """
        A simplified dict representation.

        :return: Simple dictionary
        """
        return {
            'top_layer': self.top_layer._dict_repr,
            'bottom_layer': self.bottom_layer._dict_repr,
            'area per molecule constrained': self.constrain_apm,
            'conformal roughness': self.conformal_roughness,
        }

    def as_dict(self, skip: list = None) -> dict:
        """
        Custom as_dict method to skip necessary things.

        :return: Cleaned dictionary.
        """
        if skip is None:
            skip = []
        this_dict = super().as_dict(skip=skip)
        for i in this_dict['layers']['data']:
            del i['material']
            del i['scattering_length_real']
            del i['scattering_length_imag']
        this_dict['constrain_apm'] = self.constrain_apm
        this_dict['conformal_roughness'] = self.conformal_roughness
        return this_dict
