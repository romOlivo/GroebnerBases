from test.parser_test import *
from test.groebner_test import *


def suite():
    s = unittest.TestSuite()
    #######################################
    # ---------- Testing Parse ------------
    #######################################
    # Testing get_ordered_vars
    s.addTest(TestGetOrderedVars("base_case"))
    s.addTest(TestGetOrderedVars("complete_case"))
    # Testing vectorice_char_mon
    s.addTest(TestVectoriceCharMon("base_case"))
    s.addTest(TestVectoriceCharMon("constant"))
    s.addTest(TestVectoriceCharMon("redundant_blank"))
    s.addTest(TestVectoriceCharMon("with_exponent"))
    s.addTest(TestVectoriceCharMon("with_coefficient"))
    s.addTest(TestVectoriceCharMon("large_exponent"))
    s.addTest(TestVectoriceCharMon("large_coefficient"))
    s.addTest(TestVectoriceCharMon("complete_case"))
    # Testing convert_poly
    s.addTest(TestConvertPoly("base_case"))
    s.addTest(TestConvertPoly("redundant_blank"))
    s.addTest(TestConvertPoly("simple_poly"))
    s.addTest(TestConvertPoly("positive_terms"))
    s.addTest(TestConvertPoly("negative_terms"))
    s.addTest(TestConvertPoly("first_negative"))
    s.addTest(TestConvertPoly("exponents"))
    s.addTest(TestConvertPoly("coeff"))
    s.addTest(TestConvertPoly("complete_case"))
    # Testing convert_poly_base
    s.addTest(TestConvertPolyBase("base_case"))
    s.addTest(TestConvertPolyBase("simple_poly"))
    s.addTest(TestConvertPolyBase("complete_case"))
    #######################################
    # --------- Testing Groebner ----------
    #######################################
    # Testing polynomial_division
    s.addTest(TestPolynomialDivision("no_zero_reminder"))
    s.addTest(TestPolynomialDivision("zero_reminder"))
    s.addTest(TestPolynomialDivision("complete_case"))
    # Testing LT
    s.addTest(TestLT("monomial"))
    s.addTest(TestLT("simple_poly"))
    s.addTest(TestLT("multiple_maximums"))
    s.addTest(TestLT("invalid_monomial"))
    # Testing LCM
    s.addTest(TestLCM("simple_case"))
    s.addTest(TestLCM("complete_case"))
    # Testing mult_poly
    s.addTest(TestMultPol("monomial"))
    s.addTest(TestMultPol("simply_poly"))
    s.addTest(TestMultPol("poly"))
    # Testing s_poly
    s.addTest(TestSPoly("complete_case"))
    s.addTest(TestSPoly("int_coef"))
    # Testing make_groebner_base
    s.addTest(TestMakeGroebnerBase("simple_case"))
    return s


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
