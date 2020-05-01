from model.order import lexical_order

INVALID_WORDS = ["{", "}", "^", "+", "-", " "]


class Parse:
    @staticmethod
    def convert_poly_base(base, sep=" ", var=()):
        return [Parse.convert_poly(p, var=var) for p in base.strip().split(sep=sep)]

    @staticmethod
    def convert_poly(p, var=()):
        dic = {}
        positive_div = p.split("+")
        for part_positive in positive_div:
            if part_positive == "":
                continue
            part_positive = part_positive.strip()
            m = part_positive.split("-")
            if len(m) == 1:
                if m[0] == "":
                    continue
                if part_positive[0] == "-":
                    coef, exp = Parse.vectorice_char_mon(monomial=m[0], var=var, sign=-1)
                else:
                    coef, exp = Parse.vectorice_char_mon(monomial=m[0], var=var, sign=1)
                dic[exp] = coef
            else:
                if m[0] != "":
                    coef, exp = Parse.vectorice_char_mon(monomial=m[0], var=var, sign=1)
                    dic[exp] = coef
                i = 1
                while i < len(m):
                    if m[i] != "":
                        coef, exp = Parse.vectorice_char_mon(monomial=m[i], var=var, sign=-1)
                        dic[exp] = coef
                        i += 1
        return dic

    @staticmethod
    def vectorice_char_mon(monomial, var, sign=1):
        monomial = monomial.strip()
        v = [0 for _ in range(len(var))]
        coef = 1 * sign
        i = 0
        if monomial[0].isdigit():
            j = 0
            while j < len(monomial) and monomial[j].isdigit():
                j += 1
            coef = int(monomial[i:j]) * sign
            i = j
        while i < len(monomial):
            j = i + 1
            exp = 1
            if i + 2 < len(monomial) and monomial[i+1] == "^":
                j = i + 2
                while j < len(monomial) and monomial[j].isdigit():
                    j += 1
                exp = int(monomial[i+2:j])
            v[var.index(monomial[i])] = exp
            i = j
        return coef, tuple(v)

    @staticmethod
    def get_ordered_var(f, base, sep=""):
        v = set()
        for c in f:
            if not c.isdigit() and c not in INVALID_WORDS:
                v.add(c)
        for pol in base.split(sep=sep):
            for c in pol:
                if not c.isdigit() and c not in INVALID_WORDS:
                    v.add(c)
        v = list(v)
        v.sort()
        return v

    @staticmethod
    def base_to_string(base, var, sep=" ", order=lexical_order):
        text = ""
        for poly in base:
            poly_text = ""
            for mon in order(poly.keys()):
                if poly_text != "" and poly[mon] > 0:
                    if poly[mon] == 1:
                        poly_text = "{0} +".format(poly_text, poly[mon])
                    else:
                        poly_text = "{0} +{1}".format(poly_text, poly[mon])
                elif poly[mon] == -1:
                    poly_text = "{0} -".format(poly_text)
                else:
                    if poly[mon] == -1:
                        poly_text = "-".format()
                    elif poly[mon] != 1:
                        poly_text = "{0} {1}".format(poly_text, poly[mon])
                for i in range(len(mon)):
                    exp = mon[i]
                    if exp == 0:
                        continue
                    poly_text = "{0}{1}".format(poly_text, var[i])
                    if exp > 1:
                        poly_text = "{0}^{1}".format(poly_text, exp)
            if text == "":
                text = poly_text
            else:
                text = "{0}{1}{2}".format(text, sep, poly_text)
        return text
