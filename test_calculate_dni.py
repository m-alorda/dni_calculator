from typing import Optional
import logging

import pytest

from calculate_dni import DniParser, Dni, DniCalculator

LOGGER = logging.getLogger()


class TestDniParser:
    dni_parser = DniParser()

    def test_parse_dni_invalid_dnis(self):
        INVALID_DNIS = (
            # Invalid length tests
            '',
            '11111111',
            '11_111.111',
            '11-111.111-as',
            '11.111.111-.',

            # Invalid letter tests
            '11111111!',
            '11.111.111-=',
            '11.111.111-.1',
            '11_111-111-.1',

             # Invalid digits tests
            '1X111111G',
            '11.1F1.111-E',
            '11.111.1F1-.1',
        )

        for invalid_dni in INVALID_DNIS:
            LOGGER.info(f'testing "{invalid_dni}"')
            assert self.dni_parser.parse_dni(invalid_dni) is None

    def test_parse_dni_valid_dnis(self):
        VALID_DNIS = (
            ('1?111111G', Dni(['1', None, '1', '1', '1', '1', '1', '1'], 'G')),
            ('11.1?1.111-E', Dni(['1', '1', '1', None, '1', '1', '1', '1'], 'E')),
            ('11.111.1?1-.X', Dni(['1', '1', '1', '1', '1', '1', None, '1'], 'X')),
            ('11.111.1?1-.?', Dni(['1', '1', '1', '1', '1', '1', None,  '1'], None)),
        )
        for valid_dni, expected_dni in VALID_DNIS:
            LOGGER.info(f'Testing "{valid_dni}"')
            dni = self.dni_parser.parse_dni(valid_dni)
            assert dni == expected_dni



class TestDniCalculator:
    dni_calc = DniCalculator()

    def test_find_letter(self):
        assert self.dni_calc.find_letter('11_111_111') == Dni(['1', '1', '1', '1', '1', '1', '1', '1'], 'H')

    def test_find_missing_num(self):
        assert self.dni_calc.find_missing_num('11_111_?11H') == Dni(['1', '1', '1', '1', '1', '1', '1', '1'], 'H')


if __name__ == '__main__':
    pytest.main()