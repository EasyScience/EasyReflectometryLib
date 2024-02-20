from __future__ import annotations

from copy import deepcopy

from easyCore.Fitting.Constraints import FunctionalConstraint
from easyCore.Objects.ObjectClasses import Parameter

from EasyReflectometry.special.calculations import weighted_average

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
    _material_a: Material
    _material_b: Material
    _fraction: Parameter

    def __init__(
        self,
        material_a: Material,
        material_b: Material,
        fraction: Parameter,
        name=None,
        interface=None,
    ):
        if name is None:
            name = material_a.name + '/' + material_b.name
        super().__init__(
            name,
            _material_a=material_a,
            _material_b=material_b,
            _fraction=fraction,
            interface=interface,
        )
        sld = weighted_average(
            a=self._material_a.sld.raw_value,
            b=self._material_b.sld.raw_value,
            p=self._fraction.raw_value,
        )
        isld = weighted_average(
            a=self._material_a.isld.raw_value,
            b=self._material_b.isld.raw_value,
            p=self._fraction.raw_value,
        )
        default_options = deepcopy(MATERIAL_DEFAULTS)
        del default_options['sld']['value']
        del default_options['isld']['value']

        self._sld = Parameter('sld', sld, **default_options['sld'])
        self._isld = Parameter('isld', isld, **default_options['isld'])

        self._materials_constraints()
        self.interface = interface

    def _get_linkable_attributes(self):
        return [self._sld, self._isld]

    @property
    def sld(self):
        return self._sld

    @property
    def isld(self):
        return self._isld

    def _materials_constraints(self):
        self._sld.enabled = True
        self._isld.enabled = True
        constraint = FunctionalConstraint(
            dependent_obj=self._sld,
            func=weighted_average,
            independent_objs=[self._material_a.sld, self._material_b.sld, self._fraction],
        )
        self._material_a.sld.user_constraints['sld'] = constraint
        self._material_b.sld.user_constraints['sld'] = constraint
        self._fraction.user_constraints['sld'] = constraint
        constraint()
        iconstraint = FunctionalConstraint(
            dependent_obj=self._isld,
            func=weighted_average,
            independent_objs=[self._material_a.isld, self._material_b.isld, self._fraction],
        )
        self._material_a.isld.user_constraints['isld'] = iconstraint
        self._material_b.isld.user_constraints['isld'] = iconstraint
        self._fraction.user_constraints['isld'] = iconstraint
        iconstraint()

    @property
    def fraction(self) -> Parameter:
        """
        :return: the fraction of material a.
        """
        return self._fraction

    @fraction.setter
    def fraction(self, fraction: float) -> None:
        """
        Setter for fraction of material a.

        :param fraction: double
        """
        if not isinstance(fraction, float):
            raise ValueError('fraction must be a float')
        self._fraction = fraction

    @property
    def material_a(self) -> Material:
        """
        :return: the first material.
        """
        return self._material_a

    @material_a.setter
    def material_a(self, new_material_a: Material) -> None:
        """
        Setter for material_a

        :param new_material_a: New material_a
        """
        self.name = new_material_a.name + '/' + self._material_b.name
        self._material_a = new_material_a
        self._materials_constraints()
        if self.interface is not None:
            self.interface.generate_bindings(self)

    @property
    def material_b(self) -> Material:
        """
        :return: the second material.
        """
        return self._material_b

    @material_b.setter
    def material_b(self, new_material_b: Material) -> None:
        """
        Setter for material_b

        :param new_material_b: New material_b
        """
        self.name = self._material_a.name + '/' + new_material_b.name
        self._material_b = new_material_b
        self._materials_constraints()
        if self.interface is not None:
            self.interface.generate_bindings(self)

    # Class constructors
    @classmethod
    def default(cls, interface=None) -> MaterialMixture:
        """
        Default constructor for a mixture of two materials.

        :return: Default material mixture container.
        """
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
        name=None,
        interface=None,
    ) -> MaterialMixture:
        """
        Constructor of a mixture of two materials where the parameters are known.

        :param material_a: The first material
        :param material_b: The second material
        :param fraction: The fraction of material_b in material_a
        :return: MaterialMixture container.
        """
        default_options = deepcopy(MATERIALMIXTURE_DEFAULTS)
        del default_options['fraction']['value']
        fraction = Parameter('fraction', fraction, **default_options['fraction'])

        return cls(
            material_a=material_a,
            material_b=material_b,
            fraction=fraction,
            name=name,
            interface=interface,
        )

    # Representation
    @property
    def _dict_repr(self) -> dict[str, str]:
        """
        A simplified dict representation.

        :return: Simple dictionary
        """
        return {
            self.name: {
                'fraction': self._fraction.raw_value,
                'sld': f'{self._sld.raw_value:.3f}e-6 {self._sld.unit}',
                'isld': f'{self._isld.raw_value:.3f}e-6 {self._isld.unit}',
                'material_a': self._material_a._dict_repr,
                'material_b': self._material_b._dict_repr,
            }
        }

    def as_dict(self, skip: list = None) -> dict[str, str]:
        """
        Custom as_dict method to skip necessary things.

        :return: Cleaned dictionary.
        """
        if skip is None:
            skip = []
        this_dict = super().as_dict(skip=skip)
        this_dict['material_a'] = self._material_a
        this_dict['material_b'] = self._material_b
        return this_dict
