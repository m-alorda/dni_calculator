from typing import List, Union

from dni_calculator import Dni, DniException


class DniParser:

    UNKNOWN_DIGIT = "?"
    IGNORED_CHARS = "_-."

    def parse_dni_without_letter(self, dni_str: Union[str, int, float, complex]) -> Dni:
        """Transform a string representation of a dni (without letter) to a Dni

        See parse_dni for allowed input

        Raises:
            DniParseException: if an invalid dni_str is given
        """
        dni_str = self._pre_parse(dni_str)
        if not dni_str:
            raise DniParseException(dni_str, "Is empty")

        if len(dni_str) != Dni.LENGTH_NUMS_ONLY:
            raise DniParseException(
                dni_str, f"Should contain {Dni.LENGTH_NUMS_ONLY} numbers"
            )

        return self._parse(dni_str + self.UNKNOWN_DIGIT)

    def parse_dni(self, dni_str: Union[str, int, float, complex]) -> Dni:
        """Tranform a string representation of a dni to a Dni

        Args:
            dni_str: Valid dni representations are as follows:
                11111?11H
                11_111_?11H
                11_1?1_111-H
                11_11?_?11_H
                11.111.?11.H
                11-111-?11-H
                11-111-?11-?

        Raises:
            DniParseException: if an invalid dni_str is given
        """
        dni_str = self._pre_parse(dni_str)
        if not dni_str:
            raise DniParseException(dni_str, "Is empty")

        if len(dni_str) != Dni.LENGTH:
            raise DniParseException(
                dni_str, f"Should be {Dni.LENGTH} characters long, including the letter"
            )

        return self._parse(dni_str)

    def _pre_parse(self, dni_str: Union[str, int, float, complex]) -> str:
        """Removes IGNORED_CHARS from dni_str and cast to str if needed

        Raises:
            DniParseException: if an invalid dni_str is given
        """
        if type(dni_str) in (int, float, complex):
            dni_str = str(dni_str)

        if type(dni_str) is not str:
            raise DniParseException(str(dni_str), f"Unexpected data type: {type(dni_str)}")

        for ignored_char in self.IGNORED_CHARS:
            dni_str = dni_str.replace(ignored_char, "")

        return dni_str

    def _parse(self, dni_str: str) -> Dni:
        """Does the actual parsing as described in parse_dni

        Args:
            dni_str: An str exactly Dni.LENGTH characters long not
                containing any of IGNORED_CHARS

        Raises:
            DniParseException: if an invalid dni_str is given
        """
        dni = Dni()

        dni.letter = dni_str[-1].upper()
        if dni.letter == self.UNKNOWN_DIGIT:
            dni.letter = None
        elif not dni.letter.isalpha():
            raise DniParseException(dni_str, f'Invalid letter: "{dni.letter}"')

        dni_number_str = dni_str[:-1]
        missing_digits : List[int] = list()
        for i, digit in enumerate(dni_number_str):
            if digit == self.UNKNOWN_DIGIT:
                missing_digits.append(i)
            elif not digit.isdigit():
                raise DniParseException(dni_str, f'Invalid number: "{digit}"')
        dni.missing_digits = missing_digits
        dni.number = int(dni_number_str.replace(self.UNKNOWN_DIGIT, "0"))

        return dni


class DniParseException(DniException):
    """Exception parsing a Dni from an str"""

    def __init__(self, dni_str: str, msg: str) -> None:
        super().__init__(f'Invalid dni: "{dni_str}". {msg}')
