def nb_year(p0, percent, aug, p, years = 0):
	if p0 < p:
		return nb_year(p0 + int(p0 * percent / 100) + aug, percent, aug, p, years + 1)
	return years
#############
def nb_year(p0, percent, aug, p, i=0):
    return i if p0>=p else nb_year(int(p0+p0*(percent/100)+aug), percent, aug, p, i+1)
############
def nb_year(p0, percent, aug, p, n = 0):
    while p > p0:
        p0 += p0*percent/100 + aug
        n += 1
    return n
############
from math import log, log1p, ceil

def nb_year(p0, percent, aug, p):
    # with β = 1 + percent/100 the annual growth factor,
    # we can write the equation for the population after n years as:
    # pn = p0 * β^n + aug * β^(n-1) + aug * β^(n-2) + ... + aug * β + aug =
    #    = p0 * β^n + aug * (β^n - 1)/(β - 1)
    # thus solving pn ≥ p for n we get:
    # (β-1)*p + aug ≥ β^n * ( (β-1)*p0 + aug )
    # ==> n ≥ ln( ((β-1)*p + aug) / ((β-1)*p0 + aug) ) /  ln(β)
    # (I'm actually sort of cheating, since this way 
    # the population isn't rounded down to a whole number
    # each year, but the difference is minor enough
    # that it would almost never change the result
    # and this solution runs in constant time instead of O(log(p-p0))
    if percent == 0:
        return ceil((p-p0) / aug)
    b = percent * 0.01
    alpha = (p*b + aug) / (p0*b + aug)
    # since β = 1+b i now want to take ln(α)/ln(β)
    if b < 1e-4:
        logb = log1p(b) # for numerical stability with small numbers
    else:
        logb = log(b + 1)
    if alpha < 1e-4:
        loga = log1p(alpha - 1)  # as above
    else:
        loga = log(alpha)
    year = loga / logb
    return ceil(year)  # to round up to the next whole year
###############################################
from itertools import accumulate

def nb_year(p0, pct, aug, p):
  return next(i for i, x in enumerate(accumulate([p0] * 1000, lambda px, _: px + .01 * pct * px + aug)) if x >= p)
###############
def nb_year(p0, percent, aug, p):
    inhabitants = 0
    n = 0
    while inhabitants < p:
        inhabitants = int(p0 + p0 * (percent/100) + aug)
        n += 1
        p0 = inhabitants
    return n
##################
def nb_year(p0, percent, aug, p):
    return 1 + nb_year(p0 + p0 * percent / 100 + aug, percent, aug, p) if p0 < p else 0
#############
def nb_year(p0, percent, aug, p):
    pop=p0
    y=0
    while pop<p:pop*=(1+percent/100);pop+=aug;y+=1
    return y
############
def nb_year(p0, percent, aug, p):
    no_years = 0
    while p0 < p:
        p0 += p0 * percent/100 + aug
        no_years += 1
    return no_years
