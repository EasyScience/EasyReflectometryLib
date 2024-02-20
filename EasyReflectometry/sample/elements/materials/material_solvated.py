from easyCore.Objects.ObjectClasses import Parameter

from .material import Material
from .material_mixture import MaterialMixture


class MaterialSolvated(MaterialMixture):
    def __init__(
        self,
        material: Material,
        solvent: Material,
        solvation: Parameter,
        name=None,
        interface=None,
    ):
        super().__init__(
            material_a=material,
            material_b=solvent,
            fraction=solvation,
            name=name,
            interface=interface,
        )
        if name is None:
            self._update_name()

    @property
    def material(self) -> Material:
        """
        :return: the material.
        """
        return self._material_a

    @material.setter
    def material(self, new_material: Material) -> None:
        """
        Setter for material

        :param new_material: Matrerial
        """
        # Should set the property
        self.material_a = new_material
        self._update_name()

    @property
    def solvent(self) -> Material:
        """
        :return: the solvent.
        """
        return self._material_b

    @solvent.setter
    def solvent(self, new_solvent: Material) -> None:
        """
        Setter for solvent

        :param solvent: Matrerial
        """
        # Should set the property
        self.material_b = new_solvent
        self._update_name()

    @property
    def solvation(self) -> Parameter:
        """
        :return: the solvation.
        """
        return self.fraction

    @solvation.setter
    def solvation(self, solvation: float) -> None:
        """
        Setter for solvation

        :param solvation: float
        """
        try:
            self.fraction = solvation
        except ValueError:
            raise ValueError('solvation must be a float')

    def _update_name(self) -> None:
        self.name = self._material_a.name + ' solvated in ' + self._material_b.name

    # Representation
    @property
    def _dict_repr(self) -> dict[str, str]:
        """
        A simplified dict representation.

        :return: Simple dictionary
        """
        return {
            self.name: {
                'solvation': self.solvation.raw_value,
                'sld': f'{self._sld.raw_value:.3f}e-6 {self._sld.unit}',
                'isld': f'{self._isld.raw_value:.3f}e-6 {self._isld.unit}',
                'material': self.material._dict_repr,
                'solvent': self.solvent._dict_repr,
            }
        }
