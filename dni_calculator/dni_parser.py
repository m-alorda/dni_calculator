from typing import Union

from dni_calculator import Dni

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

        dni_number_str = dni_str[:-1]
        missing_digits = []
        for i, digit in enumerate(dni_number_str):
            if digit == self.UNKNOWN_DIGIT:
                missing_digits.append(i)
            elif not digit.isdigit():
                print(f'Invalid dni: "{dni_str}". Invalid number: "{digit}"')
                return None
        dni.missing_digits = missing_digits
        dni.number = int(dni_number_str.replace(self.UNKNOWN_DIGIT, '0'))

        return dni
