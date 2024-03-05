from unittest.mock import MagicMock

import pytest

import EasyReflectometry.sample.elements.materials.material_mixture
import EasyReflectometry.sample.elements.materials.material_solvated
from EasyReflectometry.sample.elements.materials.material_solvated import MaterialSolvated


class TestMaterialMixture:
    @pytest.fixture
    def material_solvated(self, monkeypatch) -> MaterialSolvated:
        self.mock_material = MagicMock()
        self.mock_material.name = 'material'
        self.mock_solvent = MagicMock()
        self.mock_solvent.name = 'solvent'
        self.mock_solvation = MagicMock()
        self.mock_interface = MagicMock()
        self.mock_Parameter = MagicMock()
        self.mock_FunctionalConstraint = MagicMock()
        monkeypatch.setattr(EasyReflectometry.sample.elements.materials.material_mixture, 'Parameter', self.mock_Parameter)
        monkeypatch.setattr(
            EasyReflectometry.sample.elements.materials.material_mixture,
            'FunctionalConstraint',
            self.mock_FunctionalConstraint,
        )
        return MaterialSolvated(
            self.mock_material,
            self.mock_solvent,
            self.mock_solvation,
            name='name',
            interface=self.mock_interface,
        )

    def test_init(self, material_solvated: MaterialSolvated) -> None:
        # When Then Expect
        assert material_solvated.material_a == self.mock_material
        assert material_solvated.material_b == self.mock_solvent
        assert material_solvated.fraction == self.mock_solvation
        assert material_solvated.name == 'name'
        assert material_solvated.interface == self.mock_interface
        self.mock_interface.generate_bindings.call_count == 2

    def test_material(self, material_solvated: MaterialSolvated) -> None:
        # When Then Expect
        assert material_solvated.material == self.mock_material

    def test_set_material(self, material_solvated: MaterialSolvated) -> None:
        # When
        new_material = MagicMock()
        new_material.name = 'new_material'

        # Then
        material_solvated.material = new_material

        # Expect
        assert material_solvated.material == new_material
        assert material_solvated.name == 'new_material in solvent'

    def test_solvent(self, material_solvated: MaterialSolvated) -> None:
        # When Then Expect
        assert material_solvated.solvent == self.mock_solvent

    def test_set_solvent(self, material_solvated: MaterialSolvated) -> None:
        # When
        new_solvent = MagicMock()
        new_solvent.name = 'new_solvent'

        # Then
        material_solvated.solvent = new_solvent

        # Expect
        assert material_solvated.solvent == new_solvent
        assert material_solvated.name == 'material in new_solvent'

    def test_solvation(self, material_solvated: MaterialSolvated) -> None:
        # When Then Expect
        assert material_solvated.solvation == self.mock_solvation

    def test_set_solvation(self, material_solvated: MaterialSolvated) -> None:
        # When Then
        material_solvated.solvation = 1.0

        # Expect
        assert material_solvated.solvation == 1.0

    def test_set_solvation_exception(self, material_solvated: MaterialSolvated) -> None:
        # When Then Expect
        with pytest.raises(ValueError):
            material_solvated.solvation = 'not float'

    def test_dict_repr(self, material_solvated: MaterialSolvated) -> None:
        # When Then
        material_solvated._sld = MagicMock()
        material_solvated._sld.raw_value = 1.0
        material_solvated._sld.unit = 'sld_unit'
        material_solvated._isld = MagicMock()
        material_solvated._isld.raw_value = 2.0
        material_solvated._isld.unit = 'isld_unit'
        material_solvated.material._dict_repr = 'material_dict_repr'
        material_solvated.solvent._dict_repr = 'solvent_dict_repr'
        material_solvated.solvation.raw_value = 'solvation_value'

        # Expect
        assert material_solvated._dict_repr == {
            'name': {
                'solvation': 'solvation_value',
                'sld': '1.000e-6 sld_unit',
                'isld': '2.000e-6 isld_unit',
                'material': 'material_dict_repr',
                'solvent': 'solvent_dict_repr',
            }
        }

    def test_update_name(self, material_solvated: MaterialSolvated) -> None:
        # When
        mock_material_a = MagicMock()
        mock_material_a.name = 'name_a'
        material_solvated._material_a = mock_material_a
        mock_material_b = MagicMock()
        mock_material_b.name = 'name_b'
        material_solvated._material_b = mock_material_b

        # Then
        material_solvated._update_name()

        # Expect
        assert material_solvated.name == 'name_a in name_b'
