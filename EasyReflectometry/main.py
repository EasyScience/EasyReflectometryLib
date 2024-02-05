from EasyReflectometry.calculators import CalculatorFactory


def main():
    calculator = CalculatorFactory()
    print(f'Available calculators: {calculator.available_interfaces}')


if __name__ == '__main__':
    main()
