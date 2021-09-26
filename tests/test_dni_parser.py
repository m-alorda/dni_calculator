import logging

import pytest

from dni_calculator import DniParser, Dni, DniParseException


LOGGER = logging.getLogger()


class TestDniParser:
    dni_parser = DniParser()

    INVALID_DNIS = (
        # Invalid length tests
        "",
        "111111",
        "11-111.111-as",
        # Invalid letter tests
        "11111111!",
        "11.111.111-=",
        "11.111.111-.1",
        "11_111-111-.1",
        # Invalid digits tests
        "1X111111G",
        "11.1F1.111-E",
        "11.111.1F1-.1",
        # Invalid types
        1111,
        1.111,
        [1, 1, 1, 1, 1, 1, 1, 1, "H"],
        {"dni": "11_111_111-H"},
    )

    def test_parse_dni_invalid_dnis(self):
        INVALID_DNIS = self.INVALID_DNIS + (
            # Invalid length tests
            "11111111",
            "11_111.111",
            "11.111.111-.",
        )
        for invalid_dni in INVALID_DNIS:
            LOGGER.info(f'testing "{invalid_dni}"')
            with pytest.raises(DniParseException):
                self.dni_parser.parse_dni(invalid_dni)

    def test_parse_dni_without_letter_invalid_dnis(self):
        INVALID_DNIS = self.INVALID_DNIS + (
            # Invalid length tests
            "11_111.11",
            "11.111.11-.",
        )
        for invalid_dni in INVALID_DNIS:
            LOGGER.info(f'testing "{invalid_dni}"')
            with pytest.raises(DniParseException):
                self.dni_parser.parse_dni_without_letter(invalid_dni)

    def test_parse_dni_valid_dnis(self):
        VALID_DNIS = (
            ("12345678g", Dni(12_345_678, "G")),
            ("1?111111G", Dni(10_111_111, "G", [1])),
            ("11.1?1.111-E", Dni(11_101_111, "E", [3])),
            ("11.111.1?1-.X", Dni(11_111_101, "X", [6])),
            ("11.111.1?1-.?", Dni(11_111_101, None, [6])),
            (47968698j, Dni(47_968_698, "J")),
        )
        for valid_dni, expected_dni in VALID_DNIS:
            LOGGER.info(f'Testing "{valid_dni}"')
            dni = self.dni_parser.parse_dni(valid_dni)
            assert dni == expected_dni

    def test_parse_dni_without_letters_valid_dnis(self):
        VALID_DNIS = (
            ("12345678", Dni(12_345_678)),
            ("1?111111", Dni(10_111_111, None, [1])),
            ("11.1?1.111-", Dni(11_101_111, None, [3])),
            ("11.111.1?1-.", Dni(11_111_101, None, [6])),
            ("11.111.1?1-.", Dni(11_111_101, None, [6])),
            (47968698, Dni(47_968_698)),
        )
        for valid_dni, expected_dni in VALID_DNIS:
            LOGGER.info(f'Testing "{valid_dni}"')
            dni = self.dni_parser.parse_dni_without_letter(valid_dni)
            assert dni == expected_dni


if __name__ == "__main__":
    pytest.main()
