from typing import Iterable
import logging

import pytest

from dni_calculator import DniCalculator, Dni


LOGGER = logging.getLogger()


class TestDniCalculator:
    
    DIGIT_TESTS = (
        (7, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]),
        (6, [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]),
        (5, [0, 100, 200, 300, 400, 500, 600, 700, 800, 900]),
        (3, [0, 10_000, 20_000, 30_000, 40_000, 50_000, 60_000, 70_000, 80_000, 90_000]),
        (0, [0, 10_000_000, 20_000_000, 30_000_000, 40_000_000, 50_000_000, 60_000_000, 70_000_000, 80_000_000, 90_000_000])
    )

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

    dni_calc = DniCalculator()

    def test__get_generator_for_digit(self):
        for digit_pos, expected_numbers in self.DIGIT_TESTS:
            LOGGER.info(f'Testing digit_pos {digit_pos}')
            numbers = self.dni_calc._get_generator_for_digit(digit_pos)
            LOGGER.info(f'Generated numbers are: {numbers}')
            assert self._get_iterable_length(numbers) == 10
            assert self._compare_iterables(numbers, expected_numbers)

    def test__get_generator_for_digits_single_digits(self):
        for digit_pos, expected_numbers in self.DIGIT_TESTS:
            self.do_test_get_generator_for_digits((digit_pos,), expected_numbers)

    def test__get_generator_for_digits_secuential_numbers(self):
        self.test__get_generator_for_digits_secuential_numbers(largest_digit=5)

    @pytest.mark.slow
    def test__get_generator_for_digits_secuential_numbers(self, largest_digit=Dni.LENGTH_NUMS_ONLY):
        for start_pos in range(1, largest_digit+1):
            digits_pos = range(Dni.LENGTH_NUMS_ONLY-start_pos, 
                               Dni.LENGTH_NUMS_ONLY)
            expected_numbers = range(10 ** start_pos)
            self.do_test_get_generator_for_digits(digits_pos, expected_numbers)

    def test__get_generator_for_digits(self):
        digits_pos = (3, 6)
        expected_numbers = [
            0, 10, 20, 30, 40, 50, 60, 70, 80, 90,
            10_000, 10_010, 10_020, 10_030, 10_040, 10_050, 10_060, 10_070, 10_080, 10_090,
            20_000, 20_010, 20_020, 20_030, 20_040, 20_050, 20_060, 20_070, 20_080, 20_090,
            30_000, 30_010, 30_020, 30_030, 30_040, 30_050, 30_060, 30_070, 30_080, 30_090,
            40_000, 40_010, 40_020, 40_030, 40_040, 40_050, 40_060, 40_070, 40_080, 40_090,
            50_000, 50_010, 50_020, 50_030, 50_040, 50_050, 50_060, 50_070, 50_080, 50_090,
            60_000, 60_010, 60_020, 60_030, 60_040, 60_050, 60_060, 60_070, 60_080, 60_090,
            70_000, 70_010, 70_020, 70_030, 70_040, 70_050, 70_060, 70_070, 70_080, 70_090,
            80_000, 80_010, 80_020, 80_030, 80_040, 80_050, 80_060, 80_070, 80_080, 80_090,
            90_000, 90_010, 90_020, 90_030, 90_040, 90_050, 90_060, 90_070, 90_080, 90_090,
        ]
        self.do_test_get_generator_for_digits(digits_pos, expected_numbers)

    def do_test_get_generator_for_digits(self, digits_pos: Iterable[int], expected_numbers: Iterable[int]):
        LOGGER.info(f'Testing digits_pos {digits_pos}')
        numbers = self.dni_calc._get_generator_for_digits(digits_pos)
        LOGGER.info(f'Generated numbers are: {numbers}')
        assert self._get_iterable_length(numbers) == self._get_iterable_length(expected_numbers)
        assert self._compare_iterables(numbers, expected_numbers)

    def _get_iterable_length(self, iterable: Iterable):
        count = 0
        for _ in iterable:
            count +=1
        return count

    def _compare_iterables(self, iterable1: Iterable, iterable2: Iterable):
        for x1, x2 in zip(iterable1, iterable1):
            if x1 != x2:
                return False
        return True

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
        self.test_find_all_possible_dnis(max_missing_numbers=5)

    @pytest.mark.slow
    def test_find_all_possible_dnis(self, max_missing_numbers=Dni.LENGTH_NUMS_ONLY):
        for dni_to_test in self._generate_dnis_with_missing_numbers(max_missing_numbers):
            LOGGER.info(f'Testing {dni_to_test}')
            found_dnis = 0
            for dni in self.dni_calc.find_all_possible_dnis(dni_to_test):
                found_dnis += 1
                assert dni is not None
            assert found_dnis >= 1

    def _generate_dnis_with_missing_numbers(self, max_missing_numbers=Dni.LENGTH_NUMS_ONLY):
        for i in range(max_missing_numbers + 1):
            dni = '?'*i + '1'*(Dni.LENGTH_NUMS_ONLY-i) + 'H'
            yield dni


if __name__ == '__main__':
    pytest.main()
