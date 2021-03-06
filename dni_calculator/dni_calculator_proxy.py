from typing import Union, Generator, Optional

from dni_calculator import Dni, DniParser, DniCalculator, DniException


class DniCalculatorProxy:
    def __init__(self):
        self.parser = DniParser()
        self.dni_calc = DniCalculator()

    def find_letter(self, dni_str: Union[str, int]) -> Optional[Dni]:
        """Find the letter corresponding to the given dni

        Examples:
            find_letter 11111111 -> 11111111H
            find_letter 11_111_111 -> 11111111H

        Args:
            dni_str: The dni written as a number
        """
        try:
            dni = self.parser.parse_dni_without_letter(dni_str)
            return self.dni_calc.find_letter(dni)
        except DniException as e:
            print(e)
            return None

    def find_missing_num(self, dni_str: str) -> Optional[Dni]:
        """Find the first complete dni valid for the given dni_str

        Args:
            dni_str: The dni for which to find the missing numbers

                It should have '?' in place of the numbers to find

                Examples:
                    11111?11H
                    11_111_?11H
                    11_1?1_111-H
                    11_11?_?11_H

                For further details, see DniParser
        """
        return next(self.find_all_possible_dnis(dni_str), None)

    def find_all_possible_dnis(self, dni_str: str) -> Generator[Dni, None, None]:
        """Find the all of the valid dnis for the given dni_str

        Args:
            dni_str: The dni for which to find the missing numbers

                It should have '?' in place of the numbers to find

                Examples:
                    11111?11H
                    11_111_?11H
                    11_1?1_111-H
                    11_11?_?11_H

                For further details, see DniParser
        """
        try:
            dni = self.parser.parse_dni(dni_str)
            yield from self.dni_calc.find_all_possible_dnis(dni)
        except DniException as e:
            print(e)
            return None
