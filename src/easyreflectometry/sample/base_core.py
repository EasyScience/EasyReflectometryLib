from abc import abstractmethod

import yaml
from easyscience.Objects.ObjectClasses import BaseObj


class BaseCore(BaseObj):
    def __init__(
        self,
        name: str,
        interface,
        **kwargs,
    ):
        super().__init__(name=name, **kwargs)

        # Updates interface using property in base object
        self.interface = interface

    @abstractmethod
    def _dict_repr(self) -> dict[str, str]: ...

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

    # For classes with special serialization needs one must adopt the dict produced by super
    # def as_dict(self, skip: list = None) -> dict:
    #    """Should produce a cleaned dict that matches the parameters in __init__
    #
    #    :param skip: List of keys to skip, defaults to `None`.
    #    """
    #    if skip is None:
    #        skip = []
    #    this_dict = super().as_dict(skip=skip)
    #    ...
    #    Correct the dict here
    #    ...
    #    return this_dict
