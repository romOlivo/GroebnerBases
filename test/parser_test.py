import unittest
from model.parse import Parse


class TestGetOrderedVars(unittest.TestCase):
    def base_case(self):
        f = "a + 2b"
        base = "a + b\na^2"
        self.assertEqual(Parse.get_ordered_var(f=f, base=base, sep="\n"), ["a", "b"])

    def complete_case(self):
        f = "c + xy - a^2"
        base = "x^2yz + 2ab    \n yxa - 2"
        solution = ["a", "b", "c", "x", "y", "z"]
        self.assertEqual(Parse.get_ordered_var(f=f, base=base, sep="\n"), solution)


class TestVectoriceCharMon(unittest.TestCase):
    def base_case(self):
        f = "ab"
        var = ["a", "b"]
        solution = (1, (1, 1))
        self.assertEqual(Parse.vectorice_char_mon(monomial=f, var=var), solution)

    def constant(self):
        f = "1"
        var = ["a", "b"]
        solution = (1, (0, 0))
        self.assertEqual(Parse.vectorice_char_mon(monomial=f, var=var), solution)

    def redundant_blank(self):
        f = "   ab  "
        var = ["a", "b"]
        solution = (1, (1, 1))
        self.assertEqual(Parse.vectorice_char_mon(monomial=f, var=var), solution)

    def with_exponent(self):
        f = "ab^2"
        var = ["a", "b"]
        solution = (1, (1, 2))
        self.assertEqual(Parse.vectorice_char_mon(monomial=f, var=var), solution)

    def with_coefficient(self):
        f = "2ab"
        var = ["a", "b"]
        solution = (2, (1, 1))
        self.assertEqual(Parse.vectorice_char_mon(monomial=f, var=var), solution)

    def large_exponent(self):
        f = "ab^12"
        var = ["a", "b"]
        solution = (1, (1, 12))
        self.assertEqual(Parse.vectorice_char_mon(monomial=f, var=var), solution)

    def large_coefficient(self):
        f = "21ab"
        var = ["a", "b"]
        solution = (21, (1, 1))
        self.assertEqual(Parse.vectorice_char_mon(monomial=f, var=var), solution)

    def complete_case(self):
        f = "21a^210b^7"
        var = ["a", "b"]
        solution = (21, (210, 7))
        self.assertEqual(Parse.vectorice_char_mon(monomial=f, var=var), solution)


class TestConvertPoly(unittest.TestCase):
    def base_case(self):
        f = "ab"
        var = ["a", "b"]
        solution = {(1, 1): 1}
        self.assertEqual(Parse.convert_poly(p=f, var=var), solution)

    def redundant_blank(self):
        f = "     ab   + a  "
        var = ["a", "b"]
        solution = {(1, 1): 1, (1, 0): 1}
        self.assertEqual(Parse.convert_poly(p=f, var=var), solution)

    def simple_poly(self):
        f = "ab + a"
        var = ["a", "b"]
        solution = {(1, 1): 1, (1, 0): 1}
        self.assertEqual(Parse.convert_poly(p=f, var=var), solution)

    def positive_terms(self):
        f = "ab + a + 1"
        var = ["a", "b"]
        solution = {(1, 1): 1, (1, 0): 1, (0, 0): 1}
        self.assertEqual(Parse.convert_poly(p=f, var=var), solution)

    def negative_terms(self):
        f = "ab - a - b"
        var = ["a", "b"]
        solution = {(1, 1): 1, (1, 0): -1, (0, 1): -1}
        self.assertEqual(Parse.convert_poly(p=f, var=var), solution)

    def first_negative(self):
        f = "-ab"
        var = ["a", "b"]
        solution = {(1, 1): -1}
        self.assertEqual(Parse.convert_poly(p=f, var=var), solution)

    def exponents(self):
        f = "ab^2 + a^10"
        var = ["a", "b"]
        solution = {(1, 2): 1, (10, 0): 1}
        self.assertEqual(Parse.convert_poly(p=f, var=var), solution)

    def coeff(self):
        f = "2ab + 20a"
        var = ["a", "b"]
        solution = {(1, 1): 2, (1, 0): 20}
        self.assertEqual(Parse.convert_poly(p=f, var=var), solution)

    def complete_case(self):
        f = "3ab^2 + a^10 -  17ab -   15a^10b^7 "
        var = ["a", "b"]
        solution = {(1, 2): 3, (10, 0): 1, (1, 1): -17, (10, 7): -15}
        self.assertEqual(Parse.convert_poly(p=f, var=var), solution)


class TestConvertPolyBase(unittest.TestCase):
    def base_case(self):
        f = "ab"
        var = ["a", "b"]
        solution = [{(1, 1): 1}]
        self.assertEqual(Parse.convert_poly_base(base=f, var=var, sep="\n"), solution)

    def simple_poly(self):
        f = "a\nb"
        var = ["a", "b"]
        solution = [{(1, 0): 1}, {(0, 1): 1}]
        self.assertEqual(Parse.convert_poly_base(base=f, var=var, sep="\n"), solution)

    def complete_case(self):
        f = "  a^2b + 1 \n 27 + 4a   \n    17b^10 - a^2"
        var = ["a", "b"]
        solution = [{(2, 1): 1, (0, 0): 1}, {(0, 0): 27, (1, 0): 4}, {(0, 10): 17, (2, 0): -1}]
        self.assertEqual(Parse.convert_poly_base(base=f, var=var, sep="\n"), solution)


if __name__ == '__main__':
    unittest.main()
