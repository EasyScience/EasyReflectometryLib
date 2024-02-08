from __future__ import annotations

from easyCore.Fitting.Constraints import ObjConstraint
from easyCore.Objects.ObjectClasses import Parameter

from EasyReflectometry.sample.layer import LayerApm
from EasyReflectometry.sample.layers import Layers
from EasyReflectometry.sample.material import Material

from .multilayer import MultiLayer


class SurfactantLayer(MultiLayer):
    """
    A :py:class:`SurfactantLayer` constructs a series of layers representing the
    head and tail groups of a surfactant. This item allows the definition of a
    surfactant or lipid using the chemistry of the head and tail regions, additionally
    this approach will make the application of constraints such as conformal roughness
    or area per molecule more straight forward.

    More information about the usage of this item is available in the
    `item library documentation`_

    .. _`item library documentation`: ./item_library.html#surfactantlayer
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
        surfactant = Layers(layers[0], layers[1], name=name)
        super().__init__(surfactant, name, interface)

        self.interface = interface
        self.type = 'Surfactant Layer'
        self.layers[1].area_per_molecule.enabled = True
        apm = ObjConstraint(self.layers[1].area_per_molecule, '', self.layers[0].area_per_molecule)
        self.layers[0].area_per_molecule.user_constraints['apm'] = apm
        self.layers[0].area_per_molecule.user_constraints['apm'].enabled = constrain_apm
        self.layers[1].roughness.enabled = True
        roughness = ObjConstraint(self.layers[1].roughness, '', self.layers[0].roughness)
        self.layers[0].roughness.user_constraints['roughness'] = roughness
        self.layers[0].roughness.user_constraints['roughness'].enabled = conformal_roughness

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
        layer1_chemical_structure: str,
        layer1_thickness: float,
        layer1_solvent: Material,
        layer1_solvation: float,
        layer1_area_per_molecule: float,
        layer1_roughness: float,
        layer2_chemical_structure: str,
        layer2_thickness: float,
        layer2_solvent: Material,
        layer2_solvation: float,
        layer2_area_per_molecule: float,
        layer2_roughness: float,
        name: str = 'EasySurfactantLayer',
        interface=None,
    ) -> SurfactantLayer:
        """
        Constructor for the surfactant layer where the parameters are known,
        :py:attr:`layer1` is that which the neutrons interact with first.

        :param layer1_chemical_structure: Chemical formula for first layer
        :param layer1_thickness: Thicknkess of first layer
        :param layer1_solvent: Solvent in first layer
        :param layer1_solvation: Fractional solvation of first layer by
            :py:attr:`layer1_solvent`
        :param layer1_area_per_molecule: Area per molecule of first layer
        :param layer1_roughness: Roughness of first layer
        :param layer2_chemical_structure: Chemical formula for second layer
        :param layer2_thickness: Thicknkess of second layer
        :param layer2_solvent: Solvent in second layer
        :param layer2_solvation: Fractional solvation of second layer by
            :py:attr:`layer2_solvent`
        :param layer2_area_per_molecule: Area per molecule of second layer
        :param layer2_roughness: Roughness of second layer
        :param name: Name for surfactant layer
        """
        layer1 = LayerApm.from_pars(
            layer1_chemical_structure,
            layer1_thickness,
            layer1_solvent,
            layer1_solvation,
            layer1_area_per_molecule,
            layer1_roughness,
            name=name + ' Layer 1',
        )
        layer2 = LayerApm.from_pars(
            layer2_chemical_structure,
            layer2_thickness,
            layer2_solvent,
            layer2_solvation,
            layer2_area_per_molecule,
            layer2_roughness,
            name=name + ' Layer 2',
        )
        return cls([layer1, layer2], name, interface)

    @property
    def constrain_apm(self) -> bool:
        """
        :return: if the area per molecule is constrained
        """
        return self.layers[0].area_per_molecule.user_constraints['apm'].enabled

    @constrain_apm.setter
    def constrain_apm(self, x: bool):
        """
        Set the constraint such that the head and tail layers have the
        same area per molecule.

        :param x: Boolean description the presence of the constraint.
        """
        self.layers[0].area_per_molecule.user_constraints['apm'].enabled = x
        self.layers[0].area_per_molecule.value = self.layers[0].area_per_molecule.raw_value

    @property
    def conformal_roughness(self) -> bool:
        """
        :return: is the roughness is the same for both layers.
        """
        return self.layers[0].roughness.user_constraints['roughness'].enabled

    @conformal_roughness.setter
    def conformal_roughness(self, x: bool):
        """
        Set the roughness to be the same for both layers.
        """
        self.layers[0].roughness.user_constraints['roughness'].enabled = x
        self.layers[0].roughness.value = self.layers[0].roughness.raw_value

    def constrain_solvent_roughness(self, solvent_roughness: Parameter):
        """
        Add the constraint to the solvent roughness.

        :param solvent_roughness: The solvent roughness parameter.
        """
        if not self.conformal_roughness:
            raise ValueError('Roughness must be conformal to use this function.')
        solvent_roughness.value = self.layers[0].roughness.value
        rough = ObjConstraint(solvent_roughness, '', self.layers[0].roughness)
        self.layers[0].roughness.user_constraints['solvent_roughness'] = rough

    def constain_multiple_contrast(
        self,
        another_contrast: SurfactantLayer,
        layer1_thickness: bool = True,
        layer2_thickness: bool = True,
        layer1_area_per_molecule: bool = True,
        layer2_area_per_molecule: bool = True,
        layer1_fraction: bool = True,
        layer2_fraction: bool = True,
    ):
        """
        Constrain structural parameters between surfactant layer objects.

        :param another_contrast: The surfactant layer to constrain
        """
        if layer1_thickness:
            layer1_thickness_constraint = ObjConstraint(self.layers[0].thickness, '', another_contrast.layers[0].thickness)
            another_contrast.layers[0].thickness.user_constraints[f'{another_contrast.name}'] = layer1_thickness_constraint
        if layer2_thickness:
            layer2_thickness_constraint = ObjConstraint(self.layers[1].thickness, '', another_contrast.layers[1].thickness)
            another_contrast.layers[1].thickness.user_constraints[f'{another_contrast.name}'] = layer2_thickness_constraint
        if layer1_area_per_molecule:
            layer1_area_per_molecule_constraint = ObjConstraint(
                self.layers[0].area_per_molecule, '', another_contrast.layers[0].area_per_molecule
            )
            another_contrast.layers[0].area_per_molecule.user_constraints[
                f'{another_contrast.name}'
            ] = layer1_area_per_molecule_constraint
        if layer2_area_per_molecule:
            layer2_area_per_molecule_constraint = ObjConstraint(
                self.layers[1].area_per_molecule, '', another_contrast.layers[1].area_per_molecule
            )
            another_contrast.layers[1].area_per_molecule.user_constraints[
                f'{another_contrast.name}'
            ] = layer2_area_per_molecule_constraint
        if layer1_fraction:
            layer1_fraction_constraint = ObjConstraint(
                self.layers[0].material.fraction, '', another_contrast.layers[0].material.fraction
            )
            another_contrast.layers[0].material.fraction.user_constraints[
                f'{another_contrast.name}'
            ] = layer1_fraction_constraint
        if layer2_fraction:
            layer2_fraction_constraint = ObjConstraint(
                self.layers[1].material.fraction, '', another_contrast.layers[1].material.fraction
            )
            another_contrast.layers[1].material.fraction.user_constraints[
                f'{another_contrast.name}'
            ] = layer2_fraction_constraint

    @property
    def _dict_repr(self) -> dict:
        """
        A simplified dict representation.

        :return: Simple dictionary
        """
        return {
            'layer1': self.layers[0]._dict_repr,
            'layer2': self.layers[1]._dict_repr,
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
