import math
from decimal import Decimal

DEFAULT_SIG_FIGURES = 3


def significant_number(x):
    """
    Determine the number of significant figures for x
    """
    if x == 0:
        return 1
    int_part = int(abs(x))
    if int_part == 0:
        x = remove_unsignificant_zeros(x)
    return precision_and_scale(x)[0]


def min_significant_figures(*inputs):
    """
    Returns the minimum of significant figures for a tuple of values
    """
    sigfig = significant_number(inputs[0])
    for input in inputs:
        p = significant_number(input)
        if (p <= sigfig):
            sigfig = p
    return sigfig


def round_to_sigfig(x, significant_figures):
    """
   returns a float rounded to significant figures
   """
    return float(to_precision(x, significant_figures))


def precision_and_scale(x):
    """
    Utils function
    Determine the precision and scale of x
    """
    max_digits = 14
    int_part = int(abs(x))
    magnitude = 1 if int_part == 0 else int(math.log10(int_part)) + 1
    if magnitude >= max_digits:
        return (magnitude, 0)
    frac_part = abs(x) - int_part
    multiplier = 10 ** (max_digits - magnitude)
    frac_digits = multiplier + int(multiplier * frac_part + 0.5)
    while frac_digits % 10 == 0:
        frac_digits /= 10
    scale = int(math.log10(frac_digits))
    return (magnitude + scale, scale)


def remove_unsignificant_zeros(x):
    """
    Util function
    Remove unsignificant decimal zeros  in number like 0.'000'23
    """
    if (x > 1):
        return x
    divider = Decimal("0.000000001")
    x = Decimal(str(x))
    while x % divider == 0:
        divider = divider * 10
    exponent = -math.log10(divider) + 1
    return float(x * (Decimal(10 ** exponent)))

def to_precision(x, p):
    """
    Util function
    returns a string representation of x formatted with a precision of p

    http://randlet.com/blog/python-significant-figures-format/
    Based on the webkit javascript implementation taken from here:
    https://code.google.com/p/webkit-mirror/source/browse/JavaScriptCore/kjs/number_object.cpp
    """

    x = float(x)

    if x == 0.:
        return "0." + "0" * (p - 1)

    out = []

    if x < 0:
        out.append("-")
        x = -x

    e = int(math.log10(x))
    tens = math.pow(10, e - p + 1)
    n = math.floor(x / tens)

    if n < math.pow(10, p - 1):
        e = e - 1
        tens = math.pow(10, e - p + 1)
        n = math.floor(x / tens)

    if abs((n + 1.) * tens - x) <= abs(n * tens - x):
        n = n + 1

    if n >= math.pow(10, p):
        n = n / 10.
        e = e + 1

    m = "%.*g" % (p, n)

    if e < -2 or e >= p:
        out.append(m[0])
        if p > 1:
            out.append(".")
            out.extend(m[1:p])
        out.append('e')
        if e > 0:
            out.append("+")
        out.append(str(e))
    elif e == (p - 1):
        out.append(m)
    elif e >= 0:
        out.append(m[:e + 1])
        if e + 1 < len(m):
            out.append(".")
            out.extend(m[e + 1:])
    else:
        out.append("0.")
        out.extend(["0"] * -(e + 1))
        out.append(m)

    return "".join(out)
