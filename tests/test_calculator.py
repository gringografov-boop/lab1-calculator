import pytest
from src.calculator import Calculator


class TestCalculator:
    def setup_method(self):
        self.calc = Calculator()

    def test_addition(self):
        assert self.calc.calculate("2 + 3") == 5.0
        assert self.calc.calculate("10 + 20") == 30.0
        assert self.calc.calculate("0 + 0") == 0.0

    def test_subtraction(self):
        assert self.calc.calculate("5 - 3") == 2.0
        assert self.calc.calculate("10 - 20") == -10.0

    def test_multiplication(self):
        assert self.calc.calculate("3 * 4") == 12.0
        assert self.calc.calculate("2.5 * 4") == 10.0

    def test_division(self):
        assert self.calc.calculate("12 / 3") == 4.0
        assert self.calc.calculate("10 / 4") == 2.5

    def test_power(self):
        assert self.calc.calculate("2 ** 3") == 8.0
        assert self.calc.calculate("5 ** 2") == 25.0

    def test_floor_division(self):
        assert self.calc.calculate("10 // 3") == 3.0
        assert self.calc.calculate("15 // 4") == 3.0

    def test_modulo(self):
        assert self.calc.calculate("10 % 3") == 1.0
        assert self.calc.calculate("15 % 4") == 3.0

    def test_unary_minus(self):
        assert self.calc.calculate("-5") == -5.0
        assert self.calc.calculate("-(-5)") == 5.0
        assert self.calc.calculate("-5 + 3") == -2.0

    def test_unary_plus(self):
        assert self.calc.calculate("+5") == 5.0
        assert self.calc.calculate("+5 - 3") == 2.0

    def test_operator_precedence(self):
        assert self.calc.calculate("2 + 3 * 4") == 14.0
        assert self.calc.calculate("10 - 6 / 2") == 7.0

    def test_right_associativity(self):
        assert self.calc.calculate("2 ** 3 ** 2") == 512.0

    def test_parentheses(self):
        assert self.calc.calculate("(2 + 3) * 4") == 20.0
        assert self.calc.calculate("2 * (3 + 4)") == 14.0

    def test_nested_parentheses(self):
        assert self.calc.calculate("((2 + 3) * 4)") == 20.0
        assert self.calc.calculate("(2 * (3 + 4))") == 14.0

    def test_decimal_numbers(self):
        assert self.calc.calculate("1.5 + 2.5") == 4.0
        assert self.calc.calculate("3.14 * 2") == 6.28

    def test_leading_dot_numbers(self):
        assert self.calc.calculate(".5 + 1") == 1.5
        assert self.calc.calculate("2 * .25") == 0.5

    def test_division_by_zero(self):
        with pytest.raises(ZeroDivisionError):
            self.calc.calculate("5 / 0")
        with pytest.raises(ZeroDivisionError):
            self.calc.calculate("10 // 0")
        with pytest.raises(ZeroDivisionError):
            self.calc.calculate("7 % 0")

    def test_invalid_power(self):
        with pytest.raises(ZeroDivisionError):
            self.calc.calculate("0 ** -1")

    def test_unbalanced_parentheses(self):
        with pytest.raises(ValueError):
            self.calc.calculate("(2 + 3")
        with pytest.raises(ValueError):
            self.calc.calculate("2 + 3)")

    def test_invalid_characters(self):
        with pytest.raises(ValueError):
            self.calc.calculate("2 + a")
        with pytest.raises(ValueError):
            self.calc.calculate("hello")

    def test_invalid_character_position(self):
        with pytest.raises(ValueError) as exc_info:
            self.calc.calculate("1 ф + 1")
        assert "позиции 2" in str(exc_info.value)

    def test_empty_expressions(self):
        with pytest.raises(ValueError):
            self.calc.calculate("")
        with pytest.raises(ValueError):
            self.calc.calculate("   ")

    def test_whitespace_handling(self):
        assert self.calc.calculate("  2  +  3  ") == 5.0
        assert self.calc.calculate("2+3") == 5.0

    def test_complex_expression(self):
        assert self.calc.calculate("2 + 3 * 4 - 5") == 9.0
        assert self.calc.calculate("(2 + 3) * (4 - 1)") == 15.0

    @pytest.mark.parametrize("expr,expected", [
        ("1 + 1", 2.0),
        ("10 - 5", 5.0),
        ("3 * 7", 21.0),
        ("20 / 4", 5.0),
        ("3 ** 3", 27.0),
        ("17 // 5", 3.0),
        ("17 % 5", 2.0),
        ("-10", -10.0),
        ("+10", 10.0),
    ])
    def test_parametrized_operations(self, expr, expected):
        assert self.calc.calculate(expr) == expected
