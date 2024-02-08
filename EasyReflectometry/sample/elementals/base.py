from easyCore.Objects.Groups import BaseCollection as BaseGroup
from easyCore.Objects.ObjectClasses import BaseObj


class BaseElemental(BaseObj):
    def __init__(
        self,
        name: str,
        interface,
        **kwargs,
    ):
        super().__init__(name=name, **kwargs)
        self.interface = interface


class BaseCollection(BaseGroup):
    def __init__(
        self,
        name: str,
        interface,
        *args,
        **kwargs,
    ):
        super().__init__(name, *args, **kwargs)
        self.interface = interface
