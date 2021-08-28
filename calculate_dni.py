from typing import Generator, Optional, List
from dataclasses import dataclass

import fire


@dataclass
class Dni:
    digits: List[Optional[str]]
    letter: Optional[str]

    def __init__(self, digits=None, letter=None):
        self.digits = (digits
            if digits is not None
            else [None for _ in range(DniParser.ID_LENGTH_NUMS_ONLY)])
        self.letter = letter

    def get_number(self) -> int:
        return int(''.join(self.digits))

    def __str__(self):
        return ''.join(self.digits) + self.letter


class DniParser:
    ID_LENGTH_NUMS_ONLY = 8
    ID_LENGTH = ID_LENGTH_NUMS_ONLY + 1

    UNKNOWN_DIGIT = '?'
    IGNORED_CHARS = '_-.'

    def parse_dni_without_letter(self, dni_str: str) -> Dni:
        '''Transform a string representation of a dni (without letter) to a Dni

        See parse_dni for allowed input
        '''
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

        if len(dni_str) != self.ID_LENGTH:
            print(f'Invalid dni: "{dni_str}". '
                + f'Should be {self.ID_LENGTH} characters long, including the letter')
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
                print(f'')
                return None
            else:
                dni.digits[i] = digit

        return dni


class DniCalculator:
    _LETTERS = 'TRWAGMYFPDXBNJZSQVHLCKET'

    def __init__(self):
        self.parser = DniParser()

    def find_letter(self, dni_str: int) -> str:
        '''Find the letter corresponding to the given dni

        Examples:
            find_letter 11111111 -> 11111111H
            find_letter 11_111_111 -> 11111111H

        Args:
            dni_str: The dni written as a number
        '''
        dni = self.parser.parse_dni_without_letter(dni_str)
        if dni is None:
            return
        return str(dni_str) + self._LETTERS[dni.get_number() % 23]
        

    def find_missing_num(self, dni_str: str) -> str:
        '''Find the first complete dni valdni for the given dni

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
            return

    def find_all_possible_dnis(self, dni: str) -> Generator[str, str, None]:
        yield


def main():
    fire.Fire(DniCalculator)


if __name__ == '__main__':
    main()