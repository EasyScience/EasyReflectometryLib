from abc import abstractmethod
from typing import Any

import yaml
from easyCore.Fitting.Constraints import ObjConstraint
from easyCore.Objects.ObjectClasses import BaseObj

from ..elements.layer_collection import LayerCollection
from ..elements.layers.layer import Layer


class BaseAssembly(BaseObj):
    # Added in super().__init__
    name: str
    layers: LayerCollection
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
        self._type = type
        self._roughness_constraints_setup = False
        self._thickness_constraints_setup = False

    @abstractmethod
    def default(cls, interface=None) -> Any:
        ...

    @abstractmethod
    def _dict_repr(self) -> dict[str, str]:
        ...

    @property
    def uid(self) -> int:
        """
        :return: UID from the borg map
        """
        return self._borg.map.convert_id_to_key(self)

    def __repr__(self) -> str:
        """
        String representation of the layer.

        :return: a string representation of the layer
        :rtype: str
        """
        return yaml.dump(self._dict_repr, sort_keys=False)

    @property
    def top_layer(self) -> Layer:
        """
        :return: The top layer
        """
        return self.layers[0]

    @top_layer.setter
    def top_layer(self, layer: Layer) -> None:
        """
        Setter for the top layer
        """
        self.layers[0] = layer

    @property
    def bottom_layer(self) -> Layer:
        """
        :return: The bottom layer
        """
        return self.layers[-1]

    @bottom_layer.setter
    def bottom_layer(self, layer: Layer) -> None:
        """
        Setter for the bottom layer
        """
        self.layers[-1] = layer

    def _setup_thickness_constraints(self) -> None:
        """
        Setup thickness constraint, top layer is the deciding layer
        """
        for i in range(1, len(self.layers)):
            layer_constraint = ObjConstraint(
                dependent_obj=self.layers[i].thickness,
                operator='',
                independent_obj=self.top_layer.thickness,
            )
            self.top_layer.thickness.user_constraints[f'thickness_{i}'] = layer_constraint
            self.top_layer.thickness.user_constraints[f'thickness_{i}'].enabled = False
        self._thickness_constraints_setup = True

    def _enable_thickness_constaints(self):
        """
        Enable the thickness constraint.
        """
        if self._thickness_constraints_setup:
            # Make sure that the thickness constraint is enabled
            for i in range(1, len(self.layers)):
                self.top_layer.thickness.user_constraints[f'thickness_{i}'].enabled = True
            # Make sure that the thickness parameter is enabled
            for i in range(len(self.layers)):
                self.layers[i].thickness.enabled = True
            self.top_layer.thickness.value = self.top_layer.thickness.raw_value
        else:
            raise Exception('Roughness constraints not setup')

    def _disable_thickness_constaints(self):
        """
        Disable the thickness constraint.
        """
        if self._thickness_constraints_setup:
            for i in range(1, len(self.layers)):
                self.top_layer.thickness.user_constraints[f'thickness_{i}'].enabled = False
        else:
            raise Exception('Roughness constraints not setup')

    def _setup_roughness_constraints(self) -> None:
        """
        Setup roughness constraint, top layer is the deciding layer
        """
        for i in range(1, len(self.layers)):
            layer_constraint = ObjConstraint(
                dependent_obj=self.layers[i].roughness,
                operator='',
                independent_obj=self.top_layer.roughness,
            )
            self.top_layer.roughness.user_constraints[f'roughness_{i}'] = layer_constraint
            self.top_layer.roughness.user_constraints[f'roughness_{i}'].enabled = False
        self._roughness_constraints_setup = True

    def _enable_roughness_constaints(self):
        """
        Enable the roughness constraint.
        """
        if self._roughness_constraints_setup:
            # Make sure that the roughness constraint is enabled
            for i in range(1, len(self.layers)):
                self.top_layer.roughness.user_constraints[f'roughness_{i}'].enabled = True
            # Make sure that the roughness parameter is enabled
            for i in range(len(self.layers)):
                self.layers[i].roughness.enabled = True
            self.top_layer.roughness.value = self.top_layer.roughness.raw_value
        else:
            raise Exception('Roughness constraints not setup')

    def _disable_roughness_constaints(self):
        """
        Disable the roughness constraint.
        """
        if self._roughness_constraints_setup:
            for i in range(1, len(self.layers)):
                self.top_layer.roughness.user_constraints[f'roughness_{i}'].enabled = False
        else:
            raise Exception('Roughness constraints not setup')
