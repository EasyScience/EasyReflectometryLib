__author__ = "github.com/wardsimon"

import numpy as np
from abc import ABCMeta, abstractmethod

from easyCore import borg
from easyCore.Objects.core import ComponentSerializer


class InterfaceTemplate(ComponentSerializer, metaclass=ABCMeta):
    """
    This class is a template and defines all properties that an interface should have.
    """
    _interfaces = []
    _borg = borg
    _link = {}

    def __init_subclass__(cls, is_abstract: bool = False, **kwargs):
        """
        Initialise all subclasses so that they can be created in the factory

        :param is_abstract: Is this a subclass which shouldn't be dded
        :type is_abstract: bool
        :param kwargs: key word arguments
        :type kwargs: dict
        :return: None
        :rtype: noneType
        """
        super().__init_subclass__(**kwargs)
        if not is_abstract:
            cls._interfaces.append(cls)

    @abstractmethod
    def reset_storage(self) -> None:
        """
        Reset the storage for the calculator.
        """
        pass

    @abstractmethod
    def fit_func(self, x_array: np.ndarray, model_id: str) -> np.ndarray:
        """
        Function to perform a fit

        :param x_array: points to be calculated at
        :param model_id: the model id
        :return: calculated points
        """
        pass

    @abstractmethod
    def sld_profile(self, model_id: str) -> tuple:
        """
        :param model_id: the model id
        """
        pass