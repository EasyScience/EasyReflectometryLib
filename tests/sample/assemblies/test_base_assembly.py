from unittest.mock import MagicMock

import EasyReflectometry.sample.assemblies.base_assembly
from EasyReflectometry.sample.assemblies.base_assembly import apply_thickness_constraints


def test_apply_thickness_constraints(monkeypatch):
    # When 
    mock_layer_0 = MagicMock()
    mock_layer_0.thickness = MagicMock()
    mock_layer_0.thickness.user_constraints = {}
    mock_layer_1 = MagicMock()
    layers = [mock_layer_0, mock_layer_1]
    mock_layer_1.thickness = MagicMock()
    mock_obj_constraint = MagicMock()
    mock_ObjConstraint = MagicMock(return_value=mock_obj_constraint)
    monkeypatch.setattr(EasyReflectometry.sample.assemblies.base_assembly, 'ObjConstraint', mock_ObjConstraint)

    #Then
    apply_thickness_constraints(layers)

    #Expect
    assert mock_layer_0.thickness.enabled is True
    assert mock_layer_1.thickness.enabled is True
    assert layers[0].thickness.user_constraints['thickness_1'].enabled is True
    assert layers[0].thickness.user_constraints['thickness_1'] == mock_obj_constraint
    mock_ObjConstraint.assert_called_once_with(dependent_obj=mock_layer_1.thickness, operator='', independent_obj=mock_layer_0.thickness)