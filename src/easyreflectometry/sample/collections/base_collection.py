from copy import deepcopy
from typing import List

from easyscience.Objects.Groups import BaseCollection as EasyBaseCollection

from easyreflectometry.parameter_utils import yaml_dump


class BaseCollection(EasyBaseCollection):
    def __init__(
        self,
        name: str,
        interface,
        *args,
        **kwargs,
    ):
        super().__init__(name, *args, **kwargs)
        self.interface = interface

    def __repr__(self) -> str:
        """
        String representation of the collection.

        :return: a string representation of the collection
        """
        return yaml_dump(self._dict_repr)

    @property
    def _dict_repr(self) -> dict:
        """
        A simplified dict representation.

        :return: Simple dictionary
        """
        return {self.name: [i._dict_repr for i in self]}

    def _make_defalut_collection(self, default_collection: List, interface):
        elements = deepcopy(default_collection)
        for element in elements:
            element.interface = interface
        return elements
