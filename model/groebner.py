from model.order import lexical_order


class Groebner:
    @staticmethod
    def can_divide(mon, div):
        can_divide = True
        for i in range(len(mon)):
            if div[i] > mon[i]:
                can_divide = False
                break
        return can_divide

    @staticmethod
    def divide_lt(lt_mon, lt_div):
        return tuple([lt_mon[i] - lt_div[i] for i in range(len(lt_mon))])

    @staticmethod
    def substract_poly(p1, p2):
        r = p1.copy()
        for m in p2:
            if m in r:
                r[m] -= p2[m]
                if r[m] == 0:
                    r.pop(m)
            else:
                r[m] = -p2[m]
        return r

    @staticmethod
    def polinomial_division(order, p_to_divide, dividers):
        coef = [{} for _ in range(len(dividers))]
        r = {}
        p = p_to_divide.copy()
        while not Groebner.is_zero_poly(f=p):
            i = 0
            division_has_ocurred = False
            _, lt_p = Groebner.LT(f=p)
            while i < len(dividers) and not division_has_ocurred:
                _, lt_d = Groebner.LT(f=dividers[i])
                if Groebner.can_divide(lt_p, lt_d):
                    d = Groebner.divide_lt(lt_mon=lt_p, lt_div=lt_d)
                    if d not in r:
                        coef[i][d] = 0
                    coef[i][d] += p[lt_p] / dividers[i][lt_d]
                    s = Groebner.multiply_poly(p1={d: p[lt_p] / dividers[i][lt_d]}, p2=dividers[i])
                    p = Groebner.substract_poly(p1=p, p2=s)
                    division_has_ocurred = True
                i += 1
            if not division_has_ocurred:
                if lt_p not in r:
                    r[lt_p] = 0
                r[lt_p] += p[lt_p]
                p.pop(lt_p)
        return r, coef


    @staticmethod
    def pol_in_ideal(f, base, order=lexical_order):
        r, _ = Groebner.polinomial_division(order=order, p_to_divide=f, dividers=base)
        return Groebner.is_zero_poly(f=r)

    @staticmethod
    def is_zero_poly(f):
        if f is None:
            return True
        has_no_reminder = True
        for key in f.keys():
            if f[key] != 0:
                has_no_reminder = False
                break
        return has_no_reminder

    @staticmethod
    def LT(f, order=lexical_order):
        ordered = order(f)
        i = -1
        c = 0
        while i < len(ordered) and c == 0:
            i += 1
            c = f[ordered[i]]
        p = ordered[i]
        return f[p], p

    @staticmethod
    def LCM(m1, m2):
        dev = list(m1)
        for i in range(len(m2)):
            dev[i] = max(dev[i], m2[i])
        return tuple(dev)

    @staticmethod
    def multiply_poly(p1, p2):
        dev = {}
        for mon1 in p1.keys():
            for mon2 in p2.keys():
                mon = tuple([mon1[i] + mon2[i] for i in range(len(mon1))])
                if mon not in dev:
                    dev[mon] = 0
                dev[mon] += p1[mon1] * p2[mon2]
        return dev

    @staticmethod
    def s_poly(f, g):
        f = f.copy()
        g = g.copy()
        lt_f = Groebner.LT(f=f)
        lt_g = Groebner.LT(f=g)
        lcm = Groebner.LCM(m1=lt_f[1], m2=lt_g[1])
        r1, div_f = Groebner.polinomial_division(order=lexical_order, p_to_divide={lcm: 1}, dividers=[{lt_f[1]: lt_f[0]}])
        r2, div_g = Groebner.polinomial_division(order=lexical_order, p_to_divide={lcm: 1}, dividers=[{lt_g[1]: lt_g[0]}])
        term_1 = Groebner.multiply_poly(div_f[0], f)
        term_2 = Groebner.multiply_poly(div_g[0], g)
        result = {}
        for mon in term_1.keys():
            if mon in term_2:
                r = term_1[mon] - term_2[mon]
                if r == 0:
                    continue
                result[mon] = r
            else:
                result[mon] = term_1[mon]
        for mon in term_2.keys():
            if mon in term_1:
                continue
            result[mon] = -term_2[mon]
        return result

    @staticmethod
    def make_groebner_base(base, order=lexical_order):
        g_base_f = list(base)
        g_base = list(g_base_f)
        i = 1
        while i < len(g_base):
            while i < len(g_base_f):
                j = 0
                while j < i:
                    print("i: {0}, j:{1}".format(i, j))
                    s_poly = Groebner.s_poly(f=g_base_f[i], g=g_base_f[j])
                    print(s_poly)
                    s, c = Groebner.polinomial_division(order=order, p_to_divide=s_poly, dividers=g_base_f)
                    if not Groebner.is_zero_poly(f=s):
                        print(g_base_f)
                        print(s_poly)
                        print(s)
                        print(c)
                        g_base.append(s)
                    j += 1
                i += 1
            g_base_f = g_base
        return g_base_f
