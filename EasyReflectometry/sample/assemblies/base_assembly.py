from abc import abstractmethod
from typing import Any

import yaml
from easyCore.Objects.ObjectClasses import BaseObj


class BaseAssembly(BaseObj):
    def __init__(
        self,
        name: str,
        interface,
        **kwargs,
    ):
        super().__init__(name=name, **kwargs)
        self.interface = interface

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
