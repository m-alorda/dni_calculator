from typing import Union

from dni_calculator import Dni

class DniParser:
    UNKNOWN_DIGIT = '?'
    IGNORED_CHARS = '_-.'

    def parse_dni_without_letter(self, dni_str: Union[str, int, float]) -> Dni:
        '''Transform a string representation of a dni (without letter) to a Dni

        See parse_dni for allowed input
        '''
        dni_str = self._pre_parse(dni_str)

        if len(dni_str) != Dni.LENGTH_NUMS_ONLY:
            print(f'Invalid dni: "{dni_str}". '
                + f'Should contain {Dni.LENGTH_NUMS_ONLY} numbers')
            return None

        return self._parse(dni_str + self.UNKNOWN_DIGIT)

    def parse_dni(self, dni_str: Union[str, int, float]) -> Dni:
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
        dni_str = self._pre_parse(dni_str)

        if len(dni_str) != Dni.LENGTH:
            print(f'Invalid dni: "{dni_str}". '
                + f'Should be {Dni.LENGTH} characters long, including the letter')
            return None

        return self._parse(dni_str) 

    def _pre_parse(self, dni_str: Union[str, int, float]) -> str:
        '''Removes IGNORED_CHARS from dni_str and cast to str if needed'''
        if type(dni_str) is int or type(dni_str) is float:
            dni_str = str(dni_str)

        if type(dni_str) is not str:
            print(f'Invalid dni received: "{dni_str}"')
            return ''

        for ignored_char in self.IGNORED_CHARS:
            dni_str = dni_str.replace(ignored_char, '')

        return dni_str

    def _parse(self, dni_str: str) -> Dni:
        '''Does the actual parsing as described in parse_dni

        Args:
            dni_str: An str exactly Dni.LENGTH characters long not 
                containing any of IGNORED_CHARS
        '''
        dni = Dni()

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
