"""
Tests for BaseAssembly class module
"""

from typing import Any
from unittest.mock import MagicMock

import pytest

import easyreflectometry.sample.assemblies.base_assembly
from easyreflectometry.sample.assemblies.base_assembly import BaseAssembly


class TestBaseAssembly:
    @pytest.fixture
    def base_assembly(self) -> BaseAssembly:
        self.mock_layer_0 = MagicMock()
        self.mock_layer_1 = MagicMock()
        self.mock_layers = [self.mock_layer_0, self.mock_layer_1]
        self.mock_interface = MagicMock()
        BaseAssembly.__abstractmethods__ = set()
        return BaseAssembly(
            name='name',
            type='type',
            interface=self.mock_interface,
            layers=self.mock_layers,
        )

    def test_init(self, base_assembly: BaseAssembly) -> None:
        # When Then Expect
        assert base_assembly.name == 'name'
        assert base_assembly._type == 'type'
        assert base_assembly.interface == self.mock_interface
        assert base_assembly.layers == self.mock_layers
        assert base_assembly._roughness_constraints_setup is False
        assert base_assembly._thickness_constraints_setup is False

    def test_setup_thickness_constraints(self, base_assembly: BaseAssembly, monkeypatch: Any) -> None:
        # When
        self.mock_layer_0.thickness = MagicMock()
        self.mock_layer_0.thickness.user_constraints = {}
        self.mock_layer_1.thickness = MagicMock()
        mock_obj_constraint = MagicMock()
        mock_ObjConstraint = MagicMock(return_value=mock_obj_constraint)
        monkeypatch.setattr(easyreflectometry.sample.assemblies.base_assembly, 'ObjConstraint', mock_ObjConstraint)

        # Then
        base_assembly._setup_thickness_constraints()

        # Expect
        assert self.mock_layers[0].thickness.user_constraints['thickness_1'].enabled is False
        assert self.mock_layers[0].thickness.user_constraints['thickness_1'] == mock_obj_constraint
        mock_ObjConstraint.assert_called_once_with(
            dependent_obj=self.mock_layer_1.thickness,
            operator='',
            independent_obj=self.mock_layer_0.thickness,
        )
        assert base_assembly._thickness_constraints_setup is True

    def test_enable_thickness_constraints(self, base_assembly: BaseAssembly) -> None:
        # When
        base_assembly._thickness_constraints_setup = True

        # Then
        base_assembly._enable_thickness_constraints()

        # Expect
        assert self.mock_layer_0.thickness.user_constraints['thickness_1'].enabled is True
        assert self.mock_layer_0.thickness.value == self.mock_layer_0.thickness.raw_value
        assert self.mock_layer_0.thickness.enabled is True
        assert self.mock_layer_1.thickness.enabled is True

    def test_enable_thickness_constraints_exception(self, base_assembly: BaseAssembly) -> None:
        # When
        base_assembly._thickness_constraints_setup = False

        # Then
        with pytest.raises(Exception):
            base_assembly._enable_thickness_constraints()

    def test_disable_thickness_constraints(self, base_assembly: BaseAssembly) -> None:
        # When
        base_assembly._thickness_constraints_setup = True

        # Then
        base_assembly._disable_thickness_constraints()

        # Expect
        assert self.mock_layer_0.thickness.user_constraints['thickness_1'].enabled is False

    def test_setup_roughness_constraints(self, base_assembly: BaseAssembly, monkeypatch: Any) -> None:
        # When
        self.mock_layer_0.roughness = MagicMock()
        self.mock_layer_0.roughness.user_constraints = {}
        self.mock_layer_1.roughness = MagicMock()
        mock_obj_constraint = MagicMock()
        mock_ObjConstraint = MagicMock(return_value=mock_obj_constraint)
        monkeypatch.setattr(easyreflectometry.sample.assemblies.base_assembly, 'ObjConstraint', mock_ObjConstraint)

        # Then
        base_assembly._setup_roughness_constraints()

        # Expect
        assert self.mock_layers[0].roughness.user_constraints['roughness_1'].enabled is False
        assert self.mock_layers[0].roughness.user_constraints['roughness_1'] == mock_obj_constraint
        mock_ObjConstraint.assert_called_once_with(
            dependent_obj=self.mock_layer_1.roughness, operator='', independent_obj=self.mock_layer_0.roughness
        )
        assert base_assembly._roughness_constraints_setup is True

    def test_enable_roughness_constraints(self, base_assembly):
        # When
        base_assembly._roughness_constraints_setup = True

        # Then
        base_assembly._enable_roughness_constraints()

        # Expect
        assert self.mock_layer_0.roughness.user_constraints['roughness_1'].enabled is True
        assert self.mock_layer_0.roughness.value == self.mock_layer_0.roughness.raw_value
        assert self.mock_layer_0.roughness.enabled is True
        assert self.mock_layer_1.roughness.enabled is True

    def test_enable_roughness_constraints_exception(self, base_assembly: BaseAssembly) -> None:
        # When
        base_assembly._roughness_constraints_setup = False

        # Then
        with pytest.raises(Exception):
            base_assembly._enable_roughness_constraints(True)

    def test_disable_roughness_constraints(self, base_assembly: BaseAssembly) -> None:
        # When
        base_assembly._roughness_constraints_setup = True

        # Then
        base_assembly._disable_roughness_constraints()

        # Expect
        assert self.mock_layer_0.roughness.user_constraints['roughness_1'].enabled is False

    def test_front_layer(self, base_assembly: BaseAssembly) -> None:
        # When Then Expect
        assert base_assembly.front_layer == self.mock_layer_0

    def test_front_layer_none(self, base_assembly: BaseAssembly) -> None:
        # When
        base_assembly.layers = []

        # Then
        result = base_assembly.front_layer

        # Expect
        assert result is None

    def test_set_front_layer(self, base_assembly: BaseAssembly) -> None:
        # When Then
        base_assembly.front_layer = self.mock_layer_1

        # Expect
        assert base_assembly.layers == [self.mock_layer_1, self.mock_layer_1]

    def test_set_front_layer_empty(self, base_assembly: BaseAssembly) -> None:
        # When
        base_assembly.layers = []

        # Then
        base_assembly.front_layer = self.mock_layer_1

        # Expect
        assert base_assembly.layers == [self.mock_layer_1]

    def test_back_layer(self, base_assembly: BaseAssembly) -> None:
        # When Then Expect
        assert base_assembly.back_layer == self.mock_layer_1

    def test_back_layer_none(self, base_assembly: BaseAssembly) -> None:
        # When
        base_assembly.layers = []

        # Then
        result = base_assembly.back_layer

        # Expect
        assert result is None

    def test_set_back_layer(self, base_assembly: BaseAssembly) -> None:
        # When Then
        base_assembly.back_layer = self.mock_layer_0

        # Expect
        assert base_assembly.layers == [self.mock_layer_0, self.mock_layer_0]

    def test_set_back_layer_exception(self, base_assembly: BaseAssembly) -> None:
        # When
        base_assembly.layers = []

        # Then
        with pytest.raises(Exception):
            base_assembly.back_layer = self.mock_layer_1

    def test_set_back_layer_with_front(self, base_assembly: BaseAssembly) -> None:
        # When
        base_assembly.layers = [self.mock_layer_0]

        # Then
        base_assembly.back_layer = self.mock_layer_1

        # Expect
        assert base_assembly.layers == [self.mock_layer_0, self.mock_layer_1]
