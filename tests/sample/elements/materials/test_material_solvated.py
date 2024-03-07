from unittest.mock import MagicMock

import pytest

import EasyReflectometry.sample.elements.materials.material_mixture
import EasyReflectometry.sample.elements.materials.material_solvated
from EasyReflectometry.sample.elements.materials.material_solvated import MaterialSolvated


class TestMaterialSolvated:
    @pytest.fixture
    def material_solvated(self, monkeypatch) -> MaterialSolvated:
        self.mock_material = MagicMock()
        self.mock_material.name = 'material'
        self.mock_solvent = MagicMock()
        self.mock_solvent.name = 'solvent'
        self.mock_solvent_fraction = MagicMock()
        self.mock_solvent_fraction.raw_value = 0.1
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
            material=self.mock_material,
            solvent=self.mock_solvent,
            solvent_fraction=self.mock_solvent_fraction,
            name='name',
            interface=self.mock_interface,
        )

    def test_init(self, material_solvated: MaterialSolvated) -> None:
        # When Then Expect
        assert material_solvated.material_a == self.mock_material
        assert material_solvated.material_b == self.mock_solvent
        assert material_solvated.fraction == self.mock_solvent_fraction
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

    def test_solvent_fraction(self, material_solvated: MaterialSolvated) -> None:
        # When Then Expect
        assert material_solvated.solvent_fraction == self.mock_solvent_fraction

    def test_set_solvent_fraction(self, material_solvated: MaterialSolvated) -> None:
        # When Then
        material_solvated.solvent_fraction = 1.0

        # Expect
        assert material_solvated.solvent_fraction == 1.0

    def test_set_solvent_fraction_exception(self, material_solvated: MaterialSolvated) -> None:
        # When Then Expect
        with pytest.raises(ValueError):
            material_solvated.solvent_fraction = 'not float'

        with pytest.raises(ValueError):
            material_solvated.solvent_fraction = 1.1

        with pytest.raises(ValueError):
            material_solvated.solvent_fraction = -0.1

        # When Then Expect (no exception)
        material_solvated.solvent_fraction = 0.0

        # When Then Expect (no exception)
        material_solvated.solvent_fraction = 1.0

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
        material_solvated.solvent_fraction.raw_value = 'solvent_fraction_value'

        # Expect
        assert material_solvated._dict_repr == {
            'name': {
                'solvent_fraction': 'solvent_fraction_value',
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
