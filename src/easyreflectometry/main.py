from easyreflectometry.calculators import CalculatorFactory


def main():
    factory = CalculatorFactory()
    print(f'Available calculators: {factory.available_interfaces}')


if __name__ == '__main__':
    main()
