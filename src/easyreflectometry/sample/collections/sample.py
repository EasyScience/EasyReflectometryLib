from __future__ import annotations

__author__ = 'github.com/arm61'

from typing import List
from typing import Union

from easyscience.Objects.Groups import BaseCollection

from easyreflectometry.parameter_utils import yaml_dump

from ..assemblies.base_assembly import BaseAssembly
from ..assemblies.multilayer import Multilayer
from ..elements.layers.layer import Layer

NR_DEFAULT_ASSEMBLIES = 2


class Sample(BaseCollection):
    """Collection of assemblies that represent the sample for which experimental measurements exist."""

    assemblies: List[BaseAssembly]

    def __init__(
        self,
        *list_assembly_like: list[Union[Layer, BaseAssembly]],
        name: str = 'EasySample',
        interface=None,
        populate_if_none: bool = True,
        **kwargs,
    ):
        """Constructor.

        :param args: The assemblies in the sample.
        :param name: Name of the sample, defaults to 'EasySample'.
        :param interface: Calculator interface, defaults to `None`.
        """
        assemblies = []
        if not list_assembly_like:
            if populate_if_none:
                list_assembly_like = [Multilayer(interface=interface) for _ in range(NR_DEFAULT_ASSEMBLIES)]
            else:
                list_assembly_like = []
        # Needed to ensure an empty list is created when saving and instatiating the object as_dict -> from_dict
        # Else collisions might occur in global_object.map
        self.populate_if_none = False

        for assembly_like in list_assembly_like:
            if issubclass(type(assembly_like), Layer):
                assemblies.append(Multilayer(assembly_like, name=assembly_like.name))
            elif issubclass(type(assembly_like), BaseAssembly):
                assemblies.append(assembly_like)
            else:
                raise ValueError('The items must be either a Layer or an Assembly.')
        super().__init__(name, *assemblies, **kwargs)
        self.interface = interface

    def remove_assmbly(self, index: int):
        """Remove the assembly at given index from the sample.

        :param index: Index of the assembly to remove.
        """
        self._enable_changes_to_outermost_layers()
        self.assemblies.remove(index)
        self._disable_changes_to_outermost_layers()

    @property
    def superphase(self) -> Layer:
        """The superphase of the sample."""
        return self.assemblies[0].front_layer

    @property
    def subphase(self) -> Layer:
        """The superphase of the sample."""
        return self.assemblies[1].back_layer

    def _enable_changes_to_outermost_layers(self):
        """Allowed to change the outermost layers of the sample.
        Superphase can change thickness and roughness.
        Subphase can change thickness.
        """
        self.superphase.thickness.enabled = True
        self.superphase.roughness.enabled = True
        self.subphase.thickness.enabled = True

    def _disable_changes_to_outermost_layers(self):
        """No allowed to change the outermost layers of the sample.
        Superphase can change thickness and roughness.
        Subphase can change thickness.
        """
        self.superphase.thickness.enabled = False
        self.superphase.roughness.enabled = False
        self.subphase.thickness.enabled = False

    # Representation
    @property
    def _dict_repr(self) -> dict:
        """A simplified dict representation."""
        return {self.name: [i._dict_repr for i in self]}

    def __repr__(self) -> str:
        """String representation of the sample."""
        return yaml_dump(self._dict_repr)

    def as_dict(self, skip: list = None) -> dict:
        """Produces a cleaned dict using a custom as_dict method to skip necessary things.
        The resulting dict matches the parameters in __init__

        :param skip: List of keys to skip, defaults to `None`.
        """
        if skip is None:
            skip = []
        this_dict = super().as_dict(skip=skip)
        for i, assembly in enumerate(self.data):
            this_dict['data'][i] = assembly.as_dict(skip=skip)
        this_dict['populate_if_none'] = self.populate_if_none
        return this_dict
