from __future__ import annotations

from typing import Optional

from easyCore.Fitting.Constraints import ObjConstraint
from easyCore.Objects.ObjectClasses import Parameter

from ..elements.layer_collection import LayerCollection
from ..elements.layers.layer_area_per_molecule import LayerAreaPerMolecule
from ..elements.materials.material import Material
from .base_assembly import BaseAssembly


class SurfactantLayer(BaseAssembly):
    """A surfactant layer constructs a series of layers representing the
    head and tail groups of a surfactant.
    This assembly allows the definition of a surfactant or lipid using the chemistry
    of the head (head_layer) and tail (tail_layer) regions, additionally
    this approach will make the application of constraints such as conformal roughness
    or area per molecule more straight forward.

    More information about the usage of this assembly is available in the
    `surfactant documentation`_

    .. _`surfactant documentation`: ../sample/assemblies_library.html#surfactantlayer
    """

    def __init__(
        self,
        layers: list[LayerAreaPerMolecule],
        name: str = 'EasySurfactantLayer',
        constrain_area_per_molecule: bool = False,
        conformal_roughness: bool = False,
        interface=None,
    ):
        """Constructor.

        :param layers: List with the tail (index 0) and head (index 1) layer.
        :param name: Name for surfactant layer, defaults to 'EasySurfactantLayer'.
        :param constrain_area_per_molecule: Constrain the area per molecule, defaults to `False`.
        :param conformal_roughness: Constrain the roughness to be the same for both layers, defaults to `False`.
        :param interface: Calculator interface, defaults to `None`.
        """
        surfactant = LayerCollection(layers[0], layers[1], name=name)
        super().__init__(
            name=name,
            type='Surfactant Layer',
            layers=surfactant,
            interface=interface,
        )

        self.interface = interface
        self.head_layer._area_per_molecule.enabled = True
        area_per_molecule = ObjConstraint(
            dependent_obj=self.head_layer._area_per_molecule,
            operator='',
            independent_obj=self.tail_layer._area_per_molecule,
        )
        self.tail_layer._area_per_molecule.user_constraints['area_per_molecule'] = area_per_molecule
        self.tail_layer._area_per_molecule.user_constraints['area_per_molecule'].enabled = constrain_area_per_molecule

        self._setup_roughness_constraints()
        if conformal_roughness:
            self._enable_roughness_constraints()

    # Class methods for instance creation
    @classmethod
    def default(cls, interface=None) -> SurfactantLayer:
        """Default instance of a surfactant layer object.
        The default lipid type is DPPC.

        :return: Surfactant layer object.
        """
        d2o = Material.from_pars(6.36, 0, 'D2O')
        air = Material.from_pars(0, 0, 'Air')
        tail = LayerAreaPerMolecule.from_pars(
            molecular_formula='C32D64',
            thickness=16,
            solvent=air,
            solvent_fraction=0.0,
            area_per_molecule=48.2,
            roughness=3,
            name='DPPC Tail',
        )
        head = LayerAreaPerMolecule.from_pars(
            molecular_formula='C10H18NO8P',
            thickness=10.0,
            solvent=d2o,
            solvent_fraction=0.2,
            area_per_molecule=48.2,
            roughness=3.0,
            name='DPPC Head',
        )
        return cls([tail, head], interface=interface)

    @classmethod
    def from_pars(
        cls,
        tail_layer_molecular_formula: str,
        tail_layer_thickness: float,
        tail_layer_solvent: Material,
        tail_layer_solvent_fraction: float,
        tail_layer_area_per_molecule: float,
        tail_layer_roughness: float,
        head_layer_molecular_formula: str,
        head_layer_thickness: float,
        head_layer_solvent: Material,
        head_layer_solvent_fraction: float,
        head_layer_area_per_molecule: float,
        head_layer_roughness: float,
        name: str = 'EasySurfactantLayer',
        interface=None,
    ) -> SurfactantLayer:
        """Instance of a surfactant layer where the parameters are known,
        `head_layer` is the hydrophilic part.

        :param tail_layer_molecular_formula: Molecular formula of species constituting the tail layer.
        :param tail_layer_thickness: Thickness of tail layer.
        :param tail_layer_solvent: Solvent in tail layer.
        :param tail_layer_solvent_fraction: Fraction of solvent in tail layer. Fx solvation or surface coverage.
        :param tail_layer_area_per_molecule: Area per molecule of tail layer.
        :param tail_layer_roughness: Roughness of tail layer.
        :param head_layer_molecular_formula: Molecular formula of species constituting the head layer.
        :param head_layer_thickness: Thickness of head layer.
        :param head_layer_solvent: Solvent in head layer.
        :param head_layer_solvent_fraction: Fraction of solvent in head layer. Fx solvation or surface coverage.
        :param head_layer_area_per_molecule: Area per molecule of head layer.
        :param head_layer_roughness: Roughness of head layer.
        :param name: Name for surfactant layer.
        """
        head_layer = LayerAreaPerMolecule.from_pars(
            molecular_formula=head_layer_molecular_formula,
            thickness=head_layer_thickness,
            solvent=head_layer_solvent,
            solvent_fraction=head_layer_solvent_fraction,
            area_per_molecule=head_layer_area_per_molecule,
            roughness=head_layer_roughness,
            name=name + ' Head Layer',
        )
        tail_layer = LayerAreaPerMolecule.from_pars(
            molecular_formula=tail_layer_molecular_formula,
            thickness=tail_layer_thickness,
            solvent=tail_layer_solvent,
            solvent_fraction=tail_layer_solvent_fraction,
            area_per_molecule=tail_layer_area_per_molecule,
            roughness=tail_layer_roughness,
            name=name + ' Tail Layer',
        )
        return cls([tail_layer, head_layer], name, interface)

    @property
    def tail_layer(self) -> Optional[LayerAreaPerMolecule]:
        """Get the tail layer of the surfactant surface."""
        return self.front_layer

    @tail_layer.setter
    def tail_layer(self, layer: LayerAreaPerMolecule) -> None:
        """Set the tail layer of the surfactant surface."""
        self.front_layer = layer

    @property
    def head_layer(self) -> Optional[LayerAreaPerMolecule]:
        """Get the head layer of the surfactant surface."""
        return self.back_layer

    @head_layer.setter
    def head_layer(self, layer: LayerAreaPerMolecule) -> None:
        """Set the head layer of the surfactant surface."""
        self.back_layer = layer

    @property
    def constrain_area_per_molecule(self) -> bool:
        """Get the area per molecule constraint status."""
        return self.tail_layer._area_per_molecule.user_constraints['area_per_molecule'].enabled

    @constrain_area_per_molecule.setter
    def constrain_area_per_molecule(self, status: bool):
        """Set the status for the area per molecule constraint such that the head and tail layers have the
        same area per molecule.

        :param x: Boolean description the wanted of the constraint.
        """
        self.tail_layer._area_per_molecule.user_constraints['area_per_molecule'].enabled = status
        self.tail_layer._area_per_molecule.value = self.tail_layer._area_per_molecule.raw_value

    @property
    def conformal_roughness(self) -> bool:
        """Get the roughness constraint status."""
        return self.tail_layer.roughness.user_constraints['roughness_1'].enabled

    @conformal_roughness.setter
    def conformal_roughness(self, status: bool):
        """Set the status for the roughness to be the same for both layers."""
        if status:
            self._enable_roughness_constraints()
            self.tail_layer.roughness.value = self.tail_layer.roughness.raw_value
        else:
            self._disable_roughness_constraints()

    def constrain_solvent_roughness(self, solvent_roughness: Parameter):
        """Add the constraint to the solvent roughness.

        :param solvent_roughness: The solvent roughness parameter.
        """
        if not self.conformal_roughness:
            raise ValueError('Roughness must be conformal to use this function.')
        solvent_roughness.value = self.tail_layer.roughness.value
        rough = ObjConstraint(solvent_roughness, '', self.tail_layer.roughness)
        self.tail_layer.roughness.user_constraints['solvent_roughness'] = rough

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
            head_layer_thickness_constraint = ObjConstraint(
                self.head_layer.thickness, '', another_contrast.head_layer.thickness
            )
            another_contrast.head_layer.thickness.user_constraints[f'{another_contrast.name}'] = (
                head_layer_thickness_constraint
            )
        if tail_layer_thickness:
            tail_layer_thickness_constraint = ObjConstraint(
                self.tail_layer.thickness, '', another_contrast.tail_layer.thickness
            )
            another_contrast.tail_layer.thickness.user_constraints[f'{another_contrast.name}'] = (
                tail_layer_thickness_constraint
            )
        if head_layer_area_per_molecule:
            head_layer_area_per_molecule_constraint = ObjConstraint(
                self.head_layer._area_per_molecule, '', another_contrast.head_layer._area_per_molecule
            )
            another_contrast.head_layer._area_per_molecule.user_constraints[f'{another_contrast.name}'] = (
                head_layer_area_per_molecule_constraint
            )
        if tail_layer_area_per_molecule:
            tail_layer_area_per_molecule_constraint = ObjConstraint(
                self.tail_layer._area_per_molecule, '', another_contrast.tail_layer._area_per_molecule
            )
            another_contrast.tail_layer._area_per_molecule.user_constraints[f'{another_contrast.name}'] = (
                tail_layer_area_per_molecule_constraint
            )
        if head_layer_fraction:
            head_layer_fraction_constraint = ObjConstraint(
                self.head_layer.material._fraction, '', another_contrast.head_layer.material._fraction
            )
            another_contrast.head_layer.material._fraction.user_constraints[f'{another_contrast.name}'] = (
                head_layer_fraction_constraint
            )
        if tail_layer_fraction:
            tail_layer_fraction_constraint = ObjConstraint(
                self.tail_layer.material._fraction, '', another_contrast.tail_layer.material._fraction
            )
            another_contrast.tail_layer.material._fraction.user_constraints[f'{another_contrast.name}'] = (
                tail_layer_fraction_constraint
            )

    @property
    def _dict_repr(self) -> dict:
        """A simplified dict representation."""
        return {
            self.name: {
                'head_layer': self.head_layer._dict_repr,
                'tail_layer': self.tail_layer._dict_repr,
                'area per molecule constrained': self.constrain_area_per_molecule,
                'conformal roughness': self.conformal_roughness,
            }
        }

    def as_dict(self, skip: list = None) -> dict:
        """Produces a cleaned dict using a custom as_dict method to skip necessary things.
        The resulting dict matches the paramters in __init__

        :param skip: List of keys to skip, defaults to `None`.
        """
        if skip is None:
            skip = []
        this_dict = super().as_dict(skip=skip)
        this_dict['layers']['data'][0] = self.tail_layer
        this_dict['layers']['data'][1] = self.head_layer
        this_dict['constrain_area_per_molecule'] = self.constrain_area_per_molecule
        this_dict['conformal_roughness'] = self.conformal_roughness
        return this_dict
