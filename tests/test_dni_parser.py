import logging

import pytest

from dni_calculator import DniParser, Dni


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
            ('1?111111G', Dni(10_111_111, 'G', [1])),
            ('11.1?1.111-E', Dni(11_101_111, 'E', [3])),
            ('11.111.1?1-.X', Dni(11_111_101, 'X', [6])),
            ('11.111.1?1-.?', Dni(11_111_101, None, [6])),
        )
        for valid_dni, expected_dni in VALID_DNIS:
            LOGGER.info(f'Testing "{valid_dni}"')
            dni = self.dni_parser.parse_dni(valid_dni)
            assert dni == expected_dni


if __name__ == '__main__':
    pytest.main()
