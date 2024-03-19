from __future__ import annotations

from copy import deepcopy

from easyCore.Objects.ObjectClasses import Parameter

from .material import Material
from .material_mixture import MaterialMixture

MATERIAL_SOLVATED_DETAILS = {
    'solvent_fraction': {
        'description': 'Fraction of solvent in layer.',
        'value': 0.2,
        'units': 'dimensionless',
        'min': 0,
        'max': 1,
        'fixed': True,
    },
}


class MaterialSolvated(MaterialMixture):
    def __init__(
        self,
        material: Material,
        solvent: Material,
        solvent_fraction: Parameter,
        name=None,
        interface=None,
    ):
        """Constructor.

        :param material: The material being solvated.
        :param solvent: The solvent material.
        :param solvent_fraction: Fraction of solvent in layer. E.g. solvation or surface coverage.
        :param name: Name of the material, defaults to None that causes the name to be constructed.
        :param interface: Calculator interface, defaults to `None`.
        """
        # In super class, the fraction is the fraction of material b in material a
        super().__init__(
            material_a=material,
            material_b=solvent,
            fraction=solvent_fraction,
            name=name,
            interface=interface,
        )
        if name is None:
            self._update_name()

    # Class methods for instance creation
    @classmethod
    def default(cls, interface=None) -> MaterialSolvated:
        """A default instance for layer defined from molecule formula and area per molecule.

        :param interface: Calculator interface, defaults to `None`.
        """
        solvent_fraction = Parameter('solvent_fraction', **MATERIAL_SOLVATED_DETAILS['solvent_fraction'])
        material = Material.from_pars(6.36, 0, 'D2O', interface=interface)
        solvent = Material.from_pars(-0.561, 0, 'H2O', interface=interface)
        return cls(
            material=material,
            solvent=solvent,
            solvent_fraction=solvent_fraction,
            interface=interface,
        )

    @classmethod
    def from_pars(
        cls,
        material: Material,
        solvent: Material,
        solvent_fraction: float,
        name: str = 'EasyMaterialSolvated',
        interface=None,
    ) -> MaterialSolvated:
        """An instance for a layer described with the area per molecule, where the parameters are known.

        :param material: Material in the layer.
        :param solvent: Solvent in the layer.
        :param solvent_fraction: Fraction of solvent in layer. Fx solvation or surface coverage.
        :param name: Identifier, defaults to 'EasyMaterialSolvated'.
        :param interface: Calculator interface, defaults to `None`.
        """
        default_options = deepcopy(MATERIAL_SOLVATED_DETAILS)
        del default_options['solvent_fraction']['value']
        solvent_fraction = Parameter('coverage', solvent_fraction, **default_options['solvent_fraction'])

        return cls(
            material=material,
            solvent=solvent,
            solvent_fraction=solvent_fraction,
            name=name,
            interface=interface,
        )

    @property
    def material(self) -> Material:
        """Get material."""
        return self._material_a

    @material.setter
    def material(self, new_material: Material) -> None:
        """Set the material.

        :param new_material: Matrerial to be useed.
        """
        self.material_a = new_material

    @property
    def solvent(self) -> Material:
        """Get solvent."""
        return self._material_b

    @solvent.setter
    def solvent(self, new_solvent: Material) -> None:
        """Set the solvent.

        :param new_solvent: Solvent to be used.
        """
        self.material_b = new_solvent

    @property
    def solvent_fraction(self) -> Parameter:
        """Get the fraction of layer described by the solvent.
        This might be fraction of:
        Solvation where solvent is within the layer
        Patches of solvent in the layer where no material is present.
        """
        return self.fraction

    @solvent_fraction.setter
    def solvent_fraction(self, solvent_fraction: float) -> None:
        """Set the fraction of layer covered by the material.
        This might be fraction of:
        Solvation where solvent is within the layer
        Patches of solvent in the layer where no material is present.

        :param solvent_fraction : Fraction of layer described by the solvent.
        """
        try:
            self.fraction = solvent_fraction
            if solvent_fraction < 0 or solvent_fraction > 1:
                raise ValueError('solvent_fraction must be between 0 and 1')
        except ValueError:
            raise ValueError('solvent_fraction must be a float between 0 and 1')

    def _update_name(self) -> None:
        self.name = self._material_a.name + ' in ' + self._material_b.name

    # Representation
    @property
    def _dict_repr(self) -> dict[str, str]:
        """A simplified dict representation."""
        return {
            self.name: {
                'solvent_fraction': self.solvent_fraction.raw_value,
                'sld': f'{self._sld.raw_value:.3f}e-6 {self._sld.unit}',
                'isld': f'{self._isld.raw_value:.3f}e-6 {self._isld.unit}',
                'material': self.material._dict_repr,
                'solvent': self.solvent._dict_repr,
            }
        }
