import unittest
from model.groebner import Groebner
from model.order import lexical_order


class TestPolynomialDivision(unittest.TestCase):
    def no_zero_reminder(self):
        p_to_divide = {
            (3, 0): 1,
            (2, 0): 1,
            (0, 2): 1
        }
        dividers = [
            {
                (3, 0): 1
            },
            {
                (0, 1): 1
            }
        ]
        r = ({(2, 0): 1}, [{(0, 0): 1.0}, {(0, 1): 1.0}])
        self.assertEqual(Groebner.polinomial_division(order=lexical_order, p_to_divide=p_to_divide,
                                                      dividers=dividers), r)

    def zero_reminder(self):
        p_to_divide = {
            (2, 2): 1,
            (0, 3): 1
        }
        dividers = [
            {
                (2, 0): 1,
                (0, 1): 1
            }
        ]
        r = ({}, [{(0, 2): 1.0}])
        self.assertEqual(Groebner.polinomial_division(order=lexical_order, p_to_divide=p_to_divide,
                                                      dividers=dividers), r)

    def complete_case(self):
        p_to_divide = {
            (2, 2): 4,
            (0, 3): 3,
            (0, 1): 1,
            (1, 0): 2
        }
        dividers = [
            {
                (2, 0): 2,
                (0, 1): 1
            },
            {
                (0, 1): 1
            }
        ]
        r = ({(1, 0): 2}, [{(0, 2): 2.0}, {(0, 2): 1.0, (0, 0): 1.0}])
        self.assertEqual(Groebner.polinomial_division(order=lexical_order, p_to_divide=p_to_divide,
                                                      dividers=dividers), r)


class TestLT(unittest.TestCase):
    def monomial(self):
        f = {(1, 0): 3}
        sol = (3, (1, 0))
        self.assertEqual(Groebner.LT(f=f), sol)

    def simple_poly(self):
        f = {(1, 0): 1, (1, 1): 1}
        sol = (1, (1, 1))
        self.assertEqual(Groebner.LT(f=f), sol)

    def multiple_maximums(self):
        f = {(1, 0): 1, (2, 1): 1, (1, 2): 1}
        sol = (1, (2, 1))
        self.assertEqual(Groebner.LT(f=f), sol)

    def invalid_monomial(self):
        f = {(1, 0): 2, (1, 1): 0}
        sol = (2, (1, 0))
        self.assertEqual(Groebner.LT(f=f), sol)


class TestLCM(unittest.TestCase):
    def simple_case(self):
        m1 = (1, 0)
        m2 = (0, 1)
        sol = (1, 1)
        self.assertEqual(Groebner.LCM(m1=m1, m2=m2), sol)

    def complete_case(self):
        m1 = (3, 1, 4)
        m2 = (2, 1, 5)
        sol = (3, 1, 5)
        self.assertEqual(Groebner.LCM(m1=m1, m2=m2), sol)


class TestSPoly(unittest.TestCase):
    def complete_case(self):
        p1 = {
            (3, 2): 1,
            (2, 3): -1,
            (1, 0): 1
        }
        p2 = {
            (4, 1): 3,
            (0, 2): 1
        }
        sol = {
            (3, 3): -1,
            (2, 0): 1,
            (0, 3): -1/3
        }
        self.assertEqual(Groebner.s_poly(f=p1, g=p2), sol)

    def int_coef(self):
        p1 = {
            (1, 0, 0): 1,
            (0, 0, 2): -1
        }
        p2 = {
            (0, 1, 0): 1,
            (0, 0, 3): -1
        }
        sol = {
            (0, 1, 2): -1,
            (1, 0, 3): 1
        }
        self.assertEqual(Groebner.s_poly(f=p1, g=p2), sol)


class TestMultPol(unittest.TestCase):
    def monomial(self):
        p1 = {(1, 0): 3}
        p2 = {(1, 0): 1}
        sol = {(2, 0): 3}
        self.assertEqual(Groebner.multiply_poly(p1=p1, p2=p2), sol)

    def simply_poly(self):
        p1 = {(1, 1): 3}
        p2 = {(1, 0): 1, (0, 1): 1}
        sol = {(2, 1): 3, (1, 2): 3}
        self.assertEqual(Groebner.multiply_poly(p1=p1, p2=p2), sol)

    def poly(self):
        p1 = {(1, 0): 1, (0, 1): 2}
        p2 = {(1, 1): 3, (2, 1): 4}
        sol = {(2, 1): 3, (3, 1): 4, (1, 2): 6, (2, 2): 8}
        self.assertEqual(Groebner.multiply_poly(p1=p1, p2=p2), sol)


class TestMakeGroebnerBase(unittest.TestCase):
    def simple_case(self):
        base = [
            {
                (1, 0): 1,
                (0, 1): 1
            },
            {
                (1, 1): 1
            }
        ]
        sol = [
            {
                (1, 0): 1,
                (0, 1): 1
            },
            {
                (1, 1): 1
            },
            {
                (0, 2): -1
            }
        ]
        self.assertEqual(Groebner.make_groebner_base(base=base), sol)

    def complete_case(self):
        base = [
            {
                (3, 0): 1,
                (1, 1): -2
            },
            {
                (2, 1): 1,
                (0, 2): -2,
                (1, 0): 1
            }
        ]
        sol = [
            {
                (3, 0): 1,
                (1, 1): -2
            },
            {
                (2, 1): 1,
                (0, 2): -2,
                (1, 0): 1
            },
            {
                (2, 0): -1
            },
            {
                (1, 1): -2
            },
            {
                (1, 2): -2,
                (1, 0): 1
            }
        ]
        self.assertEqual(Groebner.make_groebner_base(base=base), sol)
