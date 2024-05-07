from typing import Any

import yaml
from easyCore.Objects.Groups import BaseCollection

SIZE_DEFAULT_COLLECTION = 2


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
    def uid(self) -> int:
        """
        :return: UID from the borg map
        """
        return self._borg.map.convert_id_to_key(self)

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
        return yaml.dump(self._dict_repr, sort_keys=False)

    @property
    def _dict_repr(self) -> dict:
        """
        A simplified dict representation.

        :return: Simple dictionary
        """
        return {self.name: [i._dict_repr for i in self]}

    @classmethod
    def from_dict(cls, data: dict) -> Any:
        """
        Create an instance of a collection from a dictionary.

        :param data: The dictionary for the collection
        :return: An instance of the collection
        """
        collection = super().from_dict(data)
        # Remove the default elements
        for i in range(SIZE_DEFAULT_COLLECTION):
            del collection[0]
        return collection
