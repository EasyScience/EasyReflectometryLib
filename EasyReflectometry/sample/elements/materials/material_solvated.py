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
        """Constructor.

        :param material: The material being solvated.
        :param solvent: The solvent material.
        :param solvation: The fraction of the solvent in the material.
        :param name: Name of the material, defaults to None that causes the name to be constructed.
        :param interface: Calculator interface, defaults to :py:attr:`None`.
        """
        super().__init__(
            material_a=material,
            material_b=solvent,
            fraction=solvation,
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
        # Should set the property
        self.material_b = new_solvent

    @property
    def solvation(self) -> Parameter:
        """Get solvation fraction."""
        return self.fraction

    @solvation.setter
    def solvation(self, solvation: float) -> None:
        """Set solvation fraction.

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
        """A simplified dict representation."""
        return {
            self.name: {
                'solvation': self.solvation.raw_value,
                'sld': f'{self._sld.raw_value:.3f}e-6 {self._sld.unit}',
                'isld': f'{self._isld.raw_value:.3f}e-6 {self._isld.unit}',
                'material': self.material._dict_repr,
                'solvent': self.solvent._dict_repr,
            }
        }
