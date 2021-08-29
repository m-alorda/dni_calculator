from typing import Generator
import logging

import pytest

from dni_calculator import DniCalculatorProxy, Dni
from tests import utils


LOGGER = logging.getLogger()


class TestDniCalculatorProxy:

    INVALID_DNIS = (
        # Invalid length tests
        '',
        '1111111',
        '1111111111',
        '11_111.1111-a',
        '11-111.1111-as',
        '11.111.111-1.',

        # Invalid letter tests
        '1111?111!',
        '11.1?1.111-=',
        '11.11?.111-.1',
        '11_111-??1-.1',

        # Invalid digits tests
        '1X111111G',
        '11.1F1.111-E',
        '11.111.1F1-.1',
    )

    INVALID_DNIS_FIND_LETTER = INVALID_DNIS + (
        # Letter provided
        '11111111G',
        '11.111.111-E',
        '11.111.111-.1',

        # Missing numbers
        '11111?11',
        '1111111??',
        '11.11?.111-',
        '11.111.??1-.',
        '11_??1-111-.',
    )

    INVALID_DNIS_MISSING_NUM = INVALID_DNIS + (
        # All digits provided
        '11_111.111'
        '11111111G',
        '11.111.111-E',
        '11.111.111-.1',

        # Missing letter
        '11_111.1?1?',
    )

    dni_calc = DniCalculatorProxy()

    def test_find_letter_invalid_input(self):
        for invalid_dni in self.INVALID_DNIS_FIND_LETTER:
            LOGGER.info(f'Testing dni: "{invalid_dni}"')
            assert self.dni_calc.find_letter(invalid_dni) is None

    def test_find_letter(self):
        expected_dni = Dni(11_111_111, 'H')
        assert self.dni_calc.find_letter('11_111_111') == expected_dni

    def test_find_missing_num(self):
        expected_dni = Dni(11_111_111, 'H')
        assert self.dni_calc.find_missing_num('11_111_?11H') == expected_dni

    def test_find_missing_num_more_than_one_missing_num(self):
        for dni in self._generate_dnis_with_missing_numbers():
            LOGGER.info(f'Testing {dni}')
            assert self.dni_calc.find_missing_num(dni) is not None

    def test_find_missing_num_invalid_input(self):
        for invalid_dni in self.INVALID_DNIS_MISSING_NUM:
            LOGGER.info(f'Testing "{invalid_dni}"')
            assert self.dni_calc.find_missing_num(invalid_dni) is None

    def test_find_missing_num_valid_dni_provided(self):
        expected_dni = Dni(11_111_111, 'H')
        assert self.dni_calc.find_missing_num('11_111_111-H') == expected_dni

    def test_find_all_possible_dnis_invalid_input(self):
        for invalid_dni in self.INVALID_DNIS_MISSING_NUM:
            LOGGER.info(f'Testing "{invalid_dni}"')
            assert next(self.dni_calc.find_all_possible_dnis(invalid_dni), None) is None

    def test_find_all_possible_dnis(self):
        self.test_find_all_possible_dnis_slow(max_missing_numbers=5)

    @pytest.mark.slow
    def test_find_all_possible_dnis_slow(self, max_missing_numbers=Dni.LENGTH_NUMS_ONLY):
        for dni_to_test in self._generate_dnis_with_missing_numbers(max_missing_numbers):
            LOGGER.info(f'Testing {dni_to_test}')
            found_dnis = 0
            for dni in self.dni_calc.find_all_possible_dnis(dni_to_test):
                LOGGER.debug(f'Found dni is {dni}')
                assert dni is not None
                found_dnis += 1
            assert found_dnis >= 1

    def test_find_all_possible_dnis_valid_dni_provided(self):
        expected_dni = Dni(11_111_111, 'H')
        assert utils.compare_iterables(
            self.dni_calc.find_all_possible_dnis('11_111_111-H'),
            (expected_dni,)
        )

    def _generate_dnis_with_missing_numbers(self, 
                                            max_missing_numbers: int = Dni.LENGTH_NUMS_ONLY
                                           ) -> Generator[str, None, None]:
        for i in range(max_missing_numbers + 1):
            dni = '?'*i + '1'*(Dni.LENGTH_NUMS_ONLY-i) + 'H'
            yield dni


if __name__ == '__main__':
    pytest.main()
