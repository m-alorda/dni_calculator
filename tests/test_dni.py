import pytest

from dni_calculator import Dni


class TestDni:

    def test_get_number_as_str(self):
        dni = Dni(11_111_111)
        assert dni.get_number_as_str() == '11111111'

    def test_get_number_as_str_missing_num(self):
        dni = Dni(11_011_111, missing_digits=[2])
        assert dni.get_number_as_str() == '11?11111'

    def test_get_number_as_str_zero_padding(self):
        dni = Dni(1_011_111)
        assert dni.get_number_as_str() == '01011111'

    def test_get_letter_as_str(self):
        dni = Dni(letter='a')
        assert dni.get_letter_as_str() == 'A'

    def test_get_letter_as_str_missing_letter(self):
        dni = Dni()
        assert dni.get_letter_as_str() == '?'

    def test_str(self):
        dni = Dni(11_111_111, 'H')
        assert str(dni) == '11111111H'

    def test_from_dni(self):
        dni = Dni(11_111_110, 'H', missing_digits=[7])
        copied_dni = Dni.from_dni(dni)
        assert dni == copied_dni
        assert id(dni) != id(copied_dni)
        assert id(dni.missing_digits) != id(copied_dni.missing_digits)


if __name__ == '__main__':
    pytest.main()
