from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class Dni:
    LENGTH_NUMS_ONLY = 8
    LENGTH = LENGTH_NUMS_ONLY + 1

    number: Optional[int] = None
    letter: Optional[str] = None
    missing_digits: List[int] = field(default_factory=lambda: [])

    def get_number_as_str(self) -> str:
        '''Return the number representing unknown digits as "?"

        For example, if number=11_011_111 and missing_digits=[2], 
        returned value is "11?11111"
        '''
        number = self.number if self.number is not None else 0
        number_as_str = str(number).zfill(Dni.LENGTH_NUMS_ONLY)

        # number is converted to list so that missing digits can be replaced
        number_as_list = list(number_as_str)
        if self.missing_digits:
            for missing_digit in self.missing_digits:
                number_as_list[missing_digit] = '?'

        return ''.join(number_as_list)

    def get_letter_as_str(self) -> str:
        '''Return the letter or "?" if lettter is not known'''
        return self.letter if self.letter else '?'

    def __str__(self):
        return self.get_number_as_str() + self.get_letter_as_str()
