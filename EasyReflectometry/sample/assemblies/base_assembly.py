from abc import abstractmethod
from typing import Any

import yaml
from easyCore.Fitting.Constraints import ObjConstraint
from easyCore.Objects.ObjectClasses import BaseObj

from ..elements.layer_collection import LayerCollection
from ..elements.layers.layer import Layer


class BaseAssembly(BaseObj):
    layers: LayerCollection

    def __init__(
        self,
        name: str,
        type: str,
        interface,
        **layers: LayerCollection,
    ):
        super().__init__(name=name, **layers)

        # interface is define in the base object
        self.interface = interface
        self._type = type

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


def apply_thickness_constraints(layers: list[Layer]) -> None:
    """
    Add thickness constraint, layer 0 is the deciding layer
    """
    for i in range(1, len(layers)):
        layers[i].thickness.enabled = True
        layer_constraint = ObjConstraint(
            dependent_obj=layers[i].thickness,
            operator='',
            independent_obj=layers[0].thickness,
        )
        layers[0].thickness.user_constraints[f'thickness_{i}'] = layer_constraint
        layers[0].thickness.user_constraints[f'thickness_{i}'].enabled = True

    layers[0].thickness.enabled = True
