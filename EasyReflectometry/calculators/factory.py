__author__ = 'github.com/wardsimon'

from easyCore.Objects.Inferface import InterfaceFactoryTemplate

from EasyReflectometry.calculators import CalculatorBase


class CalculatorFactory(InterfaceFactoryTemplate):
    def __init__(self):
        super(CalculatorFactory, self).__init__(CalculatorBase._interfaces)

    def reset_storage(self) -> None:
        return self().reset_storage()

    def sld_profile(self, model_id: str) -> tuple:
        return self().sld_profile(model_id)
