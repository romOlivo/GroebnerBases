@staticmethod
    def polinomial_division(order, p_to_divide, dividers):
        def multiply_pol(p1, p2):
            return tuple([p1[i] + p2[i] for i in range(len(p1))])

        def can_divide(p, d):
            dev = -1
            for i in range(len(d)):
                able_to_divide = True
                div = d[i]
                for j in range(len(div)):
                    if div[j] > p[j]:
                        able_to_divide = False
                        break
                if able_to_divide:
                    dev = i
                    break
            return dev

        def coefficient(p, d, nDiv):
            coef = tuple([p[i] - d[i] for i in range(len(d))])
            t = p_to_divide[p] / dividers[nDiv][d]
            return (coef, t)

        def divide(divid, t, c, lPol):
            for p in divid.keys():
                term = multiply_pol(p, c)
                if term not in p_to_divide:
                    p_to_divide[term] = 0
                    lPol.append(term)
                p_to_divide[term] -= t * divid[p]
                if p_to_divide[term] == 0:
                    lPol.remove(term)

        pol = order(list(p_to_divide.keys()))
        order_p_lid_dividers = [order(list(dividers[i].keys()))[0] for i in range(len(dividers))]
        coef = [{} for _ in range(len(dividers))]

        r = {}

        while len(pol) > 0:
            lt = pol[0]
            div = can_divide(lt, order_p_lid_dividers)
            if div == -1:
                r[lt] = p_to_divide[lt]
                pol.remove(lt)
            else:
                c, t = coefficient(lt, order_p_lid_dividers[div], div)
                dic = coef[div]
                if c not in dic:
                    dic[c] = 0
                dic[c] += t
                divide(dividers[div], t, c, pol)
                pol = order(pol)
        return r, coef




def lexical_order(l):
  dev = list(l)
  dev.sort(reverse=True)
  return dev



def polinomial_division(order, p_to_divide, dividers):
  def can_divide(p, d):
    dev = -1
    for i in range(len(d)):
      able_to_divide = True
      div = d[i]
      for j in range(len(div)):
        if div[j] > p[j]:
          able_to_divide = False
          break
      if able_to_divide:
        dev = i
        break
    return dev

  def coefficient(p, d, nDiv):
    coef = tuple([p[i] - d[i] for i in range(len(d))])
    t = p_to_divide[p] / dividers[nDiv][d]
    return (coef, t)

  def multiply_pol(p1, p2):
    return tuple([p1[i] + p2[i] for i in range(len(p1))])

  def divide(divid, t, c, lPol):
    for p in divid.keys():
      term = multiply_pol(p, c)
      if term not in p_to_divide:
        p_to_divide[term] = 0
        lPol.append(term)
      p_to_divide[term] -= t * divid[p]
      if p_to_divide[term] == 0:
        lPol.remove(term)

  pol = order(list(p_to_divide.keys()))
  order_p_lid_dividers = [order(list(dividers[i].keys()))[0] for i in range(len(dividers))]
  coef = [{} for _ in range(len(dividers))]

  r = {}

  while len(pol) > 0:
    lt = pol[0]
    div = can_divide(lt, order_p_lid_dividers)
    if div == -1:
      r[lt] = p_to_divide[lt]
      pol.remove(lt)
    else:
      c, t = coefficient(lt, order_p_lid_dividers[div], div)
      dic = coef[div]
      if c not in dic:
        dic[c] = 0
      dic[c] += t 
      divide(dividers[div], t, c, pol)
      pol = order(pol)

  return (r, coef)

# Test one, monomial division with rest
number_of_variables_1 = 2
order_1 = lexical_order
p_to_divide_1 = {
  (3, 0): 1,
  (2, 0): 1,
  (0, 2): 1
}
dividers_1 = [
    {
      (3, 0): 1
    },
    {
      (0, 1): 1
    }
  ]
r_1 = ({(2, 0): 1}, [{(0, 0): 1.0}, {(0, 1): 1.0}])

# Test two, polinoms in divisor with 0 rest
number_of_variables_2 = 2
order_2 = lexical_order
p_to_divide_2 = {
  (2, 2): 1,
  (0, 3): 1
}
dividers_2 = [
    {
      (2, 0): 1,
      (0, 1): 1
    }
  ]
r_2 = ({}, [{(0, 2): 1.0}])

assert polinomial_division(number_of_variables_2, order_2, p_to_divide_2, dividers_2) == r_2, "Second division wrong"

# Test three, complex division in two variables
number_of_variables_3 = 2
order_3 = lexical_order
p_to_divide_3 = {
  (2, 2): 4,
  (0, 3): 3,
  (0, 1): 1,
  (1, 0): 2
}
dividers_3 = [
    {
      (2, 0): 2,
      (0, 1): 1
    },
    {
      (0, 1): 1
    }
  ]
r_3 = ({(1, 0): 2}, [{(0, 2): 2.0}, {(0, 2): 1.0, (0, 0): 1.0}])

assert polinomial_division(number_of_variables_3, order_3, p_to_divide_3, dividers_3) == r_3, "Third division wrong"


print("All test passed!")

