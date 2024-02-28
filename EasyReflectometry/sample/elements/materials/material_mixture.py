from __future__ import annotations

from copy import deepcopy
from typing import ClassVar

from easyCore.Fitting.Constraints import FunctionalConstraint
from easyCore.Objects.ObjectClasses import Parameter

from EasyReflectometry.special.calculations import weighted_average_sld

from ..base_element import BaseElement
from .material import MATERIAL_DEFAULTS
from .material import Material

MATERIALMIXTURE_DEFAULTS = {
    'fraction': {
        'description': 'The fraction of material b in material a',
        'value': 0.5,
        'units': 'dimensionless',
        'min': 0,
        'max': 1,
        'fixed': True,
    }
}


class MaterialMixture(BaseElement):
    # Added in super().__init__
    fraction: ClassVar[Parameter]

    def __init__(
        self,
        material_a: Material,
        material_b: Material,
        fraction: Parameter,
        name: str = 'EasyMaterialMixture',
        interface=None,
    ):
        """Constructor.

        :param material_a: The first material.
        :param material_b: The second material.
        :param fraction: The fraction of material_b in material_a.
        :param name: Name of the material, defaults to 'EasyMaterialMixture'.
        :param interface: Calculator interface, defaults to :py:attr:`None`.
        """
        if name is None:
            name = material_a.name + '/' + material_b.name
        super().__init__(
            name,
            _material_a=material_a,
            _material_b=material_b,
            fraction=fraction,
            interface=interface,
        )
        sld = weighted_average_sld(self._material_a.sld.raw_value, self._material_b.sld.raw_value, self.fraction.raw_value)
        isld = weighted_average_sld(self._material_a.isld.raw_value, self._material_b.isld.raw_value, self.fraction.raw_value)
        default_options = deepcopy(MATERIAL_DEFAULTS)
        del default_options['sld']['value']
        del default_options['isld']['value']
        self._slds = [
            Parameter('sld', sld, **default_options['sld']),
            Parameter('isld', isld, **default_options['isld']),
        ]
        self._materials_constraints()
        self.interface = interface

    # Class methods for instance creation
    @classmethod
    def default(cls, interface=None) -> MaterialMixture:
        """Default instance for a mixture of two materials."""
        material_a = Material.default()
        material_b = Material.default()
        fraction = Parameter('fraction', **MATERIALMIXTURE_DEFAULTS['fraction'])
        return cls(
            material_a,
            material_b,
            fraction,
            interface=interface,
        )

    @classmethod
    def from_pars(
        cls,
        material_a: Material,
        material_b: Material,
        fraction: float,
        name: str = 'EasyMaterialMixture',
        interface=None,
    ) -> MaterialMixture:
        """Instance of mixture of two materials where the parameters are known.

        :param material_a: The first material.
        :param material_b: The second material.
        :param fraction: The fraction of material_b in material_a.
        :param name: Name of the material, defaults to 'EasyMaterialMixture'.
        :param interface: Calculator interface, defaults to :py:attr:`None`.
        """
        default_options = deepcopy(MATERIALMIXTURE_DEFAULTS)
        del default_options['fraction']['value']
        fraction = Parameter('fraction', fraction, **default_options['fraction'])

        return cls(material_a=material_a, material_b=material_b, fraction=fraction, name=name, interface=interface)

    @property
    def sld(self):
        return self._slds[0]

    @property
    def isld(self):
        return self._slds[1]

    def _get_linkable_attributes(self):
        return self._slds

    def _materials_constraints(self):
        self._slds[0].enabled = True
        self._slds[1].enabled = True
        constraint = FunctionalConstraint(
            self._slds[0], weighted_average_sld, [self._material_a.sld, self._material_b.sld, self.fraction]
        )
        self._material_a.sld.user_constraints['sld'] = constraint
        self._material_b.sld.user_constraints['sld'] = constraint
        self.fraction.user_constraints['sld'] = constraint
        constraint()
        iconstraint = FunctionalConstraint(
            self._slds[1], weighted_average_sld, [self._material_a.isld, self._material_b.isld, self.fraction]
        )
        self._material_a.isld.user_constraints['isld'] = iconstraint
        self._material_b.isld.user_constraints['isld'] = iconstraint
        self.fraction.user_constraints['isld'] = iconstraint
        iconstraint()

    @property
    def material_a(self) -> Material:
        """Getter for material_a."""
        return self._material_a

    @material_a.setter
    def material_a(self, new_material_a: Material) -> None:
        """Setter for material_a

        :param new_material_a: New Material for material_a
        """
        self.name = new_material_a.name + '/' + self._material_b.name
        self._material_a = new_material_a
        self._materials_constraints()
        if self.interface is not None:
            self.interface.generate_bindings(self)

    @property
    def material_b(self) -> Material:
        """Getter for material_b."""
        return self._material_b

    @material_b.setter
    def material_b(self, new_material_b: Material) -> None:
        """Setter for material_b

        :param new_material_b: New Materialfor material_b
        """
        self.name = self._material_a.name + '/' + new_material_b.name
        self._material_b = new_material_b
        self._materials_constraints()
        if self.interface is not None:
            self.interface.generate_bindings(self)

    # Representation
    @property
    def _dict_repr(self) -> dict[str, str]:
        """A simplified dict representation."""
        return {
            self.name: {
                'fraction': self.fraction.raw_value,
                'sld': f'{self.sld.raw_value:.3f}e-6 {self.sld.unit}',
                'isld': f'{self.isld.raw_value:.3f}e-6 {self.isld.unit}',
                'material1': self.material_a._dict_repr,
                'material2': self.material_b._dict_repr,
            }
        }

    def as_dict(self, skip: list = None) -> dict[str, str]:
        """Custom as_dict method to skip necessary things."""
        if skip is None:
            skip = []
        this_dict = super().as_dict(skip=skip)
        this_dict['material_a'] = self._material_a
        this_dict['material_b'] = self._material_b
        return this_dict
