from abc import abstractmethod
from typing import Any
from typing import Optional

import yaml
from easyCore.Fitting.Constraints import ObjConstraint
from easyCore.Objects.ObjectClasses import BaseObj

from ..elements.layer_collection import LayerCollection
from ..elements.layers.layer import Layer


class BaseAssembly(BaseObj):
    """Assembly of layers.
    The front layer (front_layer) is the layer the neutron beam starts in, it has an index of 0.
    The back layer (back_layer) is the final layer from which the unreflected neutron beam is transmitted,
    its index number depends on the number of finite layers in the system, but it might be accessed at index -1.
    """

    # Added in super().__init__
    #: Name of the assembly.
    name: str
    #: Layers in the assembly.
    layers: LayerCollection
    #: Interface to the calculator.
    interface: Any

    def __init__(
        self,
        name: str,
        type: str,
        interface,
        **layers: LayerCollection,
    ):
        super().__init__(name=name, **layers)

        # Updates interface using property in base object
        self.interface = interface
        # Type is needed when fitting in EasyCore
        self._type = type
        self._roughness_constraints_setup = False
        self._thickness_constraints_setup = False

    @abstractmethod
    def default(cls, interface=None) -> Any: ...

    @abstractmethod
    def _dict_repr(self) -> dict[str, str]: ...

    @property
    def type(self) -> str:
        """Get type of the assembly.
        Needed by the GUI.
        """
        return self._type

    @property
    def uid(self) -> int:
        """Get UID from the borg map"""
        return self._borg.map.convert_id_to_key(self)

    def __repr__(self) -> str:
        """String representation of the object."""
        return yaml.dump(self._dict_repr, sort_keys=False)

    @property
    def front_layer(self) -> Optional[Layer]:
        """Get the front layer in the assembly."""
        if len(self.layers) == 0:
            return None
        return self.layers[0]

    @front_layer.setter
    def front_layer(self, layer: Layer) -> None:
        """Set the front layer in the assembly.

        :param layer: Layer to set as the front layer.
        """
        if len(self.layers) == 0:
            self.layers.append(layer)
        else:
            self.layers[0] = layer

    @property
    def back_layer(self) -> Optional[None]:
        """Get the back layer in the assembly."""

        if len(self.layers) < 2:
            return None
        return self.layers[-1]

    @back_layer.setter
    def back_layer(self, layer: Layer) -> None:
        """Set the back layer in the assembly.

        :param layer: Layer to set as the back layer.
        """

        if len(self.layers) == 0:
            raise Exception('There is no front layer to add the back layer to. Please add a front layer first.')
        if len(self.layers) == 1:
            self.layers.append(layer)
        else:
            self.layers[-1] = layer

    def _setup_thickness_constraints(self) -> None:
        """
        Setup thickness constraint, front layer is the deciding layer
        """
        for i in range(1, len(self.layers)):
            layer_constraint = ObjConstraint(
                dependent_obj=self.layers[i].thickness,
                operator='',
                independent_obj=self.front_layer.thickness,
            )
            self.front_layer.thickness.user_constraints[f'thickness_{i}'] = layer_constraint
            self.front_layer.thickness.user_constraints[f'thickness_{i}'].enabled = False
        self._thickness_constraints_setup = True

    def _enable_thickness_constraints(self):
        """
        Enable the thickness constraint.
        """
        if self._thickness_constraints_setup:
            # Make sure that the thickness constraint is enabled
            for i in range(1, len(self.layers)):
                self.front_layer.thickness.user_constraints[f'thickness_{i}'].enabled = True
            # Make sure that the thickness parameter is enabled
            for i in range(len(self.layers)):
                self.layers[i].thickness.enabled = True
            self.front_layer.thickness.value = self.front_layer.thickness.raw_value
        else:
            raise Exception('Roughness constraints not setup')

    def _disable_thickness_constraints(self):
        """
        Disable the thickness constraint.
        """
        if self._thickness_constraints_setup:
            for i in range(1, len(self.layers)):
                self.front_layer.thickness.user_constraints[f'thickness_{i}'].enabled = False
        else:
            raise Exception('Roughness constraints not setup')

    def _setup_roughness_constraints(self) -> None:
        """
        Setup roughness constraint, front layer is the deciding layer
        """
        for i in range(1, len(self.layers)):
            layer_constraint = ObjConstraint(
                dependent_obj=self.layers[i].roughness,
                operator='',
                independent_obj=self.front_layer.roughness,
            )
            self.front_layer.roughness.user_constraints[f'roughness_{i}'] = layer_constraint
            self.front_layer.roughness.user_constraints[f'roughness_{i}'].enabled = False
        self._roughness_constraints_setup = True

    def _enable_roughness_constraints(self):
        """
        Enable the roughness constraint.
        """
        if self._roughness_constraints_setup:
            # Make sure that the roughness constraint is enabled
            for i in range(1, len(self.layers)):
                self.front_layer.roughness.user_constraints[f'roughness_{i}'].enabled = True
            # Make sure that the roughness parameter is enabled
            for i in range(len(self.layers)):
                self.layers[i].roughness.enabled = True
            self.front_layer.roughness.value = self.front_layer.roughness.raw_value
        else:
            raise Exception('Roughness constraints not setup')

    def _disable_roughness_constraints(self):
        """
        Disable the roughness constraint.
        """
        if self._roughness_constraints_setup:
            for i in range(1, len(self.layers)):
                self.front_layer.roughness.user_constraints[f'roughness_{i}'].enabled = False
        else:
            raise Exception('Roughness constraints not setup')

    def as_dict(self, skip: list = None) -> dict:
        """Should produce a cleaned dict that matches the paramters in __init__

        :param skip: List of keys to skip, defaults to `None`.
        """
        if skip is None:
            skip = []
        this_dict = super().as_dict(skip=skip)
        return this_dict
