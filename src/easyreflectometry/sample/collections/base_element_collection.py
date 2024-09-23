from copy import deepcopy
from typing import List
from typing import Optional

from easyscience.Objects.Groups import BaseCollection

from easyreflectometry.parameter_utils import yaml_dump


class BaseElementCollection(BaseCollection):
    def __init__(
        self,
        name: str,
        interface,
        *args,
        **kwargs,
    ):
        super().__init__(name, *args, **kwargs)
        self.interface = interface

    @property
    def names(self) -> list:
        """
        :returns: list of names for the elements in the collection.
        """
        return [i.name for i in self]

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

    def as_dict(self, skip: Optional[List[str]] = None) -> dict:
        """
        Create a dictionary representation of the collection.

        :return: A dictionary representation of the collection
        """
        this_dict = super().as_dict(skip=skip)
        this_dict['data'] = []
        for collection_element in self:
            this_dict['data'].append(collection_element.as_dict(skip=skip))
        return this_dict

    def _make_defalut_collection(self, default_collection: List, interface):
        elements = deepcopy(default_collection)
        for element in elements:
            element.interface = interface
        return elements
