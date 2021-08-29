from typing import Union, Iterable, Generator
import itertools

from dni_calculator import Dni, DniParser


class DniCalculator:
    _LETTERS = 'TRWAGMYFPDXBNJZSQVHLCKET'

    def __init__(self):
        self.parser = DniParser()

    def find_letter(self, dni_str: Union[str, int]) -> Dni:
        '''Find the letter corresponding to the given dni

        Examples:
            find_letter 11111111 -> 11111111H
            find_letter 11_111_111 -> 11111111H

        Args:
            dni_str: The dni written as a number
        '''
        dni = self.parser.parse_dni_without_letter(dni_str)
        if dni is None:
            return None
        if dni.missing_digits and len(dni.missing_digits) != 0:
            print(f'Invalid dni given: "{dni_str}". '
                + 'There cannot be missing numbers when finding a letter')
            return None
        dni.letter = self._get_letter(dni.number)
        return dni

    def _get_letter(self, dni_number: int) -> str:
        '''Return the letter corresponding to the given dni_number'''
        return self._LETTERS[dni_number % 23]

    def _check_valid(self, dni: Dni) -> bool:
        '''Check whether the given dni is valid

        Args:
            dni: A Dni with all digits and letter present
                Example: Dni(11_111_111, 'H')
        '''
        return self._get_letter(dni.number) == dni.letter
 
    def find_missing_num(self, dni_str: str) -> Dni:
        '''Find the first complete dni valid for the given dni_str

        Args:
            dni_str: The dni for which to find the missing numbers

                It should have '?' in place of the numbers to find
                
                Examples:
                    11111?11H
                    11_111_?11H
                    11_1?1_111-H
                    11_11?_?11_H

                For further details, see DniParser
        '''
        return next(self.find_all_possible_dnis(dni_str), None)

    def find_all_possible_dnis(self, dni_str: str) -> Generator[Dni, str, None]:
        '''Find the all of the valid dnis for the given dni_str

        Args:
            dni_str: The dni for which to find the missing numbers

                It should have '?' in place of the numbers to find
                
                Examples:
                    11111?11H
                    11_111_?11H
                    11_1?1_111-H
                    11_11?_?11_H

                For further details, see DniParser
        '''
        dni = self.parser.parse_dni(dni_str)
        if dni is None:
            return None

        if dni.letter is None:
            print(f'Cannot fing missing numbers if no letter is given: "{dni_str}"')
            return None

        num_missing_digits = len(dni.missing_digits)
        if num_missing_digits == 0:
            if self._check_valid(dni):
                print(f'The given dni is already complete and valid: "{dni_str}"')
                yield dni
            else:
                print(f'All digits provided. Unable to find missing ones "{dni_str}"')
                return None

        missing_digits = dni.missing_digits
        dni.missing_digits = []
        prev_digits_to_check = 0
        for digits_to_check in self._get_generator_for_digits(missing_digits):
            dni.number -= prev_digits_to_check
            dni.number += digits_to_check
            prev_digits_to_check = digits_to_check
            if self._check_valid(dni):
                yield dni

    def _get_generator_for_digit(self, digit_pos: int) -> Generator[int, int, None]:
        '''Return the different value the digit at position digit_pos can have

        Examples:
            digit_pos=7 -> 0, 1, 2, ..., 8, 9
            digit_pos=6 -> 0, 10, 20, ..., 80, 90
            digit_pos=0 -> 0, 10_000_000, ..., 90_000_000

        Args:
            digit_pos: A number from 0 to 9
        '''
        power = Dni.LENGTH_NUMS_ONLY - digit_pos
        for number in range(0, 10 ** power, 10**(power-1)):
            yield number

    def _get_generator_for_digits(self, digits_pos: Iterable[int]) -> Generator[int, int, None]:
        '''Returns all combinations of values the digits at position digits_pos can have


        Examples:
            digit_pos=(7,) -> 0, 1, 2, ..., 8, 9
            digit_pos=(6,) -> 0, 10, 20, ..., 80, 90
            digit_pos=(0,) -> 0, 10_000_000, ..., 90_000_000
            digit_pos=(6, 7) -> 0, 1, 2, ..., 98, 99
            digit_pos=(5, 7) -> 0, 1, 2, ..., 9, 100, 101, ... 109, 200, ..., 908, 909
            digit_pos=(0, 5) -> 0, 10_000_000, 10_000_100, 10_000_200, ..., 90_000_900

        Args:
            digits_pos: An iterable whose values have to be between 0 and 9
                For the output to be in an expectable order, the iterable
                has to return the numbers in increasing order.

                For example, if digits_pos=(7, 6), the yielded values will be:
                0, 10, 20, 30, ... 90, 1, 11, 21, ... 
        '''
        digits_generators = [self._get_generator_for_digit(digit_pos)
                             for digit_pos in digits_pos]
        digits_generator = itertools.product(*digits_generators)
        # return digits_generator
        return map(sum, digits_generator)
