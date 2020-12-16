import scipy as sci


def p_value(k, x):
    # return 1.-1./scipy.special.gamma(k/2.)*scipy.special.gammainc(k/2., x/2.)
    return sci.special.gammaincc(k / 2., x / 2.)
