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

    def test_find_letter_invalid_input(self):
        INVALID_DNIS = (
            # Invalid length tests
            '',
            '1111111',
            '11_111.11',
            '11-111.111-as',
            '11.111.11-.',

            # Invalid letter tests
            '11111111!',
            '11.111.111-=',
            '11.111.111-.1',
            '11_111-111-.1',

             # Invalid digits tests
            '1X111111G',
            '11.1F1.111-E',
            '11.111.1F1-.1',

             # Letter provided
            '11111111G',
            '11.111.111-E',
            '11.111.111-.1',
        )

        for invalid_dni in INVALID_DNIS:
            assert self.dni_calc.find_letter(invalid_dni) is None

    def test_find_letter(self):
        expected_dni = Dni(['1', '1', '1', '1', '1', '1', '1', '1'], 'H')
        assert self.dni_calc.find_letter('11_111_111') == expected_dni

    def test_find_missing_num(self):
        expected_dni = Dni(['1', '1', '1', '1', '1', '1', '1', '1'], 'H')
        assert self.dni_calc.find_missing_num('11_111_?11H') == expected_dni

    def test_find_missing_num_more_than_one_missing_num(self):
        for dni in self.generate_dnis_with_missing_numbers():
            LOGGER.info(f'Testing {dni}')
            assert self.dni_calc.find_missing_num(dni) is not None

    def test_find_missing_num_invalid_input(self):
        INVALID_DNIS = (
            # Invalid length tests
            '',
            '1111111',
            '1111111111',
            '11_111.111',
            '11-111.1111-as',
            '11.111.111-.',

            # Invalid letter tests
            '1111?111!',
            '11.1?1.111-=',
            '11.11?.111-.1',
            '11_111-??1-.1',

            # Invalid digits tests
            '1X111111G',
            '11.1F1.111-E',
            '11.111.1F1-.1',

             # All digits provided
            '11111111G',
            '11.111.111-E',
            '11.111.111-.1',
        )

        for invalid_dni in INVALID_DNIS:
            assert self.dni_calc.find_missing_num(invalid_dni) is None

    def test_find_missing_num_valid_dni_provided(self):
        expected_dni = Dni(['1', '1', '1', '1', '1', '1', '1', '1'], 'H')
        assert self.dni_calc.find_missing_num('11_111_111-H') == expected_dni

    def test_find_all_possible_dnis(self):
        for dni_to_test in self.generate_dnis_with_missing_numbers(max_missing_numbers=6):
            LOGGER.info(f'Testing {dni_to_test}')
            found_dnis = 0
            for dni in self.dni_calc.find_all_possible_dnis(dni_to_test):
                found_dnis += 1
                assert dni is not None
            assert found_dnis >= 1


    def generate_dnis_with_missing_numbers(self, max_missing_numbers=Dni.LENGTH_NUMS_ONLY):
        for i in range(max_missing_numbers + 1):
            dni = '?'*i + '1'*(Dni.LENGTH_NUMS_ONLY-i) + 'H'
            yield dni


if __name__ == '__main__':
    pytest.main()