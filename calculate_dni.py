from typing import Generator, Optional, List, Union
from dataclasses import dataclass
import itertools

import fire


@dataclass
class Dni:
    LENGTH_NUMS_ONLY = 8
    LENGTH = LENGTH_NUMS_ONLY + 1

    digits: List[Optional[str]]
    letter: Optional[str]

    def __init__(self, digits=None, letter=None):
        self.digits = (digits
            if digits is not None
            else [None for _ in range(Dni.LENGTH_NUMS_ONLY)])
        self.letter = letter

    def get_number(self) -> int:
        return int(self.get_number_as_str())

    def get_number_as_str(self) -> str:
        return ''.join(self.digits)

    def __str__(self):
        return ''.join(self.digits) + self.letter


class DniParser:
    UNKNOWN_DIGIT = '?'
    IGNORED_CHARS = '_-.'

    def parse_dni_without_letter(self, dni_str: Union[str, int]) -> Dni:
        '''Transform a string representation of a dni (without letter) to a Dni

        See parse_dni for allowed input
        '''
        if type(dni_str is int):
            dni_str = str(dni_str)
        dni = self.parse_dni(dni_str + self.UNKNOWN_DIGIT)

        return dni

    def parse_dni(self, dni_str: str) -> Dni:
        '''Tranform a string representation of a dni to a Dni

        Args:
            dni_str: Valid dni representations are as follows:
                11111?11H
                11_111_?11H
                11_1?1_111-H
                11_11?_?11_H
                11.111.?11.H
                11-111-?11-H
                11-111-?11-?
        '''
        for ignored_char in self.IGNORED_CHARS:
            dni_str = dni_str.replace(ignored_char, '')
    
        dni = Dni()

        if len(dni_str) != Dni.LENGTH:
            print(f'Invalid dni: "{dni_str}". '
                + f'Should be {Dni.LENGTH} characters long, including the letter')
            return None

        dni.letter = dni_str[-1]
        if dni.letter == self.UNKNOWN_DIGIT:
            dni.letter = None
        elif not dni.letter.isalpha():
            print(f'Invalid dni: "{dni_str}". Invalid letter: "{dni.letter}"')
            return None

        for i, digit in enumerate(dni_str[:-1]):
            if digit == self.UNKNOWN_DIGIT:
                digit = None
            elif not digit.isdigit():
                print(f'Invalid dni: "{dni_str}". Invalid number: "{digit}"')
                return None
            else:
                dni.digits[i] = digit

        return dni


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
        dni.letter = self._get_letter(dni.get_number())
        return dni

    def _get_letter(self, dni_number: int) -> str:
        return self._LETTERS[dni_number % 23]

    def _check_valid(self, dni: Dni) -> bool:
        '''Check whether the given dni is valid

        Args:
            dni: A Dni with all digits and letter present
                Example: Dni(['1', '1', '1', '1', '1', '1', '1', '1'], 'H')
        '''
        return self._get_letter(dni.get_number()) == dni.letter
 
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

        if dni.letter == None:
            print(f'Cannot fing missing numbers if no letter is given: "{dni_str}"')
            return None

        missing_digits_pos = [i for i, digit in enumerate(dni.digits) if digit is None]
        num_missing_digits = len(missing_digits_pos)
        if num_missing_digits == 0:
            if self._check_valid(dni):
                print(f'The given dni is already complete and valid: "{dni_str}"')
                yield dni
            else:
                print(f'All digits provided. Unable to find missing ones "{dni_str}"')
                return None

        for attempt in range(10 ** num_missing_digits):
            # Get the digits in attempt as a list
            missing_digits_attempt = list(str(attempt).zfill(num_missing_digits))
            for missing_pos, missing_digits_attempt \
                    in zip(missing_digits_pos, missing_digits_attempt):
                dni.digits[missing_pos] = missing_digits_attempt
            if self._check_valid(dni):
                yield dni


def main():
    fire.Fire(DniCalculator)


if __name__ == '__main__':
    main()
