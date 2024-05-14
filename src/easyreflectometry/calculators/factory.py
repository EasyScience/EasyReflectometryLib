__author__ = 'github.com/wardsimon'

from easyscience.Objects.Inferface import InterfaceFactoryTemplate

from easyreflectometry.calculators import CalculatorBase


class CalculatorFactory(InterfaceFactoryTemplate):
    def __init__(self):
        super().__init__(interface_list=CalculatorBase._calculators)

    def reset_storage(self) -> None:
        return self().reset_storage()

    def sld_profile(self, model_id: str) -> tuple:
        return self().sld_profile(model_id)
